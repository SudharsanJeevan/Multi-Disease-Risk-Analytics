"""
Pneumonia Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Pneumonia Prediction", page_icon="😷", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('pneumonia')

if not auth.require_login():
    st.stop()

st.title("😷 Pneumonia Prediction")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Symptoms & Information")
    
    with st.form("pneumonia_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age", min_value=1, max_value=120, value=40)
            gender = st.selectbox("Gender", ["Male", "Female"])
            fever = st.selectbox("Fever", ["No", "Yes"])
            cough = st.selectbox("Cough", ["No", "Yes"])
            chest_pain = st.selectbox("Chest Pain", ["No", "Yes"])
        
        with col_b:
            difficulty_breathing = st.selectbox("Difficulty Breathing", ["No", "Yes"])
            fatigue = st.selectbox("Fatigue", ["No", "Yes"])
            sputum = st.selectbox("Sputum Production", ["No", "Yes"])
            duration = st.number_input("Duration of Symptoms (days)", min_value=1, max_value=90, value=5)
            smoking = st.selectbox("Smoking History", ["No", "Yes"])
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = pd.DataFrame([{
                'Age': age,
                'Gender': 0 if gender == "Male" else 1,
                'Fever': 1 if fever == "Yes" else 0,
                'Cough': 1 if cough == "Yes" else 0,
                'ChestPain': 1 if chest_pain == "Yes" else 0,
                'DifficultyBreathing': 1 if difficulty_breathing == "Yes" else 0,
                'Fatigue': 1 if fatigue == "Yes" else 0,
                'SputumProduction': 1 if sputum == "Yes" else 0,
                'DurationOfSymptoms': duration,
                'SmokingHistory': 1 if smoking == "Yes" else 0
            }])
            
            result = predictor.predict(input_data)
            
            if result['success']:
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
                    disease_type='pneumonia',
                    input_data=input_data.to_dict('records')[0],
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ About Pneumonia")
    st.info("""
        **Pneumonia** is a lung infection that inflames air sacs.
        
        **Common Symptoms:**
        - Cough with phlegm
        - Fever, sweating
        - Shortness of breath
        - Chest pain
        - Fatigue
        
        **Seek immediate care if:**
        - High fever
        - Severe breathing difficulty
        - Confusion
        - Bluish lips/nails
    """)
