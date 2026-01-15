# Azure AI Agent Workshop

Welcome to the **Azure AI Agent Workshop**! This hands-on training teaches you how to build intelligent agents using Azure AI Foundry and extend them with custom tools via Model Context Protocol (MCP).

## 🎯 Workshop Overview

This workshop is divided into four complementary modules:

### **Module 1: Azure AI Foundry Agents** (Portal Experience)
Learn to create agents in Azure AI Foundry portal using no-code/low-code approaches.
- **Duration:** ~75 minutes
- **Level:** Beginner to Intermediate
- **Focus:** Agent creation, knowledge grounding, tool integration

### **Module 2: Microsoft Agent Framework** (Code Introduction)
Learn to connect your Foundry agent to Python code and configure tracing.
- **Duration:** ~30 minutes
- **Level:** Beginner to Intermediate
- **Focus:** Agent Framework basics, OpenTelemetry tracing, conversation threading

### **Module 3: Model Context Protocol (MCP)** (Custom Tools)
Learn to connect MCP tools with Microsoft Agent Framework and Azure AI Foundry agents.
- **Duration:** ~90 minutes
- **Level:** Intermediate
- **Focus:** MCP integration with Foundry, Agent Framework, custom tool development

### **Module 4: Multi-Agent Orchestration** (Advanced Workflows)
Learn to coordinate multiple AI agents using Microsoft Agent Framework orchestration patterns.
- **Duration:** ~60 minutes
- **Level:** Intermediate to Advanced
- **Focus:** Group chat, sequential pipelines, handoff routing, agent collaboration

## 📚 What You'll Build

### Contoso Sales Agent (Module 1)
A customer-facing agent that:
- ✅ Provides product information from internal catalogs
- ✅ Gathers competitive intelligence from the web
- ✅ Answers customer questions with friendly, professional responses

### Agent Framework Integration (Module 2)
Connect your Foundry agent to Python code:
- ✅ Pull your agent from Azure AI Foundry into code
- ✅ Configure OpenTelemetry tracing with Azure Monitor
- ✅ View traces and monitor agent performance
- ✅ Enable conversation threading for multi-turn chats
- ✅ Build interactive chatbot experiences

### Custom MCP Tools (Module 3)
Build custom tools with Model Context Protocol (separate agent):
- ✅ Create custom MCP servers with specialized tools
- ✅ Build a new agent with MCP tool integration
- ✅ Use Microsoft Agent Framework for orchestration
- ✅ Test and debug MCP-Foundry integration locally
- ✅ Deploy production-ready agent workflows

### Multi-Agent Orchestrations (Module 4)
Coordinate multiple AI agents for complex workflows:
- ✅ Build collaborative research teams with group chat
- ✅ Create sequential processing pipelines
- ✅ Implement dynamic agent handoff for customer support
- ✅ Design agents with specialized tools and expertise
- ✅ Manage multi-turn conversations with approval workflows

## 🚀 Getting Started

### Prerequisites
- **Azure subscription** with permissions to create resources
- **Python 3.10+** (for Module 2)
- **Azure CLI** (for Module 2)
- **Basic Python knowledge** (for Module 2)

### Workshop Flow

```
┌─────────────────────────────────────────────────────┐
│  Module 1: Azure AI Foundry Agents (Portal)        │
│  ├─ Exercise 1: Create agent & project (20 min)    │
│  ├─ Exercise 2: Add File Search tool (20 min)      │
│  ├─ Exercise 3: Add Bing Grounding (25 min)        │
│  └─ Exercise 4: Test & experiment (10 min)         │
└─────────────────┬───────────────────────────────────┘
                  │ Your agent is ready!
                  ▼
┌─────────────────────────────────────────────────────┐
│  Module 2: MSFT Agent Framework (Code Intro)       │
│  ├─ Exercise 1: Environment setup (5 min)          │
│  ├─ Exercise 2: Connect to Foundry agent (10 min)  │
│  ├─ Exercise 3: Enable tracing (10 min)            │
│  └─ Exercise 4: Conversation threading (5 min)     │
└─────────────────┬───────────────────────────────────┘
                  │ Agent in code with tracing!
                  ▼
┌─────────────────────────────────────────────────────┐
│  Module 3: Model Context Protocol (Custom Tools)   │
│  ├─ Exercise 1: Setup & local testing (30 min)     │
│  ├─ Exercise 2: Create MCP server (30 min)         │
│  ├─ Exercise 3: Connect to agent (20 min)          │
│  └─ Exercise 4: Test integration (10 min)          │
└─────────────────┬───────────────────────────────────┘
                  │ Add custom tools!
                  ▼
┌─────────────────────────────────────────────────────┐
│  Module 4: Multi-Agent Orchestration (Advanced)    │
│  ├─ Demo 1: Group chat orchestration (20 min)      │
│  ├─ Demo 2: Sequential pipelines (15 min)          │
│  ├─ Demo 3: Handoff routing (20 min)               │
│  └─ Experiment: Customize workflows (5 min)        │
└─────────────────────────────────────────────────────┘
```

