import streamlit as st
from chatbot import get_response, initialize_chat, process_medical_report
from PIL import Image
import PyPDF2
import io

# Page setup
st.set_page_config(page_title="Virtual Doctor", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@700&display=swap');

        body {
            background-color: #f8fbff;
        }

        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 30px;
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .logo {
            height: 60px;
        }

        .title {
            flex: 1;
            text-align: center;
            font-family: 'Ubuntu', sans-serif;
            font-size: 40px;
            background: linear-gradient(90deg, #007bff, #7f00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-right: 60px;
            animation: fadeIn 2s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .chat-bubble {
            border-radius: 10px;
            padding: 10px 15px;
            margin: 10px 0;
            max-width: 90%;
            word-wrap: break-word;
            position: relative;
        }

        .user-bubble {
            background-color: #444;
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }

        .bot-bubble {
            background-color: #e8f0ff;
            color: #111;
            align-self: flex-start;
            margin-right: auto;
        }

        .chat-input {
            margin-top: 1.5rem;
        }

        .stTextInput > label {
            display: none;
        }

        .sidebar .stFileUploader {
            padding: 10px;
        }

        .sidebar .stFileUploader > div > div {
            background-color: #e8f0ff;
            border-radius: 8px;
            padding: 10px;
        }

        .sidebar .stFileUploader label {
            font-family: 'Ubuntu', sans-serif;
            font-size: 16px;
            color: #333;
        }

    </style>
""", unsafe_allow_html=True)

# Sidebar for file upload
with st.sidebar:
    st.markdown("### Upload Medical Report")
    uploaded_file = st.file_uploader("Choose a PDF or text file", type=["pdf", "txt"])

# Header with logo and title
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    logo = Image.open("logo.png")
    st.image(logo, width=80)

with col2:
    st.markdown('<div class="title">Virtual Doctor – Your AI Health Companion</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat history session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.report_processed = False
    # Initialize chat with an opening question if no report is uploaded
    if not uploaded_file:
        initial_message = initialize_chat()
        st.session_state.messages.append({"role": "bot", "content": initial_message})

# Process uploaded medical report
if uploaded_file and not st.session_state.get("report_processed", False):
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        else:  # Text file
            text = uploaded_file.read().decode("utf-8")
        
        # Get diagnosis and summary from the report
        report_response = process_medical_report(text)
        st.session_state.messages.append({"role": "bot", "content": report_response})
        st.session_state.report_processed = True
        st.rerun()
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

# Display previous messages
with st.container():
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        role_class = "user-bubble" if role == "user" else "bot-bubble"
        st.markdown(f'<div class="chat-bubble {role_class}">{content}</div>', unsafe_allow_html=True)

# User input form
with st.form(key="chat_form", clear_on_submit=True):
    st.markdown('<div class="chat-input">', unsafe_allow_html=True)
    user_input = st.text_input("", key="user_input", placeholder="Type your response or symptoms here...")
    submit = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle user input and bot response
if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = get_response(user_input, st.session_state.messages)
    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.rerun()