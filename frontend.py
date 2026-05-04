import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
 
# ── Config ────────────────────────────────────────────────────
API_URL = "http://localhost:8000"
 
st.set_page_config(
    page_title="GradTrack AI — Client",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0a0f; }
.stApp::before {
    content:''; position:fixed; top:-50%; left:-50%; width:200%; height:200%;
    background: radial-gradient(ellipse at 20% 20%, rgba(124,58,237,0.12) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(6,182,212,0.10) 0%, transparent 50%);
    pointer-events:none; z-index:0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #0f0f1f 100%) !important;
    border-right: 1px solid rgba(124,58,237,0.2) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}
[data-testid="stSidebar"] [data-testid="stThumbValue"] {
    color: #a78bfa !important; font-weight: 700 !important;
}
div[data-baseweb="select"] > div {
    background: rgba(124,58,237,0.08) !important;
    border: 1px solid rgba(124,58,237,0.25) !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
}
div[data-baseweb="select"] svg { fill: #a78bfa !important; }
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 0.95rem !important; width: 100% !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important; padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important; color: #64748b !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(6,182,212,0.2)) !important;
    color: #a78bfa !important;
}
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 1.5rem;
}
.result-placed {
    background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(6,182,212,0.05));
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 20px; padding: 2rem; text-align: center;
}
.result-not-placed {
    background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(251,113,133,0.05));
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 20px; padding: 2rem; text-align: center;
}
.sidebar-section {
    font-size: 0.7rem !important; font-weight: 800 !important;
    text-transform: uppercase !important; letter-spacing: 2.5px !important;
    color: #7c3aed !important; margin: 1.2rem 0 0.6rem !important;
    padding-bottom: 0.4rem !important;
    border-bottom: 1px solid rgba(124,58,237,0.2) !important;
}
.api-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3);
    color: #34d399; padding: 4px 12px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600;
}
.api-badge-error {
    background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3);
    color: #f87171;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important; padding: 0.8rem !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #a78bfa !important; font-weight: 700 !important; }
hr { border-color: rgba(255,255,255,0.06) !important; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.4); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)
 
 
# ── Helper: cek koneksi API ───────────────────────────────────
def check_api():
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.status_code == 200, r.json()
    except Exception:
        return False, {}
 
 
# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:0.5rem 0 1rem;">
        <div style="font-size:2.5rem;">🎓</div>
        <div style="font-size:1.1rem; font-weight:800; color:#a78bfa;">GradTrack AI</div>
        <div style="font-size:0.72rem; color:#475569;">Decoupled Architecture</div>
    </div>
    """, unsafe_allow_html=True)
 
    # Status API
    api_ok, api_info = check_api()
    if api_ok:
        st.markdown('<div class="api-badge">🟢 API Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-badge api-badge-error">🔴 API Offline</div>', unsafe_allow_html=True)
        st.warning("Jalankan backend.py dulu:\n```\npython backend.py\n```")
 
    st.markdown('<hr>', unsafe_allow_html=True)
 
    st.markdown('<p class="sidebar-section">📚 Akademik</p>', unsafe_allow_html=True)
    cgpa               = st.slider("CGPA", 0.0, 10.0, 7.5, 0.1, format="%.1f")
    tenth_percentage   = st.slider("Nilai SMP (%)", 40.0, 100.0, 75.0, 0.5)
    twelfth_percentage = st.slider("Nilai SMA (%)", 40.0, 100.0, 75.0, 0.5)
    backlogs           = st.slider("Backlogs", 0, 20, 0)
    attendance_pct     = st.slider("Kehadiran (%)", 40.0, 100.0, 80.0, 0.5)
    study_hours        = st.slider("Jam Belajar/Hari", 0.0, 12.0, 4.0, 0.5)
 
    st.markdown('<p class="sidebar-section">💡 Keterampilan</p>', unsafe_allow_html=True)
    coding_skill   = st.slider("Coding Skill", 1, 10, 6)
    comm_skill     = st.slider("Communication Skill", 1, 10, 6)
    aptitude_skill = st.slider("Aptitude Skill", 1, 10, 6)
 
    st.markdown('<p class="sidebar-section">🚀 Pengalaman</p>', unsafe_allow_html=True)
    internships    = st.slider("Internship", 0, 5, 0)
    projects       = st.slider("Proyek Selesai", 0, 20, 2)
    hackathons     = st.slider("Hackathon", 0, 10, 1)
    certifications = st.slider("Sertifikasi", 0, 15, 1)
 
    st.markdown('<p class="sidebar-section">🌙 Gaya Hidup</p>', unsafe_allow_html=True)
    sleep_hours  = st.slider("Jam Tidur/Hari", 3.0, 10.0, 7.0, 0.5)
    stress_level = st.slider("Tingkat Stres", 1, 10, 5)
 
    st.markdown('<p class="sidebar-section">👤 Profil</p>', unsafe_allow_html=True)
    gender          = st.selectbox("Gender", ["Male", "Female"])
    branch          = st.selectbox("Jurusan", ["CSE","ECE","ME","CE","EE","IT","Other"])
    part_time_job   = st.selectbox("Part-time Job", ["Yes","No"])
    family_income   = st.selectbox("Pendapatan Keluarga", ["Low","Medium","High"])
    city_tier       = st.selectbox("Tier Kota", ["Tier 1","Tier 2","Tier 3"])
    internet        = st.selectbox("Akses Internet", ["Yes","No"])
    extracurricular = st.selectbox("Ekstrakurikuler", ["Low","Medium","High","Unknown"])
 
    st.markdown('<hr>', unsafe_allow_html=True)
 
 
# Payload untuk dikirim ke API
payload = {
    "cgpa": cgpa, "tenth_percentage": tenth_percentage,
    "twelfth_percentage": twelfth_percentage, "backlogs": backlogs,
    "attendance_percentage": attendance_pct, "study_hours_per_day": study_hours,
    "coding_skill_rating": coding_skill, "communication_skill_rating": comm_skill,
    "aptitude_skill_rating": aptitude_skill, "projects_completed": projects,
    "internships_completed": internships, "hackathons_participated": hackathons,
    "certifications_count": certifications, "sleep_hours": sleep_hours,
    "stress_level": stress_level, "gender": gender, "branch": branch,
    "part_time_job": part_time_job, "family_income_level": family_income,
    "city_tier": city_tier, "internet_access": internet,
    "extracurricular_involvement": extracurricular,
}
 
 
# ── HEADER ────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 1rem 1rem;">
    <div style="font-size:clamp(1.8rem,5vw,3rem); font-weight:900;
        background:linear-gradient(135deg,#a78bfa 0%,#06b6d4 50%,#10b981 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text; letter-spacing:-1.5px; margin-bottom:0.5rem;">
        GradTrack AI
    </div>
    <p style="color:#64748b; font-size:0.95rem;">Decoupled Architecture — Streamlit Client + FastAPI Backend</p>
    <div style="display:inline-flex; gap:0.5rem; margin-top:0.8rem; flex-wrap:wrap; justify-content:center;">
        <span style="background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);color:#a78bfa;padding:0.2rem 0.7rem;border-radius:999px;font-size:0.72rem;font-weight:600;">FastAPI Backend</span>
        <span style="background:rgba(6,182,212,0.15);border:1px solid rgba(6,182,212,0.3);color:#22d3ee;padding:0.2rem 0.7rem;border-radius:999px;font-size:0.72rem;font-weight:600;">Streamlit Frontend</span>
        <span style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);color:#34d399;padding:0.2rem 0.7rem;border-radius:999px;font-size:0.72rem;font-weight:600;">REST API</span>
    </div>
</div>
""", unsafe_allow_html=True)
 
st.markdown("---")
 
# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔮 Klasifikasi (Placement)",
    "💰 Regresi (Salary)",
    "🔄 Prediksi Keduanya"
])
 
 
# ══════════════════════════════════════════════════════════════
# TAB 1 — KLASIFIKASI
# Skenario 1: Mahasiswa berprestasi tinggi
# Skenario 2: Mahasiswa dengan performa rendah
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 🔮 Prediksi Status Placement")
    st.markdown("Mengirim request **POST** ke `/predict/classification`")
 
    col_btn1, col_btn2, col_btn3 = st.columns(3)
 
    # Tombol skenario preset
    with col_btn1:
        sc1 = st.button("📌 Skenario 1: Mahasiswa Berprestasi", use_container_width=True)
    with col_btn2:
        sc2 = st.button("📌 Skenario 2: Mahasiswa Rata-rata", use_container_width=True)
    with col_btn3:
        predict_clf = st.button("🔮 Prediksi dari Sidebar", use_container_width=True)
 
    # Skenario preset payloads
    scenario1 = {**payload, "cgpa":9.2,"coding_skill_rating":9,"internships_completed":3,
                 "projects_completed":8,"backlogs":0,"attendance_percentage":95.0,
                 "aptitude_skill_rating":9,"communication_skill_rating":8}
    scenario2 = {**payload, "cgpa":5.5,"coding_skill_rating":4,"internships_completed":0,
                 "projects_completed":1,"backlogs":5,"attendance_percentage":60.0,
                 "aptitude_skill_rating":4,"communication_skill_rating":5}
 
    clf_payload = None
    if sc1:   clf_payload = scenario1
    elif sc2: clf_payload = scenario2
    elif predict_clf: clf_payload = payload
 
    if clf_payload:
        with st.spinner("Mengirim request ke API..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict/classification",
                    json=clf_payload, timeout=10
                )
                result = response.json()
 
                if response.status_code == 200:
                    placed_prob     = result["probability_placed"] * 100
                    not_placed_prob = result["probability_not_placed"] * 100
                    is_placed       = result["placement_status"] == "Placed"
 
                    col1, col2 = st.columns([1.1, 1], gap="medium")
 
                    with col1:
                        if is_placed:
                            st.markdown(f"""
                            <div class="result-placed">
                                <div style="font-size:3rem; margin-bottom:0.5rem;">🎉</div>
                                <div style="font-size:1.8rem; font-weight:900; color:#10b981; margin-bottom:0.5rem;">PLACED!</div>
                                <p style="color:#94a3b8; font-size:0.9rem;">
                                    Probabilitas: <strong style="color:#34d399; font-family:'JetBrains Mono',monospace">{placed_prob:.1f}%</strong><br>
                                    Confidence: <strong style="color:#34d399">{result['confidence']}</strong>
                                </p>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="result-not-placed">
                                <div style="font-size:3rem; margin-bottom:0.5rem;">📈</div>
                                <div style="font-size:1.8rem; font-weight:900; color:#ef4444; margin-bottom:0.5rem;">Not Placed</div>
                                <p style="color:#94a3b8; font-size:0.9rem;">
                                    Probabilitas Placed: <strong style="color:#f87171; font-family:'JetBrains Mono',monospace">{placed_prob:.1f}%</strong><br>
                                    Confidence: <strong style="color:#f87171">{result['confidence']}</strong>
                                </p>
                            </div>""", unsafe_allow_html=True)
 
                        # Gauge
                        fig_g = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=placed_prob,
                            title={"text":"Prob. Placed","font":{"color":"#64748b","size":12}},
                            number={"font":{"color":"#a78bfa","size":36,"family":"JetBrains Mono"},"suffix":"%"},
                            gauge={
                                "axis":{"range":[0,100],"tickcolor":"#334155","tickfont":{"size":9,"color":"#475569"}},
                                "bar":{"color":"#7c3aed","thickness":0.25},
                                "bgcolor":"rgba(0,0,0,0)","borderwidth":0,
                                "steps":[
                                    {"range":[0,40],"color":"rgba(239,68,68,0.15)"},
                                    {"range":[40,70],"color":"rgba(251,191,36,0.15)"},
                                    {"range":[70,100],"color":"rgba(16,185,129,0.15)"},
                                ],
                                "threshold":{"line":{"color":"#10b981","width":2},"thickness":0.8,"value":70}
                            }
                        ))
                        fig_g.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            height=200, margin=dict(t=35,b=5,l=20,r=20)
                        )
                        st.plotly_chart(fig_g, use_container_width=True)
 
                    with col2:
                        # Donut
                        fig_d = go.Figure(go.Pie(
                            values=[not_placed_prob, placed_prob],
                            labels=["Not Placed","Placed"], hole=0.65,
                            marker_colors=["#ef4444","#10b981"],
                            marker_line=dict(color="#0a0a0f",width=3),
                            textinfo="label+percent",
                            textfont=dict(color="white",size=11),
                        ))
                        fig_d.add_annotation(
                            text=f"<b>{placed_prob:.0f}%</b><br>Placed",
                            x=0.5, y=0.5, showarrow=False,
                            font=dict(size=14,color="#a78bfa",family="JetBrains Mono"),
                        )
                        fig_d.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            showlegend=True,
                            legend=dict(font=dict(color="#94a3b8",size=10),orientation="h",x=0.15,y=-0.05),
                            height=220, margin=dict(t=20,b=30,l=10,r=10),
                        )
                        st.plotly_chart(fig_d, use_container_width=True)
 
                        st.markdown("**📋 API Response:**")
                        st.json({
                            "endpoint": "POST /predict/classification",
                            "status": result["status"],
                            "placement_status": result["placement_status"],
                            "probability_placed": result["probability_placed"],
                            "probability_not_placed": result["probability_not_placed"],
                            "confidence": result["confidence"],
                        })
                else:
                    st.error(f"API Error {response.status_code}: {result.get('detail','Unknown error')}")
 
            except requests.exceptions.ConnectionError:
                st.error("Tidak bisa terhubung ke API. Pastikan `python backend.py` sudah dijalankan di terminal lain.")
            except Exception as e:
                st.error(f"Error: {e}")
 
 
