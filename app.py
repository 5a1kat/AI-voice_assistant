import streamlit as st
from google import genai
from google.genai import types # Add this import

# Initialize Gemini with the 'v1' API version
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(api_version='v1') # This line fixes the 404 error
)


st.title("🤖 Gemini AI Voice Assistant")
st.write(f"Key loaded: {st.secrets['GEMINI_API_KEY'][:5]}...")

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
