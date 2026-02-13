"""
Kidney Disease Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Kidney Disease Prediction", page_icon="🫘", layout="wide")

auth = Authentication()
viz = Visualizer()
db = DatabaseManager()
predictor = get_predictor('kidney')

if not auth.require_login():
    st.stop()

st.title("🫘 Kidney Disease Risk Prediction")

st.markdown("""<div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
            padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
    <h3 style='color: white; margin: 0;'>About Kidney Disease Prediction</h3>
    <p style='margin: 0.5rem 0 0 0;'>Chronic kidney disease prediction using comprehensive lab parameters.</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Lab Parameters")
    
    with st.form("kidney_form"):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            age = st.number_input("Age", min_value=1, max_value=120, value=50)
            bp = st.number_input("Blood Pressure", min_value=0, max_value=200, value=80)
            sg = st.number_input("Specific Gravity", min_value=1.0, max_value=1.05, value=1.02, step=0.001)
            al = st.number_input("Albumin", min_value=0, max_value=5, value=0)
            su = st.number_input("Sugar", min_value=0, max_value=5, value=0)
            rbc = st.selectbox("Red Blood Cells", ["Normal", "Abnormal"])
        
        with col_b:
            pc = st.selectbox("Pus Cell", ["Normal", "Abnormal"])
            pcc = st.selectbox("Pus Cell Clumps", ["Not Present", "Present"])
            ba = st.selectbox("Bacteria", ["Not Present", "Present"])
            bgr = st.number_input("Blood Glucose (mg/dL)", min_value=0, max_value=500, value=120)
            bu = st.number_input("Blood Urea (mg/dL)", min_value=0, max_value=200, value=30)
            sc = st.number_input("Serum Creatinine (mg/dL)", min_value=0.0, max_value=20.0, value=1.0, step=0.1)
        
        with col_c:
            sod = st.number_input("Sodium (mEq/L)", min_value=0, max_value=200, value=140)
            pot = st.number_input("Potassium (mEq/L)", min_value=0.0, max_value=10.0, value=4.0, step=0.1)
            hemo = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=20.0, value=14.0, step=0.1)
            pcv = st.number_input("Packed Cell Volume", min_value=0, max_value=60, value=40)
            wc = st.number_input("WBC Count", min_value=0, max_value=20000, value=8000)
            rc = st.number_input("RBC Count", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
        
        submit_button = st.form_submit_button("🔍 Predict Kidney Disease Risk", use_container_width=True)
        
        if submit_button:
            input_data = {
                'Age': age, 'BloodPressure': bp, 'SpecificGravity': sg,
                'Albumin': al, 'Sugar': su, 'RedBloodCells': 1 if rbc == "Normal" else 0,
                'PusCell': 1 if pc == "Normal" else 0,
                'PusCellClumps': 0 if pcc == "Not Present" else 1,
                'Bacteria': 0 if ba == "Not Present" else 1,
                'BloodGlucoseRandom': bgr, 'BloodUrea': bu, 'SerumCreatinine': sc,
                'Sodium': sod, 'Potassium': pot, 'Hemoglobin': hemo,
                'PackedCellVolume': pcv, 'WhiteBloodCellCount': wc, 'RedBloodCellCount': rc
            }
            
            if not predictor.is_model_available():
                st.error("⚠️ Model not available. Train: `python models/kidney/train_kidney.py`")
            else:
                with st.spinner("🔮 Analyzing..."):
                    result = predictor.predict(input_data)
                
                if result.get('error'):
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.session_state.kidney_result = result
                    st.session_state.kidney_input = input_data
                    db.save_prediction(auth.get_user_id(), 'kidney', result['prediction'],
                                     result['probability'], result['risk_level'], input_data)
                    st.success("✅ Prediction completed!")
                    st.rerun()

with col2:
    st.info("""**Normal Ranges:**\n\n🩸 **Creatinine:** 0.7-1.3 mg/dL\n🧪 **Blood Urea:** 7-20 mg/dL\n💧 **Hemoglobin:** 12-16 g/dL""")

if 'kidney_result' in st.session_state:
    st.markdown("---\n## 🎯 Prediction Results")
    result = st.session_state.kidney_result
    input_data = st.session_state.kidney_input
    
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
            filename = f"Kidney_Report_{auth.get_user_id()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            recommendations = predictor.get_recommendations(result['risk_level'], 'kidney')
            pdf_path = report_gen.generate_report(filename, auth.get_user_data(), 'kidney',
                result['prediction'], result['probability'], result['risk_level'], input_data, recommendations)
            with open(pdf_path, 'rb') as f:
                st.download_button("💾 Save", f, filename, "application/pdf", use_container_width=True)
    
    with col_r3:
        st.markdown("### 📊 Key Values")
        st.text(f"Creatinine: {input_data.get('SerumCreatinine')}")
        st.text(f"Blood Urea: {input_data.get('BloodUrea')}")
        st.text(f"Hemoglobin: {input_data.get('Hemoglobin')}")
    
    st.markdown("---\n### 💊 Health Recommendations")
    for rec in predictor.get_recommendations(result['risk_level'], 'kidney'):
        if "🚨" in rec:
            st.error(rec)
        elif "⚠️" in rec:
            st.warning(rec)
        else:
            st.success(rec)
