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
    else:
        response = chatbot(user_input,max_length=500,num_return_sequences=1)
        
    return response[0]['generated_text']

def main():
    st.title("Healthcare Assistant Chatbot")
    user_input=st.text_input("How can I assist you today?")
    print(user_input)
    if st.button("Submit"):
        if user_input:
            st.write("User :", user_input)
            with st.spinner("processing your query, Please wait..."):
                response=healthcare_chatbot(user_input)
            healthcare_chatbot(user_input)
            st.write("Healthcare Assistant : ",response)
        else :
            st.write("Please enter a message to get a response")
if __name__ == "__main__":
    main()
    