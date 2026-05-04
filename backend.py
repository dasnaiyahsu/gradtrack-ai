import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional
 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
 
# ── App Init ──────────────────────────────────────────────────
app = FastAPI(
    title="GradTrack AI — Placement Prediction API",
    description="""
## Student Placement & Salary Prediction API
 
API ini menyediakan prediksi berbasis Machine Learning untuk:
- **Klasifikasi**: Status penempatan kerja mahasiswa (Placed / Not Placed)
- **Regresi**: Estimasi gaji (Salary dalam LPA)
 
### Cara Penggunaan
1. Gunakan endpoint `/predict/classification` untuk prediksi placement
2. Gunakan endpoint `/predict/regression` untuk prediksi salary
3. Gunakan endpoint `/predict/both` untuk prediksi keduanya sekaligus
    """,
    version="1.0.0",
    contact={"name": "GradTrack AI", "email": "gradtrack@ai.com"},
)
 
# ── CORS — izinkan Streamlit frontend akses API ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
# ── Load Models ───────────────────────────────────────────────
def load_pkl(path: str):
    p = Path(path)
    if not p.exists():
        return None
    with open(p, "rb") as f:
        return pickle.load(f)
 
clf_model = load_pkl("best_model.pkl")          # klasifikasi
reg_model = load_pkl("best_model_regression.pkl")  # regresi
 
 
# ══════════════════════════════════════════════════════════════
# SCHEMA — Request & Response
# ══════════════════════════════════════════════════════════════
 
class StudentInput(BaseModel):
    """Schema input data mahasiswa."""
 
    # Akademik
    cgpa: float                  = Field(..., ge=0, le=10,  example=8.5,  description="IPK mahasiswa (0-10)")
    tenth_percentage: float      = Field(..., ge=0, le=100, example=85.0, description="Nilai ujian SMP (%)")
    twelfth_percentage: float    = Field(..., ge=0, le=100, example=82.0, description="Nilai ujian SMA (%)")
    backlogs: int                = Field(..., ge=0, le=20,  example=0,    description="Jumlah mata kuliah gagal")
    attendance_percentage: float = Field(..., ge=0, le=100, example=85.0, description="Persentase kehadiran")
    study_hours_per_day: float   = Field(..., ge=0, le=24,  example=5.0,  description="Jam belajar per hari")
 
    # Skill
    coding_skill_rating: int        = Field(..., ge=1, le=10, example=8, description="Rating coding skill (1-10)")
    communication_skill_rating: int = Field(..., ge=1, le=10, example=7, description="Rating komunikasi (1-10)")
    aptitude_skill_rating: int      = Field(..., ge=1, le=10, example=8, description="Rating aptitude (1-10)")
 
    # Pengalaman
    projects_completed: int      = Field(..., ge=0, le=20, example=5,  description="Jumlah proyek selesai")
    internships_completed: int   = Field(..., ge=0, le=5,  example=2,  description="Jumlah internship")
    hackathons_participated: int = Field(..., ge=0, le=10, example=3,  description="Jumlah hackathon diikuti")
    certifications_count: int    = Field(..., ge=0, le=15, example=4,  description="Jumlah sertifikasi")
 
    # Gaya hidup
    sleep_hours: float  = Field(..., ge=0, le=24, example=7.0, description="Jam tidur per hari")
    stress_level: int   = Field(..., ge=1, le=10, example=4,   description="Tingkat stres (1-10)")
 
    # Kategorik
    gender: str                      = Field(..., example="Male",    description="Male / Female")
    branch: str                      = Field(..., example="CSE",     description="Jurusan kuliah")
    part_time_job: str               = Field(..., example="No",      description="Yes / No")
    family_income_level: str         = Field(..., example="Medium",  description="Low / Medium / High")
    city_tier: str                   = Field(..., example="Tier 1",  description="Tier 1 / Tier 2 / Tier 3")
    internet_access: str             = Field(..., example="Yes",     description="Yes / No")
    extracurricular_involvement: str = Field(..., example="Medium",  description="Low / Medium / High / Unknown")
 
    class Config:
        json_schema_extra = {
            "example": {
                "cgpa": 8.5,
                "tenth_percentage": 85.0,
                "twelfth_percentage": 82.0,
                "backlogs": 0,
                "attendance_percentage": 88.0,
                "study_hours_per_day": 5.0,
                "coding_skill_rating": 8,
                "communication_skill_rating": 7,
                "aptitude_skill_rating": 8,
                "projects_completed": 5,
                "internships_completed": 2,
                "hackathons_participated": 3,
                "certifications_count": 4,
                "sleep_hours": 7.0,
                "stress_level": 4,
                "gender": "Male",
                "branch": "CSE",
                "part_time_job": "No",
                "family_income_level": "Medium",
                "city_tier": "Tier 1",
                "internet_access": "Yes",
                "extracurricular_involvement": "Medium"
            }
        }
 
 
