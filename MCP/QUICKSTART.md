# Quick Start Guide - MCP Workshop

## 🚀 Getting Started in 5 Minutes

### 1️⃣ Setup Virtual Environment & Install Dependencies (2 min)

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Azure ML Notebooks

# Install dependencies
cd /path/to/ERM_Agents_Workshop/MCP
pip install -r requirements.txt --pre

# Authenticate with Azure (Managed Identity)
az login --identity
```

### 2️⃣ Start the MCP Server (30 seconds)

**Terminal 1:**
```bash
# Make sure venv is activated
source .venv/bin/activate
python server.py
```

✅ You should see: "Server is running... (Press CTRL+C to stop)"

### 3️⃣ Test the Server Locally (1 min)

**Terminal 2 (new terminal):**
```bash
source .venv/bin/activate
python test_mcp.py
```

✅ You should see: List of tools and test results

### 4️⃣ Configure Azure Settings (1 min)

Open [create_agent_mi.py](create_agent_mi.py) and update:
- `AZURE_AI_PROJECT_ENDPOINT` → Your project URL
- `AZURE_AI_MODEL_DEPLOYMENT_NAME` → Your model name

Find these in Azure AI Foundry Studio → Project Settings

### 5️⃣ Run Your First Agent (2 min)

**Make sure Terminal 1 (server) is still running!**

**Terminal 2:**
```bash
source .venv/bin/activate
python create_agent_mi.py
```

Try these prompts:
- `What is 25 + 17?`
- `Calculate 100 minus 45`
- `What is the sum of 12, 8, and 5?`

---

## 📋 Workshop Checklist

Before the workshop, participants should:
- [ ] Have access to Azure ML Notebooks
- [ ] Have Python 3.10+ available in Azure ML
- [ ] Have Azure CLI available in notebook environment
- [ ] Authenticate with `az login --identity`
- [ ] Have access to an Azure AI Foundry project
- [ ] Have a GPT-4o or GPT-4o-mini model deployed
- [ ] Clone this repository to Azure ML workspace
- [ ] Create virtual environment
- [ ] Test that they can run `python server.py` without errors

---

## 🆘 Quick Troubleshooting

### Problem: "Connection refused" error
**Solution:** Make sure `python server.py` is running in another terminal

### Problem: Azure authentication errors
**Solution:** Run `az login --identity` (for Azure ML Notebooks) and verify with `az account show`

### Problem: "Module not found" errors
**Solution:** Run `pip install -r requirements.txt --pre`

### Problem: Port 8080 already in use
**Solution:** 
1. Find what's using port 8080: `netstat -ano | findstr :8080`
2. Stop that process or change the port in both server.py and the agent scripts

---

## 📚 Next Steps

Once you complete the quick start:
1. Read the full [README.md](README.md) for detailed workshop exercises
2. Add your own custom tools to [server.py](server.py)
3. Experiment with different agent instructions
4. Try the advanced exercises

**Need help?** → Check [solutions/SOLUTIONS.md](solutions/SOLUTIONS.md) for examples  
**Teaching this?** → Read [docs/FACILITATOR_GUIDE.md](docs/FACILITATOR_GUIDE.md)

---

## 🎯 Workshop Flow

```
Part 1: Understanding MCP (15 min)
├── Review server.py code
└── Add a custom tool

Part 2: Testing Locally (20 min)
├── Start MCP server
├── Run test_mcp.py
└── Verify tools work

Part 3: Azure Integration (25 min)
├── Create agent with create_agent_mi.py
├── Chat with the agent
└── Observe tool invocations

Part 4: Reusing Agents (20 min)
├── Save agent ID
├── Use get_agent_mi.py
└── Compare create vs retrieve

Part 5: Advanced Topics (20 min)
├── Add custom tools
├── Test with agent
└── Explore resources
```

---

## 👥 Instructor Notes

### Before the Workshop
1. Test all scripts on your machine
2. Have your Azure credentials ready
3. Prepare example custom tools to demonstrate
4. Set up a backup MCP server (in case of network issues)

### During the Workshop
1. Start with `server.py` code walkthrough (don't run yet)
2. Explain MCP concepts before running code
3. Have participants run server first, test second
4. Save agent IDs for each participant
5. Demonstrate live debugging of tool invocations

### Common Workshop Questions
- **Q: Why use MCP instead of direct tool calls?**
  - A: MCP provides standardization, security boundaries, and easy tool discovery

- **Q: Can agents call multiple tools in sequence?**
  - A: Yes! The agent framework handles tool chaining automatically

- **Q: Do we need to restart the server after adding tools?**
  - A: Yes, the server loads tools at startup

- **Q: Can multiple agents share one MCP server?**
  - A: Yes! That's a key benefit of MCP architecture

---

## 🎓 Learning Objectives

By the end of this workshop, participants will be able to:
1. ✅ Explain what MCP is and its benefits
2. ✅ Create and run an MCP server with custom tools
3. ✅ Test MCP servers using the client library
4. ✅ Integrate MCP servers with Azure AI Foundry agents
5. ✅ Create and retrieve agents programmatically
6. ✅ Debug tool invocations and agent reasoning
7. ✅ Extend MCP servers with business-specific tools

---

**Ready to start? Go to [README.md](README.md) for the full workshop!**
