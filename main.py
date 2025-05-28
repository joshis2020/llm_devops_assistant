import sys
from router import route_intent
from memory import ContextMemory

if __name__ == "__main__":
    user_input = " ".join(sys.argv[1:])
    print(f"[LLM] Received: {user_input}")

    memory = ContextMemory()
    memory.add_user_input(user_input)

    result = route_intent(memory)
    memory.add_model_response(result)
    print(result)
