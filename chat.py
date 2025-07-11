from gtts import gTTS
import io
import streamlit as st
import google.generativeai as genai

# ----------------- CONFIG -----------------

# Supported languages
LANGUAGES = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Marathi (मराठी)": "mr",
    "Gujarati (ગુજરાતી)": "gu",
    "Bengali (বাংলা)": "bn",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Malayalam (മലയാളം)": "ml",
    "Punjabi (ਪੰਜਾਬੀ)": "pa"
}

# Page settings
st.set_page_config(page_title="Drishti Access Chatbot", layout="wide", page_icon="👁️")

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #F0F8FF;
    font-family: 'Segoe UI', sans-serif;
}
section[data-testid="stSidebar"] {
    background-color: #F0F8FF;
    border-right: 1px solid #d0d7e2;
}
.stButton > button {
    background-color: #6f4fcf;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1.2em;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #5c3bb6;
}
.chat-message {
    padding: 1em;
    background-color: #ffffff;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.user-message { border-left: 4px solid #6f4fcf; }
.bot-message { border-left: 4px solid #4caf50; }
</style>
""", unsafe_allow_html=True)

# ----------------- HEADER -----------------

st.markdown("<h1 style='color:#7B61FF;'>👁️ Drishti Access's Event Situations Simulation Chatbot</h1>", unsafe_allow_html=True)

# ----------------- SESSION -----------------

if "event_description" not in st.session_state:
    st.session_state.event_description = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

# ----------------- SIDEBAR -----------------

with st.sidebar:
    st.header("📋 Event Setup")
    venue = st.text_input("Venue Name", "Nehru Stadium")
    capacity = st.number_input("Expected Crowd", min_value=0, value=10000)
    gates = st.text_area("Gate Info", "Gate A: 8:00 AM - 11:00 AM\nGate B: 8:00 AM - 11:00 AM")
    structure = st.text_area("Venue Structure", "Stage center, Gate A East, Gate B West...")
    timeline = st.text_area("Event Timeline", "Opening: 8 AM\nMain: 12 PM\nClose: 2 PM")

    if st.button("✅ Save Event Details"):
        st.session_state.event_description = f"""
Event Name: {venue}
Expected Crowd: {capacity}
Gates:
{gates}
Structure:
{structure}
Timeline:
{timeline}
"""
        st.success("✅ Event details saved.")

    st.divider()
    st.markdown("### 🌐 Language & 🔑 API Settings")
    st.session_state.selected_language = st.selectbox("Response Language", list(LANGUAGES.keys()))

    use_custom_key = st.checkbox("Use my own Gemini API key", value=False)
    if use_custom_key:
        user_api_key = st.text_input("Enter Gemini API Key", type="password")
        if user_api_key:
            genai.configure(api_key=user_api_key)
        else:
            st.warning("Please enter a valid key.")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ----------------- CHAT -----------------

st.subheader("💬 Ask What-If Scenarios")

if st.session_state.event_description:
    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-message user-message'>{message['user']}</div>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            st.markdown(f"<div class='chat-message bot-message'>{message['bot']}</div>", unsafe_allow_html=True)
            if "audio" in message:
                st.audio(message["audio"], format="audio/mp3")

    user_input = st.chat_input("What do you want to simulate?")
    if user_input:
        lang_name = st.session_state.selected_language
        lang_code = LANGUAGES[lang_name]

        prompt = f"""
You are a crowd simulation assistant for large public events.
Based on the following event details:

{st.session_state.event_description}

Respond in {lang_name}.
Question: {user_input}
"""

        with st.spinner("🔄 Simulating..."):
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            answer = response.text
            # TTS in memory using BytesIO
            audio_bytes = None
            try:
                tts = gTTS(answer, lang=lang_code)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                audio_bytes = audio_buffer.read()
            except Exception as e:
                st.warning(f"TTS failed: {e}")

        st.session_state.chat_history.append({
            "user": user_input,
            "bot": answer,
            "audio": audio_bytes
        })

        st.rerun()
else:
    st.info("👈 Fill out event details to begin simulation.")
