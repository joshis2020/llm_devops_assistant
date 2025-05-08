from assistant.router import route_query

def handle_prompt(prompt: str):
    print(f"[LLM] Received: {prompt}")
    response = route_query(prompt)
    return response