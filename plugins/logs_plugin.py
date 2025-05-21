from assistant.llm_bedrock import invoke_bedrock_claude
import subprocess

def get_pod_logs(pod_name, namespace="default"):
    cmd = ["kubectl", "logs", pod_name, "-n", namespace]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else "Failed to get logs."

def summarize_logs():
    pod_name = input("Enter pod name: ")
    logs = get_pod_logs(pod_name)
    prompt = f"""
You are a DevOps expert. Analyze the following Kubernetes logs and return a brief diagnosis and suggested fix:

Logs:
{logs}
"""
    return invoke_bedrock_claude(prompt)
