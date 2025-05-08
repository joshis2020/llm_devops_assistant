from fastapi import FastAPI, Request
from assistant.core import handle_prompt

app = FastAPI()

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    return {"response": handle_prompt(prompt)}