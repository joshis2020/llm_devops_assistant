# config.py
import os

# AWS Configuration
# Set your AWS region via environment variable, e.g., export AWS_REGION="us-east-1"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Bedrock LLM Configuration
# Set your Bedrock model ID via environment variable, e.g., export BEDROCK_MODEL_ID="anthropic.claude-3-5-sonnet-20240620-v1:0"
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# You can add other configurations here, like API keys if not using environment variables
# (though environment variables are generally recommended for sensitive info)s