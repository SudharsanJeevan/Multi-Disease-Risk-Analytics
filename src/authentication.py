"""
Authentication Module (Extended with Role-Based Access)
Handles user/admin login, signup, session management, and role guards
"""

import streamlit as st
from src.database_manager import DatabaseManager
import sqlite3
import config

# Secret code required to create an admin account
ADMIN_ACCESS_CODE = "MDRA-ADMIN-2026"


class Authentication:
    """Manages user authentication with role support"""

    def __init__(self):
        self.db = DatabaseManager()
        self._init_session_state()
        self._inject_global_css()

    def _inject_global_css(self):
        """Injects CSS to rename the sidebar 'app' link everywhere and hide disease pages for users"""
        role = st.session_state.get('role', 'user')
        
        # Base CSS for renaming Home
        css = """
        <style>
        [data-testid="stSidebarNavItems"] li:first-child a span:first-child {
            font-size: 0 !important;
        }
        [data-testid="stSidebarNavItems"] li:first-child a span:first-child::before {
            content: "🏠 Home";
            font-size: 1rem !important;
            visibility: visible !important;
        }
        """
        
        # Additional CSS for patients (role='user')
        if role == 'user':
            css += """
            /* Hide Admin Dashboard (2nd item) */
            [data-testid="stSidebarNavItems"] li:nth-child(2) {
                display: none !important;
            }
            /* Hide Disease Predictions (4th to 18th items) */
            [data-testid="stSidebarNavItems"] li:nth-child(n+4):nth-child(-n+18) {
                display: none !important;
            }
            """
            
        # Show all sidebar nav items — no collapse/expand
        css += """
        /* Remove height limit so all items are visible */
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNav"] ul {
            max-height: none !important;
            overflow: visible !important;
        }
        /* Hide the toggle button entirely */
        [data-testid="stSidebarNavItems"] button,
        [data-testid="stSidebarNav"] button,
        button.e1pqlk4310 {
            display: none !important;
        }
        """
        
        css += "</style>"
        st.markdown(css, unsafe_allow_html=True)

    # ── Session helpers ───────────────────────────────────────────────────
    def _init_session_state(self):
        defaults = {
            'logged_in': False,
            'user_data': None,
            'user_id': None,
            'role': None,
            'show_signup': False,
            'show_admin_signup': False,
        }
        for key, val in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = val

    def is_logged_in(self):
        return st.session_state.logged_in

    def get_user_data(self):
        return st.session_state.user_data

    def get_user_id(self):
        return st.session_state.user_id

    def get_role(self):
        return st.session_state.role

    def is_admin(self):
        return st.session_state.role == 'admin'

    # ── DB helpers (read-only, doesn't modify database_manager.py) ────
    def _get_user_role(self, user_id):
        """Get role directly from DB"""
        try:
            conn = sqlite3.connect(str(config.DATABASE_PATH))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            conn.close()
            return row['role'] if row else 'user'
        except Exception:
            return 'user'

    def _set_user_role(self, user_id, role):
        """Set role directly in DB"""
        try:
            conn = sqlite3.connect(str(config.DATABASE_PATH))
            cur = conn.cursor()
            cur.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
            conn.commit()
            conn.close()
        except Exception:
            pass

    # ── Login / Signup / Logout ────────────────────────────────────────
    def login(self, username, password):
        success, message, user_data = self.db.authenticate_user(username, password)
        if success:
            role = self._get_user_role(user_data['id'])
            st.session_state.logged_in = True
            st.session_state.user_data = user_data
            st.session_state.user_id = user_data['id']
            st.session_state.role = role
        return success, message

    def signup(self, username, email, password, confirm_password,
               full_name=None, age=None, gender=None):
        """Register a new USER (role='user')"""
        if not username or not email or not password:
            return False, "All fields are required!"
        if len(username) < 3:
            return False, "Username must be at least 3 characters!"
        if len(password) < 6:
            return False, "Password must be at least 6 characters!"
        if password != confirm_password:
            return False, "Passwords don't match!"
        if '@' not in email:
            return False, "Invalid email address!"

        success, message, user_id = self.db.create_user(
            username, email, password, full_name, age, gender
        )
        if success and user_id:
            self._set_user_role(user_id, 'user')
        return success, message

    def admin_signup(self, username, email, password, confirm_password,
                     access_code, full_name=None):
        """Register a new ADMIN (requires access code)"""
        if access_code != ADMIN_ACCESS_CODE:
            return False, "❌ Invalid admin access code!"
        if not username or not email or not password:
            return False, "All fields are required!"
        if len(username) < 3:
            return False, "Username must be at least 3 characters!"
        if len(password) < 6:
            return False, "Password must be at least 6 characters!"
        if password != confirm_password:
            return False, "Passwords don't match!"
        if '@' not in email:
            return False, "Invalid email!"

        success, message, user_id = self.db.create_user(
            username, email, password, full_name
        )
        if success and user_id:
            self._set_user_role(user_id, 'admin')
        return success, message

    def logout(self):
        for key in ['logged_in', 'user_data', 'user_id', 'role',
                     'show_signup', 'show_admin_signup']:
            st.session_state[key] = None if key != 'logged_in' else False
        st.session_state.show_signup = False
        st.session_state.show_admin_signup = False

    # ── Page guards ───────────────────────────────────────────────────
    def require_login(self):
        if not self.is_logged_in():
            st.warning("⚠️ Please login to access this page")
            self.show_auth_page()
            return False
        return True

    def require_admin(self):
        """Block non-admins from accessing a page"""
        if not self.is_logged_in():
            st.warning("⚠️ Please login as an admin")
            return False
        if not self.is_admin():
            st.error("🚫 Access Denied — Admin privileges required")
            st.info("This page is only accessible to administrators.")
            return False
        return True

    def require_user(self):
        """Block non-users (admins use their own pages)"""
        if not self.is_logged_in():
            st.warning("⚠️ Please login to access this page")
            return False
        return True

    # ── Auth pages (backward compat) ──────────────────────────────────
    def show_auth_page(self):
        """Backward-compatible: show split login page"""
        self.show_split_login_page()

    # ── SPLIT LOGIN PAGE ──────────────────────────────────────────────
    def show_split_login_page(self):
        """Two-column login: User (left) | Admin (right)"""

        col_user, col_divider, col_admin = st.columns([5, 1, 5])

        # ── Left: User login/signup ───────────────────────────────────
        with col_user:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1rem 1.5rem; border-radius: 12px; text-align: center;
                            margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>👤 Patient Login</h3>
                </div>
            """, unsafe_allow_html=True)

            if st.session_state.get('show_signup'):
                self._user_signup_form()
            else:
                self._user_login_form()

        # ── Divider ───────────────────────────────────────────────────
        with col_divider:
            st.markdown("""
                <div style='display: flex; align-items: center; justify-content: center;
                            height: 100%; min-height: 400px;'>
                    <div style='width: 2px; height: 100%; min-height: 400px;
                                background: linear-gradient(180deg, transparent, #666, transparent);'>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # ── Right: Admin login/signup ─────────────────────────────────
        with col_admin:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            padding: 1rem 1.5rem; border-radius: 12px; text-align: center;
                            margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>🔧 Admin Login</h3>
                </div>
            """, unsafe_allow_html=True)

            if st.session_state.get('show_admin_signup'):
                self._admin_signup_form()
            else:
                self._admin_login_form()

    # ── Individual form renderers ─────────────────────────────────────
    def _user_login_form(self):
        with st.form("user_login_form"):
            username = st.text_input("Username", placeholder="Enter username", key="ul_user")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="ul_pass")
            submit = st.form_submit_button("🚀 Login as Patient", use_container_width=True)

            if submit and username and password:
                success, msg = self.login(username, password)
                if success:
                    if self.is_admin():
                        # Admin tried user login — allow but warn
                        pass
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            elif submit:
                st.warning("Fill in all fields!")

        if st.button("📝 Create Patient Account", key="btn_show_user_signup", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()

    def _user_signup_form(self):
        with st.form("user_signup_form"):
            c1, c2 = st.columns(2)
            with c1:
                username = st.text_input("Username *", key="us_user")
                email = st.text_input("Email *", key="us_email")
                full_name = st.text_input("Full Name", key="us_name")
            with c2:
                password = st.text_input("Password *", type="password", key="us_pass")
                confirm = st.text_input("Confirm Password *", type="password", key="us_confirm")
                age = st.number_input("Age", min_value=1, max_value=120, value=25, key="us_age")

            gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"], key="us_gender")
            gender_val = None if gender == "Select" else gender

            submit = st.form_submit_button("✅ Create Patient Account", use_container_width=True)
            if submit:
                success, msg = self.signup(username, email, password, confirm, full_name, age, gender_val)
                if success:
                    st.success(msg + " Please login.")
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error(msg)

        if st.button("🔙 Back to Login", key="back_user_login", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()

    def _admin_login_form(self):
        with st.form("admin_login_form"):
            username = st.text_input("Admin Username", placeholder="Enter admin username", key="al_user")
            password = st.text_input("Admin Password", type="password", placeholder="Enter password", key="al_pass")
            submit = st.form_submit_button("🔐 Login as Admin", use_container_width=True)

            if submit and username and password:
                success, msg = self.login(username, password)
                if success:
                    if not self.is_admin():
                        self.logout()
                        st.error("❌ This account does not have admin privileges.")
                    else:
                        st.success("✅ Admin login successful!")
                        st.rerun()
                else:
                    st.error(msg)
            elif submit:
                st.warning("Fill in all fields!")

        if st.button("🛡️ Register as Admin", key="btn_show_admin_signup", use_container_width=True):
            st.session_state.show_admin_signup = True
            st.rerun()

    def _admin_signup_form(self):
        with st.form("admin_signup_form"):
            st.warning("⚠️ Admin registration requires a valid access code.")
            access_code = st.text_input("Admin Access Code *", type="password",
                                         placeholder="Enter admin access code", key="as_code")
            c1, c2 = st.columns(2)
            with c1:
                username = st.text_input("Username *", key="as_user")
                email = st.text_input("Email *", key="as_email")
            with c2:
                password = st.text_input("Password *", type="password", key="as_pass")
                confirm = st.text_input("Confirm *", type="password", key="as_confirm")
            full_name = st.text_input("Full Name", key="as_name")

            submit = st.form_submit_button("🛡️ Create Admin Account", use_container_width=True)
            if submit:
                success, msg = self.admin_signup(username, email, password, confirm, access_code, full_name)
                if success:
                    st.success("✅ Admin account created! Please login.")
                    st.session_state.show_admin_signup = False
                    st.rerun()
                else:
                    st.error(msg)

        if st.button("🔙 Back to Admin Login", key="btn_back_admin_login", use_container_width=True):
            st.session_state.show_admin_signup = False
            st.rerun()

    # Legacy methods kept for backward compatibility
    def show_login_page(self):
        self.show_split_login_page()

    def show_signup_page(self):
        self.show_split_login_page()
