# Microsoft Agent Framework Workshop

## Overview
This workshop module teaches participants how to integrate Azure AI Foundry agents into Python applications using the Microsoft Agent Framework. Participants will learn to pull their existing Foundry agents into code and configure OpenTelemetry tracing for monitoring.

## Learning Objectives
By the end of this module, participants will be able to:
- Connect to an existing Azure AI Foundry agent from Python code
- Understand the Agent Framework architecture and components
- Configure Azure Monitor OpenTelemetry tracing
- Monitor agent performance through Application Insights

## Prerequisites
- **Completed**: Azure AI Foundry Agents workshop (you should have a working agent)
- Python 3.10+
- Azure CLI installed and logged in (`az login --identity --identity`)
- Access to your Azure AI Foundry project

## Time Estimate
**25-35 minutes**

---

## Workshop Flow

### Exercise 1: Environment Setup (5 mins)

#### Step 1.1: Create a Virtual Environment
Navigate to the workshop folder and create a Python virtual environment:

```bash
cd MSFT_Agent_Framework
python -m venv .venv
```

Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt.

#### Step 1.2: Install Dependencies
Install the required packages:

```bash
pip install -r requirements.txt
```

The key packages are:
| Package | Purpose |
|---------|---------|
| `agent-framework` | Microsoft's Agent Framework for building agent applications |
| `azure-ai-projects` | Client library for Azure AI Foundry projects |
| `azure-identity` | Azure authentication (CLI, managed identity, etc.) |
| `azure-monitor-opentelemetry` | OpenTelemetry integration with Azure Monitor |

#### Step 1.3: Verify Azure CLI Login
Ensure you're logged into Azure CLI:

```bash
az login --identity --identity
az account show
```

Confirm you're using the correct subscription where your Foundry project exists.

---

### Exercise 2: Configure Your Foundry Connection (10 mins)

Open `foundry_agent_starter.py` in your editor. You'll complete three TODO sections.

#### Step 2.1: Get Your Project Endpoint

