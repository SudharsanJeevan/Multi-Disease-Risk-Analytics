"""
Enhanced Lung Cancer Risk Prediction Page
Uses 25-feature Cancer Patients Dataset
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import pathlib
from src.authentication import Authentication
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Lung Cancer Prediction", page_icon="🫁", layout="wide")

auth = Authentication()
db = DatabaseManager()

if not auth.require_admin():
    st.stop()

# Load model, scaler, label encoder, feature names
BASE_DIR = pathlib.Path(__file__).parent.parent
MODEL_DIR = BASE_DIR / "models" / "lung_cancer"

@st.cache_resource
def load_model():
    try:
        with open(MODEL_DIR / "lung_cancer_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open(MODEL_DIR / "lung_cancer_scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        with open(MODEL_DIR / "lung_cancer_label_encoder.pkl", "rb") as f:
            le = pickle.load(f)
        with open(MODEL_DIR / "lung_cancer_features.pkl", "rb") as f:
            features = pickle.load(f)
        return model, scaler, le, features
    except Exception as e:
        return None, None, None, None

model, scaler, le, feature_names = load_model()

# ── Page Header ──────────────────────────────────────────────────────────────
st.title("🫁 Lung Cancer Risk Prediction")

st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 2rem;
                border: 1px solid #e94560;'>
        <h3 style='color: #e94560; margin: 0;'>⚠️ Enhanced Clinical Assessment</h3>
        <p style='margin: 0.5rem 0 0 0; color: #a8b2d8;'>
            This model uses <b>25 clinical features</b> including environmental exposures,
            genetic risk, lifestyle factors and symptoms to predict lung cancer severity level
            (Low / Medium / High).
        </p>
    </div>
""", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model not loaded. Please run: `python models/lung_cancer/train_lung_cancer.py`")
    st.stop()

# ── Input Form ───────────────────────────────────────────────────────────────
with st.form("lung_cancer_form"):

    # ── 1. Demographic ────────────────────────────────────────────────────────
    st.markdown("### 👤 Demographic Information")
    d1, d2 = st.columns(2)
    with d1:
        age = st.slider("Age", 1, 100, 45)
    with d2:
        gender = st.selectbox("Gender", ["Male", "Female"])

    st.markdown("---")

    # ── 2. Environmental & Occupational Exposure ──────────────────────────────
    st.markdown("### 🌫️ Environmental & Occupational Exposure")
    st.caption("Rate each factor on a scale of 1 (None) to 8 (Severe)")
    e1, e2, e3 = st.columns(3)
    with e1:
        air_pollution = st.slider("Air Pollution", 1, 8, 2,
            help="Exposure to outdoor air pollution, exhaust fumes")
        dust_allergy = st.slider("Dust Allergy", 1, 8, 2,
            help="Severity of dust-related allergies")
    with e2:
        occupational_hazards = st.slider("Occupational Hazards", 1, 8, 2,
            help="Asbestos, silica, chemicals at workplace")
        genetic_risk = st.slider("Genetic Risk", 1, 7, 2,
            help="Family history of lung cancer")
    with e3:
        balanced_diet = st.slider("Balanced Diet", 1, 7, 3,
            help="Quality of daily diet (higher = healthier)")
        passive_smoker = st.slider("Passive Smoker", 1, 8, 2,
            help="Secondhand smoke exposure level")

    st.markdown("---")

    # ── 3. Lifestyle ──────────────────────────────────────────────────────────
    st.markdown("### 🚬 Lifestyle Factors")
    l1, l2, l3 = st.columns(3)
    with l1:
        alcohol_use = st.slider("Alcohol Use", 1, 8, 2,
            help="Frequency/amount of alcohol consumption")
        smoking = st.slider("Smoking", 1, 8, 2,
            help="Smoking intensity (pack-years equivalent)")
    with l2:
        obesity = st.slider("Obesity Level", 1, 7, 3,
            help="Body weight relative to healthy range")
    with l3:
        pass

    st.markdown("---")

    # ── 4. Medical History ────────────────────────────────────────────────────
    st.markdown("### 🏥 Medical & Pulmonary History")
    m1, m2 = st.columns(2)
    with m1:
        chronic_lung_disease = st.slider("Chronic Lung Disease", 1, 7, 1,
            help="COPD, emphysema, pulmonary fibrosis severity")
    with m2:
        pulmonary_disease = st.slider("Pulmonary Disease History", 1, 6, 1,
            help="Previous pulmonary conditions")

    st.markdown("---")

    # ── 5. Clinical Symptoms ──────────────────────────────────────────────────
    st.markdown("### 🩺 Clinical Symptoms")
    st.caption("Rate each symptom: 1 = None/Rare, higher = Frequent/Severe")
    s1, s2, s3 = st.columns(3)
    with s1:
        chest_pain = st.slider("Chest Pain", 1, 9, 1)
        coughing_blood = st.slider("Hemoptysis (Coughing Blood)", 1, 9, 1)
        fatigue = st.slider("Fatigue", 1, 9, 3)
    with s2:
        weight_loss = st.slider("Unexplained Weight Loss", 1, 8, 2)
        shortness_breath = st.slider("Shortness of Breath (Dyspnea)", 1, 9, 2)
        wheezing = st.slider("Wheezing", 1, 8, 2)
    with s3:
        swallowing_difficulty = st.slider("Swallowing Difficulty", 1, 8, 1)
        clubbing_nails = st.slider("Clubbing of Finger Nails", 1, 9, 1)
        frequent_cold = st.slider("Frequent Cold / Infections", 1, 7, 2)

    s4, s5 = st.columns(2)
    with s4:
        dry_cough = st.slider("Dry Cough", 1, 7, 2)
    with s5:
        snoring = st.slider("Snoring", 1, 7, 2)

    st.markdown("---")
    submit = st.form_submit_button("🔬 Predict Lung Cancer Risk", use_container_width=True,
                                    type="primary")

