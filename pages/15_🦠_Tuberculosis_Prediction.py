"""
Tuberculosis (TB) Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="TB Prediction", page_icon="🦠", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('tuberculosis')

if not auth.require_admin():
    st.stop()

st.title("🦠 Tuberculosis (TB) Prediction")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter TB Screening Information")
    
    with st.form("tb_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            cough_duration = st.number_input("Cough Duration (weeks)", min_value=0, max_value=52, value=0)
            night_sweats = st.selectbox("Night Sweats", ["No", "Yes"])
            weight_loss = st.selectbox("Unexplained Weight Loss", ["No", "Yes"])
            fever = st.selectbox("Prolonged Fever", ["No", "Yes"])
        
        with col_b:
            chest_pain = st.selectbox("Chest Pain", ["No", "Yes"])
            blood_sputum = st.selectbox("Blood in Sputum", ["No", "Yes"])
            hiv_status = st.selectbox("HIV Positive", ["No", "Yes", "Unknown"])
            previous_tb = st.selectbox("Previous TB History", ["No", "Yes"])
            bcg_vaccine = st.selectbox("BCG Vaccination", ["No", "Yes", "Unknown"])
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = {
                'Age': age,
                'Gender': 0 if gender == "Male" else 1,
                'CoughDuration': cough_duration,
                'NightSweats': 1 if night_sweats == "Yes" else 0,
                'WeightLoss': 1 if weight_loss == "Yes" else 0,
                'Fever': 1 if fever == "Yes" else 0,
                'ChestPain': 1 if chest_pain == "Yes" else 0,
                'BloodInSputum': 1 if blood_sputum == "Yes" else 0,
                'HIVStatus': 1 if hiv_status == "Yes" else 0,
                'PreviousTB': 1 if previous_tb == "Yes" else 0,
                'BCGVaccination': 1 if bcg_vaccine == "Yes" else 0
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
                    disease_type='tuberculosis',
                    input_parameters=input_data,
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ About TB")
    st.info("""
        **TB** is a bacterial infection mainly affecting the lungs.
        
        **Classic Symptoms:**
        - Persistent cough (>3 weeks)
        - Coughing blood
        - Night sweats
        - Weight loss
        - Fever
        - Chest pain
        
        **Risk Factors:**
        - HIV infection
        - Diabetes
        - Weak immune system
        - Close contact with TB patient
    """)
