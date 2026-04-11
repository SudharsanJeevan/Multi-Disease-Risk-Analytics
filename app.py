"""
Multi-Disease Risk Analytics System
Main Application File (with Role-Based Auth)
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
    """Load custom CSS styling — professional conference-ready theme"""
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
        /* ── Global Font & Base ─────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        .main {
            padding: 0rem 1rem;
        }

        /* ── Headings ───────────────────────────────────────────── */
        h1 {
            color: #1a1a2e !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
            padding-bottom: 0.5rem;
        }
        h2 {
            color: #16213e !important;
            font-weight: 600 !important;
        }
        h3 {
            color: #0f3460 !important;
            font-weight: 600 !important;
        }

        /* ── Buttons ────────────────────────────────────────────── */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3em;
            font-weight: 600;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 0.3px;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        .stButton>button:active {
            transform: translateY(0);
        }

        /* ── Form Inputs ────────────────────────────────────────── */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div {
            border-radius: 10px;
            border: 1.5px solid #e0e5ec;
            padding: 0.6rem 1rem;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            font-family: 'Inter', sans-serif !important;
        }
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
        }

        /* ── Sidebar ────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        }
        [data-testid="stSidebar"] * {
            color: #e0e0e0 !important;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .stButton>button {
            background: linear-gradient(135deg, #e94560 0%, #c23152 100%) !important;
            border: none;
            box-shadow: 0 2px 8px rgba(233, 69, 96, 0.3);
        }
        [data-testid="stSidebar"] .stButton>button:hover {
            box-shadow: 0 6px 20px rgba(233, 69, 96, 0.5);
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.15) !important;
        }

        /* ── Metrics ────────────────────────────────────────────── */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
            border: 1px solid #e8ebf5;
            border-radius: 14px;
            padding: 1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            transition: transform 0.2s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        [data-testid="stMetricLabel"] {
            font-weight: 500 !important;
            color: #64748b !important;
            font-size: 0.85rem !important;
        }
        [data-testid="stMetricValue"] {
            font-weight: 700 !important;
            color: #1a1a2e !important;
        }

        /* ── Tabs ───────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 8px 20px;
            font-weight: 500;
            font-family: 'Inter', sans-serif !important;
        }

        /* ── Alert Boxes ────────────────────────────────────────── */
        .success-box {
            padding: 1.2rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-left: 5px solid #28a745;
            margin: 1rem 0;
            font-family: 'Inter', sans-serif;
        }
        .warning-box {
            padding: 1.2rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-left: 5px solid #ffc107;
            margin: 1rem 0;
            font-family: 'Inter', sans-serif;
        }
        .danger-box {
            padding: 1.2rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border-left: 5px solid #dc3545;
            margin: 1rem 0;
            font-family: 'Inter', sans-serif;
        }

        /* ── Expander ───────────────────────────────────────────── */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            border-radius: 10px;
        }

        /* ── DataFrames / Tables ─────────────────────────────────── */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }

        /* ── Smooth page transitions ─────────────────────────────── */
        .main .block-container {
            animation: fadeIn 0.4s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ── Scrollbar ───────────────────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# Initialize authentication
auth = Authentication()

def main():
    """Main application logic"""

    # ── Not logged in → Split login page ──
    if not auth.is_logged_in():
        st.title(f"{config.APP_ICON} {config.APP_TITLE}")

        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                <h2 style='color: white; margin: 0;'>Welcome to Multi-Disease Risk Analytics</h2>
                <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
                    AI-powered health risk assessment for 15 diseases
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 Features")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("""
                ✅ **Health Chatbot** — Guided health screening  
                ✅ **15 Disease Models** — AI-powered predictions  
                ✅ **Risk Assessment** — Color-coded risk levels  
            """)
        with col_f2:
            st.markdown("""
                ✅ **PDF Reports** — Professional medical reports  
                ✅ **Admin Dashboard** — Clinical management tools  
                ✅ **Secure & Private** — Role-based access control  
            """)

        st.markdown("---")

        # Split login page
        auth.show_split_login_page()

    # ── Logged in ──
    else:
        user_data = auth.get_user_data()
        role = auth.get_role()

        # Sidebar
        with st.sidebar:
            role_badge = "🛡️ Admin" if role == 'admin' else "👤 Patient"
            st.markdown(f"### {role_badge} {user_data['username']}")
            st.markdown("---")

            if role == 'admin':
                st.markdown("### 🔧 Admin Tools")
                st.markdown("""
                    - 🔧 **Admin Dashboard** — Clinical predictions  
                    - 📊 **Analytics** — View all data  
                    - 👤 **Profile** — Account settings  
                """)
            else:
                st.markdown("### 🏥 Navigation")
                st.markdown("""
                    - 🤖 **Health Chatbot** — Guided screening  
                    - 📊 **Analytics** — Your health trends  
                    - 👤 **Profile** — Account settings  
                """)

            st.markdown("---")

            if st.button("🚪 Logout", use_container_width=True):
                auth.logout()
                st.success("Logged out successfully!")
                st.rerun()

        # ── Main Content ──
        st.title(f"{config.APP_ICON} {config.APP_TITLE}")

        if role == 'admin':
            # Admin welcome
            st.markdown("""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                    <h2 style='color: white; margin: 0;'>🛡️ Admin Control Panel</h2>
                    <p style='margin: 0.5rem 0 0 0;'>
                        Navigate to the Admin Dashboard from the sidebar to run clinical predictions,
                        generate reports, and manage users.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Admin quick stats
            from src.database_manager import DatabaseManager
            db = DatabaseManager()

            import sqlite3
            conn = sqlite3.connect(str(config.DATABASE_PATH))
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users")
            total_users = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM predictions")
            total_preds = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
            total_admins = cur.fetchone()[0]
            conn.close()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Users", total_users)
            col2.metric("Total Predictions", total_preds)
            col3.metric("Admins", total_admins)
            col4.metric("Patients", total_users - total_admins)

            st.markdown("---")
            st.markdown("### 🔧 Quick Actions")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 1.5rem; border-radius: 10px; color: white;'>
                        <h3 style='color: white; margin: 0;'>🔬 Clinical Prediction</h3>
                        <p style='margin: 0.5rem 0 0 0;'>Enter clinical parameters and run AI predictions</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                                padding: 1.5rem; border-radius: 10px; color: white;'>
                        <h3 style='color: white; margin: 0;'>📄 Generate Reports</h3>
                        <p style='margin: 0.5rem 0 0 0;'>Create professional PDF reports for patients</p>
                    </div>
                """, unsafe_allow_html=True)

        else:
            # User (Patient) welcome
            st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                    <h2 style='color: white; margin: 0;'>Your Health Dashboard</h2>
                    <p style='margin: 0.5rem 0 0 0;'>
                        Use the 🤖 Health Chatbot from the sidebar for guided health screening
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # User stats
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
            st.markdown("### 🏥 Available Health Screenings")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                        <h3 style='color: white; margin: 0;'>🤖 Health Chatbot</h3>
                        <p style='margin: 0.5rem 0 0 0;'>Guided health screening — answer a few questions to assess your risk</p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                        <h3 style='color: white; margin: 0;'>💉 Diabetes · ❤️ Heart · 🫘 Kidney</h3>
                        <p style='margin: 0.5rem 0 0 0;'>Core disease predictions with detailed analysis</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                        <h3 style='color: white; margin: 0;'>🫀 Liver · 🎀 Breast Cancer · 🫁 Lung</h3>
                        <p style='margin: 0.5rem 0 0 0;'>Advanced screening for critical conditions</p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                    <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                                padding: 1.5rem; border-radius: 10px; color: #2c3e50; margin-bottom: 1rem;'>
                        <h3 style='color: #2c3e50; margin: 0;'>🧠 Stroke · 🦋 Thyroid · 🩸 Anemia</h3>
                        <p style='margin: 0.5rem 0 0 0;'>Plus Pneumonia, TB, Alzheimer's, COVID-19, Melanoma</p>
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
                st.info("👋 No predictions yet! Use the 🤖 Health Chatbot from the sidebar to get started.")




if __name__ == "__main__":
    main()
