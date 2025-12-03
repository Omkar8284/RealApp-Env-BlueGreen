import ollama
import os

model_name = os.getenv("LLM_MODEL", "llama3")

def generate_response(prompt: str) -> str:
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']

