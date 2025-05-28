from plugins.base_plugin import BasePlugin
from kubernetes import client, config
import re

class LogsPlugin(BasePlugin):
    def execute(self, prompt: str = None) -> str:
        pod_name = self.extract_pod_name(prompt)
        if not pod_name:
            return "Could not find a pod name in the prompt."

        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            logs = v1.read_namespaced_pod_log(name=pod_name, namespace="default", tail_lines=100)
            return f"Last 100 lines of logs for pod {pod_name}:\n\n{logs}"
        except Exception as e:
            return f"Failed to get logs for pod {pod_name}: {e}"

    def extract_pod_name(self, prompt: str) -> str:
        match = re.search(r"pod\s+([a-zA-Z0-9\-]+)", prompt)
        return match.group(1) if match else None
