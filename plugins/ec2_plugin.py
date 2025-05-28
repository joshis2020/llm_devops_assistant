from plugins.base_plugin import BasePlugin
import boto3

class EC2Plugin(BasePlugin):
    def execute(self, prompt=None):
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}])
        stopped = [
            inst["InstanceId"]
            for res in response["Reservations"]
            for inst in res["Instances"]
        ]
        return f"Stopped EC2 Instances: {stopped}" if stopped else "No stopped EC2 instances found."
