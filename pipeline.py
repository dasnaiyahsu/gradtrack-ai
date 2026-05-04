import os
import pandas as pd
import numpy as np
import pickle
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
 
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
 
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    precision_score, recall_score
)
 
# Supres git warning dari MLflow
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
 
 
 
def load_data(features_path: str, targets_path: str) -> pd.DataFrame:
    """
    Load dan merge dataset fitur dengan dataset target.
    """
    df_features = pd.read_csv(features_path)
    df_targets  = pd.read_csv(targets_path)
    df          = df_features.merge(df_targets, on="Student_ID")
    print(f"[INFO] Dataset loaded: {df.shape[0]:,} baris x {df.shape[1]} kolom")
    return df
 
 
def prepare_data(df: pd.DataFrame):
    """
    Cleaning ringan + pisahkan fitur (X) dan target (y).
    - Isi missing values extracurricular_involvement dengan 'Unknown'
    - Encode target: Placed=1, Not Placed=0
    """
    df["extracurricular_involvement"] = (
        df["extracurricular_involvement"].fillna("Unknown")
    )
 
    FEATURES = [
        "cgpa", "tenth_percentage", "twelfth_percentage", "backlogs",
        "attendance_percentage", "study_hours_per_day",
        "coding_skill_rating", "communication_skill_rating", "aptitude_skill_rating",
        "projects_completed", "internships_completed",
        "hackathons_participated", "certifications_count",
        "sleep_hours", "stress_level",
        "gender", "branch", "part_time_job", "family_income_level",
        "city_tier", "internet_access", "extracurricular_involvement",
    ]
 
    X = df[FEATURES].copy()
    y = (df["placement_status"] == "Placed").astype(int)
 
    print(f"[INFO] Fitur: {X.shape[1]} kolom | "
          f"Target distribusi: Placed={y.sum():,}, Not Placed={(1-y).sum():,}")
    return X, y
 
 

 
def build_pipeline(X: pd.DataFrame, model, model_params: dict) -> Pipeline:
    """
    Bangun sklearn Pipeline lengkap: preprocessing -> model.
    Preprocessing di-fit HANYA pada data train (no data leakage).
    """
    numeric_features = X.select_dtypes(include=np.number).columns.tolist()
    cat_features     = X.select_dtypes(include="object").columns.tolist()
 
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
 
    cat_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
 
    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_features),
        ("cat", cat_transformer,     cat_features),
    ])
 
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model",        model(**model_params)),
    ])
 
    return pipeline
 
 

 
def train_and_log(
    X_train, X_test, y_train, y_test,
    pipeline,
    model_name: str,
    model_params: dict,
    experiment_name: str = "student-placement",
):
    """
    Train pipeline, evaluasi metrik, dan log semua ke MLflow.
    Log: parameters, metrics, artifact model, Model Registry.
    """
    mlflow.set_tracking_uri("sqlite:///mlflow.db")  # tambah ini
    mlflow.set_experiment(experiment_name)
 
    with mlflow.start_run(run_name=model_name):
 
        # -- Log Parameters
        mlflow.log_param("model_name",        model_name)
        mlflow.log_param("test_size",         0.2)
        mlflow.log_param("random_state",      42)
        mlflow.log_param("imputer_numeric",   "median")
        mlflow.log_param("imputer_categoric", "most_frequent")
        mlflow.log_param("scaler",            "StandardScaler")
        mlflow.log_param("encoder",           "OneHotEncoder")
        for param, value in model_params.items():
            mlflow.log_param(param, value)
 
        # -- Training
        pipeline.fit(X_train, y_train)
 
        # -- Prediction
        y_pred  = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]
 
        # -- Metrics
        metrics = {
            "accuracy":  accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall":    recall_score(y_test, y_pred, zero_division=0),
            "f1_score":  f1_score(y_test, y_pred, zero_division=0),
            "auc_roc":   roc_auc_score(y_test, y_proba),
        }
        for metric_name, metric_val in metrics.items():
            mlflow.log_metric(metric_name, metric_val)
 
        # -- Log Model + Model Registry
        signature = infer_signature(X_train, pipeline.predict(X_train))
        mlflow.sklearn.log_model(
            sk_model              = pipeline,
            artifact_path         = "model",
            signature             = signature,
            input_example         = X_train.iloc[:3],
            registered_model_name = f"student-placement-{model_name.lower()}",
        )
 
        # -- Print hasil
        print(f"\n  {'-'*45}")
        print(f"  Model     : {model_name}")
        print(f"  Accuracy  : {metrics['accuracy']:.4f}")
        print(f"  Precision : {metrics['precision']:.4f}")
        print(f"  Recall    : {metrics['recall']:.4f}")
        print(f"  F1 Score  : {metrics['f1_score']:.4f}")
        print(f"  AUC-ROC   : {metrics['auc_roc']:.4f}")
 
    return pipeline, metrics
 
 

 
