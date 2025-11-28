# modules/tts_module.py
from gtts import gTTS
from pathlib import Path
import uuid, os
from datetime import datetime

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_tts_tempfile(text: str, lang: str = "en") -> str:
    """
    Generates an MP3 file in outputs/ and returns the full path.
    Caller should delete the file after playing.
    """
    fname = f"tts_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.mp3"
    fullpath = OUTPUT_DIR / fname
    gTTS(text=text, lang=lang).save(str(fullpath))
    return str(fullpath)

def cleanup_old_outputs(minutes: int = 10):
    """
    Optional: remove leftover files older than `minutes`.
    """
    import time
    cutoff = time.time() - (minutes * 60)
    for p in OUTPUT_DIR.iterdir():
        try:
            if p.is_file() and p.stat().st_mtime < cutoff:
                p.unlink()
        except Exception:
            pass
