# backend/api.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from core.interviewer import start_interview, submit_answer, restart_interview
import shutil
import os
import tempfile

app = FastAPI(title="AI Mock Interviewer Backend")

@app.get("/")
def root():
    return {"message": "AI Mock Interviewer Backend is running."}

@app.post("/start")
async def start(
    category: str = Form(...),
    cv: UploadFile = File(None)
):
    temp_path = None
    if cv:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cv.filename)[1]) as tmp:
            shutil.copyfileobj(cv.file, tmp)
            temp_path = tmp.name

    msg, question, audio_path = start_interview(category, temp_path)
    return JSONResponse({
        "message": msg,
        "question": question,
        "audio_path": audio_path
    })

@app.post("/submit")
async def submit(
    text: str = Form(""),
    audio: UploadFile = File(None)
):
    audio_path = None
    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            shutil.copyfileobj(audio.file, tmp)
            audio_path = tmp.name

    msg, result, audio_out = submit_answer(text, audio_path)
    return JSONResponse({
        "message": msg,
        "result": result,
        "audio_path": audio_out
    })

@app.post("/reset")
async def reset():
    msg, _, _ = restart_interview()
    return {"message": msg}
