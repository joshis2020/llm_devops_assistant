from kubernetes import client, config
import boto3
from plugins.base_plugin import BasePlugin


class K8sPlugin(BasePlugin):

    def execute(self, prompt: str) -> str:
        if prompt == "restart_crashloop_pods":
            return self.restart_crashloop_pods(namespace="default")

    def restart_crashloop_pods(self, namespace="default"):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace)
        restarted = []
        for pod in pods.items:
            for cs in pod.status.container_statuses or []:
                if cs.state.waiting and cs.state.waiting.reason == "CrashLoopBackOff":
                    v1.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace)
                    restarted.append(pod.metadata.name)
        return f"Restarted pods: {restarted}" if restarted else "No crashlooping pods found."