# ══════════════════════════════════════════════════════════════
# TAB 2 — REGRESI
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 💰 Prediksi Estimasi Gaji")
    st.markdown("Mengirim request **POST** ke `/predict/regression`")
 
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        sc3 = st.button("📌 Skenario 1: High Performer", use_container_width=True)
    with col_btn2:
        sc4 = st.button("📌 Skenario 2: Low Performer", use_container_width=True)
    with col_btn3:
        predict_reg = st.button("💰 Prediksi Gaji dari Sidebar", use_container_width=True)
 
    scenario3 = {**payload, "cgpa":9.0,"coding_skill_rating":9,"internships_completed":3,
                 "projects_completed":7,"certifications_count":6,"aptitude_skill_rating":9}
    scenario4 = {**payload, "cgpa":5.0,"coding_skill_rating":3,"internships_completed":0,
                 "projects_completed":0,"certifications_count":0,"aptitude_skill_rating":3}
 
    reg_payload = None
    if sc3:   reg_payload = scenario3
    elif sc4: reg_payload = scenario4
    elif predict_reg: reg_payload = payload
 
    if reg_payload:
        with st.spinner("Mengirim request ke API..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict/regression",
                    json=reg_payload, timeout=10
                )
                result = response.json()
 
                if response.status_code == 200:
                    salary = result["predicted_salary_lpa"]
                    col1, col2 = st.columns([1, 1], gap="medium")
 
                    with col1:
                        st.markdown(f"""
                        <div class="glass-card" style="text-align:center; padding:2rem;">
                            <div style="font-size:3rem; margin-bottom:0.5rem;">💰</div>
                            <div style="font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.5rem;">Estimated Salary</div>
                            <div style="font-size:3rem; font-weight:900; color:#10b981; font-family:'JetBrains Mono',monospace;">{salary:.2f}</div>
                            <div style="font-size:1rem; color:#64748b; margin-bottom:1rem;">LPA (Lakh Per Annum)</div>
                            <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:0.5rem 1rem; display:inline-block;">
                                <span style="color:#34d399; font-size:0.85rem; font-weight:600;">{result['salary_range']}</span>
                            </div>
                        </div>""", unsafe_allow_html=True)
 
                        # Salary gauge
                        fig_sg = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=min(salary, 25),
                            title={"text":"Salary (LPA)","font":{"color":"#64748b","size":12}},
                            number={"font":{"color":"#10b981","size":32,"family":"JetBrains Mono"},"suffix":" LPA"},
                            gauge={
                                "axis":{"range":[0,25],"tickcolor":"#334155","tickfont":{"size":9,"color":"#475569"}},
                                "bar":{"color":"#10b981","thickness":0.25},
                                "bgcolor":"rgba(0,0,0,0)","borderwidth":0,
                                "steps":[
                                    {"range":[0,5],  "color":"rgba(239,68,68,0.12)"},
                                    {"range":[5,12], "color":"rgba(251,191,36,0.12)"},
                                    {"range":[12,25],"color":"rgba(16,185,129,0.12)"},
                                ],
                            }
                        ))
                        fig_sg.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            height=200, margin=dict(t=30,b=5,l=20,r=20)
                        )
                        st.plotly_chart(fig_sg, use_container_width=True)
 
                    with col2:
                        # Salary benchmark comparison
                        benchmarks = {
                            "Entry Level\n(<3 LPA)": 2.0,
                            "Junior\n(3-6 LPA)": 4.5,
                            "Mid Level\n(6-10 LPA)": 8.0,
                            "Prediksi\nKamu": salary,
                            "Senior\n(10-15 LPA)": 12.5,
                        }
                        colors = ["#475569","#475569","#475569","#a78bfa","#475569"]
 
                        fig_bench = go.Figure(go.Bar(
                            x=list(benchmarks.keys()),
                            y=list(benchmarks.values()),
                            marker_color=colors, marker_line=dict(width=0),
                            text=[f"{v:.1f}" for v in benchmarks.values()],
                            textposition="outside",
                            textfont=dict(color="white",size=10,family="JetBrains Mono"),
                        ))
                        fig_bench.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#64748b",family="Inter"),
                            yaxis=dict(range=[0,20],gridcolor="rgba(255,255,255,0.04)",title="LPA"),
                            xaxis=dict(color="#94a3b8"),
                            height=280, margin=dict(t=20,b=10,l=20,r=20),
                            showlegend=False,
                            title=dict(text="Posisi Salary vs Benchmark",font=dict(color="#64748b",size=12),x=0.5),
                        )
                        st.plotly_chart(fig_bench, use_container_width=True)
 
                        st.markdown("**📋 API Response:**")
                        st.json({
                            "endpoint": "POST /predict/regression",
                            "status": result["status"],
                            "predicted_salary_lpa": result["predicted_salary_lpa"],
                            "salary_range": result["salary_range"],
                        })
                elif response.status_code == 503:
                    st.warning("Model regresi belum tersedia. Jalankan pipeline regresi untuk membuat `best_model_regression.pkl`.")
                else:
                    st.error(f"API Error {response.status_code}: {result.get('detail','Unknown error')}")
 
            except requests.exceptions.ConnectionError:
                st.error("Tidak bisa terhubung ke API. Pastikan `python backend.py` sudah dijalankan.")
            except Exception as e:
                st.error(f"Error: {e}")
 
 
