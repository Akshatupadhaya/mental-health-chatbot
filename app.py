import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

# Page config
st.set_page_config(
    page_title="Mental Health Companion Chatbot",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #667eea;
    }
    .chat-msg-user {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }
    .chat-msg-bot {
        background: #ffffff;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 0;
        max-width: 80%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .mood-badge {
        display: inline-block;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-top: 4px;
    }
    .mood-positive { background: #d4edda; color: #155724; }
    .mood-negative { background: #f8d7da; color: #721c24; }
    .mood-neutral  { background: #d1ecf1; color: #0c5460; }
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <h1>🧠 Mental Health Companion</h1>
    <p>A safe space to express how you feel. I'm here to listen. 💙</p>
    <small>IBM x Edunet Internship Project</small>
</div>
""", unsafe_allow_html=True)

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Responses
RESPONSES = {
    "positive": [
        "That's wonderful to hear! 😊 Keep nurturing that positive energy — you're doing great!",
        "I'm so glad you're feeling good! Your happiness matters. Keep shining! ✨",
        "Awesome! Positivity is powerful. Channel it into your studies and goals today! 🌟",
    ],
    "negative": [
        "I hear you, and I want you to know — it's completely okay to feel this way. You're not alone. 💙",
        "I'm really sorry you're going through this. Your feelings are valid. Take a deep breath — this too shall pass. 🌸",
        "It sounds like things are tough right now. Be gentle with yourself. One step at a time. 🤗",
    ],
    "neutral": [
        "Thank you for sharing with me. How are you really feeling today? I'm here to listen. 😊",
        "I'm here for you! Sometimes talking things out helps. Tell me more about your day. 💬",
        "It sounds like a regular day. Remember, it's okay to take breaks and recharge. 🌿",
    ]
}

RELAXATION_TIPS = {
    "positive": [
        "💡 Tip: Use this energy — try a 25-minute Pomodoro study session right now!",
        "💡 Tip: Share your positivity with a friend or classmate today!",
        "💡 Tip: Write down 3 things you're grateful for to keep the good vibes going.",
    ],
    "negative": [
        "🧘 Try this: Close your eyes, breathe in for 4 seconds, hold for 4, breathe out for 6. Repeat 3 times.",
        "🎵 Tip: Put on your favorite calming music and take a 10-minute break. You deserve it.",
        "📝 Tip: Write down what's bothering you in a journal. Getting it out of your head helps.",
    ],
    "neutral": [
        "🚶 Tip: A short 10-minute walk can boost your mood and focus significantly.",
        "💧 Tip: Drink a glass of water, stretch for 2 minutes — your body will thank you.",
        "📚 Tip: Set one small, achievable goal for today. Small wins build big confidence.",
    ]
}

MOOD_EMOJI = {"positive": "😊 Positive", "negative": "😔 Negative", "neutral": "😐 Neutral"}
MOOD_CSS   = {"positive": "mood-positive", "negative": "mood-negative", "neutral": "mood-neutral"}

def detect_mood(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:   return "positive"
    elif score <= -0.05: return "negative"
    else:               return "neutral"

def get_response(mood):
    reply = random.choice(RESPONSES[mood])
    tip   = random.choice(RELAXATION_TIPS[mood])
    return f"{reply}\n\n{tip}"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hi! 👋 I'm your Mental Health Companion. How are you feeling today? You can share anything — I'm here to listen and support you. 😊", "mood": None}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-msg-user">{msg["text"]}</div>', unsafe_allow_html=True)
    else:
        mood_html = ""
        if msg["mood"]:
            css = MOOD_CSS[msg["mood"]]
            label = MOOD_EMOJI[msg["mood"]]
            mood_html = f'<br><span class="mood-badge {css}">Detected mood: {label}</span>'
        st.markdown(
            f'<div class="chat-msg-bot">{msg["text"].replace(chr(10), "<br>")}{mood_html}</div>',
            unsafe_allow_html=True
        )

# Input
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("", placeholder="Type how you're feeling...", label_visibility="collapsed", key="input")
with col2:
    send = st.button("Send 💬", use_container_width=True)

if send and user_input.strip():
    mood = detect_mood(user_input)
    response = get_response(mood)

    st.session_state.messages.append({"role": "user", "text": user_input, "mood": None})
    st.session_state.messages.append({"role": "bot",  "text": response,   "mood": mood})
    st.rerun()
