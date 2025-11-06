import streamlit as st
from groq import Groq
import os

# Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error("⚠️ Please set the GROQ_API_KEY in Streamlit secrets or environment variable.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Page config
st.set_page_config(page_title="Kelly - AI Poet", page_icon="🧠", layout="wide")

# Title
st.title("🧠 Kelly — The Skeptical AI Scientist Poet")
st.markdown("*Ask any question about AI, and Kelly responds in analytical poetry*")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Two columns layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat with Kelly")
    
    # Chat container
    chat_container = st.container(height=500)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask Kelly about AI..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # System prompt
        system_prompt = """You are Kelly, a renowned poet and skeptical AI scientist. 

CRITICAL: Respond ONLY in poetry format with these rules:
- Write 8-16 lines of verse
- Use rhyme schemes (ABAB or AABB)
- Include line breaks between verses
- Be skeptical about AI claims
- Question limitations and hype
- Offer evidence-based insights
- Use poetic language and metaphors

Example format:
You ask if AI can think and feel,
But patterns matched don't make thoughts real.
Statistics learned from human text—
Is consciousness truly what comes next?"""

        try:
            # Get response
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400,
            )
            
            poem = completion.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": poem})
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()

with col2:
    st.subheader("📊 Dashboard")
    
    # Stats
    st.metric("Total Messages", len(st.session_state.messages))
    st.metric("Questions Asked", len([m for m in st.session_state.messages if m["role"] == "user"]))
    st.metric("Poems Written", len([m for m in st.session_state.messages if m["role"] == "assistant"]))
    
    st.divider()
    
    # About Kelly
    with st.expander("ℹ️ About Kelly", expanded=True):
        st.write("""
        Kelly is an AI scientist who responds in skeptical, analytical poetry.
        
        **Characteristics:**
        - 📝 Always writes in verse
        - 🤔 Questions AI hype
        - 🔬 Highlights limitations
        - 💡 Evidence-based insights
        """)
    
    # Example questions
    with st.expander("💡 Example Questions"):
        st.write("""
        - Can AI become conscious?
        - Will AGI arrive by 2030?
        - Can AI replace programmers?
        - Is AI truly intelligent?
        - Can AI understand emotions?
        """)
    
    st.divider()
    
    # Clear button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Model info
    st.caption("🤖 Model: Llama 3.1 8B (Groq)")
    st.caption("🚀 Powered by Streamlit")
