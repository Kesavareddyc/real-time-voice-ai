# main_app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modules.integrator_module import process_audio_pipeline
from modules.stt_module import convert_speech_to_text
from modules.brain_module import get_ai_response
from modules.db_module import fetch_all_interactions
from modules.tts_module import cleanup_old_outputs
from pathlib import Path
import os

app = FastAPI(
    title="Real-Time Speech Interaction System (API mode)",
    version="1.0"
)

# -------------------------------------------------------------------
# ⭐ CORS FIX (IMPORTANT)
# -------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow your HTML frontend
    allow_credentials=True,
    allow_methods=["*"],       # allow POST, GET, OPTIONS
    allow_headers=["*"],       # allow JSON headers
)

# Ensure outputs dir exists
Path("outputs").mkdir(exist_ok=True)

# # -------------------------------------------------------------------
# # Speech-To-Text (File Upload)
# # -------------------------------------------------------------------
# @app.post("/stt/")
# async def stt_endpoint(file: UploadFile = File(...)):
#     audio_bytes = await file.read()
#     text = convert_speech_to_text(audio_bytes)
#     return {"transcribed_text": text}

# -------------------------------------------------------------------
# AI Text Response
# -------------------------------------------------------------------
class PromptRequest(BaseModel):
    prompt: str

@app.post("/respond/")
def respond_endpoint(req: PromptRequest):
    reply = get_ai_response(req.prompt)
    return {"response": reply}

# -------------------------------------------------------------------
# Full Pipeline (STT → AI → DB Log)
# -------------------------------------------------------------------
@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    """
    Upload wav file -> STT -> AI -> store text only -> return text results.
    No audio file is returned or stored permanently.
    """
    audio_bytes = await file.read()
    result = process_audio_pipeline(audio_bytes)
    return JSONResponse(content=result)

# -------------------------------------------------------------------
# History Log
# -------------------------------------------------------------------
@app.get("/history/")
def history():
    return {"interactions": fetch_all_interactions()}

# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "API mode active. Live mode: python -m modules.live_assistant"
    }

# -------------------------------------------------------------------
# Cleanup Endpoint
# -------------------------------------------------------------------
@app.post("/cleanup_outputs/")
def cleanup_outputs(minutes: int = 10):
    try:
        cleanup_old_outputs(minutes=minutes)
        return {"message": "cleanup started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
