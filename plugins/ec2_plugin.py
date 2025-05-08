import boto3

def list_stopped_instances():
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances(Filters=[
        {"Name": "instance-state-name", "Values": ["stopped"]}
    ])
    instances = [i["InstanceId"] for r in response["Reservations"] for i in r["Instances"]]
    return f"Stopped instances: {instances}" if instances else "No stopped instances found."