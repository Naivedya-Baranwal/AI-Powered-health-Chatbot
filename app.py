import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
import re

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def analyze_context(user_input, chat_history):
    """Analyze the context of the conversation to provide more intelligent responses"""
    user_input_lower = user_input.lower()
    
    # Extract key information from user input
    symptoms = []
    if "fever" in user_input_lower:
        symptoms.append("fever")
    if "headache" in user_input_lower:
        symptoms.append("headache")
    if "cough" in user_input_lower:
        symptoms.append("cough")
    if "pain" in user_input_lower:
        symptoms.append("pain")
    if "dizzy" in user_input_lower:
        symptoms.append("dizziness")
    if "nausea" in user_input_lower:
        symptoms.append("nausea")
    if "fatigue" in user_input_lower:
        symptoms.append("fatigue")
    if "malaria" in user_input_lower:
        symptoms.append("malaria")
    
    # Check for urgency indicators
    urgency_words = ["emergency", "severe", "bad", "worse", "terrible", "awful", "critical"]
    is_urgent = any(word in user_input_lower for word in urgency_words)
    
    # Check for time indicators
    time_patterns = {
        "days": re.findall(r'(\d+)\s*days?', user_input_lower),
        "hours": re.findall(r'(\d+)\s*hours?', user_input_lower),
        "weeks": re.findall(r'(\d+)\s*weeks?', user_input_lower)
    }
    
    # Check for severity indicators
    severity_words = ["high", "low", "mild", "severe", "extreme"]
    severity = next((word for word in severity_words if word in user_input_lower), "moderate")
    
    return {
        "symptoms": symptoms,
        "is_urgent": is_urgent,
        "time_patterns": time_patterns,
        "severity": severity,
        "has_medication": any(word in user_input_lower for word in ["medicine", "medication", "pill", "drug", "took", "taking"]),
        "has_doctor": any(word in user_input_lower for word in ["doctor", "hospital", "clinic", "medical"])
    }

def generate_intelligent_response(user_input, context):
    """Generate intelligent, contextual responses based on analysis"""
    user_input_lower = user_input.lower()
    
    # Base response templates
    responses = {
        "fever": {
            "urgent": "Your fever sounds serious. Given the severity and duration, you should seek immediate medical attention. High fever can be dangerous.",
            "moderate": "Your fever needs attention. Rest, stay hydrated, and monitor your temperature. If it persists or worsens, see a doctor.",
            "mild": "For mild fever, rest and hydration are key. Monitor your symptoms and seek medical care if they worsen."
        },
        "malaria": {
            "urgent": "Malaria is a medical emergency. If you suspect malaria, especially with fever and other symptoms, seek immediate medical care.",
            "moderate": "Malaria requires prompt medical treatment. Don't delay - contact a healthcare provider immediately.",
            "mild": "Even mild malaria symptoms need medical evaluation. Please consult a doctor for proper diagnosis and treatment."
        },
        "general_health": {
            "urgent": "Your symptoms sound concerning. Please seek immediate medical attention for proper evaluation.",
            "moderate": "Your health concern should be evaluated by a healthcare professional. Don't hesitate to seek medical advice.",
            "mild": "While your symptoms may be mild, it's always good to consult a healthcare provider for proper guidance."
        }
    }
    
    # Generate contextual response
    if context["symptoms"]:
        primary_symptom = context["symptoms"][0]
        urgency_level = "urgent" if context["is_urgent"] else context["severity"]
        
        if primary_symptom == "fever":
            base_response = responses["fever"][urgency_level]
        elif primary_symptom == "malaria":
            base_response = responses["malaria"][urgency_level]
        else:
            base_response = responses["general_health"][urgency_level]
        
        # Add contextual details
        if context["time_patterns"]["days"]:
            days = context["time_patterns"]["days"][0]
            base_response += f" The fact that this has been going on for {days} days is concerning."
        
        if context["has_medication"]:
            base_response += " Since you've been taking medication, it's important to discuss this with your doctor."
        
        if context["has_doctor"]:
            base_response += " Good that you're considering medical care - that's the right approach."
        
        return base_response
    
    # For general queries, provide intelligent responses
    if "what is" in user_input_lower or "tell me about" in user_input_lower:
        if "malaria" in user_input_lower:
            return "Malaria is a serious parasitic disease transmitted by mosquitoes. It causes fever, chills, headache, and muscle pain. Early diagnosis and treatment are crucial for recovery."
        elif "fever" in user_input_lower:
            return "Fever is your body's natural response to infection or illness. It helps fight off pathogens, but high or persistent fever requires medical attention."
        else:
            return "I can provide general health information, but for specific medical conditions, it's best to consult a healthcare professional for accurate diagnosis and treatment."
    
    elif "how to" in user_input_lower or "cure" in user_input_lower or "treat" in user_input_lower:
        if "malaria" in user_input_lower:
            return "Malaria treatment requires prescription medications like artemisinin-based combination therapy (ACT). Self-treatment is not recommended - seek immediate medical care."
        elif "fever" in user_input_lower:
            return "For fever: rest, stay hydrated, use acetaminophen or ibuprofen, and monitor temperature. Seek medical care if fever is high (>103°F) or persistent (>3 days)."
        else:
            return "Treatment approaches vary by condition and individual factors. A healthcare provider can recommend the most appropriate treatment plan for your specific situation."
    
    else:
        return "I understand your health concern. While I can provide general information, specific medical advice should come from a healthcare professional who can evaluate your individual situation."

