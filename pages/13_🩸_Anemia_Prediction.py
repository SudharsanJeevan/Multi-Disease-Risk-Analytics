"""
Anemia Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Anemia Prediction", page_icon="🩸", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('anemia')

if not auth.require_login():
    st.stop()

st.title("🩸 Anemia Prediction")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Blood Test Results")
    
    with st.form("anemia_form"):
        gender = st.selectbox("Gender", ["Male", "Female"])
        hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=5.0, max_value=20.0, value=13.0, help="Normal: 13.5-17.5 (men), 12-15.5 (women)")
        mch = st.number_input("MCH (pg)", min_value=15.0, max_value=40.0, value=27.0, help="Mean Corpuscular Hemoglobin")
        mchc = st.number_input("MCHC (g/dL)", min_value=28.0, max_value=40.0, value=33.0, help="Mean Corpuscular Hemoglobin Concentration")
        mcv = st.number_input("MCV (fL)", min_value=60.0, max_value=110.0, value=85.0, help="Mean Corpuscular Volume")
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = {
                'Gender': 0 if gender == "Male" else 1,
                'Hemoglobin': hemoglobin,
                'MCH': mch,
                'MCHC': mchc,
                'MCV': mcv
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
                    disease_type='anemia',
                    input_parameters=input_data,
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ About Anemia")
    st.info("""
        **Anemia** occurs when you lack enough healthy red blood cells.
        
        **Types:**
        - Iron-deficiency anemia
        - Vitamin deficiency anemia
        - Aplastic anemia
        - Hemolytic anemia
        
        **Symptoms:**
        - Fatigue
        - Weakness
        - Pale skin
        - Irregular heartbeat
        - Shortness of breath
    """)
