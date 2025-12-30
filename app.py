import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

# Set your Gemini API key here
GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Mount static files (for CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Serve the chat UI
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat endpoint for AJAX
@app.post("/chat")
async def chat(user_message: str = Form(...)):
    # English: Send user message to Gemini and get reply
    # Hindi: User ka message Gemini ko bhejein aur reply lein
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)
        bot_reply = response.text.strip()
    except Exception as e:
        bot_reply = f"[Error]: {str(e)}"
    return JSONResponse({"reply": bot_reply}) 
