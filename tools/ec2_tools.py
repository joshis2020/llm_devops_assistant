# tools/ec2_tools.py
from typing import List, Dict, Any, Optional # Ensure Dict and Any are imported
from langchain_core.tools import tool
from plugins.ec2_plugin import EC2Plugin # Import the EC2Plugin
from memory_manager import set_last_listed_instances, get_last_listed_instances # Import memory functions
from config import AWS_REGION # Import region from config

# Initialize the EC2Plugin instance using the region from config
ec2_plugin_instance = EC2Plugin(region_name=AWS_REGION)

@tool
# Corrected: filters should be Optional]]
# Corrected: return type should be List]
def list_ec2_instances(instance_ids: Optional[List[str]] = None, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Lists EC2 instances based on optional IDs or filters.
    Returns a list of dictionaries, each containing 'InstanceId', 'InstanceType', 'State', 'LaunchTime', 'PrivateIpAddress', 'PublicIpAddress', and 'Tags'.
    
    Parameters:
        instance_ids (List[str]): Optional list of specific instance IDs to describe.
        filters (List[Dict[str, Any]]): Optional list of filters. Each filter is a dictionary with 'Name' and 'Values'.
    """
    result = ec2_plugin_instance.list_instances(instance_ids=instance_ids, filters=filters)
    if result and not any("error" in item for item in result):
        set_last_listed_instances(result)
    return result


@tool
def stop_ec2_instances(instance_ids: List[str]) -> Dict[str, Any]:
    """
    Stops one or more Amazon EBS-backed EC2 instances.
    This operation gracefully shuts down the instance, preserving the root device and attached EBS volumes.
    The instance can be restarted later.
    Use this tool when the user explicitly asks to 'stop' an EC2 instance.
    Parameters:
        instance_ids (List[str]): A required list of EC2 instance IDs to stop.
    """
    return ec2_plugin_instance.stop_instances(instance_ids=instance_ids)

@tool
def resolve_instance_reference(reference: str) -> Optional[str]:
    """
    Resolves a contextual reference (e.g., "first one", "second one", "instance named X")
    to an actual EC2 Instance ID from the 'last_listed_instances' in application state.
    Use this tool when the user refers to an instance by its position or a name from a previously listed set.
    Parameters:
        reference (str): The contextual reference, e.g., "first one", "instance named web-server".
    Returns:
        Optional[str]: The resolved InstanceId or None if not found.
    """
    instances = get_last_listed_instances() # Use the memory manager function
    if not instances:
        return None # No instances were previously listed

    # Simple logic for resolving common references
    if "first one" in reference.lower():
        if instances:
            # Access the 'InstanceId' of the first dictionary in the list
            return instances['InstanceId'] # Corrected to instances for first element
    elif "second one" in reference.lower():
        if len(instances) > 1:
            # Access the 'InstanceId' of the second dictionary in the list
            return instances[4]['InstanceId']
    elif "last one" in reference.lower():
        if instances:
            # Access the 'InstanceId' of the last dictionary in the list
            return instances[-1]['InstanceId']
    elif "instance named" in reference.lower():
        name_query = reference.lower().replace("instance named", "").strip()
        for inst in instances:
            for tag_key, tag_value in inst.get('Tags', {}).items():
                if tag_key.lower() == 'name' and name_query in tag_value.lower():
                    return inst['InstanceId']
    # Add more sophisticated parsing if needed
    return None

# List of all tools to be exposed to the agent
all_ec2_tools = [list_ec2_instances, stop_ec2_instances, resolve_instance_reference]