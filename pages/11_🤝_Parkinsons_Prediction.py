"""
Parkinson's Disease Prediction Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager

st.set_page_config(page_title="Parkinson's Prediction", page_icon="🤝", layout="wide")

auth = Authentication()
db = DatabaseManager()
predictor = get_predictor('parkinsons')

if not auth.require_login():
    st.stop()

st.title("🤝 Parkinson's Disease Prediction")

st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='color: white; margin: 0;'>About Parkinson's Prediction</h3>
        <p style='margin: 0.5rem 0 0 0;'>
            Parkinson's disease prediction using voice analysis measurements.
        </p>
    </div>
""", unsafe_allow_html=True)

st.info("ℹ️ **Note:** This test uses advanced voice measurements. For simplified testing, default values are provided.")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Voice Measurement Parameters")
    
    with st.form("parkinsons_form"):
        st.markdown("**Frequency Parameters**")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            mdvp_fo = st.number_input("MDVP:Fo(Hz)", min_value=80.0, max_value=300.0, value=150.0, help="Average vocal fundamental frequency")
            mdvp_fhi = st.number_input("MDVP:Fhi(Hz)", min_value=100.0, max_value=600.0, value=200.0)
            mdvp_flo = st.number_input("MDVP:Flo(Hz)", min_value=60.0, max_value=250.0, value=100.0)
        
        with col_b:
            mdvp_jitter = st.number_input("MDVP:Jitter(%)", min_value=0.0, max_value=0.05, value=0.005, format="%.5f")
            mdvp_jitter_abs = st.number_input("MDVP:Jitter(Abs)", min_value=0.0, max_value=0.001, value=0.00005, format="%.6f")
            mdvp_rap = st.number_input("MDVP:RAP", min_value=0.0, max_value=0.02, value=0.003, format="%.5f")
        
        with col_c:
            mdvp_ppq = st.number_input("MDVP:PPQ", min_value=0.0, max_value=0.02, value=0.003, format="%.5f")
            jitter_ddp = st.number_input("Jitter:DDP", min_value=0.0, max_value=0.05, value=0.009, format="%.5f")
        
        st.markdown("**Shimmer Parameters**")
        col_d, col_e, col_f = st.columns(3)
        
        with col_d:
            mdvp_shimmer = st.number_input("MDVP:Shimmer", min_value=0.0, max_value=0.15, value=0.03, format="%.5f")
            mdvp_shimmer_db = st.number_input("MDVP:Shimmer(dB)", min_value=0.0, max_value=1.5, value=0.3)
            shimmer_apq3 = st.number_input("Shimmer:APQ3", min_value=0.0, max_value=0.06, value=0.015, format="%.5f")
        
        with col_e:
            shimmer_apq5 = st.number_input("Shimmer:APQ5", min_value=0.0, max_value=0.08, value=0.02, format="%.5f")
            mdvp_apq = st.number_input("MDVP:APQ", min_value=0.0, max_value=0.15, value=0.03, format="%.5f")
            shimmer_dda = st.number_input("Shimmer:DDA", min_value=0.0, max_value=0.2, value=0.045, format="%.5f")
        
        with col_f:
            nhr = st.number_input("NHR", min_value=0.0, max_value=0.5, value=0.02, format="%.5f")
            hnr = st.number_input("HNR", min_value=5.0, max_value=40.0, value=22.0)
        
        st.markdown("**Additional Parameters**")
        col_g, col_h = st.columns(2)
        
        with col_g:
            rpde = st.number_input("RPDE", min_value=0.2, max_value=0.8, value=0.5, format="%.5f")
            dfa = st.number_input("DFA", min_value=0.5, max_value=0.85, value=0.65, format="%.5f")
            spread1 = st.number_input("Spread1", min_value=-8.0, max_value=-2.0, value=-5.0)
        
        with col_h:
            spread2 = st.number_input("Spread2", min_value=0.0, max_value=0.5, value=0.2, format="%.5f")
            d2 = st.number_input("D2", min_value=1.0, max_value=4.0, value=2.5)
            ppe = st.number_input("PPE", min_value=0.0, max_value=0.7, value=0.2, format="%.5f")
        
        submit = st.form_submit_button("🔍 Predict Risk", use_container_width=True)
        
        if submit:
            input_data = pd.DataFrame([{
                'MDVPFo': mdvp_fo, 'MDVPFhi': mdvp_fhi, 'MDVPFlo': mdvp_flo,
                'MDVPJitter': mdvp_jitter, 'MDVPJitterAbs': mdvp_jitter_abs,
                'MDVPRAP': mdvp_rap, 'MDVPPPQ': mdvp_ppq, 'JitterDDP': jitter_ddp,
                'MDVPShimmer': mdvp_shimmer, 'MDVPShimmerdB': mdvp_shimmer_db,
                'ShimmerAPQ3': shimmer_apq3, 'ShimmerAPQ5': shimmer_apq5,
                'MDVPAPQ': mdvp_apq, 'ShimmerDDA': shimmer_dda,
                'NHR': nhr, 'HNR': hnr, 'RPDE': rpde, 'DFA': dfa,
                'Spread1': spread1, 'Spread2': spread2, 'D2': d2, 'PPE': ppe
            }])
            
            result = predictor.predict(input_data)
            
            if result['success']:
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
                    disease_type='parkinsons',
                    input_data=input_data.to_dict('records')[0],
                    prediction_result=result['prediction'],
                    risk_probability=risk_prob,
                    risk_level=risk_level
                )
            else:
                st.error(f"❌ Error: {result['error']}")

with col2:
    st.markdown("### ℹ️ About the Test")
    st.info("""
        **Voice Analysis:**
        This test uses voice measurements to detect Parkinson's disease.
        
        **Key Symptoms:**
        - Tremor
        - Slowed movement
        - Rigid muscles
        - Impaired posture
        - Loss of automatic movements
        - Speech changes
        - Writing changes
    """)
