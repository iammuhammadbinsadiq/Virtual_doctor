# Virtual Doctor – AI Health Companion

Welcome to **Virtual Doctor**, an AI-powered Streamlit chatbot designed to assist users by analyzing medical reports or symptoms to provide possible diagnoses and treatment suggestions. Built with the Google Gemini API, this app mimics a doctor’s consultation process, offering a user-friendly interface with a sidebar for report uploads and a chat-based symptom input system.

**Note**: This is a prototype for educational and hackathon purposes. It is not a certified medical tool. Always consult a healthcare professional for accurate diagnoses and treatments.

## Features
- **Medical Report Analysis**: Upload PDF or text medical reports via the sidebar to receive a summary, possible diagnosis, and treatment suggestions.
- **Symptom-Based Diagnosis**: Enter symptoms in the chat interface, answer up to four doctor-like follow-up questions, and get a diagnosis based on symptoms, medical history, and lifestyle factors.
- **User-Friendly Interface**: Responsive Streamlit app with a fixed sidebar for file uploads, a chat history display, and a text input form for symptom entry.
- **Secure API Integration**: Uses the Google Gemini API (`gemini-1.5-flash`) with secure key management via environment variables or secrets.
- **Disclaimer**: Includes a clear disclaimer in all responses to emphasize that AI-generated advice is not a substitute for professional medical care.
