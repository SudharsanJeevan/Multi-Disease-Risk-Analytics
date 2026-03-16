"""
User Profile Page
"""

import streamlit as st
from src.authentication import Authentication
from src.database_manager import DatabaseManager

st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")

auth = Authentication()
db = DatabaseManager()

if not auth.require_login():
    st.stop()

st.title("👤 User Profile")

st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='color: white; margin: 0;'>Manage Your Account</h3>
        <p style='margin: 0.5rem 0 0 0;'>View and update your profile information</p>
    </div>
""", unsafe_allow_html=True)

user_data = auth.get_user_data()
user_id = auth.get_user_id()

# Profile information
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem; border-radius: 15px; text-align: center; color: white;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>👤</div>
            <h2 style='color: white; margin: 0;'>{}</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>{}</p>
        </div>
    """.format(user_data['username'], user_data.get('email', 'N/A')), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Account stats
    total_predictions = db.get_prediction_count(user_id)
    
    st.markdown("### 📊 Account Stats")
    st.metric("Total Predictions", total_predictions)
    st.metric("Member Since", user_data.get('created_at', 'N/A').split()[0] if user_data.get('created_at') else 'N/A')

with col2:
    st.markdown("### 📝 Profile Information")
    
    # Display current information with better formatting and contrast
    st.markdown(f"""
        <div style='background: #1976D2; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; color: white;'>
            <b>👤 Username:</b> {user_data.get('username', 'N/A')}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: #7B1FA2; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; color: white;'>
            <b>📧 Email:</b> {user_data.get('email', 'N/A')}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: #388E3C; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; color: white;'>
            <b>✍️ Full Name:</b> {user_data.get('full_name') or 'Not provided'}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: #F57C00; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; color: white;'>
            <b>🎂 Age:</b> {user_data.get('age') or 'Not provided'}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: #C2185B; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; color: white;'>
            <b>⚧ Gender:</b> {user_data.get('gender') or 'Not provided'}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Update profile form
    st.markdown("### ✏️ Update Profile")
    
    with st.form("update_profile_form"):
        full_name = st.text_input(
            "Full Name",
            value=user_data.get('full_name', ''),
            placeholder="Enter your full name"
        )
        
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=user_data.get('age') if user_data.get('age') else 25
            )
        
        with col_f2:
            gender = st.selectbox(
                "Gender",
                ["Select", "Male", "Female", "Other"],
                index=["Select", "Male", "Female", "Other"].index(user_data.get('gender', 'Select')) 
                      if user_data.get('gender') in ["Male", "Female", "Other"] else 0
            )
        
        submit_button = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        if submit_button:
            gender_value = None if gender == "Select" else gender
            
            success, message = db.update_user_profile(
                user_id=user_id,
                full_name=full_name if full_name else None,
                age=age,
                gender=gender_value
            )
            
            if success:
                st.success(message)
                updated_user = db.get_user_by_id(user_id)
                if updated_user:
                    st.session_state.user_data = updated_user
                st.rerun()
            else:
                st.error(message)

st.markdown("---")

# Account actions
st.markdown("### ⚙️ Account Actions")

col_a1, col_a2 = st.columns(2)

with col_a1:
    st.markdown("#### 🔑 Change Password")
    
    with st.form("change_password_form"):
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        change_pwd_button = st.form_submit_button("🔐 Change Password", use_container_width=True)
        
        if change_pwd_button:
            if not old_password or not new_password or not confirm_password:
                st.error("All fields are required")
            elif new_password != confirm_password:
                st.error("New passwords don't match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, message = db.change_password(user_id, old_password, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

with col_a2:
    st.markdown("#### 🗑️ Delete Account")
    
    st.warning("⚠️ **Warning:** This action cannot be undone!")
    
    with st.form("delete_account_form"):
        st.markdown("Are you sure you want to delete your account?")
        st.markdown("All your data and predictions will be permanently deleted.")
        
        confirm_delete = st.text_input(
            "Type your username to confirm",
            placeholder=user_data['username']
        )
        
        delete_button = st.form_submit_button(
            "🗑️ Delete My Account",
            use_container_width=True,
            type="primary"
        )
        
        if delete_button:
            if confirm_delete == user_data['username']:
                success, message = db.delete_account(user_id)
                if success:
                    st.success("Account deleted successfully. Logging out...")
                    auth.logout()
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Username doesn't match. Account not deleted.")

st.markdown("---")

# Privacy information
st.markdown("### 🔒 Privacy & Security")

st.info("""
    **Your Data is Secure**
    
    ✅ All passwords are encrypted using bcrypt  
    ✅ Prediction data is stored locally  
    ✅ No data is shared with third parties  
    ✅ You can request data deletion anytime  
""")

st.markdown("---")

# Logout button
if st.button("🚪 Logout", use_container_width=True, type="primary"):
    auth.logout()
    st.success("✅ Logged out successfully!")
    st.rerun()

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 0.85rem;'>
        <p>🔐 Your account is protected and secure</p>
    </div>
""", unsafe_allow_html=True)
