# Multi-Agent Orchestration Demo Collection

> **Comprehensive demonstrations of Microsoft Agent Framework multi-agent orchestration patterns**

This collection provides production-ready examples of different multi-agent orchestration patterns using the Microsoft Agent Framework. Each demo is designed to be educational, interactive, and easily adaptable for real-world scenarios.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Why Multi-Agent?](#why-multi-agent)
- [Orchestration Patterns](#orchestration-patterns)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Demo Details](#demo-details)
- [Configuration](#configuration)
- [Resources](#resources)

---

## 🎯 Overview

Multi-agent orchestration allows developers to create complex workflows by coordinating multiple AI agents, each with specialized skills or roles. This approach creates systems that are more robust, adaptive, and capable of solving real-world problems collaboratively.

### What's Included

| Pattern | Demo | Description |
|---------|------|-------------|
| **Group Chat** | `Group_Chat/` | Collaborative conversation with managed speaker selection |
| **Sequential** | `Sequential/` | Pipeline processing where agents work in sequence |
| **Handoff** | `Handoff/` | Dynamic routing between specialist agents |

---

## 🤔 Why Multi-Agent?

Traditional single-agent systems are limited in their ability to handle complex, multi-faceted tasks. Multi-agent orchestration provides:

✅ **Specialized Expertise** - Each agent focuses on specific domains or tasks  
✅ **Better Scalability** - Distribute work across multiple agents  
✅ **Improved Quality** - Peer review and iterative refinement  
✅ **Flexible Routing** - Dynamic delegation based on context  
✅ **Separation of Concerns** - Clear responsibilities and maintainable code  

---

## 🔄 Orchestration Patterns

### 1. Group Chat Orchestration
**Location:** `Group_Chat/agent_groupchat.py`

Coordinates multiple agents in a collaborative conversation with a manager controlling speaker selection and flow.

**Use Cases:**
- Iterative refinement and quality assurance
- Collaborative problem-solving
- Content review workflows
- Multi-perspective analysis

**Key Features:**
- ✨ Three specialized agents (Researcher, Writer, FactChecker)
- 🔧 Real research tools (web search, documentation)
- 📄 Professional document generation
- 🎛️ Multiple workflow strategies (simple, iterative, agent-managed)

**Run the Demo:**
```bash
cd Group_Chat
python agent_groupchat.py
```

**Documentation:** [Group Chat Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/group-chat?pivots=programming-language-python)

---

### 2. Sequential Orchestration
**Location:** `Sequential/agent_sequential.py`

Passes output from one agent to the next in a defined order, creating a processing pipeline.

**Use Cases:**
- Step-by-step workflows
- Data processing pipelines
- Multi-stage content creation
- Editorial workflows (write → review → edit)

**Key Features:**
- 📝 Three-stage pipeline (Writer → Reviewer → Editor)
- 🔧 Custom executor for analytics
- 📊 Pipeline statistics and metrics
- 🎨 Multiple pipeline configurations

**Run the Demo:**
```bash
cd Sequential
python agent_sequential.py
```

**Documentation:** [Sequential Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/sequential?pivots=programming-language-python)

---

### 3. Handoff Orchestration
**Location:** `Handoff/agent_handoff.py`

Dynamically passes control between agents based on context or rules, like a customer support system.

**Use Cases:**
- Customer support triage and routing
- Expert escalation workflows
- Dynamic task delegation
- Context-aware agent switching

**Key Features:**
- 🎯 Five specialized agents (Triage, Refund, Order, Account, Technical)
- ⚠️ Tool approval workflow (HITL - Human-in-the-Loop)
- 💬 Interactive multi-turn conversations
- 🔄 Agent-to-agent handoffs
- 📋 Context preservation across transfers

**Run the Demo:**
```bash
cd Handoff
python agent_handoff.py
```

**Documentation:** [Handoff Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/handoff?pivots=programming-language-python)

---

## 🛠️ Prerequisites

### Required Software
- Python 3.10 or higher
- Azure CLI
- Azure OpenAI resource

### Azure Setup

1. **Azure OpenAI Resource**
   ```bash
   # Create resource (if needed)
   az cognitiveservices account create \
     --name <your-resource-name> \
     --resource-group <your-rg> \
     --kind OpenAI \
     --sku S0 \
     --location eastus
   ```

2. **Deploy a Model**
   - Deploy `gpt-4o`, `gpt-4`, or `gpt-35-turbo`
   - Note your deployment name

3. **Authenticate**
   ```bash
   az login
   ```

### Python Dependencies

1. **Create Virtual Environment** (recommended):
   ```bash
   # Create venv
   python -m venv .venv
   
   # Activate on Windows
   .venv\Scripts\activate
   
   # Activate on Linux/Mac
   source .venv/bin/activate
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt --pre
   ```
   
   Or individually:
   ```bash
   pip install agent-framework azure-identity python-dotenv
   ```

---

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the `Multi_Agent_Demo` directory:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

**Or** set environment variables:

**Windows PowerShell:**
```powershell
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"
```

**Linux/Mac:**
```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"
```

### 3. Run a Demo

```bash
# Group Chat demo
cd Group_Chat
python agent_groupchat.py

# Sequential demo
cd Sequential
python agent_sequential.py

# Handoff demo (interactive)
cd Handoff
python agent_handoff.py
```

---

## 📚 Demo Details

### Group Chat Demo

**Scenario:** Research team answering technical questions

**Workflow:**
1. **Researcher** uses tools to gather information
   - `web_search()` - Simulated web search
   - `get_technical_docs()` - Retrieves documentation
2. **Writer** creates a polished answer
   - Uses `save_to_document()` to create professional markdown
3. **FactChecker** validates accuracy and completeness

**Output:** 
- Console output showing agent collaboration
- Professional markdown document in `output/` folder

**Customization:**
- Edit line 467 to change the default workflow
- Uncomment lines 471-474 to try other workflow strategies
- Modify task on line 464 to ask different questions

---

### Sequential Demo

**Scenario:** Marketing content creation pipeline

**Pipeline Stages:**
1. **Writer** - Creates initial tagline/content
2. **Reviewer** - Provides constructive feedback with rating
3. **Editor** - Revises based on feedback
4. **ContentAnalyzer** (Custom Executor) - Adds statistics

**Output:** 
- Streamed output showing each pipeline stage
- Final summary with all contributions

**Customization:**
- Edit line 261 to select different demo scenarios
- Modify agent instructions (lines 35-69) for different tones
- Create custom executors following the `ContentAnalyzer` pattern

---

### Handoff Demo

**Scenario:** Interactive customer support system

**Agents:**
- **Triage Agent** - Routes to appropriate specialist
- **Refund Agent** - Handles refunds (with approval)
- **Order Agent** - Tracks orders, handles shipping
- **Account Agent** - Login and account issues
- **Technical Agent** - Product troubleshooting

**Interactions:**
- 💬 Multi-turn conversations
- ⚠️ Tool approval requests (e.g., refunds, cancellations)
- 🔄 Dynamic routing between specialists
- Type `quit` or `exit` to end session

**Customization:**
- Edit line 335 to choose different scenarios
- Modify agent instructions for different support domains
- Add new specialist agents with different expertise

---

## ⚙️ Configuration

### Common Settings

All demos use the same configuration pattern:

```python
# Option 1: Environment variables
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource.openai.azure.com/"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"

# Option 2: Direct configuration
chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint="https://your-resource.openai.azure.com/",
    deployment_name="gpt-4o"
)
```

### Timing Configuration

All demos include strategic delays for demonstration purposes:

```python
time.sleep(2)    # Between agent transitions
time.sleep(0.05) # During text streaming
time.sleep(1)    # Before final summaries
```

Adjust these values in the code for faster/slower demonstrations.

---

## 📖 Resources

### Microsoft Documentation
- [Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview/)
- [Orchestration Patterns](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview)
- [Group Chat](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/group-chat?pivots=programming-language-python)
- [Sequential](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/sequential?pivots=programming-language-python)
- [Handoff](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/handoff?pivots=programming-language-python)

### Additional Patterns (Not Yet Implemented)
- [Concurrent Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/concurrent?pivots=programming-language-python) - Parallel agent execution
- [Magentic Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/magentic?pivots=programming-language-python) - Complex generalist collaboration

### Azure Resources
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)

---

## 🎓 Learning Path

**Recommended Order:**

1. **Start with Sequential** - Simplest pattern, linear flow
   - Understand agent creation and basic workflow
   - See how agents build on each other's output

2. **Move to Group Chat** - Introduces coordination
   - Learn about speaker selection
   - Understand tool usage in agents
   - See iterative refinement in action

3. **Try Handoff** - Most complex interactions
   - Master dynamic routing
   - Implement approval workflows
   - Handle multi-turn conversations

---

## 🔧 Troubleshooting

### Common Issues

**Error: "Azure OpenAI deployment name is required"**
- Solution: Set `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` environment variable

**Error: "Please provide an endpoint or a base_url"**
- Solution: Set `AZURE_OPENAI_ENDPOINT` environment variable

**Error: "DefaultAzureCredential failed to retrieve a token"**
- Solution: Run `az login` to authenticate

**Agents not responding or slow**
- Check Azure OpenAI quota and throttling limits
- Verify deployment is active and has capacity
- Try reducing `time.sleep()` delays if just testing

---

## 💡 Tips for Demo Success

### For Presentations
1. **Pre-configure** environment variables before the demo
2. **Test run** once to ensure everything works
3. **Adjust timing** - Increase `time.sleep()` values for audience comprehension
4. **Prepare questions** - Have 2-3 example questions ready
5. **Explain flow** - Point out when agents transition

### For Development
1. **Start simple** - Use basic workflows before advanced ones
2. **Mock tools first** - Like web_search(), test logic before real APIs
3. **Add logging** - Print statements help debug agent behavior
4. **Version control** - Track changes to agent instructions
5. **Iterate prompts** - Agent instructions are key to good results

---

## 📝 License

These demos are provided as educational examples for the Microsoft Agent Framework.

---

## 🤝 Contributing

To add new demos or improve existing ones:

1. Follow the existing code structure
2. Include comprehensive comments
3. Add timing delays for demo visibility
4. Update this README with new patterns
5. Test with multiple scenarios

---

## 📞 Support

- **Agent Framework Issues:** [GitHub Issues](https://github.com/microsoft/agent-framework)
- **Azure Support:** [Azure Support Portal](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/overview)
- **Documentation:** [Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/)

---

**Last Updated:** January 2026  
**Framework Version:** Microsoft Agent Framework (Latest)  
**Python Version:** 3.10+