## 📖 Module Details

### Module 1: Azure AI Foundry Agents

**Location:** [`Azure_AI_Foundry_Agents/`](Azure_AI_Foundry_Agents/)

**What you'll learn:**
- Creating Foundry projects and agents in the portal
- Using the **File Search tool** to ground agents in documents
- Adding **Bing Grounding** for real-time web intelligence
- Writing effective agent instructions
- Understanding knowledge tools vs. action tools
- Progressive agent enhancement workflow

**Key Files:**
- [README.md](Azure_AI_Foundry_Agents/README.md) - Complete workshop guide
- [QUICKSTART.md](Azure_AI_Foundry_Agents/docs/QUICKSTART.md) - Quick reference
- [FACILITATOR_GUIDE.md](Azure_AI_Foundry_Agents/docs/FACILITATOR_GUIDE.md) - Teaching guide

**Start Here:** [Azure_AI_Foundry_Agents/README.md](Azure_AI_Foundry_Agents/README.md)

---

### Module 2: Microsoft Agent Framework

**Location:** [`MSFT_Agent_Framework/`](MSFT_Agent_Framework/)

**What you'll learn:**
- Connecting to Foundry agents from Python code
- Using the **Microsoft Agent Framework** library
- Configuring **OpenTelemetry tracing** with Azure Monitor
- Viewing traces in Azure AI Foundry portal
- Managing **conversation threading** for multi-turn chats
- Building interactive chatbot experiences

**Key Files:**
- [README.md](MSFT_Agent_Framework/README.md) - Complete workshop guide
- [foundry_agent_starter.py](MSFT_Agent_Framework/foundry_agent_starter.py) - Workshop starter script
- [foundry_agent.py](MSFT_Agent_Framework/foundry_agent.py) - Completed solution
- [docs/QUICKSTART.md](MSFT_Agent_Framework/docs/QUICKSTART.md) - Quick reference

**Start Here:** [MSFT_Agent_Framework/README.md](MSFT_Agent_Framework/README.md)

---

### Module 3: Model Context Protocol (MCP)

**Location:** [`MCP/`](MCP/)

**What you'll learn:**
- Understanding Model Context Protocol (MCP) specification
- Integrating MCP tools with **Microsoft Agent Framework**
- Building custom MCP servers with Python
- Connecting MCP servers to **Azure AI Foundry agents**
- Using Agent Framework to orchestrate MCP tools
- Testing MCP-Foundry integration locally before deployment
- Leveraging Managed Identity for secure authentication
- Best practices for production MCP deployments with Foundry

**Key Files:**
- [README.md](MCP/README.md) - Complete workshop guide
- [QUICKSTART.md](MCP/QUICKSTART.md) - 5-minute setup
- [INDEX.md](MCP/INDEX.md) - Navigation guide
- [server.py](MCP/server.py) - MCP server implementation
- [test_mcp.py](MCP/test_mcp.py) - Local testing client
- [get_agent_mi.py](MCP/get_agent_mi.py) - Agent connection code

**Start Here:** [MCP/README.md](MCP/README.md)

---

### Module 4: Multi-Agent Orchestration

**Location:** [`Multi_Agent_Demo/`](Multi_Agent_Demo/)