# ── Prediction ────────────────────────────────────────────────────────────────
if submit:
    input_dict = {
        'Age': age,
        'Gender': 1 if gender == "Male" else 2,
        'Air Pollution': air_pollution,
        'Alcohol use': alcohol_use,
        'Dust Allergy': dust_allergy,
        'OccuPational Hazards': occupational_hazards,
        'Genetic Risk': genetic_risk,
        'chronic Lung Disease': chronic_lung_disease,
        'Balanced Diet': balanced_diet,
        'Obesity': obesity,
        'Smoking': smoking,
        'Passive Smoker': passive_smoker,
        'Chest Pain': chest_pain,
        'Coughing of Blood': coughing_blood,
        'Fatigue': fatigue,
        'Weight Loss': weight_loss,
        'Shortness of Breath': shortness_breath,
        'Wheezing': wheezing,
        'Swallowing Difficulty': swallowing_difficulty,
        'Clubbing of Finger Nails': clubbing_nails,
        'Frequent Cold': frequent_cold,
        'Dry Cough': dry_cough,
        'Snoring': snoring,
    }

    # Align to trained feature order
    input_df = pd.DataFrame([input_dict])
    # Add any missing columns with default 1
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 1
    input_df = input_df[feature_names]

    with st.spinner("🔮 Analyzing risk factors..."):
        input_scaled = scaler.transform(input_df)
        pred_encoded = model.predict(input_scaled)[0]
        pred_proba = model.predict_proba(input_scaled)[0]
        risk_label = le.inverse_transform([pred_encoded])[0]   # Low / Medium / High
        risk_prob = float(max(pred_proba))

    # Map to standard risk for DB
    risk_level_map = {'Low': 'Low', 'Medium': 'Moderate', 'High': 'High'}
    risk_level = risk_level_map.get(risk_label, risk_label)

    # Color scheme
    color_map = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
    icon_map  = {'Low': '✅', 'Medium': '⚠️', 'High': '🚨'}
    risk_color = color_map.get(risk_label, '#6c757d')
    risk_icon  = icon_map.get(risk_label, '❓')

    st.markdown("---")
    st.markdown("### 📊 Prediction Results")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
            <div style='background: {risk_color}; padding: 2rem;
                        border-radius: 12px; color: white; text-align: center;'>
                <h1 style='color: white; margin: 0; font-size: 3rem;'>{risk_icon}</h1>
                <h2 style='color: white; margin: 0.5rem 0;'>{risk_label} Risk</h2>
                <p style='font-size: 1.5rem; margin: 0; font-weight: bold;'>
                    Confidence: {risk_prob*100:.1f}%
                </p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("#### 🔬 Risk Factor Breakdown")
        # Probability bars for all classes
        classes = le.classes_
        probs = model.predict_proba(input_scaled)[0]
        for cls, prob in sorted(zip(classes, probs), key=lambda x: x[1], reverse=True):
            bar_col = color_map.get(cls, '#6c757d')
            st.markdown(f"""
                <div style='margin-bottom: 0.5rem;'>
                    <span style='font-weight: bold; color: {bar_col};'>{cls} Risk:</span>
                    <span style='float: right'>{prob*100:.1f}%</span>
                    <div style='background: #2d3748; border-radius: 4px; height: 12px; margin-top: 4px;'>
                        <div style='background: {bar_col}; width: {prob*100:.1f}%;
                                    height: 12px; border-radius: 4px;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Recommendations
    recs = {
        'Low': [
            "✅ Continue regular health check-ups",
            "✅ Maintain healthy lifestyle — exercise, balanced diet",
            "✅ Avoid smoking and secondhand smoke",
            "✅ Reduce environmental pollution exposure where possible",
        ],
        'Medium': [
            "⚠️ Schedule a consultation with a pulmonologist",
            "⚠️ Consider low-dose CT scan screening",
            "⚠️ Quit smoking immediately if applicable",
            "⚠️ Monitor symptoms — persistent cough, weight loss, blood",
            "⚠️ Reduce occupational hazard exposure",
        ],
        'High': [
            "🚨 URGENT: Seek immediate medical consultation",
            "🚨 Request CT scan and biomarker tests (CEA, CYFRA 21-1)",
            "🚨 Discuss biopsy / bronchoscopy with your doctor",
            "🚨 Complete cessation of smoking required",
            "🚨 Avoid all environmental toxin exposure",
            "🚨 Consider referral to oncology specialist",
        ]
    }

    st.markdown("#### 💡 Recommendations")
    for rec in recs.get(risk_label, []):
        st.markdown(rec)

    # Save to DB
    try:
        db.save_prediction(
            user_id=auth.get_user_id(),
            disease_type='lung_cancer',
            prediction_result=pred_encoded,
            risk_probability=risk_prob,
            risk_level=risk_level,
            input_parameters=input_dict
        )
        st.success("✅ Prediction saved to your history.")
    except Exception as e:
        st.warning(f"Could not save to history: {e}")

# ── Info Sidebar ───────────────────────────────────────────────────────────────
with st.expander("ℹ️ About This Prediction Model"):
    st.markdown("""
    **Model:** XGBoost / Random Forest (best performer selected automatically)

    **Dataset:** Cancer Patients and Air Pollution dataset (Kaggle) – 1,000 patients, 25 features

    **Target:** Cancer Risk Level → **Low**, **Medium**, **High**

    **Features used:**
    - 🌍 Environmental: Air pollution, dust allergy, occupational hazards
    - 🧬 Genetic: Family risk, passive smoking
    - 🚬 Lifestyle: Smoking, alcohol, obesity, diet quality
    - 🏥 Medical: Chronic lung disease, pulmonary history
    - 🩺 Symptoms: Chest pain, hemoptysis, weight loss, dyspnea, wheezing,
      swallowing difficulty, finger clubbing, dry cough, frequent cold, snoring

    **Disclaimer:** This tool is for educational purposes only. Always consult a qualified
    healthcare professional for diagnosis and treatment.
    """)
