import streamlit as st
import pickle
import numpy as np
import base64
import plotly.graph_objects as go

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
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        [data-testid="stSidebar"] {{
            background: rgba(173, 216, 230, 0.85);
            color: black !important;
        }}
        .stNumberInput input, .stSelectbox select, .stTextInput input {{
            background-color: black !important;
            color: white !important;
            border-radius: 10px !important;
            border: 1px solid #000 !important;
        }}
        label, .stMarkdown, .stRadio label {{
            color: black !important;
            font-weight: 500 !important;
        }}
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
        h1 {{
            text-align: center;
            color: white !important;
            margin-top: -30px;
            margin-bottom: 10px;
        }}
        .stImage img {{
            margin-top: -20px;
            margin-bottom: 10px;
        }}
        .nav-button {{
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            margin: 5px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("22-01.jpg")  # Set your background image here

# ============================================
# 🔄 SESSION STATE INITIALIZATION
# ============================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

if 'prediction_proba' not in st.session_state:
    st.session_state.prediction_proba = None

if 'employee_data' not in st.session_state:
    st.session_state.employee_data = {}

# ============================================
# 🧠 LOAD MODELS
# ============================================
@st.cache_resource
def load_models():
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
    
    return {
        'rf': rf, 'sc': sc, 'enc_attrition': enc_attrition,
        'enc_businesstravel': enc_businesstravel, 'enc_department': enc_department,
        'enc_educationfield': enc_educationfield, 'enc_gender': enc_gender,
        'enc_jobrole': enc_jobrole, 'enc_maritalstatus': enc_maritalstatus,
        'enc_overtime': enc_overtime
    }

# ============================================
# 📄 HOME PAGE
# ============================================
def home_page():
    st.title("🏢 Employee Churn Prediction System")
    st.image("img.jpg", use_container_width=True)
    st.markdown("---")

    # First row of boxes
    col1, col2 = st.columns(2, gap="medium")
    box_style = "padding:20px; border-radius:12px; min-height:200px;"
    heading_style = "font-weight:bold; font-size:18px; margin-bottom:10px;"

    with col1:
        st.markdown(
            f"""
            <div style='background-color:#E0F7FA; {box_style}'>
                <div style='{heading_style}'>📊 What is Employee Attrition?</div>
                Gradual reduction in employee numbers due to resignations, retirements, or other departures. 
                High attrition affects productivity, morale, and performance.
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='background-color:#FFF3E0; {box_style}'>
                <div style='{heading_style}'>🎯 Purpose of This Tool</div>
                <ul style='padding-left:20px;'>
                    <li>Predict high-risk employees</li>
                    <li>Identify key attrition factors</li>
                    <li>Take proactive retention measures</li>
                    <li>Optimize HR strategies</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---")

    # Centered How It Works
    st.markdown(
        f"""
        <div style='max-width:600px; margin:auto; background-color:#E8F5E9; {box_style}'>
            <div style='{heading_style} text-align:center;'>🚀 How It Works</div>
            <ul style='padding-left:20px;'>
                <li>Analyzes 16 employee attributes</li>
                <li>Demographics, job info, work patterns, career progression, salary</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Centered Start Prediction button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("🔍 Start Prediction", key="start_button",
                  on_click=lambda: st.session_state.update({'page': 'input'}),
                  use_container_width=True)

# ============================================
# 📄 INPUT PAGE
# ============================================
def input_page():
    models = load_models()
    
    st.markdown("<h1>📝 Employee Information Entry</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: rgba(255, 255, 255, 0.85); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <p style='color: #2c3e50; font-size: 16px; text-align: center;'>
        Please enter the employee details below to predict attrition risk
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("👤 Personal Information")
        age = st.number_input("Age", 18, 65, 30)
        gender = st.selectbox("Gender", models['enc_gender'].classes_)
        marital_status = st.selectbox("Marital Status", models['enc_maritalstatus'].classes_)
        distance_from_home = st.number_input("Distance From Home (km)", 1, 50, 5)
        
        st.subheader("📊 Work Experience")
        total_working_years = st.number_input("Total Working Years", 0, 40, 5)
        years_at_company = st.number_input("Years At Company", 0, 40, 2)
        years_in_current_role = st.number_input("Years In Current Role", 0, 20, 1)
        job_satisfaction = st.selectbox("Job Satisfaction", [1,2,3,4])

    with col_right:
        st.subheader("💼 Job Information")
        department = st.selectbox("Department", models['enc_department'].classes_)
        job_role = st.selectbox("Job Role", models['enc_jobrole'].classes_)
        job_level = st.selectbox("Job Level", [1,2,3,4,5])
        business_travel = st.selectbox("Business Travel", models['enc_businesstravel'].classes_)
        overtime = st.selectbox("OverTime", models['enc_overtime'].classes_)
        education = st.selectbox("Education Level", [1,2,3,4,5])
        education_field = st.selectbox("Education Field", models['enc_educationfield'].classes_)
        monthly_income = st.number_input("Monthly Income ($)", 1000, 20000, 5000)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Home"):
            st.session_state.page = 'home'
            st.rerun()

    with col2:
        if st.button("🔮 Predict Attrition Risk"):
            try:
                # Encode categorical
                inputs = [
                    age,
                    models['enc_gender'].transform([gender])[0],
                    models['enc_maritalstatus'].transform([marital_status])[0],
                    models['enc_department'].transform([department])[0],
                    models['enc_businesstravel'].transform([business_travel])[0],
                    models['enc_jobrole'].transform([job_role])[0],
                    job_level, education,
                    models['enc_educationfield'].transform([education_field])[0],
                    models['enc_overtime'].transform([overtime])[0],
                    total_working_years, years_at_company, years_in_current_role,
                    monthly_income, distance_from_home, job_satisfaction
                ]

                X_scaled = models['sc'].transform(np.array(inputs).reshape(1,-1))
                pred = models['rf'].predict(X_scaled)[0]
                pred_proba = models['rf'].predict_proba(X_scaled)[0]
                result_label = models['enc_attrition'].inverse_transform([pred])[0]

                st.session_state.prediction_result = result_label
                st.session_state.prediction_proba = pred_proba
                st.session_state.employee_data = {
                    'Age': age, 'Gender': gender, 'Marital Status': marital_status,
                    'Department': department, 'Job Role': job_role, 'Job Level': job_level,
                    'Education': education, 'Education Field': education_field,
                    'Business Travel': business_travel, 'OverTime': overtime,
                    'Total Working Years': total_working_years, 'Years At Company': years_at_company,
                    'Years In Current Role': years_in_current_role, 'Monthly Income': monthly_income,
                    'Distance From Home': distance_from_home, 'Job Satisfaction': job_satisfaction
                }

                st.session_state.page = 'results'
                st.rerun()

            except Exception as e:
                st.error(f"⚠️ Error during prediction: {e}")

# ============================================
# 📄 RESULTS PAGE
# ============================================
def results_page():
    st.markdown("<h1>📊 Prediction Results</h1>", unsafe_allow_html=True)
    
    if st.session_state.prediction_result is None:
        st.warning("No prediction available. Please go back and enter employee data.")
        if st.button("⬅️ Back to Input"):
            st.session_state.page = 'input'
            st.rerun()
        return

    result = st.session_state.prediction_result
    proba = st.session_state.prediction_proba
    risk_percentage = proba[1] * 100

    # Determine risk text and gradient
    if risk_percentage <= 50:
        risk_text = "✅ LOW RISK OF ATTRITION"
        bg_color = "linear-gradient(135deg, #a8e6cf, #dcedc1)"  # soft green
        text_color = "#056608"
        message = "Employee is likely to stay with the organization."
    elif 50 < risk_percentage <= 65:
        risk_text = "⚠️ RISK OF ATTRITION"
        bg_color = "linear-gradient(135deg, #ffd3b6, #ffaaa5)"  # soft orange
        text_color = "#b35000"
        message = "Moderate risk. Consider retention measures."
    else:
        risk_text = "⚠️ HIGH RISK OF ATTRITION"
        bg_color = "linear-gradient(135deg, #ff6b6b, #ff5252)"  # soft red
        text_color = "#7a0000"
        message = "Immediate action recommended to retain this employee."

    # Display risk card with gradient
    st.markdown(f"""
    <div style="
        background: {bg_color};
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        font-family: 'Montserrat', sans-serif;
    ">
        <h2 style='color: {text_color}; font-size: 28px; margin-bottom: 10px;'>{risk_text}</h2>
        <p style='color: {text_color}; font-size: 18px; margin-top: 5px;'>{message}</p>
        <p style='color: {text_color}; font-size: 18px; margin-top: 5px;'>
            Attrition probability: {risk_percentage:.1f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Attrition Risk Score", 'font': {'size': 24, 'color': 'white'}},
            number={'suffix': "%", 'font': {'size': 40, 'color': 'white'}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "darkred" if risk_percentage > 50 else "darkgreen"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(52, 199, 89, 0.3)'},
                    {'range': [30, 70], 'color': 'rgba(255, 204, 0, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(255, 69, 58, 0.3)'}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 50}
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Montserrat"},
            height=400
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        fig_bar = go.Figure(data=[go.Bar(
            x=['Will Stay', 'Will Leave'],
            y=[proba[0]*100, proba[1]*100],
            marker_color=['rgba(52, 199, 89, 0.8)', 'rgba(255, 69, 58, 0.8)'],
            text=[f'{proba[0]*100:.1f}%', f'{proba[1]*100:.1f}%'],
            textposition='outside',
            textfont=dict(size=16, color='white')
        )])
        fig_bar.update_layout(
            title={'text': 'Prediction Probabilities', 'font': {'size': 24, 'color': 'white'}},
            xaxis={'title': 'Outcome', 'color': 'white'},
            yaxis={'title': 'Probability (%)', 'range': [0, 105], 'color': 'white'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.1)',
            font={'family': "Montserrat"},
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Employee Summary
    st.markdown("""
    <div style='background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h3 style='color: #2c3e50;'>📋 Employee Summary</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    data = st.session_state.employee_data

    with col1:
        st.markdown(f"""
        <div style='background-color: rgba(173, 216, 230, 0.7); padding: 15px; border-radius: 8px;'>
            <p><strong>Age:</strong> {data['Age']}</p>
            <p><strong>Gender:</strong> {data['Gender']}</p>
            <p><strong>Marital Status:</strong> {data['Marital Status']}</p>
            <p><strong>Distance from Home:</strong> {data['Distance From Home']} km</p>
            <p><strong>Education Level:</strong> {data['Education']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background-color: rgba(173, 216, 230, 0.7); padding: 15px; border-radius: 8px;'>
            <p><strong>Department:</strong> {data['Department']}</p>
            <p><strong>Job Role:</strong> {data['Job Role']}</p>
            <p><strong>Job Level:</strong> {data['Job Level']}</p>
            <p><strong>Business Travel:</strong> {data['Business Travel']}</p>
            <p><strong>OverTime:</strong> {data['OverTime']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background-color: rgba(173, 216, 230, 0.7); padding: 15px; border-radius: 8px;'>
            <p><strong>Total Working Years:</strong> {data['Total Working Years']}</p>
            <p><strong>Years at Company:</strong> {data['Years At Company']}</p>
            <p><strong>Years in Current Role:</strong> {data['Years In Current Role']}</p>
            <p><strong>Monthly Income:</strong> ${data['Monthly Income']}</p>
            <p><strong>Job Satisfaction:</strong> {data['Job Satisfaction']}/4</p>
        </div>
        """, unsafe_allow_html=True)

    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    with col3:
        if st.button("🔄 New Prediction", use_container_width=True):
            st.session_state.prediction_result = None
            st.session_state.prediction_proba = None
            st.session_state.employee_data = {}
            st.session_state.page = 'input'
            st.rerun()

# ============================================
# 🎯 MAIN APP LOGIC
# ============================================
def main():
    st.sidebar.title("🧭 Navigation")
    
    if st.sidebar.button("🏠 Home"):
        st.session_state.page = 'home'
        st.rerun()
    if st.sidebar.button("📝 Enter Data"):
        st.session_state.page = 'input'
        st.rerun()
    if st.sidebar.button("📊 View Results"):
        if st.session_state.prediction_result is not None:
            st.session_state.page = 'results'
            st.rerun()
        else:
            st.sidebar.warning("No prediction available yet!")
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Current Page:** {st.session_state.page.title()}")

    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'input':
        input_page()
    elif st.session_state.page == 'results':
        results_page()

if __name__ == "__main__":
    main()