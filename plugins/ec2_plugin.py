# plugins/ec2_plugin.py
import boto3
from typing import List, Dict, Any, Optional # Ensure Dict and Any are imported

class EC2Plugin:
    """
    A plugin for managing AWS EC2 instances using Boto3.
    """
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initializes the EC2 client.
        Args:
            region_name (str): The AWS region to operate in.
        """
        self.ec2_client = boto3.client('ec2', region_name=region_name)

    # Corrected: filters should be Optional]]
    # Corrected: return type should be List]
    #df list_instances(self, instance_ids: Optional[List[str]] = None, filters: Optional]] = None) -> List]:
    def list_instances(self, instance_ids: Optional[List[str]] = None, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:

        """
        Describes the specified instances or all instances.
        # Useful for getting instance IDs, states, and other details.
        Referenced from.[1, 2]

        Args:
            instance_ids (List[str], optional): A list of EC2 instance IDs to describe. Defaults to None.
            filters (List], optional): A list of filters to apply to the describe_instances call. Defaults to None.
                                            Example: [{'Name': 'instance-state-name', 'Values': ['running']}]

        Returns:
            List]: A list of dictionaries, each representing an EC2 instance with its details.
                        Returns an error dictionary if an exception occurs.
        """
        try:
            response = self.ec2_client.describe_instances(
                InstanceIds=instance_ids if instance_ids else [],
                Filters=filters if filters else []
            )
            instances = []
            for reservation in response.get('Reservations',):
                for instance in reservation.get('Instances',):
                    instance_info = {
                        'InstanceId': instance.get('InstanceId'),
                        'InstanceType': instance.get('InstanceType'),
                        'State': instance.get('State', {}).get('Name'),
                        'LaunchTime': instance.get('LaunchTime').isoformat() if instance.get('LaunchTime') else None,
                        'PrivateIpAddress': instance.get('PrivateIpAddress'),
                        'PublicIpAddress': instance.get('PublicIpAddress'),
                        'Tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags',) if 'Key' in tag and 'Value' in tag}
                    }
                    instances.append(instance_info)
            return instances
        except self.ec2_client.exceptions.ClientError as e:
            return
        except Exception as e:
            return [{"error": f"An unexpected error occurred while listing instances: {e}"}]

    def stop_instances(self, instance_ids: List[str]) -> Dict[str, Any]:
        """
        Stops one or more Amazon EBS-backed EC2 instances.
        This operation shuts down the instance, preserving the root device and attached EBS volumes.
        The instance can be restarted later.
        Referenced from.[3]

        Args:
            instance_ids (List[str]): A list of EC2 instance IDs to stop.

        Returns:
            Dict: A dictionary containing the stopping instances' details or an error.
        """
        if not instance_ids:
            return {"status": "error", "message": "No instance IDs provided for stopping."}

        try:
            response = self.ec2_client.stop_instances(
                InstanceIds=instance_ids,
                DryRun=False
            )
            stopping_details = []
            for inst in response.get('StoppingInstances',):
                stopping_details.append({
                    'InstanceId': inst.get('InstanceId'),
                    'CurrentState': inst.get('CurrentState', {}).get('Name'),
                    'PreviousState': inst.get('PreviousState', {}).get('Name')
                })
            return {"status": "success", "details": stopping_details}
        except self.ec2_client.exceptions.ClientError as e:
            return {"status": "error", "message": f"AWS Client Error: {e.response.get('Error', {}).get('Message', str(e))}"}
        except Exception as e:
            return {"status": "error", "message": f"An unexpected error occurred: {e}"}