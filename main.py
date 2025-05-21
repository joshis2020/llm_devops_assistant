import sys
from assistant.core import handle_prompt

def main():
    if len(sys.argv) < 2:
        print("Usage: python assistant/main.py '<your prompt>'")
        return
    prompt = sys.argv[1]
    response = handle_prompt(prompt)
    print(response)

if __name__ == "__main__":
    main()
