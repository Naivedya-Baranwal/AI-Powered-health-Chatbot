import streamlit as st
#nltk for natural language processing task
import nltk
# pipeline used for importing pretrained transformers from hugging face
from transformers import pipeline
# it is for getting the important words
from nltk.corpus import stopwords
# for tokenizing the sentence into words
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

chatbot = pipeline("text-generation",model="distilgpt2")

def healthcare_chatbot(user_input):
    if "symptom" in user_input:
        return "Please consult a doctor for proper diagnosis and treatment."
    elif "appointment" in user_input:
        return "Please contact your healthcare provider to schedule an appointment."
    elif "medication" in user_input:
        return "Please consult a doctor for proper medication treatment."
    elif "fever" in user_input.lower():
        return "If you have a fever, rest, stay hydrated, and monitor your temperature. If it's above 103°F (39.4°C) or persists for more than 3 days, consult a doctor."
    elif "headache" in user_input.lower():
        return "For headaches, try rest, hydration, and over-the-counter pain relievers. If severe or persistent, seek medical attention."
    elif "cough" in user_input.lower():
        return "Stay hydrated, use honey for soothing, and rest. If cough persists for more than 2 weeks or is severe, see a doctor."
    elif "pain" in user_input.lower():
        return "Pain can have many causes. If it's severe, persistent, or accompanied by other symptoms, please seek medical attention immediately."
    elif "dizzy" in user_input.lower():
        return "If you're feeling dizzy, sit or lie down immediately. If it's severe or accompanied by other symptoms, seek medical help."
    elif "nausea" in user_input.lower():
        return "Try small sips of clear fluids and bland foods. If severe or persistent, consult a doctor."
    elif "fatigue" in user_input.lower():
        return "Ensure adequate sleep, nutrition, and hydration. If fatigue is severe or persistent, it could indicate an underlying condition."
    else:
        # For general queries, provide a more helpful response
        if any(word in user_input.lower() for word in ["how", "what", "why", "when", "where"]):
            return "I'm here to help with general health information. For specific medical advice, please consult a healthcare professional. How can I assist you today?"
        else:
            return "I'm your healthcare assistant. I can provide general health information, but for specific medical advice, please consult a healthcare professional. What would you like to know about?"

def main():
    st.title("Healthcare Assistant Chatbot")
    user_input=st.text_input("How can I assist you today?")
    print(user_input)
    if st.button("Submit"):
        if user_input:
            st.write("User :", user_input)
            with st.spinner("processing your query, Please wait..."):
                response=healthcare_chatbot(user_input)
            st.write("Healthcare Assistant : ",response)
        else :
            st.write("Please enter a message to get a response")
if __name__ == "__main__":
    main()
    