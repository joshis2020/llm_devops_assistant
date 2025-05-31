# memory_manager.py
from typing import Dict, Any, List, Optional

# This dictionary will store dynamic data that the LLM needs to reference contextually.
# In a multi-user system, this would be per-session/user, managed by a higher-level component.
session_app_state: Dict[str, Any] = {}

def set_last_listed_instances(instances: List[Dict[str, Any]]):
    """
    Stores the last list of EC2 instances retrieved by a tool call.
    """
    session_app_state['last_listed_instances'] = instances


def get_last_listed_instances() -> Optional[List[Dict[str, Any]]]:
    """
    Retrieves the last list of EC2 instances from the application state.
    """
    return session_app_state.get('last_listed_instances')
