import json
import re
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from google import genai
import os

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY environment variable.")

client = genai.Client(api_key=api_key)

# Route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# Endpoint to check essays
@app.post("/check")
def check_essay(essay: str = Form(...), rubric: str = Form(...)):
    prompt = f"""
Grade the following essay according to this rubric.

RUBRIC:
{rubric}

ESSAY:
{essay}

Respond ONLY with JSON in this format:
{{
"criteria_scores": {{}},
"total_score": "",
"strengths": "",
"weaknesses": "",
"suggestions": ""
}}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text

        # Remove Markdown code blocks if present
        text = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE)

        # Convert the string to JSON
        parsed_json = json.loads(text)

        return JSONResponse(content=parsed_json)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
