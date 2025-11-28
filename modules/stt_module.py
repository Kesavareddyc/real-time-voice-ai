# modules/stt_module.py
import speech_recognition as sr
import io

def convert_speech_to_text(audio_bytes: bytes) -> str:
    """
    Convert WAV bytes -> text using speech_recognition (Google).
    Returns text or an error string starting with "ERROR:".
    """
    recognizer = sr.Recognizer()
    audio_file = io.BytesIO(audio_bytes)

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "ERROR: Could not understand audio."
    except sr.RequestError as e:
        return f"ERROR: Speech recognition service error: {e}"
    except Exception as e:
        return f"ERROR: {e}"
