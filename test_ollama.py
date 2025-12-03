import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {"role": "user", "content": "Explain DevOps in simple words"}
    ]
)

print(response['message']['content'])

