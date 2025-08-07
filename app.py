import streamlit as st
import os
from chat_utils import get_gpt_response
from audio_to_text import transcribe_audio
from voice_redorder import record_audio
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="🎤 Voice Chat with AI")
st.title("🎤 Voice Chat With AI")
st.markdown("Talk to an AI using your voice!")

option = st.radio("Choose input method:", ["Upload Audio File", "Record Your Voice"])

if option == "Upload Audio File":
    uploaded_file = st.file_uploader("📁 Upload an audio file", type=["mp3", "wav"])

    if uploaded_file is not None:
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        user_input = transcript.text
        st.markdown("#### 📝 Transcription:")
        st.success(user_input)

elif option == "Record Your Voice":
    audio_path = record_audio()

    if audio_path:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        user_input = transcript.text
        st.markdown("#### 📝 Transcription:")
        st.success(user_input)


if 'user_input' in locals() and user_input:
    st.markdown("#### 💬 AI Response:")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    st.info(response.choices[0].message.content)
