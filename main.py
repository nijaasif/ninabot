# =========================
# Imports
# =========================
import os
import csv
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI


# =========================
# Load ENV first
# =========================
load_dotenv(Path(__file__).with_name(".env"))


# =========================
# FastAPI App
# =========================
app = FastAPI(title="NINA – Hospital AI Assistant")


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Serve Frontend
# =========================
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")


# =========================
# OpenAI Client (ONLY ONCE)
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# Emergency Handling
# =========================
emergency_keywords = [
    "chest pain", "heart attack", "stroke", "breathing problem",
    "shortness of breath", "unconscious", "bleeding heavily",
    "severe pain", "accident", "emergency"
]

EMERGENCY_MESSAGE = (
    "⚠️ This may be a medical emergency.\n"
    "Please seek urgent medical help now:\n"
    "- Call your local emergency number\n"
    "- OR go to the nearest Emergency Department immediately\n\n"
    "If you tell me your city, I can help locate emergency care nearby."
)


# =========================
# Knowledge Loader
# =========================
def load_knowledge() -> str:
    kb = Path(__file__).with_name("hospital_knowledge.txt")
    return kb.read_text(encoding="utf-8") if kb.exists() else ""


# =========================
# System Prompt
# =========================
NINA_RULES = """
You are NINA, a generic AI assistant for hospitals.

- Be professional, calm, caring
- Ask one question at a time
- Do NOT diagnose or prescribe
- For emergencies: advise immediate ER visit
- Use hospital knowledge base only
"""


# =========================
# Session Store (Demo)
# =========================
sessions = {}


# =========================
# Request Schema
# =========================
class ChatRequest(BaseModel):
    message: str
    session_id: str = "demo"


# =========================
# Health Check (API)
# =========================
@app.get("/health")
def health():
    return {"status": "ok", "bot": "NINA"}


# =========================
# Chat Endpoint
# =========================
@app.post("/chat")
def chat(req: ChatRequest):
    user_text = req.message.strip()
    user_lower = user_text.lower()
    session_id = req.session_id

    # Emergency guard
    if any(k in user_lower for k in emergency_keywords):
        return {"reply": EMERGENCY_MESSAGE}

    # Create session
    if session_id not in sessions:
        sessions[session_id] = {
            "stage": None,
            "name": None,
            "phone": None,
            "department": None,
            "preferred_datetime": None,
            "reason": None,
        }

    s = sessions[session_id]

    # ---- Appointment Flow ----
    if s["stage"] is None and "appointment" in user_lower:
        s["stage"] = "ask_name"
        return {"reply": "Sure — what is the patient’s full name?"}

    if s["stage"] == "ask_name":
        s["name"] = user_text
        s["stage"] = "ask_phone"
        return {"reply": "Please share a phone number (03XXXXXXXXX)."}

    if s["stage"] == "ask_phone":
        s["phone"] = user_text
        s["stage"] = "ask_department"
        return {"reply": "Which department do you want?"}

    if s["stage"] == "ask_department":
        s["department"] = user_text
        s["stage"] = "ask_datetime"
        return {"reply": "Preferred date & time? (YYYY-MM-DD HH:MM AM/PM)"}

    if s["stage"] == "ask_datetime":
        s["preferred_datetime"] = user_text
        s["stage"] = "ask_reason"
        return {"reply": "Reason for visit? (Optional — type 'skip')"}

    if s["stage"] == "ask_reason":
        s["reason"] = "" if user_lower == "skip" else user_text
        s["stage"] = "confirm"

        return {
            "reply": (
                "Please confirm your appointment:\n\n"
                f"- Name: {s['name']}\n"
                f"- Phone: {s['phone']}\n"
                f"- Department: {s['department']}\n"
                f"- Date/Time: {s['preferred_datetime']}\n"
                f"- Reason: {s['reason'] or 'Not provided'}\n\n"
                "Reply: confirm or edit"
            )
        }

    if s["stage"] == "confirm":
        if user_lower == "confirm":
            csv_path = Path("appointments.csv")
            new = not csv_path.exists()

            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if new:
                    writer.writerow(
                        ["timestamp", "name", "phone", "department", "datetime", "reason"]
                    )
                writer.writerow([
                    datetime.now().isoformat(),
                    s["name"], s["phone"],
                    s["department"], s["preferred_datetime"], s["reason"]
                ])

            sessions[session_id] = {"stage": None}
            return {"reply": "✅ Appointment submitted. Hospital staff will contact you."}

        if user_lower == "edit":
            sessions[session_id] = {"stage": "ask_name"}
            return {"reply": "Okay, restarting. What is the patient’s full name?"}

        return {"reply": "Please reply with confirm or edit."}

    # ---- Normal AI Response ----
    knowledge = load_knowledge()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": NINA_RULES},
            {"role": "system", "content": f"Hospital Knowledge:\n{knowledge}"},
            {"role": "user", "content": user_text},
        ],
        temperature=0.2,
    )

    return {"reply": response.choices[0].message.content.strip()}
