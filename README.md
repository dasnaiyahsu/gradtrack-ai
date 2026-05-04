# 🎓 GradTrack AI — Student Placement & Salary Prediction System

<div align="center">
  
  <img width="1904" height="1055" alt="suda jadi" src="https://github.com/user-attachments/assets/07668d7e-03da-41f0-bbc5-2b9761faf01e" />
  <img width="1906" height="929" alt="coba prediksi" src="https://github.com/user-attachments/assets/305b4c2f-734d-4cf8-a0de-873d503b0d5c" />


<img width="1907" height="1058" alt="ai client" src="https://github.com/user-attachments/assets/33be790b-2712-4b76-86b5-825443ac6588" />


![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)

**An ML-powered system that predicts student job placement status and estimates salary — deployed as a decoupled REST API architecture.**

[Live Demo](#-how-to-run) · [API Docs](#-api-endpoints) · [Model Performance](#-model-performance)

</div>

---

##  Overview

GradTrack AI is a machine learning system built as part of the **Model Deployment** course (UTS Mid Term) at **Binus University**. It addresses a real problem: students often have no data-driven insight into their employability prospects.

The system solves **two tasks**:
-  **Classification** — Predict whether a student will be **Placed** or **Not Placed**
-  **Regression** — Estimate the student's expected **salary in LPA** (Lakh Per Annum)

Built on a **decoupled architecture** — FastAPI handles all ML logic as a REST API, while Streamlit acts as an independent frontend client.

---

##  Architecture

```
┌─────────────────────────┐         HTTP POST (JSON)        ┌──────────────────────────┐
│                         │ ──────────────────────────────▶ │                          │
│   Streamlit Frontend    │                                  │   FastAPI Backend        │
│   (frontend.py)         │ ◀────────────────────────────── │   (backend.py)           │
│   localhost:8501        │         JSON Response            │   localhost:8000         │
│                         │                                  │                          │
└─────────────────────────┘                                  └──────────┬───────────────┘
                                                                        │
                                                             ┌──────────▼───────────────┐
                                                             │   ML Models (.pkl)        │
                                                             │   best_model.pkl          │
                                                             │   best_model_regression   │
                                                             └──────────────────────────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| Placement Prediction | Classifies student as **Placed** or **Not Placed** with probability score |
| Salary Estimation | Predicts estimated salary with benchmark comparison chart |
| Combined Prediction | Single API call returns both placement + salary simultaneously |
| Interactive Dashboard | Gauge charts, donut charts, and salary benchmark visualization |
| Swagger UI | Auto-generated API documentation at `/docs` |
| MLflow Tracking | All experiments logged with parameters, metrics, and artifacts |

---

##  Model Performance

### Classification (Placement Prediction)

| Model | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.8512 | 0.8701 | 0.9102 | 0.8892 | 0.9105 |
| **Random Forest ✓** | **0.8920** | **0.9120** | **0.9680** | **0.9392** | **0.8933** |
| Gradient Boosting | 0.8864 | 0.9047 | 0.9691 | 0.9358 | 0.9022 |
| SVM | 0.8600 | 0.8793 | 0.9124 | 0.8948 | 0.8889 |

> ✅ **Best Model: Random Forest** — F1-Score: **0.9392**

### Regression (Salary Prediction)

| Model | MAE | RMSE | R² |
|-------|-----|------|-----|
| Linear Regression | 2.891 | 3.812 | 0.541 |
| Ridge Regression | 2.887 | 3.809 | 0.542 |
| Random Forest | 2.634 | 3.601 | 0.589 |
| **Gradient Boosting ✓** | **2.576** | **3.534** | **0.587** |

> ✅ **Best Model: Gradient Boosting** — MAE: **2.576 LPA**

---

##  Dataset

- **Source**: A.csv (features) + A_targets.csv (targets)
- **Size**: 5,000 student records
- **Features**: 22 input features (15 numerical + 7 categorical)
- **Targets**: `placement_status` (Placed/Not Placed) + `salary_lpa` (continuous)

### Feature Categories

| Category | Features |
|----------|---------|
| Academic | CGPA, 10th %, 12th %, Backlogs, Attendance, Study Hours |
| Skills | Coding, Communication, Aptitude (rated 1–10) |
| Experience | Internships, Projects, Hackathons, Certifications |
| Lifestyle | Sleep Hours, Stress Level |
| Profile | Gender, Branch, Part-time Job, Family Income, City Tier, Internet Access, Extracurricular |

### Engineered Features (7 new)
```python
skill_composite    = avg(coding + communication + aptitude)
academic_score     = weighted avg(cgpa×0.4 + twelfth×0.3 + tenth×0.3)
experience_score   = internships×2 + projects + hackathons + certifications
study_efficiency   = cgpa / (study_hours + 1)
wellness_score     = sleep_hours - (stress_level / 10)
has_no_backlog     = 1 if backlogs == 0 else 0
high_attendance    = 1 if attendance >= 75% else 0
```

---

##  How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Step 1 — Start Backend (FastAPI)
```bash
python backend.py
# Running on: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

### Step 2 — Start Frontend (Streamlit) in a new terminal
```bash
streamlit run frontend.py
# Running on: http://localhost:8501
```

### Step 3 — (Optional) Train Models
```bash
# Classification model
python pipeline.py

# Regression model
python pipeline_regression.py
```

---

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Check API & model status |
| `GET` | `/model/info` | Model algorithm & metrics info |
| `POST` | `/predict/classification` | Predict Placed / Not Placed |
| `POST` | `/predict/regression` | Predict estimated salary (LPA) |
| `POST` | `/predict/both` | Predict placement + salary in one call |

### Example Request
```bash
curl -X POST "http://localhost:8000/predict/classification" \
  -H "Content-Type: application/json" \
  -d '{
    "cgpa": 8.5,
    "coding_skill_rating": 8,
    "internships_completed": 2,
    "backlogs": 0,
    "attendance_percentage": 88.0,
    "branch": "CSE",
    "gender": "Female",
    "city_tier": "Tier 1",
    ...
  }'
```

### Example Response
```json
{
  "status": "success",
  "placement_status": "Placed",
  "probability_placed": 0.9724,
  "probability_not_placed": 0.0276,
  "confidence": "Sangat Tinggi",
  "input_summary": {
    "cgpa": 8.5,
    "coding_skill": 8,
    "internships": 2,
    "backlogs": 0,
    "attendance": 88.0
  }
}
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Framework | scikit-learn (Pipeline, ColumnTransformer) |
| Experiment Tracking | MLflow |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit + Plotly |
| Data Processing | Pandas, NumPy |
| Model Serialization | Pickle |
| API Validation | Pydantic v2 |

---

##  Project Structure

```
Dsny-uts-modep/
│
├── EDA_model.ipynb          # Exploratory Data Analysis notebook
├── pipeline.py              # Classification ML pipeline + MLflow tracking
├── pipeline_regression.py   # Regression ML pipeline
├── backend.py               # FastAPI REST API server
├── frontend.py              # Streamlit decoupled frontend client
├── app.py                   # Streamlit standalone version
├── best_model.pkl           # Trained Random Forest Classifier
├── best_model_regression.pkl# Trained Gradient Boosting Regressor
└── requirements.txt         # Python dependencies
```

---

##  Author

**Dasnaiya Hsu**
Binus University · Semester 4
📧 dasnaiyaiirene@gmail.com

---

<div align="center">
Made with ❤️ for Model Deployment Course — Binus University 2026
</div>
