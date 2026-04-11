"""
Thyroid Disorder Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Thyroid Prediction", page_icon="🦋", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('thyroid')

if not auth.require_admin():
    st.stop()

st.title("🦋 Thyroid Disorder Prediction")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Thyroid Test Results")
    
    with st.form("thyroid_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age", min_value=1, max_value=120, value=40)
            sex = st.selectbox("Sex", ["Male", "Female"])
            on_thyroxine = st.selectbox("On Thyroxine", ["No", "Yes"])
            query_thyroxine = st.selectbox("Query on Thyroxine", ["No", "Yes"])
            thyroid_surgery = st.selectbox("Thyroid Surgery", ["No", "Yes"])
            tumor = st.selectbox("Tumor", ["No", "Yes"])
        
        with col_b:
            tsh = st.number_input("TSH Level", min_value=0.0, max_value=50.0, value=2.0, help="Thyroid Stimulating Hormone")
            t3 = st.number_input("T3 Level", min_value=0.0, max_value=10.0, value=2.0, help="Triiodothyronine")
            tt4 = st.number_input("TT4 Level", min_value=0.0, max_value=300.0, value=100.0, help="Total Thyroxine")
            t4u = st.number_input("T4U Level", min_value=0.0, max_value=3.0, value=1.0, help="Thyroxine Utilization")
            fti = st.number_input("FTI", min_value=0.0, max_value=300.0, value=100.0, help="Free Thyroxine Index")
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = {
                'Age': age,
                'Sex': 0 if sex == "Male" else 1,
                'OnThyroxine': 1 if on_thyroxine == "Yes" else 0,
                'QueryOnThyroxine': 1 if query_thyroxine == "Yes" else 0,
                'ThyroidSurgery': 1 if thyroid_surgery == "Yes" else 0,
                'Tumor': 1 if tumor == "Yes" else 0,
                'TSH': tsh,
                'T3': t3,
                'TT4': tt4,
                'T4U': t4u,
                'FTI': fti
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
                    disease_type='thyroid',
                    input_parameters=input_data,
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ About Thyroid")
    st.info("""
        **Thyroid Function:**
        The thyroid gland regulates metabolism through hormone production.
        
        **Conditions:**
        - Hypothyroidism (underactive)
        - Hyperthyroidism (overactive)
        - Thyroid nodules
        - Goiter
        
        **Key Tests:**
        - TSH (0.4-4.0 normal)
        - T3, T4 levels
        - Antibody tests
    """)
