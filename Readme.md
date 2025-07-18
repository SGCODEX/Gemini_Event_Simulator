# 👁️ Drishti Access – Event Situations Simulation Chatbot

Drishti Access is a multilingual, AI-powered chatbot designed to simulate and respond to crowd management scenarios during large public events. Using Google's Gemini API and Text-to-Speech, it lets you define venue structure, crowd size, gate timings, and ask realistic "what-if" questions like:

> *“What happens if Gate A is closed at 12 PM while Gate B remains open?”*

> *“Imagine 2000 people came more. How should we make them disperse properly at 2PM to avoid stampede?”*

**It also reads out responses in the selected Indian language!**

---

## 🚀 Features

- 🧠 **Gemini-Powered Simulation**  
  Responds intelligently to what-if crowd management scenarios.

- 🗺️ **Event Setup Panel**  
  Define venue name, structure, gate timings, timelines, and crowd size.

- 🗣️ **Multilingual Support**  
  Supports 10 Indian languages for both response and TTS playback:
  - Hindi, Bengali, Marathi, Tamil, Telugu, Gujarati, Kannada, Malayalam, Punjabi, English

- 🔊 **In-Browser TTS**  
  Uses `gTTS` to play voice feedback for every response.

- 🧾 **Custom Gemini API Key Option**  
  Use your own API key securely via the sidebar.

---

## 💡 Topics Covered

- Streamlit UI Development
- Google Gemini (Generative AI) Integration
- Event Simulation Logic
- Text-to-Speech (gTTS)
- Multilingual Natural Language Processing
- In-Memory Audio Generation (`io.BytesIO`)

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/drishti-access-chatbot.git
   cd drishti-access-chatbot

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

3. **Set up secrets:**
Create a .streamlit/secrets.toml file and add your Gemini API key:
    ```bash
    GEMINI_API_KEY = "your-api-key-here"

3. **Run the app:**
    ```bash
    streamlit run chat.py

---
## 📺 Demo
<img width="1366" height="540" alt="image" src="https://github.com/user-attachments/assets/5ba23c43-6f65-4b1e-931f-0279459fd891" />
<img width="1366" height="557" alt="image" src="https://github.com/user-attachments/assets/87ee8198-3a03-404a-bca5-139a159e5c83" />

---
**Made by Shivam Gupta for Google Agentic AI Day Hackathon**
