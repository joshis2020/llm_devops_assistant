# plugins/logs_plugin.py
from plugins.base_plugin import BasePlugin
from assistant.llm_client import invoke_bedrock
from kubernetes import client, config
import re

class LogsPlugin(BasePlugin):
    def execute(self, prompt: str) -> str:
        try:
            # Step 1: Extract pod name from prompt
            pod_name = self._extract_pod_name(prompt)
            #pod_name = "nginx"
            if not pod_name:
                return "Could not find a pod name in the prompt."

            # Step 2: Get logs from the pod
            logs = self._get_pod_logs(pod_name)
            #print("get logs response: ", logs)
            if not logs:
                return f"No logs found for pod '{pod_name}'."

            if "Error" in logs:
                return "There was an error fetching the logs: " +  logs

            # Step 3: Build prompt for LLM
            system_prompt = "You are a helpful assistant that summarizes Kubernetes pod logs."
            full_prompt = f"""\n\nHuman: {system_prompt}\n\nHere are the logs from pod '{pod_name}':\n{logs}\n\nPlease summarize the key issues and insights.\n\nAssistant:"""

            # Step 4: Get summary from Bedrock
            summary = invoke_bedrock(full_prompt)
            return summary

        except Exception as e:
            return f"Error summarizing logs: {str(e)}"

    def _extract_pod_name(self, text: str) -> str:
        text = text.lower().strip()
       
        # Common patterns to match "pod nginx", "nginx pod", etc.
        patterns = [
            r'pod\s+([a-zA-Z0-9\-]+)',            # "pod nginx"
            r'logs\s+(?:of|for|from)\s+pod\s+([a-zA-Z0-9\-]+)',  # "logs for pod nginx"
            r'logs\s+(?:of|for|from)\s+([a-zA-Z0-9\-]+)',        # "logs for nginx"
            r'summarize\s+logs\s+.*\s+([a-zA-Z0-9\-]+)',         # "summarize logs for nginx"
            r'([a-zA-Z0-9\-]+)\s+pod'              # "nginx pod"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                pod_name = match.group(1).strip().strip(".,?")
                print(f"[DEBUG] Extracted pod name: {pod_name}")
                return pod_name

        print("[DEBUG] No pod name found in prompt")
        return None


    def _get_pod_logs(self, pod_name: str, namespace="default") -> str:
        # Load kube config (assumes it's available, like in a local or EKS setup)
        config.load_kube_config()
        v1 = client.CoreV1Api()
        try:
            return v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, tail_lines=100)
        except Exception as e:
            return f"Error fetching logs from pod '{pod_name}': {str(e)}"
