import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder

np.random.seed(42)
n = 5000

df = pd.DataFrame({
    "cgpa": np.random.uniform(4, 10, n),
    "tenth_percentage": np.random.uniform(40, 100, n),
    "twelfth_percentage": np.random.uniform(40, 100, n),
    "backlogs": np.random.randint(0, 10, n),
    "attendance_percentage": np.random.uniform(40, 100, n),
    "study_hours_per_day": np.random.uniform(0, 12, n),
    "coding_skill_rating": np.random.randint(1, 11, n),
    "communication_skill_rating": np.random.randint(1, 11, n),
    "aptitude_skill_rating": np.random.randint(1, 11, n),
    "projects_completed": np.random.randint(0, 15, n),
    "internships_completed": np.random.randint(0, 5, n),
    "hackathons_participated": np.random.randint(0, 10, n),
    "certifications_count": np.random.randint(0, 10, n),
    "sleep_hours": np.random.uniform(3, 10, n),
    "stress_level": np.random.randint(1, 11, n),
    "gender": np.random.choice(["Male", "Female"], n),
    "branch": np.random.choice(["CSE","ECE","ME","CE","EE","IT","Other"], n),
    "part_time_job": np.random.choice(["Yes","No"], n),
    "family_income_level": np.random.choice(["Low","Medium","High"], n),
    "city_tier": np.random.choice(["Tier 1","Tier 2","Tier 3"], n),
    "internet_access": np.random.choice(["Yes","No"], n),
    "extracurricular_involvement": np.random.choice(["Low","Medium","High","Unknown"], n),
})

df["salary"] = (
    df["cgpa"] * 1.2 +
    df["coding_skill_rating"] * 0.8 +
    df["internships_completed"] * 1.5 +
    df["projects_completed"] * 0.3 +
    df["certifications_count"] * 0.4 +
    df["aptitude_skill_rating"] * 0.5 -
    df["backlogs"] * 0.5 +
    np.random.normal(0, 1.5, n)
).clip(1, 30)

cat_cols = ["gender","branch","part_time_job","family_income_level",
            "city_tier","internet_access","extracurricular_involvement"]
num_cols = [c for c in df.columns if c not in cat_cols + ["salary"]]

X = df.drop("salary", axis=1)
y = df["salary"]

preprocessor = ColumnTransformer(transformers=[
    ("num", "passthrough", num_cols),
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), cat_cols),
])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

with open("best_model_regression.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ best_model_regression.pkl berhasil dibuat!")