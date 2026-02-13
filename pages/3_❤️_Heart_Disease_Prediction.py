"""
Heart Disease Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator
from src.database_manager import DatabaseManager

# Page config
st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="wide")

# Initialize
auth = Authentication()
viz = Visualizer()
db = DatabaseManager()
predictor = get_predictor('heart')

if not auth.require_login():
    st.stop()

st.title("❤️ Heart Disease Risk Prediction")

st.markdown("""<div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
            padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
    <h3 style='color: white; margin: 0;'>About Heart Disease Prediction</h3>
    <p style='margin: 0.5rem 0 0 0;'>Heart disease prediction using cardiac health parameters from the Cleveland Heart Disease dataset.</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Your Health Parameters")
    
    with st.form("heart_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
            sex = st.selectbox("Sex", ["Male", "Female"])
            cp = st.selectbox("Chest Pain Type", ["Type 0", "Type 1", "Type 2", "Type 3"])
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0, max_value=300, value=120)
            chol = st.number_input("Cholesterol (mg/dL)", min_value=0, max_value=600, value=200)
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No", "Yes"])
        
        with col_b:
            restecg = st.selectbox("Resting ECG", ["Normal", "ST-T Abnormality", "LV Hypertrophy"])
            thalach = st.number_input("Max Heart Rate", min_value=0, max_value=250, value=150)
            exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
            oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
            slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])
        
        submit_button = st.form_submit_button("🔍 Predict Heart Disease Risk", use_container_width=True)
        
        if submit_button:
            input_data = {
                'Age': age,
                'Sex': 1 if sex == "Male" else 0,
                'ChestPainType': int(cp.split()[-1]),
                'RestingBP': trestbps,
                'Cholesterol': chol,
                'FastingBS': 1 if fbs == "Yes" else 0,
                'RestingECG': ["Normal", "ST-T Abnormality", "LV Hypertrophy"].index(restecg),
                'MaxHR': thalach,
                'ExerciseAngina': 1 if exang == "Yes" else 0,
                'Oldpeak': oldpeak,
                'ST_Slope': ["Upsloping", "Flat", "Downsloping"].index(slope)
            }
            
            if not predictor.is_model_available():
                st.error("⚠️ Model not available. Train the model first: `python models/heart/train_heart.py`")
            else:
                with st.spinner("🔮 Analyzing..."):
                    result = predictor.predict(input_data)
                
                if result.get('error'):
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.session_state.heart_result = result
                    st.session_state.heart_input = input_data
                    
                    db.save_prediction(
                        user_id=auth.get_user_id(),
                        disease_type='heart',
                        prediction_result=result['prediction'],
                        risk_probability=result['probability'],
                        risk_level=result['risk_level'],
                        input_parameters=input_data
                    )
                    
                    st.success("✅ Prediction completed!")
                    st.rerun()

with col2:
    st.info("""**Normal Ranges:**\n\n💓 **Resting BP:** 120/80 mm Hg\n🩸 **Cholesterol:** < 200 mg/dL\n❤️ **Max HR:** 220 - Age""")

if 'heart_result' in st.session_state:
    st.markdown("---")
    st.markdown("## 🎯 Prediction Results")
    
    result = st.session_state.heart_result
    input_data = st.session_state.heart_input
    
    col_r1, col_r2, col_r3 = st.columns([2, 2, 2])
    
    with col_r1:
        fig = viz.create_risk_gauge(result['probability'], result['risk_level'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r2:
        st.markdown("### 📋 Assessment")
        prediction_text = "**Positive**" if result['prediction'] == 1 else "**Negative**"
        prediction_color = "#dc3545" if result['prediction'] == 1 else "#28a745"
        
        st.markdown(f"""<div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
            <h4>Prediction: <span style='color: {prediction_color};'>{prediction_text}</span></h4>
            <p><b>Risk:</b> {result['probability']*100:.1f}%</p>
            <p><b>Level:</b> <b>{result['risk_level']}</b></p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("📄 Download PDF Report", use_container_width=True):
            report_gen = ReportGenerator()
            filename = f"Heart_Report_{auth.get_user_id()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            recommendations = predictor.get_recommendations(result['risk_level'], 'heart')
            pdf_path = report_gen.generate_report(
                filename, auth.get_user_data(), 'heart',
                result['prediction'], result['probability'], result['risk_level'],
                input_data, recommendations
            )
            with open(pdf_path, 'rb') as f:
                st.download_button("💾 Save Report", f, filename, "application/pdf", use_container_width=True)
    
    with col_r3:
        st.markdown("### 📊 Your Input")
        for key, value in input_data.items():
            st.text(f"{key}: {value}")
    
    st.markdown("---")
    st.markdown("### 💊 Health Recommendations")
    recommendations = predictor.get_recommendations(result['risk_level'], 'heart')
    for rec in recommendations:
        if "🚨" in rec:
            st.error(rec)
        elif "⚠️" in rec:
            st.warning(rec)
        else:
            st.success(rec)

st.markdown("---")
st.info("💡 These predictions should not replace professional medical advice.")