# ══════════════════════════════════════════════════════════════
# TAB 3 — BOTH (Prediksi Sekaligus)
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔄 Prediksi Placement + Gaji Sekaligus")
    st.markdown("Mengirim **satu request POST** ke `/predict/both`")
 
    predict_both_btn = st.button("🚀 Prediksi Semuanya Sekarang", use_container_width=True)
 
    if predict_both_btn:
        with st.spinner("Mengirim request ke API..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict/both",
                    json=payload, timeout=10
                )
                result = response.json()
 
                if response.status_code == 200:
                    placed_prob = result["probability_placed"] * 100
                    is_placed   = result["placement_status"] == "Placed"
                    salary      = result.get("predicted_salary_lpa")
 
                    col1, col2, col3 = st.columns(3, gap="medium")
 
                    with col1:
                        status_color = "#10b981" if is_placed else "#ef4444"
                        status_emoji = "🎉" if is_placed else "📈"
                        st.markdown(f"""
                        <div class="glass-card" style="text-align:center; border-color:{status_color}33;">
                            <div style="font-size:2.5rem; margin-bottom:0.5rem;">{status_emoji}</div>
                            <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:2px;">Placement</div>
                            <div style="font-size:1.5rem; font-weight:900; color:{status_color}; margin:0.3rem 0;">{result['placement_status']}</div>
                            <div style="font-size:0.8rem; color:#64748b;">Prob: <span style="color:{status_color}; font-family:'JetBrains Mono',monospace; font-weight:700;">{placed_prob:.1f}%</span></div>
                            <div style="font-size:0.8rem; color:#64748b; margin-top:4px;">Confidence: <span style="color:{status_color};">{result['confidence']}</span></div>
                        </div>""", unsafe_allow_html=True)
 
                    with col2:
                        if salary is not None:
                            st.markdown(f"""
                            <div class="glass-card" style="text-align:center; border-color:rgba(16,185,129,0.3);">
                                <div style="font-size:2.5rem; margin-bottom:0.5rem;">💰</div>
                                <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:2px;">Est. Salary</div>
                                <div style="font-size:1.8rem; font-weight:900; color:#10b981; font-family:'JetBrains Mono',monospace; margin:0.3rem 0;">{salary:.2f}</div>
                                <div style="font-size:0.8rem; color:#64748b;">LPA</div>
                                <div style="font-size:0.75rem; color:#34d399; margin-top:4px;">{result.get('salary_range','')}</div>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="glass-card" style="text-align:center;">
                                <div style="font-size:2.5rem; margin-bottom:0.5rem;">💰</div>
                                <div style="color:#64748b; font-size:0.85rem;">Model regresi<br>tidak tersedia</div>
                            </div>""", unsafe_allow_html=True)
 
                    with col3:
                        st.markdown(f"""
                        <div class="glass-card" style="text-align:center; border-color:rgba(124,58,237,0.3);">
                            <div style="font-size:2.5rem; margin-bottom:0.5rem;">📊</div>
                            <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:2px;">Input Summary</div>
                            <div style="margin-top:0.8rem; text-align:left;">
                                <div style="color:#94a3b8; font-size:0.8rem; margin:3px 0;">CGPA: <span style="color:#a78bfa; font-family:'JetBrains Mono',monospace;">{result['input_summary']['cgpa']}</span></div>
                                <div style="color:#94a3b8; font-size:0.8rem; margin:3px 0;">Coding: <span style="color:#a78bfa; font-family:'JetBrains Mono',monospace;">{result['input_summary']['coding_skill']}/10</span></div>
                                <div style="color:#94a3b8; font-size:0.8rem; margin:3px 0;">Internship: <span style="color:#a78bfa; font-family:'JetBrains Mono',monospace;">{result['input_summary']['internships']}x</span></div>
                                <div style="color:#94a3b8; font-size:0.8rem; margin:3px 0;">Backlogs: <span style="color:#a78bfa; font-family:'JetBrains Mono',monospace;">{result['input_summary']['backlogs']}</span></div>
                                <div style="color:#94a3b8; font-size:0.8rem; margin:3px 0;">Jurusan: <span style="color:#a78bfa; font-family:'JetBrains Mono',monospace;">{result['input_summary']['branch']}</span></div>
                            </div>
                        </div>""", unsafe_allow_html=True)
 
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("**📋 Full API Response:**")
                    st.json(result)
 
                else:
                    st.error(f"API Error {response.status_code}: {result.get('detail','Unknown error')}")
 
            except requests.exceptions.ConnectionError:
                st.error("Tidak bisa terhubung ke API. Pastikan `python backend.py` sudah dijalankan.")
            except Exception as e:
                st.error(f"Error: {e}")