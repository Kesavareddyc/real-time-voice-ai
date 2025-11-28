# modules/brain_module.py
from openai import OpenAI
from dotenv import load_dotenv
import os, traceback

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

def generate_fallback(prompt: str) -> str:
    text = (prompt or "").strip().lower()
    if any(g in text for g in ["hi", "hello", "hey"]):
        return "Hello! I am here. How can I help you today?"
    if "your name" in text or "who are you" in text:
        return "I am your demo voice assistant."
    if any(q in text for q in ["help", "what can you do", "how to use"]):
        return "I can convert speech to text and speak replies. Ask me something simple."
    return f"I heard: {prompt}"

def get_ai_response(prompt: str) -> str:
    """
    Uses OpenAI Responses API to generate a reply.
    If OpenAI fails or key missing, returns a simple fallback reply.
    """
    if not prompt:
        return "Please say something for me to respond to."

    if not client:
        return generate_fallback(prompt)

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": "You are a friendly voice assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Attempt common extraction path
        try:
            return response.output[0].content[0].text.strip()
        except Exception:
            # Generic fallback extraction
            parts = []
            for item in getattr(response, "output", []):
                if isinstance(item, dict) and "content" in item:
                    for block in item["content"]:
                        if isinstance(block, dict) and "text" in block:
                            parts.append(block["text"])
            if parts:
                return " ".join(parts).strip()
        # If extraction failed, fallback
        return generate_fallback(prompt)
    except Exception as e:
        traceback.print_exc()
        return generate_fallback(prompt)
