# gradtrack-ai
🎓 GradTrack AI — Student Placement & Salary Prediction System
<div align="center">
  <img width="1907" height="1058" alt="ai client" src="https://github.com/user-attachments/assets/70b379d3-bcef-44d6-92fd-c029bf8c01fc" />
<img width="1906" height="929" alt="coba prediksi" src="https://github.com/user-attachments/assets/f59efb72-de37-4848-981a-0accc5f14b03" />
<img width="1904" height="1055" alt="suda jadi" src="https://github.com/user-attachments/assets/f4e59195-5eba-42d6-ab5a-d866c96f05f3" />


An ML-powered system that predicts student job placement status and estimates salary — deployed as a decoupled REST API architecture.
Live Demo · API Docs · Model Performance
</div>

 Overview
GradTrack AI is a machine learning system built as part of the Model Deployment course (UTS Mid Term) at Binus University. It addresses a real problem: students often have no data-driven insight into their employability prospects.
The system solves two tasks:

 Classification — Predict whether a student will be Placed or Not Placed
 Regression — Estimate the student's expected salary in LPA (Lakh Per Annum)

Built on a decoupled architecture — FastAPI handles all ML logic as a REST API, while Streamlit acts as an independent frontend client.

 Architecture
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

 Features
FeatureDescription🔮 Placement PredictionClassifies student as Placed or Not Placed with probability score💰 Salary EstimationPredicts estimated salary with benchmark comparison chart🔄 Combined PredictionSingle API call returns both placement + salary simultaneously📊 Interactive DashboardGauge charts, donut charts, and salary benchmark visualization📝 Swagger UIAuto-generated API documentation at /docs🧪 MLflow TrackingAll experiments logged with parameters, metrics, and artifacts

 Model Performance
Classification (Placement Prediction)
ModelAccuracyPrecisionRecallF1-ScoreAUC-ROCLogistic Regression0.85120.87010.91020.88920.9105Random Forest ✓0.89200.91200.96800.93920.8933Gradient Boosting0.88640.90470.96910.93580.9022SVM0.86000.87930.91240.89480.8889

✅ Best Model: Random Forest — F1-Score: 0.9392

Regression (Salary Prediction)
ModelMAERMSER²Linear Regression2.8913.8120.541Ridge Regression2.8873.8090.542Random Forest2.6343.6010.589Gradient Boosting ✓2.5763.5340.587

✅ Best Model: Gradient Boosting — MAE: 2.576 LPA


 Dataset

Source: A.csv (features) + A_targets.csv (targets)
Size: 5,000 student records
Features: 22 input features (15 numerical + 7 categorical)
Targets: placement_status (Placed/Not Placed) + salary_lpa (continuous)

Feature Categories
CategoryFeaturesAcademicCGPA, 10th %, 12th %, Backlogs, Attendance, Study HoursSkillsCoding, Communication, Aptitude (rated 1–10)ExperienceInternships, Projects, Hackathons, CertificationsLifestyleSleep Hours, Stress LevelProfileGender, Branch, Part-time Job, Family Income, City Tier, Internet Access, Extracurricular
Engineered Features (7 new)
pythonskill_composite    = avg(coding + communication + aptitude)
academic_score     = weighted avg(cgpa×0.4 + twelfth×0.3 + tenth×0.3)
experience_score   = internships×2 + projects + hackathons + certifications
study_efficiency   = cgpa / (study_hours + 1)
wellness_score     = sleep_hours - (stress_level / 10)
has_no_backlog     = 1 if backlogs == 0 else 0
high_attendance    = 1 if attendance >= 75% else 0

 How to Run
Prerequisites
bashpip install -r requirements.txt
Step 1 — Start Backend (FastAPI)
bashpython backend.py
# Running on: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
Step 2 — Start Frontend (Streamlit) in a new terminal
bashstreamlit run frontend.py
# Running on: http://localhost:8501
Step 3 — (Optional) Train Models
bash# Classification model
python pipeline.py

# Regression model
python pipeline_regression.py

 API Endpoints
MethodEndpointDescriptionGET/healthCheck API & model statusGET/model/infoModel algorithm & metrics infoPOST/predict/classificationPredict Placed / Not PlacedPOST/predict/regressionPredict estimated salary (LPA)POST/predict/bothPredict placement + salary in one call
Example Request
bashcurl -X POST "http://localhost:8000/predict/classification" \
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
Example Response
json{
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

Tech Stack
LayerTechnologyML Frameworkscikit-learn (Pipeline, ColumnTransformer)Experiment TrackingMLflowBackend APIFastAPI + UvicornFrontendStreamlit + PlotlyData ProcessingPandas, NumPyModel SerializationPickleAPI ValidationPydantic v2


 Project Structure
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

👩‍💻 Author
Dasnaiya Hsu
Binus University · Semester 4
📧 dasnaiyaiirene@gmail.com

<div align="center">
Made with ❤️ for Model Deployment Course — Binus University 2026
</div>
