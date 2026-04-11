"""
Stroke Risk Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Stroke Prediction", page_icon="🧠", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('stroke')

if not auth.require_admin():
    st.stop()

st.title("🧠 Stroke Risk Prediction")

st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='color: white; margin: 0;'>About Stroke Prediction</h3>
        <p style='margin: 0.5rem 0 0 0;'>
            Stroke occurs when blood flow to the brain is interrupted. Early prediction can save lives.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Your Health Information")
    
    with st.form("stroke_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            gender = st.selectbox("Gender", ["Male", "Female"])
            age = st.number_input("Age", min_value=1, max_value=120, value=50)
            hypertension = st.selectbox("Hypertension", ["No", "Yes"])
            heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
            ever_married = st.selectbox("Ever Married", ["No", "Yes"])
        
        with col_b:
            work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "Children", "Never_worked"])
            residence = st.selectbox("Residence Type", ["Urban", "Rural"])
            avg_glucose = st.number_input("Average Glucose Level (mg/dL)", min_value=0.0, max_value=300.0, value=100.0)
            bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)
            smoking = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown"])
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            work_map = {"Private": 0, "Self-employed": 1, "Govt_job": 2, "Children": 3, "Never_worked": 4}
            smoking_map = {"never smoked": 0, "formerly smoked": 1, "smokes": 2, "Unknown": 3}
            
            input_data = {
                'Gender': 0 if gender == "Male" else 1,
                'Age': age,
                'Hypertension': 1 if hypertension == "Yes" else 0,
                'HeartDisease': 1 if heart_disease == "Yes" else 0,
                'EverMarried': 1 if ever_married == "Yes" else 0,
                'WorkType': work_map.get(work_type, 0),
                'ResidenceType': 0 if residence == "Urban" else 1,
                'AvgGlucoseLevel': avg_glucose,
                'BMI': bmi,
                'SmokingStatus': smoking_map.get(smoking, 0)
            }
            
            result = predictor.predict(input_data)
            
            if not result.get('error'):
                st.success("✅ Prediction completed!")
                risk_prob = result['probability']
                risk_level = result['risk_level']
                
                risk_color = {'Low': '#28a745', 'Moderate': '#ffc107', 'High': '#dc3545'}[risk_level]
                
                st.markdown(f"""
                    <div style='background: {risk_color}; padding: 2rem; border-radius: 10px; color: white; text-align: center;'>
                        <h2 style='color: white; margin: 0;'>{risk_level} Risk</h2>
                        <p style='font-size: 2rem; margin: 0.5rem 0 0 0;'>{risk_prob*100:.1f}%</p>
                    </div>
                """, unsafe_allow_html=True)
                
                db.save_prediction(
                    user_id=auth.get_user_id(),
                    disease_type='stroke',
                    input_parameters=input_data,
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ Risk Factors")
    st.info("""
        **Major Risk Factors:**
        - High blood pressure
        - Heart disease
        - Diabetes
        - High cholesterol
        - Smoking
        - Age (55+)
        - Family history
        
        **Warning Signs:**
        - Sudden numbness
        - Confusion/trouble speaking
        - Vision problems
        - Difficulty walking
        - Severe headache
    """)