**What you'll learn:**
- Understanding **orchestration patterns** for multi-agent systems
- Building **group chat** workflows for collaborative tasks
- Creating **sequential pipelines** for step-by-step processing
- Implementing **handoff patterns** for dynamic agent routing
- Designing agents with specialized tools and expertise
- Managing **Human-in-the-Loop** (HITL) approval workflows
- Using custom executors for non-LLM processing
- Best practices for multi-agent coordination

**Three Complete Demos:**
1. **Group Chat** - Collaborative research team (Researcher, Writer, FactChecker)
2. **Sequential** - Content pipeline (Writer → Reviewer → Editor)
3. **Handoff** - Customer support routing (Triage → Specialists)

**Key Files:**
- [README.md](Multi_Agent_Demo/README.md) - Complete demo guide
- [Group_Chat/agent_groupchat.py](Multi_Agent_Demo/Group_Chat/agent_groupchat.py) - Group chat demo
- [Sequential/agent_sequential.py](Multi_Agent_Demo/Sequential/agent_sequential.py) - Sequential demo
- [Handoff/agent_handoff.py](Multi_Agent_Demo/Handoff/agent_handoff.py) - Handoff demo

**Start Here:** [Multi_Agent_Demo/README.md](Multi_Agent_Demo/README.md)

---

## 🎓 Learning Path

### Recommended Order

**Complete All Modules (Recommended):**
1. Start with **Module 1** to understand agents in the portal
2. Create your agent with File Search and Bing Grounding
3. Proceed to **Module 2** to connect your agent to Python code with tracing
4. Continue to **Module 3** to learn MCP custom tool development (creates separate agent)
5. Explore **Module 4** to learn multi-agent orchestration patterns
6. Build collaborative agent systems with specialized roles

**Portal Experience Only:**
- Complete **Module 1** for no-code/low-code agent creation
- Perfect for business users, product managers, and beginners

**Code Introduction:**
- Complete **Module 1** then **Module 2** for a gentle intro to Agent Framework
- Learn to pull agents into code and configure tracing
- Great stepping stone before MCP or Multi-Agent modules

**Developer Deep-Dive:**
- Skip to **Module 3** if you already have a Foundry agent and understand Agent Framework
- Focuses on custom tool development with MCP
- Best for developers and engineers

**Advanced Orchestration:**
- Jump to **Module 4** if you understand Agent Framework basics
- Learn group chat, sequential, and handoff patterns
- Ideal for architects designing complex agent systems

## 📊 Workshop Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Azure AI Foundry Platform                      │
│                                                             │
│  ┌──────────────────────────────┐  ┌──────────────────────┐│
│  │   Contoso Sales Agent       │  │    MCP Demo Agent    ││
│  │   (Modules 1 & 2)           │  │    (Module 3)        ││
│  └────────────┬────────────────┘  └──────────┬───────────┘│
│               │                              │             │
│    ┌──────────▼────────┐      ┌─────────────▼──────────┐  │
│    │  Built-in Tools   │      │   Custom MCP Tools     │  │
│    ├───────────────────┤      ├────────────────────────┤  │
│    │ • File Search     │      │ • MCP Server           │  │
│    │ • Bing Grounding  │      │ • Custom Functions     │  │
│    │ • Code Interpreter│      │ • Local Testing        │  │
│    └───────────────────┘      └────────────────────────┘  │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │       Multi-Agent Orchestration (Module 4)         │   │
│  │  • Group Chat  • Sequential  • Handoff Patterns    │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Setup Instructions

### Module 1 Setup (5 minutes)
```bash
# No local setup required!
# Just navigate to Azure AI Foundry portal
https://ai.azure.com
```

### Module 2 Setup (5 minutes)
```bash
# Navigate to MSFT Agent Framework directory
cd MSFT_Agent_Framework/

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Login to Azure
az login --identity 
```

### Module 3 Setup (10 minutes)
```bash
# Navigate to MCP directory
cd MCP/

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt --pre

# Login to Azure (for authentication)
az login --identity

# Or use managed identity (for Azure ML workspace)
az login --identity --identity
```

### Module 4 Setup (10 minutes)
```bash
# Navigate to Multi_Agent directory
cd Multi_Agent_Workshop/

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (create .env file)
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o

# Login to Azure (for authentication)
az login --identity

# Or use managed identity (for Azure ML workspace)
az login --identity --identity
```

## 📚 Additional Resources

