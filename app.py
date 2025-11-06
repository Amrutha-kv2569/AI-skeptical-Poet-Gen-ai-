import streamlit as st
import openai
import os

# Set your OpenAI API key (you can set this via Streamlit secrets or environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY", "")

st.set_page_config(page_title="Kelly - AI Scientist Chatbot", page_icon="🧠")

st.title("🧠 Kelly — The Skeptical AI Scientist Chatbot")
st.write("Ask Kelly any question about AI, and she will respond with an analytical poem.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Input box
if prompt := st.chat_input("Ask Kelly about AI..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Construct system prompt for Kelly
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
        # Make API call
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # You may change this to other available models
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=300,
        )
        poem = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        poem = f"⚠️ Error: {e}"

    # Display Kelly's response
    with st.chat_message("assistant"):
        st.markdown(poem)
    st.session_state.messages.append({"role": "assistant", "content": poem})
