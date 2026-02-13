"""
Diabetes Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator
from src.database_manager import DatabaseManager
import config

# Page config
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="💉",
    layout="wide"
)

# Initialize
auth = Authentication()
viz = Visualizer()
db = DatabaseManager()
predictor = get_predictor('diabetes')

# Check authentication
if not auth.require_login():
    st.stop()

# Main content
st.title("💉 Diabetes Risk Prediction")

st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='color: white; margin: 0;'>About Diabetes Prediction</h3>
        <p style='margin: 0.5rem 0 0 0;'>
            Diabetes is a chronic condition that affects how your body processes blood sugar (glucose).
            This test uses the PIMA Indian Diabetes dataset to predict your risk based on key health metrics.
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Your Health Parameters")
    
    with st.form("diabetes_form"):
        # Create input fields
        col_a, col_b = st.columns(2)
        
        with col_a:
            pregnancies = st.number_input(
                "Number of Pregnancies",
                min_value=0,
                max_value=20,
                value=0,
                help="Number of times pregnant (0 for males)"
            )
            
            glucose = st.number_input(
                "Glucose Level (mg/dL)",
                min_value=0,
                max_value=300,
                value=120,
                help="Plasma glucose concentration (70-100 is normal fasting)"
            )
            
            blood_pressure = st.number_input(
                "Blood Pressure (mm Hg)",
                min_value=0,
                max_value=200,
                value=80,
                help="Diastolic blood pressure (60-80 is normal)"
            )
            
            skin_thickness = st.number_input(
                "Skin Thickness (mm)",
                min_value=0,
                max_value=100,
                value=20,
                help="Triceps skin fold thickness"
            )
        
        with col_b:
            insulin = st.number_input(
                "Insulin Level (μU/mL)",
                min_value=0,
                max_value=900,
                value=80,
                help="2-Hour serum insulin"
            )
            
            bmi = st.number_input(
                "BMI (Body Mass Index)",
                min_value=0.0,
                max_value=70.0,
                value=25.0,
                step=0.1,
                help="Weight in kg / (Height in m)² (18.5-24.9 is normal)"
            )
            
            dpf = st.number_input(
                "Diabetes Pedigree Function",
                min_value=0.0,
                max_value=3.0,
                value=0.5,
                step=0.01,
                help="Diabetes heredity score (higher = more family history)"
            )
            
            age = st.number_input(
                "Age (years)",
                min_value=1,
                max_value=120,
                value=30,
                help="Your age in years"
            )
        
        st.markdown("---")
        
        col_submit, col_clear = st.columns([3, 1])
        
        with col_submit:
            submit_button = st.form_submit_button(
                "🔍 Predict Diabetes Risk",
                use_container_width=True
            )
        
        with col_clear:
            clear_button = st.form_submit_button(
                "🔄 Clear",
                use_container_width=True
            )
        
        if submit_button:
            # Prepare input data
            input_data = {
                'Pregnancies': pregnancies,
                'Glucose': glucose,
                'BloodPressure': blood_pressure,
                'SkinThickness': skin_thickness,
                'Insulin': insulin,
                'BMI': bmi,
                'DiabetesPedigreeFunction': dpf,
                'Age': age
            }
            
            # Get prediction
            if not predictor.is_model_available():
                st.error("""
                    ⚠️ Diabetes prediction model is not available yet. 
                    Please train the model first by running:
                    ```
                    python models/diabetes/train_diabetes.py
                    ```
                """)
            else:
                with st.spinner("🔮 Analyzing your data..."):
                    result = predictor.predict(input_data)
                
                if result.get('error'):
                    st.error(f"❌ Error: {result['error']}")
                else:
                    # Store prediction
                    st.session_state.diabetes_result = result
                    st.session_state.diabetes_input = input_data
                    
                    # Save to database
                    db.save_prediction(
                        user_id=auth.get_user_id(),
                        disease_type='diabetes',
                        prediction_result=result['prediction'],
                        risk_probability=result['probability'],
                        risk_level=result['risk_level'],
                        input_parameters=input_data
                    )
                    
                    st.success("✅ Prediction completed!")
                    st.rerun()

with col2:
    st.markdown("### 💡 Tips")
    st.info("""
        **Normal Ranges:**
        
        🩸 **Glucose:** 70-100 mg/dL (fasting)
        
        💓 **Blood Pressure:** 60-80 mm Hg
        
        ⚖️ **BMI:** 18.5-24.9
        
        📊 **Higher values** in these parameters may indicate increased risk.
    """)
    
    st.markdown("### 📊 Risk Factors")
    st.warning("""
        Common diabetes risk factors:
        - High blood glucose
        - Obesity (high BMI)
        - Family history
        - Age over 45
        - Physical inactivity
        - High blood pressure
    """)

# Display results if available
if 'diabetes_result' in st.session_state:
    st.markdown("---")
    st.markdown("## 🎯 Prediction Results")
    
    result = st.session_state.diabetes_result
    input_data = st.session_state.diabetes_input
    
    # Create three columns for results
    res_col1, res_col2, res_col3 = st.columns([2, 2, 2])
    
    with res_col1:
        # Risk gauge
        fig = viz.create_risk_gauge(result['probability'], result['risk_level'])
        st.plotly_chart(fig, use_container_width=True)
    
    with res_col2:
        # Prediction details
        st.markdown("### 📋 Assessment")
        
        prediction_text = "**Positive**" if result['prediction'] == 1 else "**Negative**"
        prediction_color = "#dc3545" if result['prediction'] == 1 else "#28a745"
        
        st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
                <h4>Prediction: <span style='color: {prediction_color};'>{prediction_text}</span></h4>
                <p><b>Risk Probability:</b> {result['probability']*100:.1f}%</p>
                <p><b>Risk Level:</b> <span style='color: {predictor.get_risk_color(result["risk_level"])};'>
                    <b>{result['risk_level']}</b></span></p>
            </div>
        """, unsafe_allow_html=True)
        
        # Download report button
        if st.button("📄 Download PDF Report", use_container_width=True):
            report_gen = ReportGenerator()
            user_data = auth.get_user_data()
            
            filename = f"Diabetes_Report_{auth.get_user_id()}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            recommendations = predictor.get_recommendations(
                result['risk_level'],
                'diabetes'
            )
            
            pdf_path = report_gen.generate_report(
                filename=filename,
                user_data=user_data,
                disease_type='diabetes',
                prediction_result=result['prediction'],
                risk_probability=result['probability'],
                risk_level=result['risk_level'],
                input_parameters=input_data,
                recommendations=recommendations
            )
            
            with open(pdf_path, 'rb') as f:
                st.download_button(
                    label="💾 Save Report",
                    data=f,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
    
    with res_col3:
        # Input summary
        st.markdown("### 📊 Your Input")
        
        for key, value in input_data.items():
            st.text(f"{key}: {value}")
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💊 Health Recommendations")
    
    recommendations = predictor.get_recommendations(result['risk_level'], 'diabetes')
    
    for rec in recommendations:
        if "🚨" in rec:
            st.error(rec)
        elif "⚠️" in rec:
            st.warning(rec)
        else:
            st.success(rec)
    
    st.markdown("---")
    st.info("💡 **Note:** These predictions are based on machine learning models and should not replace professional medical advice. Please consult a healthcare provider for proper diagnosis and treatment.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 0.85rem;'>
        <p>Diabetes Prediction using PIMA Indian Diabetes Dataset</p>
    </div>
""", unsafe_allow_html=True)
