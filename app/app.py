from fastapi import FastAPI
from app.model import generate_response

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Local LLM API running"}

@app.post("/generate")
def generate(prompt: str):
    output = generate_response(prompt)
    return {"response": output}