1. Navigate to [Azure AI Foundry](https://ai.azure.com)
2. Open your project (created in the previous workshop)
3. Go to **Project Overview** 
4. Find **Project Endpoint** - it looks like:
   ```
   https://<account-name>.services.ai.azure.com/api/projects/<project-name>
   ```
5. Copy this endpoint

In `foundry_agent_starter.py`, replace the placeholder:

```python
# BEFORE
PROJECT_ENDPOINT = "YOUR_PROJECT_ENDPOINT_HERE"

# AFTER (example)
PROJECT_ENDPOINT = "https://agent-workshop.services.ai.azure.com/api/projects/agent-workshop-project"
```

#### Step 2.2: Get Your Agent ID

1. In Azure AI Foundry, navigate to **Agents**
2. Click on your **Contoso Sales Agent** (or the agent you created)
3. Look for the **Agent ID** - it starts with `asst_` followed by alphanumeric characters
4. Copy this ID

In `foundry_agent_starter.py`, replace the placeholder:

```python
# BEFORE
AGENT_ID = "YOUR_AGENT_ID_HERE"

# AFTER (example)
AGENT_ID = "asst_RAaC0bqdGcOGJT34ysxP2tvq"
```

#### Step 2.3: Test the Connection

Run the script to verify your configuration:

```bash
python foundry_agent_starter.py
```

**Expected output:**
```
🚀 Connecting to Azure AI Foundry Agent...
📝 Make sure you've completed Exercises 1 & 2 (endpoint + agent ID)

✓ Connected to agent: asst_RAaC0bqdGcOGJT34ysxP2tvq

============================================================
💬 Interactive Chat Mode
============================================================
Chat with your Contoso Sales Agent
Type 'exit', 'quit', or 'q' to end
============================================================

You: 
```

Try asking questions like:
- "What tents do you offer?"
- "Tell me about your camping gear"
- "What's the best tent for winter camping?"

Type `exit` to quit the chat.

**Troubleshooting:**
- `AuthenticationError`: Run `az login --identity --identity` again
- `ResourceNotFound`: Double-check your PROJECT_ENDPOINT
- `Agent not found`: Verify your AGENT_ID is correct

---

### Exercise 3: Enable OpenTelemetry Tracing (10 mins)

Now let's add monitoring capabilities to track your agent's performance.

#### Step 3.1: Connect Application Insights to Your Foundry Project

Before your code can send traces, you need to connect an Application Insights resource to your Foundry project.

> 📖 **Reference**: [Monitor your generative AI applications](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/monitor-applications?view=foundry-classic)

1. Navigate to [Azure AI Foundry](https://ai.azure.com) and open your project
2. Select **Monitoring** in the left navigation pane
3. Click on the **Application analytics** tab
4. If you don't have an Application Insights resource connected:
   - Click **Create new** to create a new Application Insights resource
   - Or select an existing Application Insights resource from your subscription
5. Click **Connect** to link the resource to your Foundry project

![Application Insights Setup](https://learn.microsoft.com/en-us/azure/ai-foundry/media/how-to/monitor-applications/customize-dashboard-2.png)

> **Note:** This step only needs to be done once per project. Once connected, all traces from your applications will flow to this Application Insights instance.

#### Step 3.2: Understanding the Tracing Architecture

The Agent Framework integrates with Azure Monitor through OpenTelemetry:

```
┌─────────────────┐     ┌─────────────────┐     ┌────────────────────┐
│  Your Agent     │────▶│  OpenTelemetry  │────▶│ Application        │
│  Application    │     │  SDK            │     │ Insights           │
└─────────────────┘     └─────────────────┘     └────────────────────┘
                                                         │
                                                         ▼
                                                ┌────────────────────┐
                                                │ Azure AI Foundry   │
                                                │ Monitoring Tab     │
                                                └────────────────────┘
```

#### Step 3.3: Enable Tracing

In `foundry_agent_starter.py`, find the Exercise 3 section and **uncomment** the tracing line:

```python
# BEFORE
# await client.configure_azure_monitor(enable_live_metrics=True)

# AFTER
await client.configure_azure_monitor(enable_live_metrics=True)
```

#### Step 3.4: Run with Tracing Enabled

Run the script again:

```bash
python foundry_agent_starter.py
```

The output will be the same, but now traces are being sent to Azure Monitor.

#### Step 3.5: View Traces in Azure AI Foundry

1. Go to [Azure AI Foundry](https://ai.azure.com)
2. Open your project
3. Navigate to **Tracing** (in the left sidebar under "Evaluate and improve")
4. You should see your recent agent invocations with:
   - Latency metrics
   - Token usage
   - Request/response details (if sensitive data logging is enabled)

> **Note:** Traces may take 1-2 minutes to appear in the portal.

---

### Exercise 4: Enable Conversation Threading (5 mins)

By default, each message to the agent is independent. To enable multi-turn conversations where the agent remembers context, you need to create a thread.

#### Step 4.1: Create a Thread

In `foundry_agent_starter.py`, find the Exercise 4 section and **uncomment** the thread creation line:

```python
# BEFORE
# thread = agent.get_new_thread()

# AFTER
thread = agent.get_new_thread()
```

#### Step 4.2: Pass the Thread to agent.run()

Find the `agent.run()` call and update it to pass the thread:

```python
# BEFORE
result = await agent.run(user_input)

# AFTER
result = await agent.run(user_input, thread=thread)
```

#### Step 4.3: Test Conversation Memory

Run the script and test multi-turn conversations:

```bash
python foundry_agent_starter.py
```

Try this conversation:
```
You: What tents do you offer?
🤖 Assistant: [Lists tents...]

You: Which one is best for winter?
🤖 Assistant: [Recommends based on previous context...]

You: How does it compare to competitor's winter tents?
🤖 Assistant: [Knows you're asking about the winter tent...]
```

Without threading, the agent wouldn't know what "it" refers to in the third question!

---

## Understanding the Code

### Key Components Explained

```python
async with (
    # 1. Authentication - uses your Azure CLI credentials
    AzureCliCredential() as credential,
    
    # 2. Project Client - connects to your Foundry project
    AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential) as project_client,
    
    # 3. Azure AI Client - agent framework wrapper
    AzureAIClient(project_client=project_client) as client,
    
    # 4. Your Agent - references your Foundry agent by ID
    ChatAgent(
        chat_client=AzureAIAgentClient(
            credential=credential,
            agent_id=AGENT_ID
        ),
        name="FoundryAgent",
    ) as agent,
):
```

### Why Use the Agent Framework?

| Feature | Direct API | Agent Framework |
|---------|-----------|-----------------|
| Authentication | Manual setup | Built-in |
| Tracing | Manual OpenTelemetry | One-line config |
| Error handling | Custom | Built-in retries |
| Async support | Varies | Native async |
| Multi-agent | Complex | Simplified |

---

## Exercise Checklist

- [ ] Installed requirements (`pip install -r requirements.txt`)
- [ ] Configured `PROJECT_ENDPOINT` with your Foundry endpoint
- [ ] Configured `AGENT_ID` with your agent's ID
- [ ] Successfully ran the script and started chatting with the agent
- [ ] Enabled OpenTelemetry tracing (`configure_azure_monitor`)
- [ ] Viewed traces in Azure AI Foundry portal
- [ ] Enabled conversation threading (`get_new_thread()` and `thread=thread`)

---

## Next Steps
After completing this workshop, you can:
- Explore the **Multi-Agent Workshop** to orchestrate multiple agents
- Learn about the **MCP (Model Context Protocol)** for tool integration
- Build production applications with proper error handling and monitoring

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: agent_framework` | Run `pip install -r requirements.txt` |
| `AuthenticationError` | Run `az login --identity` and select correct subscription |
| `ResourceNotFoundError` | Verify PROJECT_ENDPOINT is correct |
| `Agent not found` | Verify AGENT_ID exists in your Foundry project |
| Traces not appearing | Wait 1-2 minutes, refresh the Tracing page |

### Getting Help
- Check the Agent Framework documentation
- Review Azure AI Foundry docs at [learn.microsoft.com](https://learn.microsoft.com)
- Ask your facilitator for assistance

---

## Files in This Module

| File | Purpose |
|------|---------|
| `foundry_agent_starter.py` | Workshop starter script (complete the TODOs) |
| `foundry_agent.py` | Completed solution for reference |
| `requirements.txt` | Python dependencies |
| `README.md` | This workshop guide |