class ClassificationResponse(BaseModel):
    status: str
    placement_status: str
    probability_placed: float
    probability_not_placed: float
    confidence: str
    input_summary: dict
 
 
class RegressionResponse(BaseModel):
    status: str
    predicted_salary_lpa: float
    salary_range: str
    input_summary: dict
 
 
class BothResponse(BaseModel):
    status: str
    placement_status: str
    probability_placed: float
    probability_not_placed: float
    predicted_salary_lpa: Optional[float]
    salary_range: Optional[str]
    confidence: str
    input_summary: dict
 
 
# ══════════════════════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════════════════════
 
def to_dataframe(data: StudentInput) -> pd.DataFrame:
    """Konversi Pydantic model ke DataFrame."""
    return pd.DataFrame([{
        "cgpa":                       data.cgpa,
        "tenth_percentage":           data.tenth_percentage,
        "twelfth_percentage":         data.twelfth_percentage,
        "backlogs":                   data.backlogs,
        "attendance_percentage":      data.attendance_percentage,
        "study_hours_per_day":        data.study_hours_per_day,
        "coding_skill_rating":        data.coding_skill_rating,
        "communication_skill_rating": data.communication_skill_rating,
        "aptitude_skill_rating":      data.aptitude_skill_rating,
        "projects_completed":         data.projects_completed,
        "internships_completed":      data.internships_completed,
        "hackathons_participated":    data.hackathons_participated,
        "certifications_count":       data.certifications_count,
        "sleep_hours":                data.sleep_hours,
        "stress_level":               data.stress_level,
        "gender":                     data.gender,
        "branch":                     data.branch,
        "part_time_job":              data.part_time_job,
        "family_income_level":        data.family_income_level,
        "city_tier":                  data.city_tier,
        "internet_access":            data.internet_access,
        "extracurricular_involvement": data.extracurricular_involvement,
    }])
 
 
def get_confidence(prob: float) -> str:
    if prob >= 0.85:   return "Sangat Tinggi"
    if prob >= 0.70:   return "Tinggi"
    if prob >= 0.55:   return "Sedang"
    return "Rendah"
 
 
def get_salary_range(salary: float) -> str:
    if salary < 3:    return "< 3 LPA (Entry Level)"
    if salary < 6:    return "3-6 LPA (Junior)"
    if salary < 10:   return "6-10 LPA (Mid Level)"
    if salary < 15:   return "10-15 LPA (Senior)"
    return "> 15 LPA (Expert)"
 
 
# ══════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════
 
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "GradTrack AI — Placement Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "classification": "/predict/classification",
            "regression":     "/predict/regression",
            "both":           "/predict/both",
            "health":         "/health",
            "model_info":     "/model/info",
        }
    }
 
 
@app.get("/health", tags=["Health"])
def health_check():
    """Cek status API dan ketersediaan model."""
    return {
        "status": "healthy",
        "classification_model": "loaded" if clf_model else "not found",
        "regression_model":     "loaded" if reg_model else "not found",
    }
 
 
@app.get("/model/info", tags=["Model"])
def model_info():
    """Informasi model yang digunakan."""
    return {
        "classification": {
            "algorithm":    "Random Forest Classifier",
            "n_estimators": 100,
            "max_depth":    12,
            "f1_score":     0.9392,
            "accuracy":     0.8920,
            "auc_roc":      0.8933,
        },
        "regression": {
            "algorithm": "Gradient Boosting Regressor",
            "n_estimators": 100,
            "max_depth":    5,
            "mae":          2.576,
            "r2":           0.587,
        },
        "training_data": "5.000 mahasiswa",
        "features":      22,
        "train_test_split": "80:20 stratified",
    }
 
 
