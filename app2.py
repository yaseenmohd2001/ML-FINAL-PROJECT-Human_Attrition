import streamlit as st
import pickle
import numpy as np
import base64

# ============================================
# 🎨 PAGE CONFIG & BACKGROUND
# ============================================
st.set_page_config(page_title="Employee Churn Prediction", layout="wide")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Montserrat', sans-serif !important;
        }}

        /* 🌈 Background image */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}

        /* 🧭 Sidebar styling (transparent cyan background) */
        [data-testid="stSidebar"] {{
            background: rgba(173, 216, 230, 0.85);
            color: black !important;
        }}

        /* 🧾 Input elements */
        .stNumberInput input, .stSelectbox select, .stTextInput input {{
            background-color: black !important;
            color: white !important;
            border-radius: 10px !important;
            border: 1px solid #000 !important;
        }}

        /* Outside label text */
        label, .stMarkdown, .stRadio label {{
            color: black !important;
            font-weight: 500 !important;
        }}

        /* 🟩 Predict Button */
        div.stButton > button:first-child {{
            background-color: black;
            color: white;
            border-radius: 12px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            margin-top: -10px;
            border: none;
        }}
        div.stButton > button:first-child:hover {{
            background-color: white;
            color: black;
            border: 2px solid black;
        }}

        /* Heading & layout adjustments */
        h1 {{
            text-align: center;
            color: white !important;
            margin-top: -30px;
            margin-bottom: 10px;
        }}

        /* Adjust image placement (closer to heading) */
        .stImage img {{
            margin-top: -20px;
            margin-bottom: 10px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Apply background
add_bg_from_local("22-01.jpg")  # Your cyan background image

# ============================================
# 🧠 MODEL, SCALER, ENCODERS
# ============================================
rf = pickle.load(open("rf.sav", "rb"))
sc = pickle.load(open("sc.sav", "rb"))

enc_attrition = pickle.load(open("enc_attrition.sav", "rb"))
enc_businesstravel = pickle.load(open("enc_businesstravel.sav", "rb"))
enc_department = pickle.load(open("enc_department.sav", "rb"))
enc_educationfield = pickle.load(open("enc_educationfield.sav", "rb"))
enc_gender = pickle.load(open("enc_gender.sav", "rb"))
enc_jobrole = pickle.load(open("enc_jobrole.sav", "rb"))
enc_maritalstatus = pickle.load(open("enc_maritalstatus.sav", "rb"))
enc_overtime = pickle.load(open("enc_overtime.sav", "rb"))

# ============================================
# 🏷️ TITLE & IMAGE
# ============================================
st.markdown("<h1>Employee Churn Prediction</h1>", unsafe_allow_html=True)
st.image("Types-of-Employee-Attrition.jpg", use_container_width=True)

# ============================================
# 🧾 SIDEBAR INPUTS
# ============================================
st.sidebar.header("Employee Details")

age = st.sidebar.number_input("Age", 18, 65, 30)
gender = st.sidebar.selectbox("Gender", enc_gender.classes_)
marital_status = st.sidebar.selectbox("Marital Status", enc_maritalstatus.classes_)
department = st.sidebar.selectbox("Department", enc_department.classes_)
business_travel = st.sidebar.selectbox("Business Travel", enc_businesstravel.classes_)
job_role = st.sidebar.selectbox("Job Role", enc_jobrole.classes_)
job_level = st.sidebar.selectbox("Job Level", [1, 2, 3, 4, 5])
education = st.sidebar.selectbox("Education Level", [1, 2, 3, 4, 5])
education_field = st.sidebar.selectbox("Education Field", enc_educationfield.classes_)
overtime = st.sidebar.selectbox("OverTime", enc_overtime.classes_)
total_working_years = st.sidebar.number_input("Total Working Years", 0, 40, 5)
years_at_company = st.sidebar.number_input("Years At Company", 0, 40, 2)
years_in_current_role = st.sidebar.number_input("Years In Current Role", 0, 20, 1)
monthly_income = st.sidebar.number_input("Monthly Income", 1000, 20000, 5000)
distance_from_home = st.sidebar.number_input("Distance From Home", 1, 50, 5)
job_satisfaction = st.sidebar.selectbox("Job Satisfaction (1=Low, 4=High)", [1, 2, 3, 4])

# ============================================
# 🔮 PREDICTION BUTTON
# ============================================
if st.button("Predict Attrition Risk"):
    try:
        business_travel_encoded = enc_businesstravel.transform([business_travel])[0]
        department_encoded = enc_department.transform([department])[0]
        education_field_encoded = enc_educationfield.transform([education_field])[0]
        gender_encoded = enc_gender.transform([gender])[0]
        job_role_encoded = enc_jobrole.transform([job_role])[0]
        marital_status_encoded = enc_maritalstatus.transform([marital_status])[0]
        overtime_encoded = enc_overtime.transform([overtime])[0]

        inputs = [
            age, gender_encoded, marital_status_encoded, department_encoded,
            business_travel_encoded, job_role_encoded, job_level, education,
            education_field_encoded, overtime_encoded, total_working_years,
            years_at_company, years_in_current_role, monthly_income,
            distance_from_home, job_satisfaction
        ]

        X_scaled = sc.transform(np.array(inputs).reshape(1, -1))
        pred = rf.predict(X_scaled)[0]
        result_label = enc_attrition.inverse_transform([pred])[0]

        if result_label == "Yes":
            st.warning("⚠️ High Risk of Attrition! Immediate action recommended.")
        else:
            st.success("✅ Low Risk of Attrition. Employee likely to stay.")

    except Exception as e:
        st.error(f"⚠️ Error during prediction: {e}")
