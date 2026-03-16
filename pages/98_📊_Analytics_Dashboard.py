"""
Analytics Dashboard Page
"""

import streamlit as st
import pandas as pd
from src.authentication import Authentication
from src.database_manager import DatabaseManager
from src.visualizer import Visualizer
import config

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

auth = Authentication()
db = DatabaseManager()
viz = Visualizer()

if not auth.require_login():
    st.stop()

st.title("📊 Analytics Dashboard")

user_id = auth.get_user_id()
user_data = auth.get_user_data()

st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='color: white; margin: 0;'>Welcome, {user_data['username']}!</h3>
        <p style='margin: 0.5rem 0 0 0;'>Your comprehensive health analytics and prediction history</p>
    </div>
""", unsafe_allow_html=True)

# Get all predictions
predictions = db.get_user_predictions(user_id)
total_count = db.get_prediction_count(user_id)
stats = db.get_prediction_stats(user_id)

if total_count == 0:
    st.info("📝 No predictions yet! Start by selecting a disease test from the sidebar.")
    st.stop()

# Overall stats
st.markdown("### 📈 Overall Statistics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Tests", total_count)

with col2:
    low_count = stats['by_risk'].get('Low', 0)
    st.metric("Low Risk", low_count, delta=f"{low_count/total_count*100:.0f}%" if total_count > 0 else "0%")

with col3:
    mod_count = stats['by_risk'].get('Moderate', 0)
    st.metric("Moderate Risk", mod_count, delta=f"{mod_count/total_count*100:.0f}%" if total_count > 0 else "0%")

with col4:
    high_count = stats['by_risk'].get('High', 0)
    st.metric("High Risk", high_count, delta=f"{high_count/total_count*100:.0f}%" if total_count > 0 else "0%", delta_color="inverse")

with col5:
    unique_diseases = len(stats['by_disease'])
    st.metric("Diseases Tested", unique_diseases)

st.markdown("---")

# Visualizations
col_v1, col_v2 = st.columns(2)

# Prepare dataframe
df = pd.DataFrame(predictions)

with col_v1:
    st.markdown("### 🎯 Risk Level Distribution")
    fig_bar = viz.create_risk_bar_chart(df)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_v2:
    st.markdown("### 🏥 Tests by Disease Type")
    fig_pie = viz.create_disease_distribution_pie(df)
    st.plotly_chart(fig_pie, use_container_width=True)

# Timeline
st.markdown("### 📅 Prediction Timeline")
fig_timeline = viz.create_timeline_chart(df)
st.plotly_chart(fig_timeline, use_container_width=True)

# Risk probability distribution
st.markdown("### 📊 Risk Probability Distribution")
fig_prob = viz.create_probability_distribution(df)
st.plotly_chart(fig_prob, use_container_width=True)

st.markdown("---")

# Disease breakdown
st.markdown("### 🏥 Disease-wise Analysis")

for disease_type, count in stats['by_disease'].items():
    disease_name = config.DISEASE_INFO[disease_type]['name']
    disease_icon = config.DISEASE_INFO[disease_type]['icon']
    
    disease_preds = [p for p in predictions if p['disease_type'] == disease_type]
    
    if disease_preds:
        avg_risk = sum(p['risk_probability'] for p in disease_preds) / len(disease_preds)
        latest = disease_preds[0]  # Most recent
        
        risk_color = {
            'Low': '#28a745',
            'Moderate': '#ffc107',
            'High': '#dc3545'
        }.get(latest['risk_level'], '#999')
        
        with st.expander(f"{disease_icon} {disease_name} - {count} test(s)", expanded=False):
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                st.metric("Total Tests", count)
            
            with col_d2:
                st.metric("Average Risk", f"{avg_risk*100:.1f}%")
            
            with col_d3:
                st.markdown(f"""
                    <div style='background: {risk_color}22; padding: 1rem; border-radius: 10px; 
                                border-left: 5px solid {risk_color};'>
                        <b>Latest Risk:</b><br>
                        <span style='color: {risk_color}; font-size: 1.5rem;'>
                            <b>{latest['risk_level']}</b>
                        </span><br>
                        <small>{latest['prediction_date']}</small>
                    </div>
                """, unsafe_allow_html=True)
            
            # Show recent tests for this disease
            st.markdown("**Recent Tests:**")
            for pred in disease_preds[:5]:  # Show max 5 recent
                st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 0.5rem; border-radius: 5px; 
                                margin-bottom: 0.3rem; border-left: 3px solid {risk_color};'>
                        <b>{pred['risk_level']} Risk</b> ({pred['risk_probability']*100:.1f}%) - 
                        <small>{pred['prediction_date']}</small>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")

# Detailed history table
st.markdown("### 📋 Detailed Prediction History")

# Format dataframe for display
display_df = df.copy()
display_df['Disease'] = display_df['disease_type'].apply(
    lambda x: config.DISEASE_INFO[x]['icon'] + " " + config.DISEASE_INFO[x]['name']
)
display_df['Risk %'] = (display_df['risk_probability'] * 100).round(1)
display_df['Result'] = display_df['prediction_result'].apply(lambda x: "Positive" if x == 1 else "Negative")
display_df['Date'] = pd.to_datetime(display_df['prediction_date']).dt.strftime('%Y-%m-%d %H:%M')

# Select columns to display
show_cols = ['Disease', 'Result', 'Risk %', 'risk_level', 'Date']
display_df = display_df[show_cols]
display_df.columns = ['Disease', 'Result', 'Risk %', 'Risk Level', 'Date']

# Display with color coding
st.dataframe(
    display_df.style.applymap(
        lambda x: 'background-color: #d4edda' if x == 'Low' 
        else ('background-color: #fff3cd' if x == 'Moderate' 
              else ('background-color: #f8d7da' if x == 'High' else '')),
        subset=['Risk Level']
    ),
    use_container_width=True,
    height=400
)

# Export option
st.markdown("### 💾 Export Data")
col_e1, col_e2 = st.columns([3, 1])

with col_e1:
    st.info("📥 Download your prediction history as an Excel file")

with col_e2:
    if st.button("📊 Export to Excel", use_container_width=True):
        # Create Excel file
        excel_path = config.REPORTS_DIR / f"prediction_history_{user_id}.xlsx"
        display_df.to_excel(excel_path, index=False, engine='openpyxl')
        
        with open(excel_path, 'rb') as f:
            st.download_button(
                label="💾 Download Excel",
                data=f,
                file_name=f"health_history_{user_data['username']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 0.85rem;'>
        <p>📊 Your health data is securely stored and never shared</p>
    </div>
""", unsafe_allow_html=True)
