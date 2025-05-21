import boto3
from plugins.base_plugin import BasePlugin


class EC2Plugin(BasePlugin):

    def match(self, prompt: str) -> bool:
        return "ec2" in prompt.lower() and "stopped" in prompt.lower()


    def execute(self, prompt: str) -> str:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances(Filters=[
            {"Name": "instance-state-name", "Values": ["stopped"]}
        ])
        instances = [i["InstanceId"] for r in response["Reservations"] for i in r["Instances"]]
        return f"Stopped instances: {instances}" if instances else "No stopped instances found."

