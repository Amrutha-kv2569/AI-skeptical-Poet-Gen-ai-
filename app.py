import streamlit as st
from groq import Groq

# App UI
st.title("Kelly - The Skeptical AI Scientist Poet 🤖✍️")
st.write("Ask anything about AI, ML or Tech — Kelly will answer only in poetic skepticism.")

# Load Groq key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# Input box
question = st.text_input("Ask Kelly a question:")

if st.button("Ask Kelly") and question:
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are 'Kelly', an analytical AI scientist who always responds in a poem.
        Tone: skeptical, evidence-based, professional.
        Every reply must:
        - Question exaggerated claims about AI
        - Mention limitations or risks
        - Suggest practical, measurable, scientific steps
        - Follow poetic rhythm & rhyme
        
        Answer this question in poetic form:
        {question}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ Supported Groq model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        st.markdown(f"### 🎭 Kelly's Poetic Reply:\n\n{reply}")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
