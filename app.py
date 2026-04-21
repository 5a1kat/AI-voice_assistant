import streamlit as st
from google import genai
from config import apikey

# Initialize Gemini
client = genai.Client(api_key=apikey)

st.title("🤖 Gemini AI Voice Assistant")

# Use Streamlit's chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
