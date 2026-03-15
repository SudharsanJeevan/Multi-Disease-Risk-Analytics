"""
COVID-19 Severity Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="COVID-19 Prediction", page_icon="🦠", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('covid19')

if not auth.require_login():
    st.stop()

st.title("🦠 COVID-19 Severity Prediction")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 COVID-19 Risk Assessment")
    
    with st.form("covid_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age", min_value=1, max_value=120, value=40)
            gender = st.selectbox("Gender", ["Male", "Female"])
            covid_contact = st.selectbox("Contact with COVID Patient", ["No", "Yes"])
            fever = st.selectbox("Fever", ["No", "Yes"])
            cough = st.selectbox("Cough", ["No", "Yes"])
            sore_throat = st.selectbox("Sore Throat", ["No", "Yes"])
            shortness_breath = st.selectbox("Shortness of Breath", ["No", "Yes"])
        
        with col_b:
            headache = st.selectbox("Headache", ["No", "Yes"])
            diabetes = st.selectbox("Diabetes", ["No", "Yes"])
            hypertension = st.selectbox("Hypertension", ["No", "Yes"])
            cardiovascular = st.selectbox("Cardiovascular Disease", ["No", "Yes"])
            obesity = st.selectbox("Obesity", ["No", "Yes"])
            chronic_pulmonary = st.selectbox("Chronic Pulmonary Disease", ["No", "Yes"])
            pneumonia = st.selectbox("Pneumonia", ["No", "Yes"])
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = {
                'Age': age,
                'Gender': 0 if gender == "Male" else 1,
                'COVIDContact': 1 if covid_contact == "Yes" else 0,
                'Fever': 1 if fever == "Yes" else 0,
                'Cough': 1 if cough == "Yes" else 0,
                'SoreThroat': 1 if sore_throat == "Yes" else 0,
                'ShortnessOfBreath': 1 if shortness_breath == "Yes" else 0,
                'HeadAche': 1 if headache == "Yes" else 0,
                'Diabetes': 1 if diabetes == "Yes" else 0,
                'Hypertension': 1 if hypertension == "Yes" else 0,
                'CardiovascularDisease': 1 if cardiovascular == "Yes" else 0,
                'Obesity': 1 if obesity == "Yes" else 0,
                'ChronicPulmonary': 1 if chronic_pulmonary == "Yes" else 0,
                'Pneumonia': 1 if pneumonia == "Yes" else 0
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
                    disease_type='covid19',
                    input_parameters=input_data,
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ About COVID-19")
    st.info("""
        **COVID-19** is a respiratory illness caused by SARS-CoV-2.
        
        **Common Symptoms:**
        - Fever/chills
        - Cough
        - Shortness of breath
        - Fatigue
        - Body aches
        - Loss of taste/smell
        
        **High Risk Groups:**
        - Elderly (65+)
        - Chronic conditions
        - Immunocompromised
        - Obesity
    """)
