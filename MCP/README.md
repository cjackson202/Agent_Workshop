# Model Context Protocol (MCP) Workshop

## 🎯 Workshop Overview

This hands-on workshop teaches you how to:
1. Create and run a custom MCP server
2. Test MCP tools locally
3. Integrate MCP servers with Azure AI Foundry agents
4. Build extensible AI agents with custom tool capabilities

**Duration:** ~1.5 hours  
**Skill Level:** Intermediate Python

## 📚 Background Resources

This workshop is based on:
- [MCP for Beginners (Microsoft)](https://github.com/microsoft/mcp-for-beginners/tree/main)
- [Azure AI Foundry Agent Types](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/azure-ai-foundry-agent?pivots=programming-language-python)
- [Using MCP with Foundry Agents](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents?pivots=programming-language-python)

## 📋 Prerequisites

### Required Software
- Python 3.10 or higher
- Azure CLI (for authentication)
- Azure ML Notebooks environment
- Azure AI Foundry project (created in Day 2)

### Required Azure Resources
- Azure AI Foundry Project
- GPT-4o or GPT-4o-mini model deployment
- Managed Identity or Azure CLI authentication configured

### Knowledge Prerequisites
- Basic Python programming
- Familiarity with async/await in Python
- Understanding of AI agents (from Day 1 & 2)

## � Directory Structure

```
MCP/
├── README.md              # 👈 Start here! Main workshop guide
├── QUICKSTART.md          # Quick 5-minute setup
├── INDEX.md               # Navigation guide
├── requirements.txt       # Python dependencies
├── server.py              # 🔧 MCP server (you'll run this)
├── test_mcp.py            # 🔧 Local testing client
├── get_agent_mi.py        # 🔧 Connect to your portal agent
├── docs/                  # 📚 Facilitator materials
│   ├── FACILITATOR_GUIDE.md
│   ├── SLIDES_OUTLINE.md
│   ├── WORKSHOP_SUMMARY.md
│   ├── DIAGRAMS.md
│   └── CHEATSHEET.md
├── solutions/             # 💡 Exercise answers (check here if stuck)
│   └── SOLUTIONS.md
└── archive/               # 🗄️ Unused files (ignore these)
    ├── create_agent_sp.py
    └── get_agent_sp.py
```

**Participants:** Focus on files marked with 🔧  
**Facilitators:** See `docs/` folder for teaching materials

## �🚀 Workshop Setup

### Step 1: Create and Activate Virtual Environment

**Important:** We're using Azure ML Notebooks for this workshop. Create a virtual environment first:

```bash
# Navigate to /MCP
cd MCP

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac (Azure ML Notebooks)
# OR
.venv\Scripts\activate  # Windows (if running locally)
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt --pre
```

The `requirements.txt` includes:
- `uvicorn` - ASGI server for running the MCP server
- `mcp[cli]` - Model Context Protocol SDK
- `agent-framework` - Microsoft Agent Framework

### Step 3: Configure Azure Environment

**Authenticate with Azure (Managed Identity):**

Since we're using Azure ML Notebooks, authenticate using managed identity:

```bash
az login --identity
```
***Note***: User object will need the `Azure AI User` role assigned.

**Update Azure Settings:**

1. Open [get_agent_mi.py](get_agent_mi.py)
2. Update these environment variables with your values:

```python
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://YOUR-PROJECT.services.ai.azure.com/api/projects/YOUR-PROJECT-NAME"
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"
```

**Create Your Agent in the Portal:**

1. Go to [Azure AI Foundry Studio](https://ai.azure.com)
2. Navigate to your project
3. Click "Agents" in the left sidebar
4. Click "Create Agent"
5. Configure your agent:
   - **Name:** "Workshop_MCP_Agent" (or your choice)
   - **Instructions:** "You are an intelligent Math Professor at University of Scholars. You are very humorous and friendly. Use the tools provided to you to help users."
   - **Model:** Select your model deployment
6. Click "Create"
7. **Copy the Agent ID** from the agent details page
8. Paste the Agent ID into [get_agent_mi.py](get_agent_mi.py) in the `AGENT_ID` variable

> **Authentication Note:** We're using Azure CLI Managed Identity authentication in Azure ML Notebooks. The `az login --identity` command authenticates using the notebook's managed identity.

---

## 🎓 Workshop Exercises

### Exercise 1: Understanding the MCP Server (15 mins)

**Goal:** Understand how MCP servers expose tools and resources to AI agents.

#### 1.1 Review the Server Code

Open [server.py](server.py) and examine the code:

**Key Components:**
- **MCP Server Initialization:** Creates a FastMCP server with a name and port
- **Tools:** Functions decorated with `@mcp.tool()` that agents can call
  - `add(a, b)` - Adds two numbers
  - `subtract(a, b)` - Subtracts two numbers
- **Resources:** Dynamic content accessed via URI patterns
  - `greeting://{name}` - Personalized greeting resource
- **Transport:** Uses HTTP streamable transport on port 8080

#### 1.2 Customize Your MCP Server

**Task:** Add a new multiplication tool

```python
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers
    
    Args:
        a: Multiplicand number being multiplied
        b: Multiplier number which the multiplicand is multiplied
        
    Returns:
        The product (a * b)
    """
    print('-'*50)
    print(f"Multiply tool being used for product of:")
    print(a)
    print('×')
    print(b)
    print('-'*50)
    return a * b
```

Add this function to [server.py](server.py) after the `subtract` function.

---

### Exercise 2: Running and Testing the MCP Server (20 mins)

**Goal:** Start your MCP server and verify it works locally.

#### 2.1 Start the MCP Server

In your Azure ML Notebook terminal, run:

```bash
# Make sure your virtual environment is activated
cd /path/to/ERM_Agents_Workshop/MCP
python server.py
```

**Expected Output:**
```
Starting MCP server with streamable-http transport
Endpoint: http://0.0.0.0:8080/mcp
Available tools: add, subtract, multiply
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

> **Keep this terminal open!** The server needs to run continuously.

#### 2.2 Test the MCP Server Locally

Open a **new terminal** in Azure ML Notebooks and run the test client:

```bash
# Activate virtual environment in new terminal
source .venv/bin/activate
cd /path/to/ERM_Agents_Workshop/MCP
python test_mcp.py
```

**What the test does:**
1. Connects to your local MCP server
2. Lists all available tools
3. Tests the `add` tool with 5 + 3
4. Tests the `subtract` tool with 5 - 3

**Expected Output:**
```
============================================================
MCP Server Test Client
============================================================
Connecting to: http://localhost:8080/mcp

🔌 Initializing MCP session...
✅ Session initialized successfully

📋 Fetching available tools...
✅ Found 2 tool(s):

1. Tool: add
   Description: Add two numbers
   Input Schema:
      - a (integer): 
      - b (integer): 
   Required: a, b

2. Tool: subtract
   Description: Subtract two numbers
   ...

🧮 Testing 'add' tool (5 + 3)...
✅ Result: 8

🧮 Testing 'subtract' tool (5 - 3)...
✅ Result: 2
```

#### 2.3 Verify Your Changes

If you added the `multiply` tool in Exercise 1.2, you should see it listed in the tools output!

**Checkpoint Questions:**
- ✅ Is your MCP server running without errors?
- ✅ Do you see all tools listed (including multiply if you added it)?
- ✅ Are the test calculations correct?

---

### Exercise 3: Connect Your Portal Agent to MCP (25 mins)

**Goal:** Connect the agent you created in Azure AI Foundry portal to your local MCP server.

#### 3.1 Verify Your Portal Agent

1. Go to [Azure AI Foundry Studio](https://ai.azure.com)
2. Navigate to your project → Agents
3. Confirm your agent is listed
4. Click on your agent to view details
5. **Copy the Agent ID** (starts with "asst_")

#### 3.2 Understand the Connection Script

Review [get_agent_mi.py](get_agent_mi.py):

**Key Components:**
1. **Authentication:** Uses Azure CLI credentials (Managed Identity)
2. **Agent Connection:** Connects to your portal agent by ID
3. **MCP Tool Configuration:** Adds your local ***HTTP*** MCP server to the agent
   ```python
   mcp_tool = MCPStreamableHTTPTool(
       name="Custom MCP Server",
       url="http://localhost:8080/mcp",
       chat_client=chat_client
   )
   ```
4. **Interactive Loop:** Allows you to chat with the agent

#### 3.3 Connect Your Agent to MCP

**Make sure your MCP server is still running**, then in a new terminal:

```bash
# Activate virtual environment
source .venv/bin/activate
cd /path/to/ERM_Agents_Workshop/MCP
python get_agent_mi.py
```

**Expected Output:**
```
✓ MCP tool configured for localhost:8080
✓ Agent connected with MCP tool

============================================================
Interactive Chat Mode - Type 'exit', 'quit', or 'q' to end
============================================================

You: 
```

#### 3.3 Test Your Agent

Try these prompts to see your agent use the MCP tools:

**Test 1: Simple Math**
```
You: What is 15 + 27?
```

**Test 2: Multi-Step Calculation**
```
You: Calculate (100 + 50) - 25
```

**Test 3: Your Custom Tool** (if you added multiply)
```
You: What is 7 times 8?
```

**Observe the Server Logs:**
- Switch back to your server terminal
- Watch the tool invocations print in real-time
- See which tools the agent chooses to use

#### 3.4 Understanding the Flow

```
User Input → Azure AI Agent → MCP Server (localhost:8080) → Tool Execution → Result → Agent Response
```

**Key Observations:**
- The agent automatically selects which tool to use
- Multiple tool calls can be chained together
- The MCP server logs show when tools are invoked
- Results are integrated into the agent's response

---

### Exercise 4: Advanced Customization (20 mins)

**Goal:** Extend your MCP server with real-world capabilities.

#### 5.1 Add a Weather Tool (Example)

Add this tool to [server.py](server.py):

```python
@mcp.tool()
def get_temperature_advice(temperature: int) -> str:
    """Get clothing advice based on temperature in Fahrenheit"""
    print('-'*50)
    print(f"Temperature advice requested for: {temperature}°F")
    print('-'*50)
    
    if temperature < 32:
        return "It's freezing! Wear a heavy coat, gloves, and a hat."
    elif temperature < 50:
        return "It's cold. A jacket and long pants are recommended."
    elif temperature < 70:
        return "It's mild. A light sweater or long sleeves would be good."
    elif temperature < 85:
        return "It's warm. T-shirt and shorts weather!"
    else:
        return "It's hot! Stay hydrated and wear light clothing."
```

**After adding:**
1. Restart your MCP server (Ctrl+C, then `python server.py`)
2. Restart your agent script (`python get_agent_mi.py`)
3. Try: `"What should I wear if it's 45 degrees?"`

#### 4.2 Challenge: Add Your Own Tool

**Ideas for custom tools:**
- `calculate_percentage(value, total)` - Calculate percentage
- `convert_currency(amount, from_currency, to_currency)` - Currency converter (mock data)
- `validate_email(email)` - Email format validator
- `generate_password(length)` - Password generator

**Requirements:**
- Must have clear input parameters with type hints
- Must return a useful result
- Must include a descriptive docstring
- Should include helpful debug logging

#### 4.3 Test Your Custom Tool

1. Add your tool to [server.py](server.py)
2. Restart the MCP server
3. Run `python test_mcp.py` to verify it appears in the tool list
4. Test it with your agent using natural language prompts

---

## 🎯 Workshop Checkpoints

By the end of this workshop, you should be able to:

- ✅ **Explain** what MCP is and why it's useful for AI agents
- ✅ **Create** a custom MCP server with tools and resources
- ✅ **Test** MCP servers locally using the test client
- ✅ **Integrate** MCP servers with Azure AI Foundry agents
- ✅ **Retrieve** and reuse existing agents
- ✅ **Extend** MCP servers with custom business logic

---

## 📁 Workshop Files Reference

| File | Purpose | When to Use |
|------|---------|------------|
| [server.py](server.py) | MCP server with tools and resources | Main server to run and customize |
| [test_mcp.py](test_mcp.py) | Local MCP client test | Verify server works before agent integration |
| [get_agent_mi.py](get_agent_mi.py) | Connect to portal agent with MCP | Connect your portal-created agent to MCP server |
| [requirements.txt](requirements.txt) | Python dependencies | Initial setup |

---

## 🐛 Troubleshooting

### Issue: "Connection refused" when testing MCP

**Solution:**
- Ensure `python server.py` is running in a separate terminal
- Check that port 8080 is not blocked by firewall
- Verify the URL is `http://localhost:8080/mcp`

### Issue: Azure authentication errors

**Solution:**
```bash
# For Azure ML Notebooks (Managed Identity)
az login --identity
az account show  # Verify correct subscription
```

### Issue: Agent not finding tools

**Solution:**
- Restart MCP server after adding new tools
- Check server logs for errors
- Verify tool is decorated with `@mcp.tool()`
- Ensure docstring is present (required for tool description)

### Issue: "Module not found" errors

**Solution:**
```powershell
pip install -r requirements.txt --pre
```

The `--pre` flag ensures pre-release versions are installed, which is required for the agent-framework.

---

## 🎓 Next Steps

### After This Workshop

1. **Integrate with Real APIs**: Replace mock tools with actual API calls
2. **Add Authentication**: Secure your MCP server with API keys
3. **Deploy to Azure**: Host your MCP server in Azure Container Apps or App Service
4. **Monitor and Log**: Add structured logging and monitoring
5. **Multi-Agent Scenarios**: Connect multiple agents to the same MCP server

### Advanced Topics to Explore

- **MCP Resources**: Dynamic content accessible via URI patterns
- **Streaming Responses**: Real-time tool execution updates
- **Tool Chaining**: Complex multi-step reasoning workflows
- **Error Handling**: Graceful failure and retry mechanisms
- **Security**: Authentication, authorization, and input validation

---

## 📖 Additional Resources

### Documentation
- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/microsoft/mcp-for-beginners)
- [Azure Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)

### Sample Projects
- [MCP for Beginners (GitHub)](https://github.com/microsoft/mcp-for-beginners/tree/main)
- [Azure AI Samples](https://github.com/Azure-Samples/azure-ai-agent-samples)

### Community
- [Azure AI Discord](https://discord.gg/azure-ai)
- [Stack Overflow - Azure AI](https://stackoverflow.com/questions/tagged/azure-ai)

---

## ✨ Workshop Feedback

This workshop is continuously improving! Please share your experience:
- What worked well?
- What was confusing?
- What would you like to see added?

---

**Happy Building! 🚀**
