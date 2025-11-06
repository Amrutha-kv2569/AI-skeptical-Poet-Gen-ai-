import streamlit as st
from groq import Groq

# Streamlit App Title
st.title("Kelly - The Skeptical AI Scientist Poet 🤖✍️")
st.write("Ask me anything about AI, Machine Learning or Tech — and I'll reply in poetic skepticism! 🎭")

# Input for Groq API Key
api_key = st.text_input("Enter your Groq API Key", type="password")

# User Prompt Input
question = st.text_input("Ask Kelly a question:")

if st.button("Ask Kelly") and question and api_key:
    try:
        client = Groq(api_key=api_key)

        # Prepare Kelly's poetic, skeptical prompt
        prompt = f"""
        You are 'Kelly', an AI Scientist Chatbot who always responds in the form of a poem.
        Respond to this question in a skeptical, analytical and professional poetic tone.
        Question: {question}
        """

        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Updated model name
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )

        # Access and display Kelly's poetic reply
        reply = response.choices[0].message.content
        st.markdown(f"**Kelly's Reply:**\n\n{reply}")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
elif not api_key:
    st.warning("Please enter your Groq API key to continue.")
