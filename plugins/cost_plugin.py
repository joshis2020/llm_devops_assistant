import boto3
from datetime import datetime, timedelta
from plugins.base_plugin import BasePlugin

class CostPlugin(BasePlugin):
    def match(self, prompt: str) -> bool:
        return "cost" in prompt.lower() and "report" in prompt.lower()


    def execute(self, prompt: str) -> str:
        ce = boto3.client("ce")
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": str(yesterday), "End": str(today)},
            Granularity="DAILY",
            Metrics=["UnblendedCost"]
        )
        amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
        return f"Yesterday's AWS cost: ${float(amount):.2f}"

