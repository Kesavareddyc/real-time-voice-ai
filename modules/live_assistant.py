# modules/live_assistant.py
import speech_recognition as sr
import time, os
from modules.brain_module import get_ai_response
from modules.db_module import save_interaction
from modules.tts_module import generate_tts_tempfile, cleanup_old_outputs
import uuid
import pygame

def _safe_play_and_delete(filepath: str):
    """
    Play an mp3 using pygame and delete the file afterwards.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print("Playback error:", e)
    finally:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass

def run_live_assistant():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("\n🤖 Live Voice Assistant (phone-call style) started. Say 'exit' to stop.\n")
    # optional cleanup on start
    cleanup_old_outputs(minutes=60)

    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                print("🎙️ Listening...")
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)

            # 1) STT
            try:
                user_text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("⚠️ Could not understand audio.")
                continue
            except sr.RequestError as e:
                print("⚠️ STT service error:", e)
                continue

            print(f"You: {user_text}")

            if user_text.strip().lower() in ("exit", "quit", "stop"):
                print("👋 Stopping assistant.")
                break

            # 2) AI
            ai_reply = get_ai_response(user_text)
            print(f"AI: {ai_reply}")

            # 3) Save only text to DB
            try:
                save_interaction(user_text, ai_reply)
            except Exception:
                pass

            # 4) TTS -> temp file -> play -> delete
            try:
                mp3_file = generate_tts_tempfile(ai_reply)
                _safe_play_and_delete(mp3_file)
            except Exception as e:
                print("⚠️ TTS/playback error:", e)

            # small pause to avoid immediate re-trigger
            time.sleep(0.3)

        except KeyboardInterrupt:
            print("\n👋 Interrupted by user.")
            break
        except Exception as e:
            print("⚠️ Live assistant error:", e)
            # don't crash—the assistant should keep running
            time.sleep(0.5)

if __name__ == "__main__":
    run_live_assistant()