### Official Documentation
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Foundry Agents Quickstart](https://learn.microsoft.com/azure/ai-foundry/agents/quickstart)
- [Using MCP with Foundry Agents](https://learn.microsoft.com/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP for Beginners (Microsoft)](https://github.com/microsoft/mcp-for-beginners)
- [Orchestration Patterns Overview](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/overview)
- [Group Chat Orchestration](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/group-chat)
- [Sequential Orchestration](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/sequential)
- [Handoff Orchestration](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/handoff)

### Workshop References
- [Azure AI Foundry Tools Overview](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools-classic/overview)
- [Azure AI Foundry Agent Types](https://learn.microsoft.com/agent-framework/user-guide/agents/agent-types/azure-ai-foundry-agent)
- [Using MCP with Foundry Agents](https://learn.microsoft.com/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents)
- [Microhack: Agentic AI](https://github.com/Boykai/octo-microhack-agentic-ai)

## 🤝 Workshop Support

### During the Workshop
- **Ask questions** - Facilitators are here to help!
- **Share discoveries** - Learn from each other
- **Experiment freely** - Break things and fix them

### Common Issues & Solutions

**Module 1:**
- **Can't create project?** → Check Azure subscription permissions
- **File upload fails?** → Verify file size (max 512MB)
- **Agent not using tools?** → Ensure tools are enabled and instructions reference them

**Module 2:**
- **Python dependency errors?** → Ensure Python 3.10+ and virtual environment activated
- **Authentication fails?** → Run `az login --identity` (or `az login --identity --identity` in Azure ML workspace)
- **MCP server won't start?** → Check port 5000 is available

**Module 3:**
- **Azure OpenAI errors?** → Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
- **Agent not responding?** → Check deployment quota and throttling limits
- **Import errors?** → Install agent-framework: `pip install agent-framework`
- **Authentication fails?** → Run `az login --identity` (or `az login --identity --identity` in Azure ML workspace)

See individual module READMEs for detailed troubleshooting.

## 🎯 Learning Outcomes

By the end of this workshop, you will:
- ✅ Understand Azure AI Foundry agent architecture
- ✅ Know when to use built-in vs. custom MCP tools
- ✅ Create agents using both portal and code approaches
- ✅ Integrate MCP tools with **Microsoft Agent Framework**
- ✅ Connect MCP servers to **Azure AI Foundry agents**
- ✅ Write effective agent instructions for tool selection
- ✅ Build and test custom MCP servers
- ✅ Use Agent Framework for MCP orchestration
- ✅ Test and debug MCP-Foundry integration
- ✅ Understand authentication patterns (Managed Identity, Azure CLI, Azure ML workspace)
- ✅ Design and implement **multi-agent orchestration** patterns
- ✅ Build **group chat**, **sequential**, and **handoff** workflows
- ✅ Create agents with specialized tools and expertise
- ✅ Implement Human-in-the-Loop (HITL) approval workflows
- ✅ Coordinate multiple agents for complex real-world scenarios

## 📝 Feedback

We value your feedback! After completing the workshop, please share:
- What worked well?
- What was confusing?
- What would you like to see added?
- How was the pacing?

## 📄 License

This workshop content is provided for educational purposes.

---

## 🚦 Next Steps

**Ready to start?**

1. **Begin with Module 1:** [Azure_AI_Foundry_Agents/README.md](Azure_AI_Foundry_Agents/README.md)
2. **Continue to Module 2:** [MCP/README.md](MCP/README.md)
3. **Explore Module 3:** [Multi_Agent_Demo/README.md](Multi_Agent_Demo/README.md)

**Have an existing agent?**
- Jump straight to: [MCP/README.md](MCP/README.md)

**Want to learn multi-agent patterns?**
- Skip to: [Multi_Agent_Demo/README.md](Multi_Agent_Demo/README.md)

**Questions before starting?**
- Review [Azure_AI_Foundry_Agents/docs/QUICKSTART.md](Azure_AI_Foundry_Agents/docs/QUICKSTART.md)
- Check [MCP/QUICKSTART.md](MCP/QUICKSTART.md)
- See [Multi_Agent_Demo/README.md](Multi_Agent_Demo/README.md)

---

### Happy Building! 🚀
