import streamlit as st
from transformers import pipeline

# Load a local sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Define a list of questions to ask the user
QUESTIONS = [
    "How have you been feeling lately?",
    "Have you been experiencing any stress or anxiety?",
    "Do you feel lonely or isolated?",
    "How is your sleep quality?",
    "Have you lost interest in activities you used to enjoy?",
    "Do you have thoughts of self-harm or suicide?",
]

# Function to analyze the user's responses using a local model
def analyze_responses(responses):
    # Combine all responses into a single prompt
    prompt = "The user has provided the following responses to mental health questions:\n"
    for i, response in enumerate(responses):
        prompt += f"Q: {QUESTIONS[i]}\nA: {response}\n\n"

    # Analyze the sentiment of the combined responses
    try:
        result = sentiment_analyzer(prompt)[0]
        sentiment = result['label']
        score = result['score']

        # Provide a basic analysis based on sentiment
        if sentiment == "NEGATIVE" and score > 0.8:
            analysis = (
                "Based on your responses, it seems like you're experiencing significant distress. "
                "Please consider reaching out to a mental health professional for support."
            )
        elif sentiment == "NEGATIVE":
            analysis = (
                "Your responses suggest you're feeling down or stressed. "
                "Try mindfulness exercises or journaling to help manage your feelings."
            )
        else:
            analysis = (
                "Your responses seem positive. Keep practicing self-care and reach out if you need support."
            )
    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")
        analysis = "Sorry, something went wrong while analyzing your response. Please try again."

    return analysis

# Streamlit app
st.title("Mental Health Chatbot")
st.write("Welcome to MentaLyze! This is a mental health chatbot that provides a report about your emotional standing.")

# Chat input
user_message = st.text_input("How are you feeling today?", "")

if st.button("Send"):
    if user_message:
        responses = [user_message]
        analysis = analyze_responses(responses)
        st.write("Bot:", analysis)
    else:
        st.warning("Please enter a message.")

# Emergency button
if st.button("🚨 Emergency Alert"):
    st.warning("Emergency alert triggered! Please contact a trusted person or helpline.")