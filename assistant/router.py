def route_query(prompt):

    if "ec2" in prompt.lower() and "stopped" in prompt.lower():
        from plugins.ec2_plugin import list_stopped_instances
        return list_stopped_instances()
    return "Sorry, I don't understand that yet."