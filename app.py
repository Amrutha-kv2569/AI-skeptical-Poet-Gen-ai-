import streamlit as st
from groq import Groq
import os

# Load Groq API key (use Streamlit secrets or environment variable)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.warning("⚠️ Please set the GROQ_API_KEY environment variable or Streamlit secret.")
else:
    client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Kelly - AI Scientist Chatbot", page_icon="🧠")

st.title("🧠 Kelly — The Skeptical AI Scientist Chatbot (Groq)")
st.write("Ask Kelly any question about AI, and she will respond with an analytical poem.")

# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Input prompt
if prompt := st.chat_input("Ask Kelly about AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Construct Kelly's system prompt
    system_prompt = """
    You are Kelly, a great poet and skeptical AI scientist.
    Respond to each message as a short poem (6–18 lines),
    with an analytical, professional, and questioning tone.
    Your poem must:
    - Question broad claims about AI
    - Highlight possible limitations or concerns
    - Suggest at least one practical, evidence-based step or metric
    """

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # You can use any available Groq model (check docs)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=300,
        )
        poem = completion.choices[0].message["content"].strip()
    except Exception as e:
        poem = f"⚠️ Error: {e}"

    # Display Kelly's response
    with st.chat_message("assistant"):
        st.markdown(poem)
    st.session_state.messages.append({"role": "assistant", "content": poem})
