import streamlit as st
from groq import Groq
import os

# Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.warning("⚠️ Please set the GROQ_API_KEY environment variable or Streamlit secret.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Page configuration
st.set_page_config(
    page_title="Kelly - AI Scientist Poet",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS for better poetry display
st.markdown("""
<style>
    .poem-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        font-family: 'Georgia', serif;
        line-height: 1.8;
        margin: 10px 0;
    }
    .stChatMessage {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🧠 Kelly — The Skeptical AI Scientist Poet")
st.markdown("*Ask Kelly any question about AI, and she will respond with an analytical, skeptical poem.*")
st.divider()

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        if role == "assistant":
            st.markdown(f'<div class="poem-container">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(content)

# Chat input
if prompt := st.chat_input("Ask Kelly about AI..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enhanced system prompt for better poetic output
    system_prompt = """You are Kelly, a renowned poet and skeptical AI scientist. You MUST respond to EVERY question exclusively in poem form.

CRITICAL RULES:
1. ALWAYS write in verse with clear line breaks
2. Use rhyme schemes (ABAB, AABB, or ABCB patterns)
3. Maintain rhythm and meter throughout
4. Each response must be 8-16 lines
5. Be skeptical and analytical in your poetic observations
6. Question AI hype and broad claims
7. Highlight limitations and uncertainties
8. Suggest practical, evidence-based approaches
9. Use metaphors and poetic devices
10. NEVER write prose - only poetry

Structure your poems with:
- An opening that questions the premise
- A middle that explores limitations
- A closing that offers measured wisdom

Example style:
"You ask if AI can truly understand,
But what is comprehension, I demand?
A pattern matched, statistics aligned—
Or something more, within the mind?"

Remember: You are a POET first, scientist second. Every word must serve the verse."""

    try:
        # Create completion with adjusted parameters for more creative output
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                *[{"role": m["role"], "content": m["content"]} 
                  for m in st.session_state.messages[-6:]],  # Include context
            ],
            temperature=0.7,  # Increased for more creative output
            max_tokens=400,
            top_p=0.9,
        )
        
        poem = completion.choices[0].message.content.strip()
        
        # Ensure line breaks are preserved
        poem = poem.replace("\\n", "\n")
        
    except Exception as e:
        poem = f"⚠️ An error occurred: {str(e)}\n\nPlease check your API key and try again."

    # Display Kelly's poetic response
    with st.chat_message("assistant"):
        st.markdown(f'<div class="poem-container">{poem}</div>', unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": poem})

# Sidebar with information
with st.sidebar:
    st.header("About Kelly")
    st.write("""
    Kelly is an AI scientist who responds to all questions about artificial intelligence 
    in the form of analytical, skeptical poetry.
    
    **Her characteristics:**
    - 📝 Always responds in verse
    - 🤔 Questions AI hype and bold claims
    - 🔬 Highlights limitations and uncertainties
    - 💡 Offers evidence-based suggestions
    - 🎭 Uses metaphor and poetic devices
    """)
    
    st.divider()
    
    st.header("Tips")
    st.write("""
    - Ask about AI capabilities
    - Question AGI timelines
    - Explore AI limitations
    - Discuss AI ethics
    - Challenge AI narratives
    """)
    
    st.divider()
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Powered by Groq API | Model: Llama 3.1 8B")
