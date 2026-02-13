"""
Multi-Disease Risk Analytics System
Main Application File
"""

import streamlit as st
from src.authentication import Authentication
import config

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state=config.INITIAL_SIDEBAR_STATE
)

# Custom CSS
def load_custom_css():
    """Load custom CSS styling"""
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            font-weight: 600;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
        }
        h1 {
            color: #2c3e50;
            padding-bottom: 1rem;
        }
        h2 {
            color: #34495e;
        }
        .success-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #d4edda;
            border-left: 5px solid #28a745;
            margin: 1rem 0;
        }
        .warning-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            margin: 1rem 0;
        }
        .danger-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #f8d7da;
            border-left: 5px solid #dc3545;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# Initialize authentication
auth = Authentication()

def main():
    """Main application logic"""
    
    # Check if user is logged in
    if not auth.is_logged_in():
        # Show authentication page
        st.title(f"{config.APP_ICON} {config.APP_TITLE}")
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                <h2 style='color: white; margin: 0;'>Welcome to Multi-Disease Risk Analytics</h2>
                <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
                    Predict risk for 5 major diseases using advanced machine learning
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🎯 Features")
            st.markdown("""
                ✅ **Multi-Disease Prediction** - Diabetes, Heart, Kidney, Liver, Breast Cancer  
                ✅ **AI-Powered Analysis** - Advanced machine learning models  
                ✅ **Risk Assessment** - Color-coded risk levels  
                ✅ **Professional Reports** - Download PDF reports  
                ✅ **Analytics Dashboard** - Track your health trends  
                ✅ **Secure & Private** - Your data is protected  
            """)
            
            st.markdown("---")
            
            # Show auth form
            auth.show_auth_page()
            
            st.markdown("---")
            st.markdown("""
                <div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
                    <p>⚠️ <b>Disclaimer:</b> This platform is for educational purposes only. 
                    Always consult qualified healthcare professionals for medical advice.</p>
                </div>
            """, unsafe_allow_html=True)
    
    else:
        # User is logged in - show main dashboard
        user_data = auth.get_user_data()
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"### 👤 Welcome, {user_data['username']}!")
            st.markdown("---")
            
            st.markdown("### 🏥 Navigation")
            st.markdown("""
                Use the pages above to:
                - 🏠 **Home** - Dashboard overview
                - 💉 **Diabetes** - Test diabetes risk
                - ❤️ **Heart** - Test heart disease risk
                - 🫘 **Kidney** - Test kidney disease risk
                - 🫀 **Liver** - Test liver disease risk
                - 🎀 **Breast Cancer** - Test cancer risk
                - 📊 **Analytics** - View your history
                - 👤 **Profile** - Manage account
            """)
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                auth.logout()
                st.success("Logged out successfully!")
                st.rerun()
        
        # Main content
        st.title(f"{config.APP_ICON} {config.APP_TITLE}")
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                <h2 style='color: white; margin: 0;'>Your Health Dashboard</h2>
                <p style='margin: 0.5rem 0 0 0;'>
                    Select a disease prediction from the sidebar to get started
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        from src.database_manager import DatabaseManager
        db = DatabaseManager()
        
        stats = db.get_prediction_stats(auth.get_user_id())
        total_predictions = db.get_prediction_count(auth.get_user_id())
        
        st.markdown("### 📊 Quick Stats")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tests", total_predictions)
        
        with col2:
            low_risk = stats['by_risk'].get('Low', 0)
            st.metric("Low Risk", low_risk, delta="Good" if low_risk > 0 else None)
        
        with col3:
            moderate_risk = stats['by_risk'].get('Moderate', 0)
            st.metric("Moderate Risk", moderate_risk, delta="Watch" if moderate_risk > 0 else None)
        
        with col4:
            high_risk = stats['by_risk'].get('High', 0)
            st.metric("High Risk", high_risk, delta="Alert" if high_risk > 0 else None, delta_color="inverse")
        
        st.markdown("---")
        
        # Disease cards
        st.markdown("### 🏥 Available Disease Predictions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>💉 Diabetes Prediction</h3>
                    <p style='margin: 0.5rem 0 0 0;'>Test your diabetes risk using blood sugar and BMI data</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>🫘 Kidney Disease Prediction</h3>
                    <p style='margin: 0.5rem 0 0 0;'>Assess kidney health with comprehensive lab values</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>🎀 Breast Cancer Prediction</h3>
                    <p style='margin: 0.5rem 0 0 0;'>Early detection screening using cell characteristics</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>❤️ Heart Disease Prediction</h3>
                    <p style='margin: 0.5rem 0 0 0;'>Evaluate heart health with cardiac parameters</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                            padding: 1.5rem; border-radius: 10px; color: #2c3e50; margin-bottom: 1rem;'>
                    <h3 style='color: #2c3e50; margin: 0;'>🫀 Liver Disease Prediction</h3>
                    <p style='margin: 0.5rem 0 0 0;'>Check liver function with enzyme levels</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recent activity
        if total_predictions > 0:
            st.markdown("### 📋 Recent Activity")
            
            recent_predictions = db.get_user_predictions(auth.get_user_id())[:5]
            
            if recent_predictions:
                for pred in recent_predictions:
                    disease_name = config.DISEASE_INFO[pred['disease_type']]['name']
                    icon = config.DISEASE_INFO[pred['disease_type']]['icon']
                    
                    risk_color = {
                        'Low': '#28a745',
                        'Moderate': '#ffc107',
                        'High': '#dc3545'
                    }.get(pred['risk_level'], '#999')
                    
                    st.markdown(f"""
                        <div style='background: rgba(45, 55, 72, 0.6); padding: 1rem; border-radius: 10px; 
                                    border-left: 5px solid {risk_color}; margin-bottom: 0.5rem;'>
                            <b>{icon} {disease_name}</b> - 
                            <span style='color: {risk_color};'><b>{pred['risk_level']} Risk</b></span>
                            ({pred['risk_probability']*100:.1f}%) - 
                            <small>{pred['prediction_date']}</small>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("👋 No predictions yet! Start by selecting a disease test from the sidebar.")
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: #7f8c8d; font-size: 0.85rem; padding: 1rem;'>
                <p>🏥 Multi-Disease Risk Analytics Platform | Powered by Machine Learning</p>
                <p>⚠️ For educational purposes only. Consult healthcare professionals for medical advice.</p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
