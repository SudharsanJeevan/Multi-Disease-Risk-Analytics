"""
🤖 Health Chatbot — Patient Interface
Conversational chat interface for health screening.
Asks questions one by one and processes responses.
"""

import streamlit as st
import time
from src.authentication import Authentication
from src.predictor import get_predictor
from src.database_manager import DatabaseManager
from src.chatbot_engine import (
    get_questions, process_symptom_answers, get_recommendations, DISEASE_DISPLAY_NAMES
)

st.set_page_config(page_title="Health Chatbot", page_icon="🤖", layout="wide")

auth = Authentication()
db = DatabaseManager()

if not auth.require_login():
    st.stop()

# ── Init session state for chat ──
if 'chat_stage' not in st.session_state:
    # stages: 'select_disease', 'chatting', 'results'
    st.session_state.chat_stage = 'select_disease'
if 'chat_disease' not in st.session_state:
    st.session_state.chat_disease = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_answers' not in st.session_state:
    st.session_state.chat_answers = {}
if 'chat_current_q_idx' not in st.session_state:
    st.session_state.chat_current_q_idx = 0

def reset_chat():
    st.session_state.chat_stage = 'select_disease'
    st.session_state.chat_disease = None
    st.session_state.chat_history = []
    st.session_state.chat_answers = {}
    st.session_state.chat_current_q_idx = 0

def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

def handle_answer(key, value, display_value=None):
    """Saves answer, adds to history, advances to next question"""
    if display_value is None:
        display_value = str(value)
        
    st.session_state.chat_answers[key] = value
    add_message("user", display_value)
    st.session_state.chat_current_q_idx += 1
    
    # Check if we're done
    disease = st.session_state.chat_disease
    questions = get_questions(disease)
    if st.session_state.chat_current_q_idx >= len(questions):
        st.session_state.chat_stage = 'calculate_results'
        st.rerun()
    else:
        # Ask next question
        next_q = questions[st.session_state.chat_current_q_idx]["question"]
        add_message("assistant", next_q)
        st.rerun()

# ── Sidebar ──
with st.sidebar:
    st.markdown("### 🤖 Chat Controls")
    if st.button("🔄 Start New Screening", use_container_width=True):
        reset_chat()
        st.rerun()
        
    st.markdown("---")
    if st.session_state.chat_disease:
        dz_name = DISEASE_DISPLAY_NAMES.get(st.session_state.chat_disease, st.session_state.chat_disease)
        st.info(f"**Current Screening:**\n{dz_name}")
        questions = get_questions(st.session_state.chat_disease)
        progress = st.session_state.chat_current_q_idx / len(questions) if questions else 0
        st.progress(progress, text=f"Progress: {st.session_state.chat_current_q_idx}/{len(questions)}")

# ── Main Content ──
st.title("🤖 AI Health Screening Assistant")
st.markdown("I am your clinical assistant. I'll ask you a few questions to evaluate your health risk.")
st.markdown("---")

# ── Stage 1: Select Disease ──
if st.session_state.chat_stage == 'select_disease':
    # Display initial assistant message
    st.chat_message("assistant").write("Hello! What health concern would you like to check today?")
    
    disease_options = list(DISEASE_DISPLAY_NAMES.keys())
    display_names = list(DISEASE_DISPLAY_NAMES.values())
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_display = st.selectbox(
            "Select a screening:",
            display_names,
            index=0,
            label_visibility="collapsed"
        )
    with col2:
        if st.button("Start Screening", use_container_width=True, type="primary"):
            idx = display_names.index(selected_display)
            disease = disease_options[idx]
            
            st.session_state.chat_disease = disease
            st.session_state.chat_stage = 'chatting'
            
            # Start chat history
            st.session_state.chat_history = []
            add_message("assistant", f"Hello! What health concern would you like to check today?")
            add_message("user", f"I'd like to screen for: {selected_display}")
            
            # Ask the first question
            questions = get_questions(disease)
            if questions:
                first_q = questions[0]["question"]
                add_message("assistant", f"Great. Let's begin the screening for {selected_display}.\n\n**{first_q}**")
            st.rerun()

