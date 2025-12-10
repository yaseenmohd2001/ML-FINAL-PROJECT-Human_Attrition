import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json

# ============================================
# 🎨 PAGE CONFIG & GLOBAL STYLE
# ============================================
st.set_page_config(page_title="Employee Churn Prediction", layout="wide")

# Enhanced Background + Text Styling with Black Background and Beige Text
page_bg = """
<style>
/* Main Background - Black */
.stApp {
    background: #000000 !important;
}

/* All text outside boxes - Beige */
h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: #F5F5DC !important;
}

/* Brown Titles - Changed to Beige */
h1, h2, h3 {
    color: #F5F5DC !important;
    font-weight: 700 !important;
}

h4, h5, h6 {
    color: #F5F5DC !important;
    font-weight: 600 !important;
}

/* Labels and text */
label {
    color: #F5F5DC !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

/* Remove column background for cleaner look */
div[data-testid="column"] {
    background-color: transparent !important;
    padding: 10px !important;
}

/* ===== NUMBER INPUT STYLING - IMPROVED VISIBILITY ===== */
.stNumberInput > div {
    background-color: transparent !important;
}

.stNumberInput > div > div {
    background-color: transparent !important;
}

.stNumberInput > div > div > input {
    background-color: #2A2A2A !important; /* Dark gray for better contrast */
    color: #F5F5DC !important;
    border: 2px solid #D2B48C !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    padding: 12px 16px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stNumberInput > div > div > input:hover {
    border-color: #F5DEB3 !important;
    box-shadow: 0 4px 12px rgba(210, 180, 140, 0.4) !important;
}

.stNumberInput > div > div > input:focus {
    border-color: #FFD700 !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5) !important;
    background-color: #3A3A3A !important;
}

/* Placeholder text for number inputs */
.stNumberInput > div > div > input::placeholder {
    color: #A0A0A0 !important;
    font-style: italic !important;
}

/* Number input buttons - IMPROVED */
.stNumberInput button {
    background-color: #D2B48C !important;
    color: #000000 !important;
    border: 1px solid #D2B48C !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}

.stNumberInput button:hover {
    background-color: #F5DEB3 !important;
    transform: scale(1.05) !important;
}

/* Text inputs - MATCHING STYLE */
.stTextInput > div > div > input {
    background-color: #2A2A2A !important;
    color: #F5F5DC !important;
    border: 2px solid #D2B48C !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    padding: 12px 16px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:hover {
    border-color: #F5DEB3 !important;
    box-shadow: 0 4px 12px rgba(210, 180, 140, 0.4) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #FFD700 !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5) !important;
    background-color: #3A3A3A !important;
}

.stTextInput > div > div > input::placeholder {
    color: #A0A0A0 !important;
    font-style: italic !important;
}

/* Text area */
.stTextArea textarea {
    background-color: #2A2A2A !important;
    color: #F5F5DC !important;
    border: 2px solid #D2B48C !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    padding: 12px 16px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
}

.stTextArea textarea::placeholder {
    color: #A0A0A0 !important;
    font-style: italic !important;
}

/* ===== SELECTBOX STYLING - IMPROVED TO MATCH NUMBER INPUT ===== */
/* Selectbox container */
div[data-baseweb="select"] {
    background-color: transparent !important;
}

div[data-baseweb="select"] > div {
    background-color: #2A2A2A !important; /* Same as number input */
    border: 2px solid #D2B48C !important;
    border-radius: 10px !important;
    padding: 4px 12px !important;
    min-height: 50px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease !important;
}

/* Hover effect for selectbox */
div[data-baseweb="select"] > div:hover {
    border-color: #F5DEB3 !important;
    box-shadow: 0 4px 12px rgba(210, 180, 140, 0.4) !important;
}

/* Focus effect for selectbox */
div[data-baseweb="select"] > div:focus-within {
    border-color: #FFD700 !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5) !important;
    background-color: #3A3A3A !important;
}

/* Selected text in selectbox */
div[data-baseweb="select"] > div > div {
    color: #F5F5DC !important; /* Same as input text */
    font-weight: 500 !important;
    font-size: 16px !important;
    padding: 6px 0 !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    fill: #F5F5DC !important;
    transition: transform 0.3s ease !important;
}

div[data-baseweb="select"] > div:hover svg {
    fill: #F5DEB3 !important;
}

/* Dropdown menu */
ul[role="listbox"] {
    background-color: #2A2A2A !important;
    border: 2px solid #D2B48C !important;
    border-radius: 10px !important;
    margin-top: 5px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
}

/* Dropdown options */
li[role="option"] {
    background-color: #2A2A2A !important;
    color: #F5F5DC !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
    transition: all 0.2s ease !important;
}

/* Hover state for options */
li[role="option"]:hover {
    background-color: #3A3A3A !important;
    color: #FFD700 !important;
}

/* Selected option */
li[role="option"][aria-selected="true"] {
    background-color: #D2B48C !important;
    color: #000000 !important;
    font-weight: 600 !important;
}

/* ===== BUTTON STYLING ===== */
.stButton > button {
    background: linear-gradient(135deg, #D2B48C 0%, #B8860B 100%) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 20px rgba(210, 180, 140, 0.4) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(210, 180, 140, 0.5) !important;
    background: linear-gradient(135deg, #F5DEB3 0%, #D2B48C 100%) !important;
}

/* Home button styling */
.home-button {
    background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%) !important;
    color: #F5F5DC !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 10px rgba(139, 69, 19, 0.4) !important;
    transition: all 0.3s ease !important;
}

.home-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(139, 69, 19, 0.5) !important;
    background: linear-gradient(135deg, #A0522D 0%, #8B4513 100%) !important;
}

/* Info cards - Dark gray background */
.info-card {
    background: #2A2A2A !important;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
    border-left: 5px solid #D2B48C;
    margin: 10px 0;
    height: 320px; /* Reduced height */
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    border: 1px solid #444 !important;
    overflow-y: auto;
}

/* Info card text - Beige */
.info-card h3, .info-card h4 {
    color: #F5F5DC !important;
    border-bottom: 2px solid #D2B48C;
    padding-bottom: 10px;
    margin-bottom: 15px;
    font-size: 1.2em;
}

.info-card p {
    color: #D2B48C !important;
    line-height: 1.5;
    margin-bottom: 8px;
    font-size: 0.95em;
}

.info-card strong {
    color: #F5F5DC !important;
}

.info-card ul, .info-card ol {
    color: #D2B48C !important;
    padding-left: 20px;
    margin-bottom: 10px;
}

.info-card li {
    margin-bottom: 5px;
    font-size: 0.95em;
}

/* Employee summary cards */
.summary-card {
    background: #2A2A2A !important;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    margin: 10px 0;
    border: 1px solid #444 !important;
}

/* Summary card text */
.summary-card h4 {
    color: #F5F5DC !important;
    border-bottom: 2px solid #D2B48C;
    padding-bottom: 10px;
    margin-bottom: 15px;
}

.summary-card p {
    color: #D2B48C !important;
}

.summary-card strong {
    color: #F5F5DC !important;
}

/* Risk alert box */
.risk-alert {
    background: linear-gradient(135deg, rgba(210, 180, 140, 0.9) 0%, rgba(184, 134, 11, 0.9) 100%);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
    margin: 20px 0;
    border: 2px solid #F5F5DC !important;
}

.risk-alert h2, .risk-alert h3, .risk-alert p {
    color: #000000 !important;
}

/* Metric styling */
div[data-testid="stMetricValue"] {
    color: #F5F5DC !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

div[data-testid="stMetricLabel"] {
    color: #F5F5DC !important;
    font-weight: 600 !important;
}

/* Error messages */
.stAlert {
    background-color: rgba(139, 0, 0, 0.2) !important;
    border: 2px solid #8B0000 !important;
    border-radius: 8px !important;
    color: #F5F5DC !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    gap: 10px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: #2A2A2A !important;
    color: #F5F5DC !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid #444 !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: #3A3A3A !important;
    border-color: #D2B48C !important;
}

.stTabs [aria-selected="true"] {
    background-color: #D2B48C !important;
    color: #000000 !important;
    border-color: #D2B48C !important;
}

/* Radio button styling */
.stRadio > div {
    background-color: #2A2A2A !important;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444 !important;
}

.stRadio label {
    color: #F5F5DC !important;
}

/* Slider styling */
.stSlider > div > div > div {
    background-color: #D2B48C !important;
}

.stSlider > div > div > div > div {
    background-color: #F5F5DC !important;
}

/* Make Lottie animation background transparent */
.st_lottie {
    background-color: transparent !important;
}

/* Fix for any remaining white backgrounds */
iframe {
    background-color: transparent !important;
}

/* Make sure all containers have transparent backgrounds */
section.main > div, div.block-container {
    background-color: transparent !important;
}

/* Scrollbar styling for info cards */
.info-card::-webkit-scrollbar {
    width: 8px;
}

.info-card::-webkit-scrollbar-track {
    background: #1A1A1A;
    border-radius: 4px;
}

.info-card::-webkit-scrollbar-thumb {
    background: #D2B48C;
    border-radius: 4px;
}

.info-card::-webkit-scrollbar-thumb:hover {
    background: #B8860B;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load Lottie animations with double size
def load_lottie(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

# ============================================
# SESSION STATE
# ============================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "prediction_proba" not in st.session_state:
    st.session_state.prediction_proba = None
if "emp_data" not in st.session_state:
    st.session_state.emp_data = {}

# ============================================
# LOAD MODELS
# ============================================
@st.cache_resource
def load_models():
    return {
        "rf": pickle.load(open("rf.sav", "rb")),
        "sc": pickle.load(open("sc.sav", "rb")),
        "enc_attrition": pickle.load(open("enc_attrition.sav", "rb")),
        "enc_businesstravel": pickle.load(open("enc_businesstravel.sav", "rb")),
        "enc_department": pickle.load(open("enc_department.sav", "rb")),
        "enc_educationfield": pickle.load(open("enc_educationfield.sav", "rb")),
        "enc_gender": pickle.load(open("enc_gender.sav", "rb")),
        "enc_jobrole": pickle.load(open("enc_jobrole.sav", "rb")),
        "enc_maritalstatus": pickle.load(open("enc_maritalstatus.sav", "rb")),
        "enc_overtime": pickle.load(open("enc_overtime.sav", "rb")),
    }

# ============================================
# HOME PAGE - Updated with Lottie animation at top (0.75x size = 360px)
# ============================================
def home_page():
    st.title("🏢 Employee Churn Prediction System")
    st.markdown("### *Predict and Prevent Employee Attrition with AI-Powered Insights*")

    # Lottie Animation at the TOP below heading - Reduced to 0.75 of original (360px)
    lottie_data = load_lottie("home.json")
    if lottie_data:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Transparent container for Lottie animation
            st.markdown(
                '<div style="background-color: transparent; border-radius: 15px; padding: 10px;">',
                unsafe_allow_html=True,
            )
            st_lottie(lottie_data, height=360, key="home_lottie")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Project Overview - ONLY 3 info boxes with corrected HTML (escaped ampersands)
    st.markdown("## 📌 Project Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="info-card">
                <h3>📊 Employee Attrition</h3>
                <p>Employee attrition refers to the gradual reduction in workforce due to resignations, retirements, or departures without immediate replacements.</p>
                <p><strong>Impact on Business:</strong></p>
                <ul>
                    <li>Reduced productivity &amp; efficiency</li>
                    <li>Increased recruitment costs</li>
                    <li>Loss of institutional knowledge</li>
                    <li>Decreased team morale</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="info-card">
                <h3>🎯 Why Predict Attrition?</h3>
                <p><strong>Proactive Approach:</strong></p>
                <p>Identify at-risk employees before they decide to leave, allowing for timely intervention.</p>
                <p><strong>Cost Savings:</strong></p>
                <p>Reduce turnover costs by addressing issues before they lead to resignation.</p>
                <p><strong>Talent Retention:</strong></p>
                <p>Improve employee satisfaction by identifying and resolving pain points.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="info-card">
                <h3>🚀 How It Works</h3>
                <p><strong>Step 1:</strong> Enter employee data through our intuitive interface</p>
                <p><strong>Step 2:</strong> Our ML model analyzes the data for patterns</p>
                <p><strong>Step 3:</strong> Get risk assessment with probability score</p>
                <p><strong>Step 4:</strong> Receive actionable insights for retention</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Start Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Start Prediction", use_container_width=True, key="home_start_button"):
            st.session_state.page = "input"
            st.rerun()

    # Home button (already on home page, just for consistency)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding: 20px;">
                <p style="color: #D2B48C; font-size: 14px;">You are currently on the Home Page</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================
# INPUT PAGE - Fixed duplicate element ID error
# ============================================
def input_page():
    models = load_models()
    st.header("📝 Employee Information Entry")
    st.markdown("*Please provide accurate information for best prediction results*")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Function to create selectbox with unique keys
    def sel(label, options, key_suffix):
        st.markdown(f"<div style='margin-bottom: 5px;'>{label}</div>", unsafe_allow_html=True)
        return st.selectbox("", ["- Select -"] + list(options), 
                          label_visibility="collapsed", 
                          key=f"select_{key_suffix}")
    
    with col1:
        st.markdown("### 👤 Personal Information")
        age = st.number_input("Age", 18, 65, 18, help="Employee's current age", key="age_input")
        gender = sel("Gender", models["enc_gender"].classes_, "gender")
        marital = sel("Marital Status", models["enc_maritalstatus"].classes_, "marital")
        dist = st.number_input("Distance From Home (km)", 0, 50, 0, 
                              help="Distance from home to workplace in kilometers", key="dist_input")
        
        st.markdown("### 💼 Work Experience")
        total_years = st.number_input("Total Working Years", 0, 40, 0, 
                                     help="Total years of professional experience", key="total_years_input")
        yrs_comp = st.number_input("Years At Company", 0, 40, 0, 
                                  help="Years with current company", key="yrs_comp_input")
        yrs_role = st.number_input("Years in Current Role", 0, 20, 0, 
                                  help="Years in current position", key="yrs_role_input")
        
        st.markdown("### 🎓 Education")
        education = sel("Education Level (1-5)", [1, 2, 3, 4, 5], "education")
        edu_field = sel("Education Field", models["enc_educationfield"].classes_, "edu_field")
    
    with col2:
        st.markdown("### 🏢 Job Details")
        dept = sel("Department", models["enc_department"].classes_, "dept")
        job = sel("Job Role", models["enc_jobrole"].classes_, "job")
        job_lvl = sel("Job Level (1-5)", [1, 2, 3, 4, 5], "job_lvl")
        
        st.markdown("### 💰 Compensation & Work")
        income = st.number_input("Monthly Income ($)", 0, 20000, 0, 
                                help="Gross monthly income in USD", key="income_input")
        travel = sel("Business Travel", models["enc_businesstravel"].classes_, "travel")
        overtime = sel("OverTime", models["enc_overtime"].classes_, "overtime")
        
        st.markdown("### 😊 Job Satisfaction")
        job_sat = sel("Job Satisfaction (1-4)", [1, 2, 3, 4], "job_sat")
    
    required = [gender, marital, dept, job, job_lvl, travel, overtime, edu_field, job_sat, education]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔮 Predict Attrition", use_container_width=True, key="predict_button"):
            if any(r == "- Select -" for r in required):
                st.error("⚠️ Please fill all required fields.")
                return
            
            # Store employee data
            st.session_state.emp_data = {
                "Age": age,
                "Gender": gender,
                "Marital Status": marital,
                "Distance from Home": f"{dist} km",
                "Education Level": education,
                "Education Field": edu_field,
                "Department": dept,
                "Job Role": job,
                "Job Level": job_lvl,
                "Business Travel": travel,
                "OverTime": overtime,
                "Total Working Years": total_years,
                "Years at Company": yrs_comp,
                "Years in Current Role": yrs_role,
                "Monthly Income": f"${income}",
                "Job Satisfaction": f"{job_sat}/4"
            }
            
            X = [
                age,
                models["enc_gender"].transform([gender])[0],
                models["enc_maritalstatus"].transform([marital])[0],
                models["enc_department"].transform([dept])[0],
                models["enc_businesstravel"].transform([travel])[0],
                models["enc_jobrole"].transform([job])[0],
                int(job_lvl),
                int(education),
                models["enc_educationfield"].transform([edu_field])[0],
                models["enc_overtime"].transform([overtime])[0],
                total_years,
                yrs_comp,
                yrs_role,
                income,
                dist,
                int(job_sat)
            ]
            
            X_scaled = models["sc"].transform(np.array(X).reshape(1, -1))
            pred = models["rf"].predict(X_scaled)[0]
            proba = models["rf"].predict_proba(X_scaled)[0]
            
            st.session_state.prediction_result = pred
            st.session_state.prediction_proba = proba
            st.session_state.page = "results"
            st.rerun()
    
    # Home button at bottom
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏠 Go to Home", use_container_width=True, key="input_home_button"):
            st.session_state.page = "home"
            st.rerun()

# ============================================
# RESULT PAGE - Updated with Lottie animation below risk box (0.75x size = 300px)
# ============================================
def results_page():
    st.markdown("# 📊 Prediction Results")
    
    proba = st.session_state.prediction_proba
    risk = proba[1] * 100
    stay = proba[0] * 100
    
    # Risk Assessment
    if risk < 30:
        risk_level = "LOW"
        risk_message = "Low risk. Employee is likely to stay."
        risk_color = "#90EE90"
        border_color = "#4CAF50"
    elif risk < 70:
        risk_level = "MODERATE"
        risk_message = "Moderate risk. Consider retention measures."
        risk_color = "#FFD700"
        border_color = "#FF9800"
    else:
        risk_level = "HIGH"
        risk_message = "High risk. Immediate action recommended."
        risk_color = "#FF6347"
        border_color = "#F44336"
    
    st.markdown(f"""
    <div class="risk-alert" style="background: linear-gradient(135deg, {risk_color}80 0%, {risk_color}60 100%); border-color: {border_color} !important;">
        <h2 style="color: #000000; font-size: 32px;">⚠️ {risk_level} RISK OF ATTRITION</h2>
        <p style="font-size: 20px; color: #000000; font-weight: 600; margin: 15px 0;">{risk_message}</p>
        <h3 style="color: #000000; margin-top: 20px; font-size: 28px;">Attrition probability: {risk:.1f}%</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Lottie Animation BELOW risk box - Reduced to 0.75 of original (300px)
    lottie_data = load_lottie("result.json")
    if lottie_data:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Transparent container for Lottie animation
            st.markdown("""
            <div style="background-color: transparent; border-radius: 15px; padding: 10px;">
            """, unsafe_allow_html=True)
            st_lottie(lottie_data, height=300, key="results_lottie")
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Attrition Risk Score")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'size': 40, 'color': '#F5F5DC'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#F5F5DC"},
                'bar': {'color': "#8B0000"},
                'bgcolor': "rgba(0,0,0,0.3)",
                'borderwidth': 2,
                'bordercolor': "#F5F5DC",
                'steps': [
                    {'range': [0, 30], 'color': '#90EE90'},
                    {'range': [30, 70], 'color': '#FFD700'},
                    {'range': [70, 100], 'color': '#FF6347'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': risk
                }
            }
        ))
        fig_gauge.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0.5)',
            font={'color': "#F5F5DC", 'size': 14}
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("### Prediction Probabilities")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=['Will Stay', 'Will Leave'],
            y=[stay, risk],
            text=[f'{stay:.1f}%', f'{risk:.1f}%'],
            textposition='outside',
            marker_color=['#4CAF50', '#F44336'],
            textfont=dict(size=16, color='#F5F5DC', family='Arial Black'),
            marker_line_color='#F5F5DC',
            marker_line_width=2
        ))
        fig_bar.update_layout(
            height=350,
            yaxis=dict(
                title=dict(text="Probability (%)", font=dict(size=14, color='#F5F5DC')),
                range=[0, 100],
                tickfont=dict(size=12, color='#F5F5DC'),
                gridcolor='rgba(245, 245, 220, 0.2)'
            ),
            xaxis=dict(
                title=dict(text="Outcome", font=dict(size=14, color='#F5F5DC')),
                tickfont=dict(size=12, color='#F5F5DC')
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0.5)',
            plot_bgcolor='rgba(0,0,0,0.3)',
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Employee Summary
    st.markdown("## 📋 Employee Summary")
    
    emp_data = st.session_state.emp_data
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="summary-card">
            <h4 style="color: #F5F5DC;">👤 Personal Details</h4>
            <p><strong>Age:</strong> {emp_data['Age']}</p>
            <p><strong>Gender:</strong> {emp_data['Gender']}</p>
            <p><strong>Marital Status:</strong> {emp_data['Marital Status']}</p>
            <p><strong>Distance from Home:</strong> {emp_data['Distance from Home']}</p>
            <p><strong>Education Level:</strong> {emp_data['Education Level']}</p>
            <p><strong>Education Field:</strong> {emp_data['Education Field']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="summary-card">
            <h4 style="color: #F5F5DC;">💼 Job Information</h4>
            <p><strong>Department:</strong> {emp_data['Department']}</p>
            <p><strong>Job Role:</strong> {emp_data['Job Role']}</p>
            <p><strong>Job Level:</strong> {emp_data['Job Level']}</p>
            <p><strong>Business Travel:</strong> {emp_data['Business Travel']}</p>
            <p><strong>OverTime:</strong> {emp_data['OverTime']}</p>
            <p><strong>Job Satisfaction:</strong> {emp_data['Job Satisfaction']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="summary-card">
            <h4 style="color: #F5F5DC;">📊 Work Experience</h4>
            <p><strong>Total Working Years:</strong> {emp_data['Total Working Years']}</p>
            <p><strong>Years at Company:</strong> {emp_data['Years at Company']}</p>
            <p><strong>Years in Current Role:</strong> {emp_data['Years in Current Role']}</p>
            <p><strong>Monthly Income:</strong> {emp_data['Monthly Income']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔄 New Prediction", use_container_width=True, key="new_pred_button"):
            st.session_state.page = "input"
            st.rerun()
    with col2:
        if st.button("📊 View Details", use_container_width=True, key="view_details_button"):
            # This could be expanded to show more detailed analysis
            st.info("Detailed analysis feature coming soon!")
    with col3:
        if st.button("🏠 Go to Home", use_container_width=True, key="results_home_button"):
            st.session_state.page = "home"
            st.rerun()

# ============================================
# MAIN
# ============================================
def main():
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "input":
        input_page()
    elif st.session_state.page == "results":
        results_page()

main()