# ── POST: Klasifikasi ─────────────────────────────────────────
@app.post(
    "/predict/classification",
    response_model=ClassificationResponse,
    tags=["Prediction"],
    summary="Prediksi Status Placement",
    description="Prediksi apakah mahasiswa akan **Placed** atau **Not Placed** berdasarkan data akademik, skill, dan profil.",
)
def predict_classification(data: StudentInput):
    if clf_model is None:
        raise HTTPException(status_code=503, detail="Model klasifikasi tidak ditemukan. Pastikan best_model.pkl tersedia.")
 
    df          = to_dataframe(data)
    prediction  = clf_model.predict(df)[0]
    probability = clf_model.predict_proba(df)[0]
 
    placed_prob     = float(probability[1])
    not_placed_prob = float(probability[0])
    placement_label = "Placed" if prediction == 1 else "Not Placed"
 
    return ClassificationResponse(
        status               = "success",
        placement_status     = placement_label,
        probability_placed   = round(placed_prob, 4),
        probability_not_placed = round(not_placed_prob, 4),
        confidence           = get_confidence(placed_prob if prediction == 1 else not_placed_prob),
        input_summary        = {
            "cgpa":             data.cgpa,
            "coding_skill":     data.coding_skill_rating,
            "internships":      data.internships_completed,
            "backlogs":         data.backlogs,
            "attendance":       data.attendance_percentage,
        }
    )
 
 
# ── POST: Regresi ─────────────────────────────────────────────
@app.post(
    "/predict/regression",
    response_model=RegressionResponse,
    tags=["Prediction"],
    summary="Prediksi Estimasi Gaji",
    description="Prediksi estimasi **gaji (LPA)** mahasiswa berdasarkan profil akademik dan skill.",
)
def predict_regression(data: StudentInput):
    if reg_model is None:
        raise HTTPException(
            status_code=503,
            detail="Model regresi tidak ditemukan. Jalankan pipeline.py untuk membuat best_model_regression.pkl."
        )
 
    df             = to_dataframe(data)
    predicted_salary = float(reg_model.predict(df)[0])
    predicted_salary = max(0.0, round(predicted_salary, 2))
 
    return RegressionResponse(
        status                = "success",
        predicted_salary_lpa  = predicted_salary,
        salary_range          = get_salary_range(predicted_salary),
        input_summary         = {
            "cgpa":         data.cgpa,
            "coding_skill": data.coding_skill_rating,
            "internships":  data.internships_completed,
            "branch":       data.branch,
        }
    )
 
 
# ── POST: Both ────────────────────────────────────────────────
@app.post(
    "/predict/both",
    response_model=BothResponse,
    tags=["Prediction"],
    summary="Prediksi Placement + Gaji Sekaligus",
    description="Prediksi **status placement** dan **estimasi gaji** dalam satu request.",
)
def predict_both(data: StudentInput):
    if clf_model is None:
        raise HTTPException(status_code=503, detail="Model klasifikasi tidak ditemukan.")
 
    df          = to_dataframe(data)
    prediction  = clf_model.predict(df)[0]
    probability = clf_model.predict_proba(df)[0]
 
    placed_prob     = float(probability[1])
    not_placed_prob = float(probability[0])
    placement_label = "Placed" if prediction == 1 else "Not Placed"
 
    # Regresi (opsional jika model ada)
    salary = None
    salary_range = None
    if reg_model is not None:
        salary       = float(max(0.0, round(reg_model.predict(df)[0], 2)))
        salary_range = get_salary_range(salary)
 
    return BothResponse(
        status                 = "success",
        placement_status       = placement_label,
        probability_placed     = round(placed_prob, 4),
        probability_not_placed = round(not_placed_prob, 4),
        predicted_salary_lpa   = salary,
        salary_range           = salary_range,
        confidence             = get_confidence(placed_prob if prediction == 1 else not_placed_prob),
        input_summary          = {
            "cgpa":         data.cgpa,
            "coding_skill": data.coding_skill_rating,
            "internships":  data.internships_completed,
            "backlogs":     data.backlogs,
            "branch":       data.branch,
        }
    )
 
 
# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)