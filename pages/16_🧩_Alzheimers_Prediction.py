"""
Alzheimer's Risk Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Alzheimer's Prediction", page_icon="🧩", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('alzheimers')

if not auth.require_login():
    st.stop()

st.title("🧩 Alzheimer's Risk Prediction")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Cognitive Assessment")
    
    with st.form("alzheimers_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age", min_value=40, max_value=120, value=70)
            gender = st.selectbox("Gender", ["Male", "Female"])
            education = st.number_input("Years of Education", min_value=0, max_value=25, value=12)
            mmse = st.number_input("MMSE Score (0-30)", min_value=0, max_value=30, value=25, help="Mini Mental State Examination")
            functional = st.number_input("Functional Assessment (0-30)", min_value=0, max_value=30, value=20)
        
        with col_b:
            memory = st.selectbox("Memory Complaints", ["No", "Yes"])
            behavior = st.selectbox("Behavioral Problems", ["No", "Yes"])
            adl = st.number_input("ADL Score (0-28)", min_value=0, max_value=28, value=20, help="Activities of Daily Living")
            iadl = st.number_input("IADL Score (0-8)", min_value=0, max_value=8, value=6, help="Instrumental ADL")
            cdr = st.number_input("CDR Score (0-3)", min_value=0.0, max_value=3.0, value=0.0, step=0.5, help="Clinical Dementia Rating")
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = pd.DataFrame([{
                'Age': age,
                'Gender': 0 if gender == "Male" else 1,
                'EducationLevel': education,
                'MMSEScore': mmse,
                'FunctionalAssessment': functional,
                'MemoryComplaints': 1 if memory == "Yes" else 0,
                'BehavioralProblems': 1 if behavior == "Yes" else 0,
                'ADL': adl,
                'IADL': iadl,
                'CDR': cdr
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
                    disease_type='alzheimers',
                    input_data=input_data.to_dict('records')[0],
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ About Alzheimer's")
    st.info("""
        **Alzheimer's** is a progressive brain disorder affecting memory and thinking.
        
        **Early Signs:**
        - Memory loss
        - Difficulty planning
        - Confusion with time/place
        - Trouble with words
        - Misplacing things
        - Poor judgment
        - Personality changes
        
        **Risk Factors:**
        - Age (65+)
        - Family history
        - Education level
        - Head injuries
    """)
