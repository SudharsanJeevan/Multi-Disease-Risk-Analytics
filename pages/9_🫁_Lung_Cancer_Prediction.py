"""
Lung Cancer Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager
import config

st.set_page_config(page_title="Lung Cancer Prediction", page_icon="🫁", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('lung_cancer')

if not auth.require_login():
    st.stop()

st.title("🫁 Lung Cancer Risk Prediction")

st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='color: white; margin: 0;'>About Lung Cancer Prediction</h3>
        <p style='margin: 0.5rem 0 0 0;'>
            Lung cancer screening based on symptoms and lifestyle factors.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Your Information")
    
    with st.form("lung_cancer_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            gender = st.selectbox("Gender", ["Male", "Female"])
            age = st.number_input("Age", min_value=1, max_value=120, value=50)
            smoking = st.selectbox("Smoking", ["No", "Yes"])
            yellow_fingers = st.selectbox("Yellow Fingers", ["No", "Yes"])
            anxiety = st.selectbox("Anxiety", ["No", "Yes"])
            peer_pressure = st.selectbox("Peer Pressure", ["No", "Yes"])
            chronic_disease = st.selectbox("Chronic Disease", ["No", "Yes"])
            fatigue = st.selectbox("Fatigue", ["No", "Yes"])
        
        with col_b:
            allergy = st.selectbox("Allergy", ["No", "Yes"])
            wheezing = st.selectbox("Wheezing", ["No", "Yes"])
            alcohol = st.selectbox("Alcohol Consumption", ["No", "Yes"])
            coughing = st.selectbox("Coughing", ["No", "Yes"])
            shortness_breath = st.selectbox("Shortness of Breath", ["No", "Yes"])
            swallowing_diff = st.selectbox("Swallowing Difficulty", ["No", "Yes"])
            chest_pain = st.selectbox("Chest Pain", ["No", "Yes"])
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = pd.DataFrame([{
                'Gender': 0 if gender == "Male" else 1,
                'Age': age,
                'Smoking': 2 if smoking == "Yes" else 1,
                'YellowFingers': 2 if yellow_fingers == "Yes" else 1,
                'Anxiety': 2 if anxiety == "Yes" else 1,
                'PeerPressure': 2 if peer_pressure == "Yes" else 1,
                'ChronicDisease': 2 if chronic_disease == "Yes" else 1,
                'Fatigue': 2 if fatigue == "Yes" else 1,
                'Allergy': 2 if allergy == "Yes" else 1,
                'Wheezing': 2 if wheezing == "Yes" else 1,
                'Alcohol': 2 if alcohol == "Yes" else 1,
                'Coughing': 2 if coughing == "Yes" else 1,
                'ShortnessOfBreath': 2 if shortness_breath == "Yes" else 1,
                'SwallowingDifficulty': 2 if swallowing_diff == "Yes" else 1,
                'ChestPain': 2 if chest_pain == "Yes" else 1
            }])
            
            result = predictor.predict(input_data)
            
            if result['success']:
                st.success("✅ Prediction completed!")
                
                risk_prob = result['probability']
                risk_level = result['risk_level']
                
                # Display results
                st.markdown("### 📊 Prediction Results")
                
                risk_color = {'Low': '#28a745', 'Moderate': '#ffc107', 'High': '#dc3545'}[risk_level]
                
                st.markdown(f"""
                    <div style='background: {risk_color}; padding: 2rem; border-radius: 10px; color: white; text-align: center;'>
                        <h2 style='color: white; margin: 0;'>{risk_level} Risk</h2>
                        <p style='font-size: 2rem; margin: 0.5rem 0 0 0;'>{risk_prob*100:.1f}%</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Save prediction
                db.save_prediction(
                    user_id=auth.get_user_id(),
                    disease_type='lung_cancer',
                    input_data=input_data.to_dict('records')[0],
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
        - Smoking history
        - Age (50+)
        - Chronic respiratory disease
        - Family history
        - Occupational exposure
        
        **Symptoms to Watch:**
        - Persistent cough
        - Chest pain
        - Shortness of breath
        - Weight loss
        - Coughing blood
    """)
