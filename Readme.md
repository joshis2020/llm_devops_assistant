# LLM-Powered DevOps Assistant

A modular assistant powered by LLMs to answer cloud engineering and DevOps queries and perform safe actions on AWS and Kubernetes.

This is a project to understand how LLM can be integrated in the DevOps domain to make the developers life easy.

We want the LLM (Claude via AWS Bedrock) to analyze a simple human prompt in natural language, classify it and there by route the request to the right plugin to help the DevOps assistant take action. The heavy lifting of checking the ec2 instances, getting the pod logs would be done by Boto3 and Kubernetes clients.

## 🔍 Features
- Ask natural language questions like:
  - "Which EC2 instances are stopped?"
  - "Restart pods in crashloop in dev namespace."
  - "Show today's AWS cost."
  - "Summarise the logs for the pod nginx"
- CLI and optional FastAPI interface
- Modular plugin-based architecture

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`
- AWS credentials configured (for `boto3`)
- K8s context set (for `kubernetes` Python client)

### Run (CLI):
```bash
python assistant/main.py "Which EC2s are stopped?"
```

### Run (API):
```bash
uvicorn api.app:app --reload
```

## 📁 Folder Structure
```
llm-devops-assistant/
├── assistant/
│   ├── core.py          # Prompt to plugin logic
│   ├── prompt_templates/
│   └── router.py        # Dispatch to plugin
├── plugins/             # Individual task handlers
│   ├── ec2_plugin.py
│   ├── k8s_plugin.py
│   └── cost_plugin.py
|   └── logs_plugin.py

├── api/                 # FastAPI app
│   └── app.py
├── requirements.txt
└── README.md
```