import streamlit as st
from groq import Groq

st.title("Kelly - The Skeptical AI Scientist Poet 🤖✍️")
st.write("Ask anything about AI or Machine Learning — Kelly will answer only in poetic skepticism.")

# Load API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# User question box
question = st.text_input("Ask Kelly a question:")

if st.button("Ask Kelly") and question:
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are 'Kelly', an AI Scientist who always replies in a poem.
        Tone: skeptical, analytical, professional.
        Each answer must question assumptions about AI, mention limitations, and give evidence-based advice.
        Now answer this question in poetic form:
        {question}
        """

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        st.markdown(f"### 📌 Kelly's Reply\n\n{reply}")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