def save_model(model, filename: str = "best_model.pkl") -> None:
    """Simpan model terbaik ke file .pkl menggunakan Pickle."""
    with open(filename, "wb") as f:
        pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"\n[INFO] Model terbaik disimpan -> {filename}")
 
 
def load_model(filename: str = "best_model.pkl"):
    """Load model dari file .pkl."""
    with open(filename, "rb") as f:
        model = pickle.load(f)
    print(f"[INFO] Model loaded dari -> {filename}")
    return model
 
 

 
if __name__ == "__main__":
 
    print("=" * 55)
    print("  Student Placement - sklearn Pipeline + MLflow")
    print("=" * 55)
 
    # Step 1: Load Data
    print("\n[STEP 1] Data Ingestion")
    df = load_data("A.csv", "A_targets.csv")
 
    # Step 2: Prepare Data
    print("\n[STEP 2] Prepare Data")
    X, y = prepare_data(df)
 
    # Step 3: Train-Test Split (80:20, stratified)
    print("\n[STEP 3] Train-Test Split 80:20")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )
    print(f"[INFO] Train: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")
 
    # Step 4: Definisi Model
    experiments = [
        (
            "LogisticRegression",
            LogisticRegression,
            {"max_iter": 1000, "random_state": 42, "C": 1.0, "class_weight": "balanced"},
        ),
        (
            "RandomForest",
            RandomForestClassifier,
            {"n_estimators": 100, "max_depth": 12, "random_state": 42,
             "class_weight": "balanced", "n_jobs": -1},
        ),
        (
            "GradientBoosting",
            GradientBoostingClassifier,
            {"n_estimators": 100, "learning_rate": 0.1, "max_depth": 5, "random_state": 42},
        ),
        (
            "SVM",
            SVC,
            {"kernel": "rbf", "C": 1.0, "probability": True,
             "random_state": 42, "class_weight": "balanced"},
        ),
    ]
 
    # Step 5: Training + MLflow Tracking
    print("\n[STEP 4] Training & Experiment Tracking (MLflow)")
    all_results = {}
    for model_name, model_class, model_params in experiments:
        pipeline = build_pipeline(X_train, model_class, model_params)
        trained_pipeline, metrics = train_and_log(
            X_train, X_test, y_train, y_test,
            pipeline=pipeline,
            model_name=model_name,
            model_params=model_params,
        )
        all_results[model_name] = {"pipeline": trained_pipeline, "metrics": metrics}
 
    # Step 6: Pilih Model Terbaik
    print("\n[STEP 5] Pilih & Simpan Model Terbaik")
    best_name  = max(all_results, key=lambda k: all_results[k]["metrics"]["f1_score"])
    best_model = all_results[best_name]["pipeline"]
    best_f1    = all_results[best_name]["metrics"]["f1_score"]
    print(f"\n  [BEST] Model  : {best_name}")
    print(f"         F1 Score: {best_f1:.4f}")
 
    # Step 7: Simpan ke .pkl
    save_model(best_model, filename="best_model.pkl")
 
   
    print("\n" + "=" * 55)
    print("  HASIL SEMUA MODEL")
    print("=" * 55)
    summary = pd.DataFrame({
        name: {k: round(v, 4) for k, v in res["metrics"].items()}
        for name, res in all_results.items()
    }).T
    print(summary.to_string())
    print("\n[DONE] Pipeline selesai.")