# Essay Checker

A web app built with **FastAPI** that grades essays based on a custom rubric using **Google Gemini API**.

## Features
- Input your essay and rubric
- Automatically get JSON feedback with scores, strengths, weaknesses, and suggestions
- Interactive front-end with HTML and JavaScript

## Tech Stack
- Python, FastAPI
- Google Gemini API
- HTML, JavaScript

## How to Run
```bash
pip install -r requirements.txt
uvicorn app:app --reload