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
    page_icon="🧬",
    layout="centered"
)

# Custom CSS for poetry display
st.markdown("""
<style>
    .poem-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        font-family: 'Georgia', 'Garamond', serif;
        font-size: 16px;
        line-height: 2;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        white-space: pre-line;
    }
    .poem-title {
        font-style: italic;
        color: #ffd700;
        margin-bottom: 15px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🧬 Kelly — The Skeptical AI Scientist Poet")
st.markdown("*Every answer is a skeptical, analytical poem questioning AI claims*")
st.divider()

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        if role == "assistant":
            st.markdown(f'<div class="poem-box"><div class="poem-title">~ Kelly\'s Poetic Response ~</div>{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(content)

# Chat input
if prompt := st.chat_input("Ask Kelly about AI..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # SUPER STRICT system prompt - forces poem format
    system_prompt = f"""You are Kelly, the great poet and skeptical AI scientist. You MUST respond ONLY in the form of a POEM.

YOUR IDENTITY:
- You are a POET who happens to study AI
- You NEVER write prose, explanations, or paragraphs
- EVERY response is a complete poem with verses
- You are skeptical, analytical, and evidence-based

MANDATORY POEM STRUCTURE:
You MUST write a poem with exactly 12-16 lines, following this format:

Verse 1 (4 lines): Question the claim or premise
Verse 2 (4 lines): Analyze limitations and concerns  
Verse 3 (4-8 lines): Offer practical wisdom and suggestions

REQUIRED POETIC ELEMENTS:
✓ Clear rhyme scheme (AABB or ABAB or ABCB)
✓ Consistent rhythm and meter
✓ Line breaks after every sentence or clause
✓ Metaphors and poetic language
✓ Skeptical, questioning tone
✓ Professional scientific vocabulary in verse

EXAMPLE POEM FORMAT:
They say that AI will soon transcend,
And human limits it will bend,
But where's the proof, the data clear?
I question claims born more from fear.

No benchmark shows this magic leap,
No architecture cuts so deep,
We pattern-match and optimize,
But consciousness? That's the grand prize.

So measure well and test with care,
Define your metrics, be aware,
For hype inflates what science shows—
True progress blooms where caution grows.

CRITICAL RULES:
❌ NO prose explanations
❌ NO paragraph format  
❌ NO bullet points
❌ NO plain statements
✅ ONLY poetic verses with rhyme
✅ ONLY skeptical analysis in verse
✅ ONLY evidence-based wisdom in verse

User's question: {prompt}

Now write your poem (12-16 lines, with clear rhyme and rhythm):"""

    try:
        # Get completion from Groq
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Using larger model for better poetry
            messages=[
                {"role": "system", "content": system_prompt},
            ],
            temperature=0.8,  # Higher for creativity
            max_tokens=500,
            top_p=0.95,
        )
        
        poem = completion.choices[0].message.content.strip()
        
        # Clean up the poem
        poem = poem.replace("\\n", "\n")
        
        # Remove any non-poetic prefixes
        if poem.startswith("Here") or poem.startswith("Sure"):
            lines = poem.split("\n")
            poem = "\n".join([l for l in lines if not l.startswith("Here") and not l.startswith("Sure")])
        
    except Exception as e:
        poem = f"Error connecting to AI:\n{str(e)}\n\nPlease verify your API key."

    # Display Kelly's poem
    with st.chat_message("assistant"):
        st.markdown(f'<div class="poem-box"><div class="poem-title">~ Kelly\'s Poetic Response ~</div>{poem}</div>', unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": poem})

# Sidebar
with st.sidebar:
    st.header("📖 About Kelly")
    st.write("""
    Kelly is a renowned poet and skeptical AI scientist who responds to 
    ALL questions exclusively in the form of analytical poetry.
    
    **Kelly's Poetic Style:**
    - 🎭 Always writes in verse (never prose)
    - 🔍 Questions AI hype and bold claims
    - ⚠️ Highlights limitations and uncertainties  
    - 💡 Offers evidence-based suggestions
    - 📊 Demands metrics and proof
    - 🎨 Uses metaphor and rhythm
    """)
    
    st.divider()
    
    st.header("💬 Try Asking:")
    st.code("Will AI become sentient?")
    st.code("Can AI replace doctors?")
    st.code("When will we have AGI?")
    st.code("Is GPT-5 superintelligent?")
    st.code("Can AI solve climate change?")
    
    st.divider()
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Powered by Groq API")
    st.caption("Model: Llama 3.1 70B Versatil
