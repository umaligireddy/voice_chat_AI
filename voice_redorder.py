import av
import streamlit as st
import numpy as np
import wave
import queue
import tempfile
from streamlit_webrtc import webrtc_streamer, WebRtcMode

audio_queue = queue.Queue()

def audio_callback(frame):
    audio = frame.to_ndarray()
    audio_queue.put(audio)
    return frame


def record_audio():
    st.subheader("🎙️ Record Your Voice")
    result_path = st.empty()


    webrtc_ctx = webrtc_streamer(
        key="voice-recorder",
        mode=WebRtcMode.SENDRECV,
        audio_receiver_size=1024,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
        audio_frame_callback=audio_callback,
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )

    if webrtc_ctx.state.playing:
        st.info("🔴 Recording... Click 'Stop' in Streamlit control bar to end.")


    if webrtc_ctx.state.playing is False and not audio_queue.empty():
        st.success("✅ Recording finished. Processing...")

        audio_frames = []
        while not audio_queue.empty():
            audio_frames.append(audio_queue.get())

        audio_np = np.concatenate(audio_frames, axis=0)

    
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(wav_file.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(48000)
            wf.writeframes(audio_np.tobytes())

        st.success("✅ Audio saved successfully.")
        result_path.success(f"Saved: {wav_file.name}")
        return wav_file.name

    return None
