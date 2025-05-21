from kubernetes import client, config

# def restart_crashloop_pods(namespace="default"):
#     config.load_kube_config()
#     v1 = client.CoreV1Api()
#     pods = v1.list_namespaced_pod(namespace)
#     restarted = []
#     for pod in pods.items:
#         for cs in pod.status.container_statuses or []:
#             if cs.state.waiting and cs.state.waiting.reason == "CrashLoopBackOff":
#                 v1.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace)
#                 restarted.append(pod.metadata.name)
#     return f"Restarted pods: {restarted}" if restarted else "No crashlooping pods found."

import boto3
from plugins.base_plugin import BasePlugin


class K8sPlugin(BasePlugin):

    def match(self, prompt: str) -> bool:
        return "ec2" in prompt.lower() and "stopped" in prompt.lower()


    def execute(self, prompt: str) -> str:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances(Filters=[
            {"Name": "instance-state-name", "Values": ["stopped"]}
        ])
        instances = [i["InstanceId"] for r in response["Reservations"] for i in r["Instances"]]
        return f"Stopped instances: {instances}" if instances else "No stopped instances found."

