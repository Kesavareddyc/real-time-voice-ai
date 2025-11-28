# modules/integrator_module.py
from modules.stt_module import convert_speech_to_text
from modules.brain_module import get_ai_response
from modules.db_module import save_interaction

def process_audio_pipeline(audio_bytes: bytes):
    """
    API-mode full pipeline for uploaded audio:
    - STT -> AI -> save TEXT only to DB -> return text response (no audio)
    """
    text = convert_speech_to_text(audio_bytes)
    if text.startswith("ERROR"):
        return {"transcribed_text": text, "ai_reply": "", "status": "stt_error"}

    ai_reply = get_ai_response(text)

    # Save only text to DB
    try:
        save_interaction(text, ai_reply)
    except Exception:
        # DB errors shouldn't break API; ignore or log as needed
        pass

    # Return text only: API mode does not return audio.
    return {
        "transcribed_text": text,
        "ai_reply": ai_reply,
        "status": "stored_text_only"
    }