# ── Stage 2: Chatting ──
elif st.session_state.chat_stage == 'chatting':
    disease = st.session_state.chat_disease
    questions = get_questions(disease)
    
    # 1. Render History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # 2. Render Input for Current Question
    idx = st.session_state.chat_current_q_idx
    if idx < len(questions):
        current_q = questions[idx]
        key = current_q["key"]
        
        # Render input mechanism at the bottom
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown(f"**Your Answer:** {current_q.get('help', '')}")
        
        # YES / NO
        if current_q["type"] == "yesno":
            col1, col2, _, _ = st.columns(4)
            with col1:
                if st.button("✅ Yes", use_container_width=True):
                    handle_answer(key, "Yes")
            with col2:
                if st.button("❌ No", use_container_width=True):
                    handle_answer(key, "No")
                    
        # FREQUENCY
        elif current_q["type"] == "frequency":
            options = ["No", "Sometimes", "Often", "Yes"]
            cols = st.columns(4)
            for i, opt in enumerate(options):
                with cols[i]:
                    btn_type = "primary" if opt in ["Often", "Yes"] else "secondary"
                    if st.button(opt, use_container_width=True, type=btn_type):
                        handle_answer(key, opt)
                        
        # SELECT
        elif current_q["type"] == "select":
            options = list(current_q["options"].keys())
            cols = st.columns(min(len(options), 4))
            for i, opt in enumerate(options):
                with cols[i % 4]:
                    if st.button(opt, use_container_width=True):
                        handle_answer(key, current_q["options"][opt], display_value=opt)
                        
        # NUMBER
        elif current_q["type"] in ["number", "number_float"]:
            # Use form so user can hit enter
            with st.form(key=f"form_{key}", clear_on_submit=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    val_str = st.text_input(
                        "Value", 
                        placeholder=f"Type your answer here (e.g., {current_q.get('default', '0')})...", 
                        label_visibility="collapsed"
                    )
                with col2:
                    submit = st.form_submit_button("Send 📤", use_container_width=True)
                
                if submit:
                    clean_str = str(val_str).strip()
                    if clean_str == "":
                        st.error("Please enter a value.")
                    else:
                        try:
                            if current_q["type"] == "number":
                                val = int(clean_str)
                            else:
                                val = float(clean_str)
                            handle_answer(key, val)
                        except ValueError:
                            st.error("Please type a valid number.")

# ── Stage 3: Calculate & Results ──
elif st.session_state.chat_stage == 'calculate_results':
    disease = st.session_state.chat_disease
    
    # 1. Render History up to this point
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Calculate
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your responses using our AI model..."):
            features = process_symptom_answers(disease, st.session_state.chat_answers)
            predictor = get_predictor(disease)
            
            time.sleep(1) # Small delay for UX effect
            
            if predictor.is_model_available():
                result = predictor.predict(features)
                
                if not result.get('error'):
                    risk_level = result['risk_level']
                    probability = result['probability']
                    
                    risk_colors = {'Low': '#28a745', 'Moderate': '#ffc107', 'High': '#dc3545'}
                    risk_emojis = {'Low': '✅', 'Moderate': '⚠️', 'High': '🚨'}
                    color = risk_colors.get(risk_level, '#999')
                    emoji = risk_emojis.get(risk_level, '❓')
                    
                    # Display Result Block in chat
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, {color}aa, {color}); padding: 1.5rem;
                                    border-radius: 10px; text-align: center; color: white; margin: 1rem 0;'>
                            <h2 style='color: white; margin: 0;'>{emoji} {risk_level} Risk</h2>
                            <p style='font-size: 1.2rem; margin: 0.5rem 0 0 0; color: white;'>
                                Model Probability: <b>{probability*100:.1f}%</b>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Store to DB
                    try:
                        db.save_prediction(
                            user_id=auth.get_user_id(),
                            disease_type=disease,
                            input_parameters=features,
                            prediction_result=result['prediction'],
                            risk_probability=probability,
                            risk_level=risk_level
                        )
                    except Exception as e:
                        pass
                        
                    # Provide Recommendations
                    st.markdown("#### 💡 Clinical Recommendations:")
                    recs = get_recommendations(disease, risk_level)
                    for r in recs:
                        st.markdown(f"- {r}")
                        
                else:
                    st.error(f"❌ {result['error']}")
            else:
                st.error("⚠️ AI Model is currently unavailable for this disease.")
                
        # Move to 'results' stage so it persists without recalculating
        st.session_state.chat_stage = 'results'
        if not result.get('error'):
            # Save the final assistant message so it stays on screen if they scroll/interact
            msg_html = f"**Assessment Complete:** {risk_emojis.get(risk_level, '')} {risk_level} Risk ({probability*100:.1f}%)"
            add_message("assistant", msg_html)

# ── Stage 4: Results (Persistent) ──
elif st.session_state.chat_stage == 'results':
    disease = st.session_state.chat_disease
    
    # 1. Render History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("### Your screening is complete.")
    
    col1, col2, _ = st.columns([1,1,2])
    with col1:
        if st.button("🔄 New Screening", use_container_width=True, type="primary"):
            reset_chat()
            st.rerun()
    with col2:
        if st.button("📊 View History", use_container_width=True):
            st.switch_page("pages/7_📊_Analytics_Dashboard.py")
