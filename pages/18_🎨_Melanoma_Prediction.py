"""
Melanoma (Skin Cancer) Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Melanoma Prediction", page_icon="🎨", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('melanoma')

if not auth.require_login():
    st.stop()

st.title("🎨 Melanoma (Skin Cancer) Prediction")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Skin Assessment Information")
    
    with st.form("melanoma_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age", min_value=1, max_value=120, value=45)
            gender = st.selectbox("Gender", ["Male", "Female"])
            family_history = st.selectbox("Family History of Melanoma", ["No", "Yes"])
            sun_exposure = st.slider("Sun Exposure Level", min_value=1, max_value=5, value=3, help="1=Low, 5=High")
            moles_count = st.number_input("Number of Moles", min_value=0, max_value=200, value=20)
        
        with col_b:
            mole_changes = st.selectbox("Recent Mole Changes", ["No", "Yes"])
            irregular_borders = st.selectbox("Irregular Mole Borders", ["No", "Yes"])
            color_variation = st.selectbox("Color Variation in Moles", ["No", "Yes"])
            diameter = st.number_input("Largest Mole Diameter (mm)", min_value=1.0, max_value=30.0, value=5.0)
            evolution = st.selectbox("Mole Evolution/Change", ["No", "Yes"])
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = {
                'Age': age,
                'Gender': 0 if gender == "Male" else 1,
                'FamilyHistory': 1 if family_history == "Yes" else 0,
                'SunExposure': sun_exposure,
                'MolesCount': moles_count,
                'MoleChanges': 1 if mole_changes == "Yes" else 0,
                'IrregularBorders': 1 if irregular_borders == "Yes" else 0,
                'ColorVariation': 1 if color_variation == "Yes" else 0,
                'Diameter': diameter,
                'Evolution': 1 if evolution == "Yes" else 0
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
                    disease_type='melanoma',
                    input_parameters=input_data,
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ ABCDE Rule")
    st.info("""
        **Warning Signs (ABCDE):**
        
        **A**symmetry - One half unlike the other
        
        **B**order - Irregular, scalloped edges
        
        **C**olor - Varied colors (brown, black, tan, red, white, blue)
        
        **D**iameter - Larger than 6mm (pencil eraser)
        
        **E**volving - Changes in size, shape, or color
        
        **See a doctor if:**
        - New unusual spot
        - Existing mole changes
        - Bleeding/itching mole
    """)
