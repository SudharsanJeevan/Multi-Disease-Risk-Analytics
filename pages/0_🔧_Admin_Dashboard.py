"""
🔧 Admin Dashboard — Clinical Interface
Admin-only page for manual clinical predictions, PDF reports,
prediction history, and user management.
"""

import streamlit as st
import sqlite3
import json
from datetime import datetime
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager
from src.report_generator import ReportGenerator
from src.chatbot_engine import get_questions, DISEASE_DISPLAY_NAMES
import config

st.set_page_config(page_title="Admin Dashboard", page_icon="🔧", layout="wide")

auth = Authentication()
db = DatabaseManager()

# ── Security Gate ──
if not auth.require_admin():
    st.stop()

# ── Header ──
st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 1.5rem 2rem; border-radius: 15px; margin-bottom: 1.5rem;'>
        <h2 style='color: white; margin: 0;'>🔧 Admin Clinical Dashboard</h2>
        <p style='color: rgba(255,255,255,0.85); margin: 0.3rem 0 0 0;'>
            Run clinical predictions, generate reports, and manage users
        </p>
    </div>
""", unsafe_allow_html=True)

# ── Tabs ──
tab_predict, tab_reports, tab_history, tab_users = st.tabs([
    "🔬 Clinical Prediction", "📄 PDF Reports", "📋 Prediction History", "👥 User Management"
])


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: Clinical Prediction
# ═══════════════════════════════════════════════════════════════════════════
with tab_predict:
    st.markdown("### 🔬 Run Clinical Prediction")
    st.info("Enter clinical parameters to predict disease risk using the AI models.")

    disease_options = list(DISEASE_DISPLAY_NAMES.keys())
    display_names = list(DISEASE_DISPLAY_NAMES.values())

    selected_display = st.selectbox("Select Disease", display_names, key="admin_disease")
    idx = display_names.index(selected_display)
    disease = disease_options[idx]

    questions = get_questions(disease, is_admin=True)

    if questions:
        with st.form("admin_predict_form"):
            st.markdown(f"#### Parameters for {selected_display}")
            answers = {}

            cols = st.columns(2)
            for i, q in enumerate(questions):
                with cols[i % 2]:
                    key = q["key"]
                    help_text = q.get("help", None)

                    if q["type"] == "yesno":
                        val = st.selectbox(q["question"], ["No", "Yes"],
                                           key=f"ap_{key}", help=help_text)
                        answers[key] = 1 if val == "Yes" else 0
                    elif q["type"] == "select":
                        options = list(q["options"].keys())
                        val = st.selectbox(q["question"], options,
                                           key=f"ap_{key}", help=help_text)
                        answers[key] = q["options"][val]
                    elif q["type"] == "number":
                        answers[key] = st.number_input(
                            q["question"],
                            min_value=q.get("min", 0),
                            max_value=q.get("max", 999),
                            value=q.get("default", 0),
                            key=f"ap_{key}", help=help_text
                        )
                    elif q["type"] == "number_float":
                        answers[key] = st.number_input(
                            q["question"],
                            min_value=float(q.get("min", 0.0)),
                            max_value=float(q.get("max", 999.0)),
                            value=float(q.get("default", 0.0)),
                            step=0.1,
                            key=f"ap_{key}", help=help_text
                        )

            submit = st.form_submit_button("🔍 Run Prediction", use_container_width=True,
                                            type="primary")

            if submit:
                predictor = get_predictor(disease)
                if predictor.is_model_available():
                    result = predictor.predict(answers)

                    if not result.get('error'):
                        st.session_state.admin_last_result = result
                        st.session_state.admin_last_disease = disease
                        st.session_state.admin_last_inputs = answers

                        # Save to DB
                        try:
                            db.save_prediction(
                                user_id=auth.get_user_id(),
                                disease_type=disease,
                                input_parameters=answers,
                                prediction_result=result['prediction'],
                                risk_probability=result['probability'],
                                risk_level=result['risk_level']
                            )
                        except Exception:
                            pass
                    else:
                        st.error(f"❌ {result['error']}")
                else:
                    st.error("⚠️ Model not available.")

        # Show results
        if 'admin_last_result' in st.session_state and st.session_state.get('admin_last_disease') == disease:
            result = st.session_state.admin_last_result
            risk_colors = {'Low': '#28a745', 'Moderate': '#ffc107', 'High': '#dc3545'}
            risk_emojis = {'Low': '✅', 'Moderate': '⚠️', 'High': '🚨'}
            color = risk_colors.get(result['risk_level'], '#999')
            emoji = risk_emojis.get(result['risk_level'], '❓')

            st.markdown("---")
            
            # Rich Visualizer matched with standalone pages
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, {color}aa, {color}); padding: 1.5rem;
                            border-radius: 10px; text-align: center; color: white; margin: 1rem 0;'>
                    <h2 style='color: white; margin: 0;'>{emoji} {result['risk_level']} Risk detected for {display_names[disease_options.index(disease)]}</h2>
                    <p style='font-size: 1.2rem; margin: 0.5rem 0 0 0; color: white;'>
                        AI Model Probability: <b>{result['probability']*100:.1f}%</b>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Fetch Recommendations dynamically (or use placeholders if specific logic isn't tied here)
            # Reusing the get_recommendations logic from chatbot engine for parity:
            from src.chatbot_engine import get_recommendations
            st.markdown("### 💡 Clinical Recommendations")
            recs = get_recommendations(disease, result['risk_level'])
            if recs:
                for r in recs:
                    st.markdown(f"- {r}")
            else:
                 st.info("Monitor patient closely and refer to specialist if symptoms persist.")

    else:
        st.warning("No question mapping found for this disease.")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: PDF Reports
# ═══════════════════════════════════════════════════════════════════════════
with tab_reports:
    st.markdown("### 📄 Generate PDF Report")

    if 'admin_last_result' in st.session_state:
        result = st.session_state.admin_last_result
        disease = st.session_state.admin_last_disease
        inputs = st.session_state.admin_last_inputs
        display_name = DISEASE_DISPLAY_NAMES.get(disease, disease)

        st.success(f"✅ Latest prediction: **{display_name}** — **{result['risk_level']} Risk** ({result['probability']*100:.1f}%)")

        patient_name = st.text_input("Patient Name (for report)", value=auth.get_user_data().get('full_name', 'Admin'))

        recommendations = [
            "Follow up with specialist for detailed evaluation.",
            "Maintain regular health check-ups.",
            "Follow prescribed treatment plans.",
            "Adopt a healthy lifestyle with proper diet and exercise.",
        ]

        if st.button("📄 Generate PDF Report", use_container_width=True, type="primary"):
            try:
                report = ReportGenerator()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"admin_report_{disease}_{timestamp}.pdf"

                user_data = auth.get_user_data().copy()
                user_data['full_name'] = patient_name

                pdf_path = report.generate_report(
                    filename=filename,
                    user_data=user_data,
                    disease_type=disease,
                    prediction_result=result['prediction'],
                    risk_probability=result['probability'],
                    risk_level=result['risk_level'],
                    input_parameters=inputs,
                    recommendations=recommendations
                )

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download PDF Report",
                        data=f.read(),
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.success(f"✅ Report generated: `{filename}`")
            except Exception as e:
                st.error(f"❌ Error generating report: {e}")
    else:
        st.info("ℹ️ Run a clinical prediction first (Tab 1), then come here to generate the PDF report.")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3: Prediction History
# ═══════════════════════════════════════════════════════════════════════════
with tab_history:
    st.markdown("### 📋 All Prediction History")

    try:
        conn = sqlite3.connect(str(config.DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT p.*, u.username, u.full_name
            FROM predictions p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.prediction_date DESC
            LIMIT 100
        """)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        if rows:
            st.markdown(f"Showing **{len(rows)}** most recent predictions")

            for row in rows:
                disease_name = config.DISEASE_INFO.get(row['disease_type'], {}).get('name', row['disease_type'])
                risk_color = {'Low': '#28a745', 'Moderate': '#ffc107', 'High': '#dc3545'}.get(
                    row['risk_level'], '#999')
                user_display = row.get('full_name') or row.get('username', 'Unknown')

                st.markdown(f"""
                    <div style='background: rgba(45, 55, 72, 0.6); padding: 0.8rem 1rem;
                                border-radius: 10px; border-left: 5px solid {risk_color};
                                margin-bottom: 0.5rem;'>
                        <b>{disease_name}</b> —
                        <span style='color: {risk_color};'><b>{row['risk_level']} Risk</b></span>
                        ({row['risk_probability']*100:.1f}%) —
                        👤 {user_display} —
                        <small>{row['prediction_date']}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No predictions recorded yet.")
    except Exception as e:
        st.error(f"Error loading history: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 4: User Management
# ═══════════════════════════════════════════════════════════════════════════
with tab_users:
    st.markdown("### 👥 Registered Users")

    try:
        conn = sqlite3.connect(str(config.DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id, u.username, u.email, u.full_name, u.role, u.created_at,
                   COUNT(p.id) as total_predictions
            FROM users u
            LEFT JOIN predictions p ON u.id = p.user_id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """)
        users = [dict(r) for r in cur.fetchall()]
        conn.close()

        if users:
            # Stats
            total = len(users)
            admins = sum(1 for u in users if u.get('role') == 'admin')
            patients = total - admins

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Users", total)
            col2.metric("Patients", patients)
            col3.metric("Admins", admins)

            st.markdown("---")

            for user in users:
                role_badge = "🛡️ Admin" if user.get('role') == 'admin' else "👤 Patient"
                role_color = "#f5576c" if user.get('role') == 'admin' else "#667eea"

                st.markdown(f"""
                    <div style='background: rgba(45, 55, 72, 0.5); padding: 0.8rem 1rem;
                                border-radius: 10px; border-left: 4px solid {role_color};
                                margin-bottom: 0.4rem;'>
                        <b>{user['username']}</b>
                        <span style='background: {role_color}; color: white; padding: 2px 8px;
                                     border-radius: 12px; font-size: 0.75rem; margin-left: 8px;'>
                            {role_badge}
                        </span>
                        — {user.get('email', 'N/A')}
                        — 📊 {user['total_predictions']} predictions
                        — <small>{user.get('created_at', '')}</small>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add action buttons underneath or inline using columns
                col_info, col_action = st.columns([5, 1])
                with col_action:
                    # Prevent admin from deleting themselves
                    if user['id'] != auth.get_user_id():
                        if st.button("🗑️ Delete", key=f"del_{user['id']}", use_container_width=True):
                            success, msg = db.delete_user(user['id'])
                            if success:
                                st.success(f"Deleted user: {user['username']}")
                                st.rerun()
                            else:
                                st.error(msg)
        else:
            st.info("No users found.")
    except Exception as e:
        st.error(f"Error loading users: {e}")
