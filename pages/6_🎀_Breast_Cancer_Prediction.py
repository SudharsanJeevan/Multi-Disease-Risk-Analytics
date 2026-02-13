"""
Breast Cancer Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Breast Cancer Prediction", page_icon="🎀", layout="wide")

auth = Authentication()
viz = Visualizer()
db = DatabaseManager()
predictor = get_predictor('breast_cancer')

if not auth.require_login():
    st.stop()

st.title("🎀 Breast Cancer Risk Prediction")

st.markdown("""<div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
            padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
    <h3 style='color: white; margin: 0;'>About Breast Cancer Prediction</h3>
    <p style='margin: 0.5rem 0 0 0;'>Breast cancer prediction using cell nucleus characteristics from the Wisconsin dataset.</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Cell Characteristics (Mean Values)")
    
    with st.form("breast_cancer_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            radius = st.number_input("Mean Radius", min_value=0.0, max_value=50.0, value=14.0, step=0.1,
                                    help="Mean of distances from center to points on the perimeter")
            texture = st.number_input("Mean Texture", min_value=0.0, max_value=50.0, value=19.0, step=0.1,
                                     help="Standard deviation of gray-scale values")
            perimeter = st.number_input("Mean Perimeter", min_value=0.0, max_value=250.0, value=92.0, step=0.1)
            area = st.number_input("Mean Area", min_value=0.0, max_value=2500.0, value=655.0, step=1.0)
            smoothness = st.number_input("Mean Smoothness", min_value=0.0, max_value=1.0, value=0.1, step=0.001,
                                        help="Local variation in radius lengths")
        
        with col_b:
            compactness = st.number_input("Mean Compactness", min_value=0.0, max_value=1.0, value=0.1, step=0.001,
                                         help="Perimeter^2 / area - 1.0")
            concavity = st.number_input("Mean Concavity", min_value=0.0, max_value=1.0, value=0.09, step=0.001,
                                       help="Severity of concave portions of the contour")
            concave_points = st.number_input("Mean Concave Points", min_value=0.0, max_value=1.0, value=0.05, step=0.001,
                                            help="Number of concave portions of the contour")
            symmetry = st.number_input("Mean Symmetry", min_value=0.0, max_value=1.0, value=0.18, step=0.001)
            fractal_dim = st.number_input("Mean Fractal Dimension", min_value=0.0, max_value=1.0, value=0.06, step=0.001,
                                         help="Coastline approximation - 1")
        
        submit_button = st.form_submit_button("🔍 Predict Breast Cancer Risk", use_container_width=True)
        
        if submit_button:
            input_data = {
                'MeanRadius': radius,
                'MeanTexture': texture,
                'MeanPerimeter': perimeter,
                'MeanArea': area,
                'MeanSmoothness': smoothness,
                'MeanCompactness': compactness,
                'MeanConcavity': concavity,
                'MeanConcavePoints': concave_points,
                'MeanSymmetry': symmetry,
                'MeanFractalDimension': fractal_dim
            }
            
            if not predictor.is_model_available():
                st.error("⚠️ Model not available. Train: `python models/breast_cancer/train_breast_cancer.py`")
            else:
                with st.spinner("🔮 Analyzing..."):
                    result = predictor.predict(input_data)
                
                if result.get('error'):
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.session_state.bc_result = result
                    st.session_state.bc_input = input_data
                    db.save_prediction(auth.get_user_id(), 'breast_cancer', result['prediction'],
                                     result['probability'], result['risk_level'], input_data)
                    st.success("✅ Prediction completed!")
                    st.rerun()

with col2:
    st.info("""**About Parameters:**\n\nThese values are typically obtained from:
    
🔬 **Fine Needle Aspirate (FNA)** of breast mass

📊 Cell nucleus characteristics analyzed digitally

💡 Values are normalized measurements""")
    
    st.warning("""**Important:**\n\n⚕️ This is a screening tool only\n\n🏥 Always consult oncologist\n\n🔍 Clinical testing required for diagnosis""")

if 'bc_result' in st.session_state:
    st.markdown("---\n## 🎯 Prediction Results")
    result = st.session_state.bc_result
    input_data = st.session_state.bc_input
    
    col_r1, col_r2, col_r3 = st.columns([2, 2, 2])
    
    with col_r1:
        fig = viz.create_risk_gauge(result['probability'], result['risk_level'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r2:
        st.markdown("### 📋 Assessment")
        # For breast cancer, we might want to show "Malignant" vs "Benign" instead of positive/negative
        pred_text = "**Malignant**" if result['prediction'] == 1 else "**Benign**"
        pred_color = "#dc3545" if result['prediction'] == 1 else "#28a745"
        st.markdown(f"""<div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
            <h4>Prediction: <span style='color: {pred_color};'>{pred_text}</span></h4>
            <p><b>Risk:</b> {result['probability']*100:.1f}%</p>
            <p><b>Level:</b> <b>{result['risk_level']}</b></p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("📄 Download Report", use_container_width=True):
            report_gen = ReportGenerator()
            filename = f"BreastCancer_Report_{auth.get_user_id()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            recommendations = predictor.get_recommendations(result['risk_level'], 'breast_cancer')
            pdf_path = report_gen.generate_report(filename, auth.get_user_data(), 'breast_cancer',
                result['prediction'], result['probability'], result['risk_level'], input_data, recommendations)
            with open(pdf_path, 'rb') as f:
                st.download_button("💾 Save", f, filename, "application/pdf", use_container_width=True)
    
    with col_r3:
        st.markdown("### 📊 Key Features")
        st.text(f"Radius: {input_data.get('MeanRadius'):.2f}")
        st.text(f"Texture: {input_data.get('MeanTexture'):.2f}")
        st.text(f"Area: {input_data.get('MeanArea'):.2f}")
        st.text(f"Concavity: {input_data.get('MeanConcavity'):.3f}")
    
    st.markdown("---\n### 💊 Health Recommendations")
    for rec in predictor.get_recommendations(result['risk_level'], 'breast_cancer'):
        if "🚨" in rec:
            st.error(rec)
        elif "⚠️" in rec:
            st.warning(rec)
        else:
            st.success(rec)
