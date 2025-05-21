# assistant/router.py

from assistant.llm_client import classify_intent

def route_query(prompt: str):
    intent = classify_intent(prompt)

    if intent == "list_stopped_instances":
        from plugins.ec2_plugin import EC2Plugin
        return EC2Plugin().execute(intent)

    if intent == "restart_crashloop_pods":
        from plugins.k8s_plugin import K8sPlugin
        return K8sPlugin().execute(intent)

    if intent == "get_daily_cost":
        from plugins.cost_plugin import CostPlugin
        return CostPlugin().execute(intent)

    if intent == "summarize_logs":
        from plugins.logs_plugin import LogsPlugin
        return LogsPlugin().execute(intent)

    return f"Unknown intent: {intent}"
