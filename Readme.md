# LLM-Powered DevOps Assistant

A modular assistant powered by LLMs to answer cloud engineering and DevOps queries and perform safe actions on AWS and Kubernetes.

## 🔍 Features
- Ask natural language questions like:
  - "Which EC2 instances are stopped?"
  - "Restart pods in crashloop in dev namespace."
  - "Show today's AWS cost."
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
    └── logs_plugin.py

├── api/                 # FastAPI app
│   └── app.py
├── requirements.txt
└── README.md
```