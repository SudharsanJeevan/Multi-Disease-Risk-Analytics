"""
Authentication Module
Handles user login, signup, and session management for Streamlit
"""

import streamlit as st
from src.database_manager import DatabaseManager

class Authentication:
    """Manages user authentication in Streamlit"""
    
    def __init__(self):
        """Initialize authentication system"""
        self.db = DatabaseManager()
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return st.session_state.logged_in
    
    def get_user_data(self):
        """Get current user data"""
        return st.session_state.user_data
    
    def get_user_id(self):
        """Get current user ID"""
        return st.session_state.user_id
    
    def login(self, username, password):
        """
        Login user
        Returns: (success: bool, message: str)
        """
        success, message, user_data = self.db.authenticate_user(username, password)
        
        if success:
            st.session_state.logged_in = True
            st.session_state.user_data = user_data
            st.session_state.user_id = user_data['id']
        
        return success, message
    
    def signup(self, username, email, password, confirm_password, 
               full_name=None, age=None, gender=None):
        """
        Register new user
        Returns: (success: bool, message: str)
        """
        # Validation
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
        
        # Create user
        success, message, user_id = self.db.create_user(
            username, email, password, full_name, age, gender
        )
        
        return success, message
    
    def logout(self):
        """Logout current user"""
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.user_id = None
    
    def show_login_page(self):
        """Display login page"""
        st.title("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", 
                                    placeholder="Enter your password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
            with col2:
                signup_btn = st.form_submit_button("📝 Sign Up Instead", 
                                                   use_container_width=True)
            
            if submit:
                if username and password:
                    success, message = self.login(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields!")
            
            if signup_btn:
                st.session_state.show_signup = True
                st.rerun()
    
    def show_signup_page(self):
        """Display signup page"""
        st.title("📝 Create Account")
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username *", 
                                        placeholder="Choose a username")
                email = st.text_input("Email *", 
                                     placeholder="your.email@example.com")
                full_name = st.text_input("Full Name", 
                                         placeholder="Your full name (optional)")
            
            with col2:
                password = st.text_input("Password *", type="password",
                                        placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm Password *", 
                                                type="password",
                                                placeholder="Re-enter password")
                age = st.number_input("Age", min_value=1, max_value=120, 
                                     value=None, placeholder="Optional")
            
            gender = st.selectbox("Gender", 
                                 ["Select", "Male", "Female", "Other"])
            gender = None if gender == "Select" else gender
            
            st.markdown("**Required fields*")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button("✅ Create Account", 
                                              use_container_width=True)
            with col2:
                login_btn = st.form_submit_button("🔐 Login Instead", 
                                                 use_container_width=True)
            
            if submit:
                success, message = self.signup(
                    username, email, password, confirm_password,
                    full_name, age, gender
                )
                if success:
                    st.success(message)
                    st.info("Please login with your credentials")
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error(message)
            
            if login_btn:
                st.session_state.show_signup = False
                st.rerun()
    
    def show_auth_page(self):
        """Show appropriate auth page based on state"""
        if 'show_signup' not in st.session_state:
            st.session_state.show_signup = False
        
        if st.session_state.show_signup:
            self.show_signup_page()
        else:
            self.show_login_page()
    
    def require_login(self):
        """
        Decorator-like function to require login for a page
        Returns True if user is logged in, False otherwise
        """
        if not self.is_logged_in():
            st.warning("⚠️ Please login to access this page")
            self.show_auth_page()
            return False
        return True
