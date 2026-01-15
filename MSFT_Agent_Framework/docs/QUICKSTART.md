# MSFT Agent Framework - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd MSFT_Agent_Framework
pip install -r requirements.txt
```

### 2. Login to Azure
```bash
az login --identity
```

### 3. Get Your Credentials from Azure AI Foundry

**Project Endpoint:**
- Go to [ai.azure.com](https://ai.azure.com) → Your Project → Settings
- Copy the "Project Endpoint"

**Agent ID:**
- Go to Agents → Select your agent
- Copy the Agent ID (starts with `asst_`)

### 4. Update the Script
Open `foundry_agent_starter.py` and replace:

```python
PROJECT_ENDPOINT = "YOUR_PROJECT_ENDPOINT_HERE"  # ← Your endpoint
AGENT_ID = "YOUR_AGENT_ID_HERE"                  # ← Your agent ID
```

### 5. Connect Application Insights (Required for Tracing)
1. Go to [ai.azure.com](https://ai.azure.com) → Your Project
2. Select **Monitoring** → **Application analytics** tab
3. Create or connect an Application Insights resource

> 📖 [Full instructions](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/monitor-applications?view=foundry-classic)

### 6. Enable Tracing
Uncomment this line:
```python
await client.configure_azure_monitor(enable_live_metrics=True)
```

### 7. Run It
```bash
python foundry_agent_starter.py
```

### 8. View Traces
Azure AI Foundry → Monitoring → Application analytics → See your agent calls!

---

## Exercise Summary

| Exercise | Task | Time |
|----------|------|------|
| 1 | Install dependencies | 2 min |
| 2 | Configure endpoint & agent ID | 5 min |
| 3 | Enable OpenTelemetry tracing | 5 min |
| **Total** | | **~12 min** |