def generate_ai_response(user_input, chat_history=None):
    """Generate intelligent AI responses based on context analysis"""
    if chat_history is None:
        chat_history = []
    
    # Analyze the context of the conversation
    context = analyze_context(user_input, chat_history)
    
    # Generate intelligent response
    intelligent_response = generate_intelligent_response(user_input, context)
    
    # Add some variation and personality
    variations = [
        f"🤔 Based on what you've described, {intelligent_response.lower()}",
        f"💭 Let me think about this... {intelligent_response}",
        f"📋 Here's what I understand: {intelligent_response}",
        f"🔍 Analyzing your symptoms: {intelligent_response}",
        f"💡 My assessment: {intelligent_response}"
    ]
    
    return random.choice(variations)

def healthcare_chatbot(user_input):
    user_input_lower = user_input.lower()
    rule_response = ""
    
    # Medical rule-based responses for immediate safety
    if "symptom" in user_input_lower:
        rule_response = "Please consult a doctor for proper diagnosis and treatment."
    elif "appointment" in user_input_lower:
        rule_response = "Please contact your healthcare provider to schedule an appointment."
    elif "medication" in user_input_lower:
        rule_response = "Please consult a doctor for proper medication treatment."
    elif "fever" in user_input_lower:
        rule_response = "If you have a fever, rest, stay hydrated, and monitor your temperature. If it's above 103°F (39.4°C) or persists for more than 3 days, consult a doctor. For persistent fever, especially with other symptoms, seek immediate medical attention."
    elif "headache" in user_input_lower:
        rule_response = "For headaches, try rest, hydration, and over-the-counter pain relievers. If severe or persistent, seek medical attention."
    elif "cough" in user_input_lower:
        rule_response = "Stay hydrated, use honey for soothing, and rest. If cough persists for more than 2 weeks or is severe, see a doctor."
    elif "pain" in user_input_lower:
        rule_response = "Pain can have many causes. If it's severe, persistent, or accompanied by other symptoms, please seek medical attention immediately."
    elif "dizzy" in user_input_lower:
        rule_response = "If you're feeling dizzy, sit or lie down immediately. If it's severe or accompanied by other symptoms, seek medical help."
    elif "nausea" in user_input_lower:
        rule_response = "Try small sips of clear fluids and bland foods. If severe or persistent, consult a doctor."
    elif "fatigue" in user_input_lower:
        rule_response = "Ensure adequate sleep, nutrition, and hydration. If fatigue is severe or persistent, it could indicate an underlying condition."
    elif "malaria" in user_input_lower:
        rule_response = "Malaria is a serious disease requiring immediate medical treatment. Symptoms include fever, chills, headache, and muscle pain. Seek emergency medical care if you suspect malaria."
    
    # Generate intelligent AI response
    ai_response = generate_ai_response(user_input)
    
    # Combine rule-based and AI responses
    if rule_response:
        return f"🏥 **Medical Advice:**\n{rule_response}\n\n🤖 **AI Analysis:**\n{ai_response}"
    else:
        return f"🤖 **AI Analysis:**\n{ai_response}"

def main():
    st.title("🏥 Healthcare Assistant Chatbot")
    st.markdown("---")
    
    # Add some styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How can I assist you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your query..."):
                response = healthcare_chatbot(prompt)
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About This Assistant")
        st.markdown("""
        This healthcare assistant provides:
        - **Medical Advice**: Rule-based responses for common health issues
        - **AI Analysis**: Intelligent, contextual responses
        - **Context Awareness**: Understands conversation flow
        - **Safety First**: Always recommends consulting healthcare professionals
        
        **Important**: This is not a substitute for professional medical advice.
        """)
        
        st.header("🚨 Emergency")
        st.markdown("""
        If you're experiencing a medical emergency, call emergency services immediately.
        
        **Emergency Numbers:**
        - US: 911
        - UK: 999
        - EU: 112
        """)

if __name__ == "__main__":
    main()
 