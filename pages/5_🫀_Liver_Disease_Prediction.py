"""
Liver Disease Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Liver Disease Prediction", page_icon="🫀", layout="wide")

auth = Authentication()
viz = Visualizer()
db = DatabaseManager()
predictor = get_predictor('liver')

if not auth.require_login():
    st.stop()

st.title("🫀 Liver Disease Risk Prediction")

st.markdown("""<div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
            padding: 1.5rem; border-radius: 10px; color: #2c3e50; margin-bottom: 2rem;'>
    <h3 style='color: #2c3e50; margin: 0;'>About Liver Disease Prediction</h3>
    <p style='margin: 0.5rem 0 0 0;'>Liver disease prediction using liver function test parameters.</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Liver Function Parameters")
    
    with st.form("liver_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=40)
            gender = st.selectbox("Gender", ["Male", "Female"])
            tb = st.number_input("Total Bilirubin (mg/dL)", min_value=0.0, max_value=100.0, value=1.0, step=0.1)
            direct_bil = st.number_input("Direct Bilirubin (mg/dL)", min_value=0.0, max_value=50.0, value=0.3, step=0.1)
            alkphos = st.number_input("Alkaline Phosphatase (IU/L)", min_value=0, max_value=2000, value=200)
        
        with col_b:
            sgpt = st.number_input("SGPT/ALT (IU/L)", min_value=0, max_value=2000, value=30)
            sgot = st.number_input("SGOT/AST (IU/L)", min_value=0, max_value=2000, value=30)
            tp = st.number_input("Total Proteins (g/dL)", min_value=0.0, max_value=15.0, value=7.0, step=0.1)
            alb = st.number_input("Albumin (g/dL)", min_value=0.0, max_value=10.0, value=4.0, step=0.1)
            ag_ratio = st.number_input("Albumin/Globulin Ratio", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
        
        submit_button = st.form_submit_button("🔍 Predict Liver Disease Risk", use_container_width=True)
        
        if submit_button:
            input_data = {
                'Age': age,
                'Gender': 1 if gender == "Male" else 0,
                'TotalBilirubin': tb,
                'DirectBilirubin': direct_bil,
                'AlkalinePhosphatase': alkphos,
                'AlamineAminotransferase': sgpt,
                'AspartateAminotransferase': sgot,
                'TotalProteins': tp,
                'Albumin': alb,
                'AlbuminGlobulinRatio': ag_ratio
            }
            
            if not predictor.is_model_available():
                st.error("⚠️ Model not available. Train: `python models/liver/train_liver.py`")
            else:
                with st.spinner("🔮 Analyzing..."):
                    result = predictor.predict(input_data)
                
                if result.get('error'):
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.session_state.liver_result = result
                    st.session_state.liver_input = input_data
                    db.save_prediction(auth.get_user_id(), 'liver', result['prediction'],
                                     result['probability'], result['risk_level'], input_data)
                    st.success("✅ Prediction completed!")
                    st.rerun()

with col2:
    st.info("""**Normal Ranges:**\n\n🧪 **Bilirubin:** 0.1-1.2 mg/dL\n📊 **ALT:** 7-56 IU/L\n📊 **AST:** 10-40 IU/L\n🩸 **Albumin:** 3.5-5.5 g/dL""")

if 'liver_result' in st.session_state:
    st.markdown("---\n## 🎯 Prediction Results")
    result = st.session_state.liver_result
    input_data = st.session_state.liver_input
    
    col_r1, col_r2, col_r3 = st.columns([2, 2, 2])
    
    with col_r1:
        fig = viz.create_risk_gauge(result['probability'], result['risk_level'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r2:
        st.markdown("### 📋 Assessment")
        pred_text = "**Positive**" if result['prediction'] == 1 else "**Negative**"
        pred_color = "#dc3545" if result['prediction'] == 1 else "#28a745"
        st.markdown(f"""<div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
            <h4>Prediction: <span style='color: {pred_color};'>{pred_text}</span></h4>
            <p><b>Risk:</b> {result['probability']*100:.1f}%</p>
            <p><b>Level:</b> <b>{result['risk_level']}</b></p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("📄 Download Report", use_container_width=True):
            report_gen = ReportGenerator()
            filename = f"Liver_Report_{auth.get_user_id()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            recommendations = predictor.get_recommendations(result['risk_level'], 'liver')
            pdf_path = report_gen.generate_report(filename, auth.get_user_data(), 'liver',
                result['prediction'], result['probability'], result['risk_level'], input_data, recommendations)
            with open(pdf_path, 'rb') as f:
                st.download_button("💾 Save", f, filename, "application/pdf", use_container_width=True)
    
    with col_r3:
        st.markdown("### 📊 Key Enzymes")
        st.text(f"Bilirubin: {input_data.get('TotalBilirubin')}")
        st.text(f"ALT: {input_data.get('AlamineAminotransferase')}")
        st.text(f"AST: {input_data.get('AspartateAminotransferase')}")
    
    st.markdown("---\n### 💊 Health Recommendations")
    for rec in predictor.get_recommendations(result['risk_level'], 'liver'):
        if "🚨" in rec:
            st.error(rec)
        elif "⚠️" in rec:
            st.warning(rec)
        else:
            st.success(rec)
