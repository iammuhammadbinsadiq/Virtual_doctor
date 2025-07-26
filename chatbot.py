# chatbot.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Start persistent Gemini Flash chat session
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

# State to track conversation phase
if "chat_state" not in globals():
    chat_state = {
        "phase": "symptom_collection",
        "symptoms": [],
        "question_count": 0,
        "medical_history": [],
        "lifestyle_factors": []
    }

# List of targeted follow-up questions to mimic a real doctor
FOLLOW_UP_QUESTIONS = [
    "How long have you been experiencing these symptoms?",
    "Can you describe the severity of your symptoms (mild, moderate, or severe)?",
    "Have you noticed any triggers, such as specific foods, activities, or environments?",
    "Are you experiencing any associated symptoms, like nausea, dizziness, or fatigue?",
    "Do you have any existing medical conditions, such as diabetes or hypertension?",
    "Have you taken any medications or treatments for these symptoms?",
    "Do you have a history of allergies or reactions to medications?",
    "Are you experiencing any changes in appetite, sleep, or energy levels?",
    "Have you had any recent injuries or infections that might be related?",
    "Can you tell me about your lifestyle, such as stress levels, diet, or exercise habits?"
]

def initialize_chat():
    """Initialize the chat with an opening question."""
    global chat_state
    chat_state["phase"] = "symptom_collection"
    chat_state["symptoms"] = []
    chat_state["question_count"] = 0
    chat_state["medical_history"] = []
    chat_state["lifestyle_factors"] = []
    return "Hello! I'm your Virtual Doctor. To assist you better, please tell me about any symptoms you're experiencing, such as fever, cough, or pain."

def process_medical_report(report_text):
    """Process a medical report to provide a summary and diagnosis."""
    try:
        prompt = f"""
        You are an AI doctor. You have received the following medical report:
        {report_text}

        Provide a concise summary of the report and a possible diagnosis based on the information provided. 
        Suggest appropriate treatment or medicine. If the report lacks sufficient information, suggest possible conditions and recommend further tests.
        Include a disclaimer that this is not a substitute for professional medical advice.
        Format the response as:
        **Report Summary**: [Summary of key findings]
        **Possible Diagnosis**: [Diagnosis or possible conditions]
        **Suggested Treatment**: [Treatment/Medicine or recommendations]
        **Disclaimer**: This is an AI-generated response and not a substitute for professional medical advice. Please consult a doctor for an accurate diagnosis and treatment plan.
        """
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error processing medical report: {str(e)}"

def get_response(user_input, messages):
    """Handle user input, manage conversation state, and generate bot response."""
    global chat_state
    try:
        if chat_state["phase"] == "symptom_collection":
            # Store user input based on question context
            if chat_state["question_count"] == 0:
                chat_state["symptoms"].append(user_input)
            elif chat_state["question_count"] in [1, 2, 3]:
                if "medical condition" in FOLLOW_UP_QUESTIONS[chat_state["question_count"] - 1].lower() or \
                   "allergies" in FOLLOW_UP_QUESTIONS[chat_state["question_count"] - 1].lower():
                    chat_state["medical_history"].append(user_input)
                elif "lifestyle" in FOLLOW_UP_QUESTIONS[chat_state["question_count"] - 1].lower():
                    chat_state["lifestyle_factors"].append(user_input)
                else:
                    chat_state["symptoms"].append(user_input)
            chat_state["question_count"] += 1

            # Ask follow-up questions up to 4 times
            if chat_state["question_count"] < 4:
                # Select a random follow-up question, avoiding repetition
                available_questions = [q for q in FOLLOW_UP_QUESTIONS if q not in messages[-2]["content"] if len(messages) >= 2]
                next_question = random.choice(available_questions) if available_questions else FOLLOW_UP_QUESTIONS[0]
                return f"Thank you for sharing. {next_question}"
            else:
                # Move to diagnosis phase
                chat_state["phase"] = "diagnosis"
                prompt = f"""
                You are an AI doctor. Based on the following information:
                - **Symptoms**: {', '.join(chat_state["symptoms"])}
                - **Medical History**: {', '.join(chat_state["medical_history"]) if chat_state["medical_history"] else "None reported"}
                - **Lifestyle Factors**: {', '.join(chat_state["lifestyle_factors"]) if chat_state["lifestyle_factors"] else "None reported"}
                Provide a possible diagnosis and suggest appropriate treatment or medicine. 
                Ensure the diagnosis considers the symptoms, medical history, and lifestyle factors. 
                If the information is insufficient, suggest possible conditions and recommend consulting a doctor for further tests.
                Include a disclaimer that this is not a substitute for professional medical advice.
                Format the response as:
                **Possible Diagnosis**: [Diagnosis or possible conditions]
                **Suggested Treatment**: [Treatment/Medicine or recommendations]
                **Disclaimer**: This is an AI-generated response and not a substitute for professional medical advice. Please consult a doctor for an accurate diagnosis and treatment plan.
                """
                response = chat.send_message(prompt)
                chat_state["phase"] = "complete"
                return response.text.strip()
        
        elif chat_state["phase"] == "diagnosis":
            # If in diagnosis phase but more input comes, update symptoms and provide diagnosis
            chat_state["symptoms"].append(user_input)
            prompt = f"""
            You are an AI doctor. Based on the following information:
            - **Symptoms**: {', '.join(chat_state["symptoms"])}
            - **Medical History**: {', '.join(chat_state["medical_history"]) if chat_state["medical_history"] else "None reported"}
            - **Lifestyle Factors**: {', '.join(chat_state["lifestyle_factors"]) if chat_state["lifestyle_factors"] else "None reported"}
            Provide a possible diagnosis and suggest appropriate treatment or medicine. 
            Ensure the diagnosis considers the symptoms, medical history, and lifestyle factors. 
            If the information is insufficient, suggest possible conditions and recommend consulting a doctor for further tests.
            Include a disclaimer that this is not a substitute for professional medical advice.
            Format the response as:
            **Possible Diagnosis**: [Diagnosis or possible conditions]
            **Suggested Treatment**: [Treatment/Medicine or recommendations]
            **Disclaimer**: This is an AI-generated response and not a substitute for professional medical advice. Please consult a doctor for an accurate diagnosis and treatment plan.
            """
            chat_state["phase"] = "complete"
            response = chat.send_message(prompt)
            return response.text.strip()
        
        else:
            # After diagnosis, continue normal chat
            response = chat.send_message(user_input)
            return response.text.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"