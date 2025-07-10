import streamlit as st
import google.generativeai as genai

# 🌐 Gemini Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 🧠 App Meta
st.set_page_config(page_title="Event Simulation Chatbot - Drishti Access", layout="wide", page_icon="👁️")

# 🎨 Inject Custom CSS for Theming
st.markdown("""
    <style>
    /* Light pastel background */
    .stApp {
        background-color: #F0F8FF;
        font-family: 'Segoe UI', sans-serif;
    }
            
     h1, h2, h3, h4 {
        color: #1C1E21;
    }            
            
    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #F0F8FF;
        border-right: 1px solid #d0d7e2;
    }

    /* Titles & Headers */
    .st-emotion-cache-10trblm {
        color: #3a3a50;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        background-color: #6f4fcf;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        border: none;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #5c3bb6;
    }

    /* Chat messages */
    .chat-message {
        padding: 1em;
        background-color: #ffffff;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    .user-message {
        border-left: 4px solid #6f4fcf;
    }

    .bot-message {
        border-left: 4px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

# 🧾 Title
st.markdown("<h1 style='color:#7B61FF;'> 👁️ Drishti Access's Event Simulation Chatbot </h1>", unsafe_allow_html=True)
#st.title("<h1 style='color:#7B61FF;'>👁️ Drishti Access's Event Simulation Chatbot")

# Session State
if "event_description" not in st.session_state:
    st.session_state.event_description = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🎛️ Sidebar
with st.sidebar:
    st.header("📋 Event Setup")

    venue_name = st.text_input("Venue Name", "Nehru Stadium")
    total_capacity = st.number_input("Expected Crowd", min_value=0, value=10000)
    gates = st.text_area("Gate Info (Name, Opening Time, Closing Time)",
                         "Gate A: 8:00 AM - 11:00 AM\nGate B: 8:00 AM - 11:00 AM")
    structure = st.text_area("Venue Structure",
                             "Main Stage at center, Gate A on East end, Gate B on west end, Food area near Gate A, Toilets near Gate B, etc.")
    event_timeline = st.text_area("Event Timeline",
                                  "Opening: 8 AM\nMain Performance: 12 PM\nClosing: 2 PM")

    if st.button("✅ Save Event Details"):
        event_prompt = f"""
        Event Name: {venue_name}
        Expected Crowd: {total_capacity}
        Gates:\n{gates}
        Structure:\n{structure}
        Timeline:\n{event_timeline}
        """
        st.session_state.event_description = event_prompt
        st.success("✅ Event details saved.")

    st.divider()
    st.markdown("### 🔑 API Configuration")

    use_custom_key = st.checkbox("Use my own Gemini API key", value=False)

    if use_custom_key:
        user_api_key = st.text_input("Enter your Gemini API Key", type="password")
        if user_api_key:
            genai.configure(api_key=user_api_key)
        else:
            st.warning("Please enter a valid API key to use your own.")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# 💬 Chat Interface
if st.session_state.event_description:
    st.subheader("💡 Ask What-If Scenarios")

    # Show chat history
    for message in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-message user-message'>{message['user']}</div>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            st.markdown(f"<div class='chat-message bot-message'>{message['bot']}</div>", unsafe_allow_html=True)

    user_input = st.chat_input("What do you want to simulate?")
    if user_input:
        full_prompt = f"""
        You are a crowd simulation assistant for large public events.
        Based on the following event details:

        {st.session_state.event_description}

        Answer the following question with clear logic and realistic assumptions.
        Focus on movement logic and actionable outcomes.

        Question: {user_input}
        """

        with st.spinner("🔄 Simulating crowd response..."):
            response = model.generate_content(full_prompt)
            answer = response.text

        st.session_state.chat_history.append({"user": user_input, "bot": answer})
        st.experimental_rerun()
else:
    st.info("👈 Please describe your event in the sidebar to start simulation.")

