# assistant/llm_client.py

import boto3
import json

bedrock = boto3.client("bedrock-runtime")

def classify_intent(prompt: str) -> str:
    model_id = "anthropic.claude-instant-v1"

    formatted_prompt = f"""\
Human: You are a DevOps assistant. Based on the user input, extract and respond with one of the following valid intents **only** (no explanations):
[list_stopped_instances, restart_crashloop_pods, get_daily_cost, summarize_logs]

User input: "{prompt}"

Assistant:"""

    body = {
        "prompt": formatted_prompt,
        "max_tokens_to_sample": 20,
        "temperature": 0.2,
        "top_k": 250,
        "top_p": 1,
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    completion = json.loads(response["body"].read())["completion"]
    return completion.strip()


def invoke_bedrock(prompt: str, model_id="anthropic.claude-instant-v1", max_tokens=500) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"] if "content" in result else "No response from Bedrock."
