# MCP Workshop - Quick Reference Card

> Print this page or keep it open for quick reference during the workshop!

---

## 🚀 Essential Commands

```bash
# Setup (run once in Azure ML Notebooks)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --pre

# Azure Login (Managed Identity)
az login --identity
az account show

# Start MCP Server (Terminal 1 - keep running)
source .venv/bin/activate
python server.py

# Test MCP Server (Terminal 2)
source .venv/bin/activate
python test_mcp.py

# Create New Agent (Terminal 2)
source .venv/bin/activate
python create_agent_mi.py

# Use Existing Agent (Terminal 2)
source .venv/bin/activate
python get_agent_mi.py
```

---

## 📝 Tool Template

```python
@mcp.tool()
def your_tool_name(param1: type, param2: type) -> return_type:
    """Clear description of what this tool does
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of what is returned
    """
    # Your code here
    result = param1 + param2  # Example
    
    # Optional: Logging
    print('-'*50)
    print(f"Tool executed with {param1} and {param2}")
    print('-'*50)
    
    return result
```

**Must Have:**
- ✅ `@mcp.tool()` decorator
- ✅ Type hints on all parameters
- ✅ Docstring (used by agent!)
- ✅ Return value

---

## 🔧 Azure Configuration

Update in `create_agent_mi.py` and `get_agent_mi.py`:

```python
# Your Azure AI Foundry project endpoint
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://YOUR-PROJECT.services.ai.azure.com/api/projects/YOUR-PROJECT"

# Your model deployment name
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"

# For get_agent_mi.py only: Your agent ID
AGENT_ID = "asst_xxxxxxxxxxxxx"
```

Find these in: **Azure AI Foundry Studio → Project Settings**

---

## 🐛 Common Issues & Fixes

| Issue | Quick Fix |
|-------|-----------|
| "Connection refused" | Start server: `python server.py` |
| "Port 8080 in use" | `netstat -an \| grep :8080` then kill process |
| "Azure auth failed" | Run: `az login --identity` (Azure ML) |
| "Module not found" | Activate venv: `source .venv/bin/activate` then `pip install -r requirements.txt --pre` |
| "venv not activated" | Run: `source .venv/bin/activate` |
| "Tool not found" | Restart server after adding tool |
| "Agent not using tool" | Check `@mcp.tool()` decorator and docstring |

---

## 📊 Workflow Diagram

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Start   │────►│  Test    │────►│  Create  │
│  Server  │     │  Locally │     │  Agent   │
└──────────┘     └──────────┘     └──────────┘
     │                │                 │
     │                │                 │
 Terminal 1       Terminal 2        Terminal 2
 server.py        test_mcp.py    create_agent_mi.py
```

---

## ✅ File Checklist

- [ ] **server.py** - MCP server (modify this!)
- [ ] **test_mcp.py** - Test client (run to verify)
- [ ] **create_agent_mi.py** - Create agent (configure Azure)
- [ ] **get_agent_mi.py** - Retrieve agent (use later)
- [ ] **requirements.txt** - Dependencies (install once)

---

## 🎯 Workshop Exercises

**Exercise 1 (15 min):** Add multiplication tool  
**Exercise 2 (20 min):** Test server locally  
**Exercise 3 (25 min):** Create Azure agent  
**Exercise 4 (20 min):** Retrieve existing agent  
**Exercise 5 (20 min):** Build custom tool  

---

## 💡 Test Prompts

Try these with your agent:

```
"What is 25 + 17?"
"Calculate 100 minus 45"
"What's 7 times 8?" (if you added multiply)
"Compute (50 + 30) divided by 4"
"Add 12, 8, and 5 together"
```

---

## 📞 Help Resources

**Stuck on Exercise X?**  
→ See SOLUTIONS.md

**Server won't start?**  
→ Check port, check dependencies

**Azure issues?**  
→ Verify `az account show`

**General questions?**  
→ Ask instructor or check README.md

---

## 🎓 Key Concepts

**MCP** = Model Context Protocol  
- Standardized way for agents to call tools
- Tools hosted in separate server
- Discoverable via HTTP

**Tool** = Function an agent can call  
- Decorated with `@mcp.tool()`
- Has type hints and docstring
- Returns simple types

**Agent** = AI that uses tools  
- Hosted in Azure AI Foundry
- Automatically selects which tools to use
- Chains multiple tools together

---

## 🏆 Success Criteria

By end of workshop, you should have:
- ✅ MCP server running
- ✅ Tools tested locally
- ✅ Agent created in Azure
- ✅ Agent using your tools
- ✅ At least 1 custom tool added

---

## 📁 Quick File Access

| Need | Open This |
|------|-----------|
| Add tool | server.py |
| Test tool | test_mcp.py |
| Configure Azure | create_agent_mi.py |
| Reuse agent | get_agent_mi.py |
| See examples | SOLUTIONS.md |
| Full guide | README.md |

---

## 🔐 Authentication Notes

**We use Managed Identity (MI):**
- Simpler than Service Principal
- Uses Azure CLI credentials
- Run `az login` once, you're authenticated
- Good for development

**For production:** Consider Service Principal (SP)

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Install dependencies | 2 min |
| Start server | 30 sec |
| Test locally | 2 min |
| Configure Azure | 3 min |
| Create agent | 2 min |
| Chat with agent | 5+ min |
| Add custom tool | 10 min |

**Total first run:** ~25 minutes

---

## 💻 Terminal Setup

**Recommended layout:**

```
┌──────────────────┬──────────────────┐
│                  │                  │
│  Terminal 1      │  Terminal 2      │
│  python server.py│  python test.py  │
│                  │  or agent.py     │
│  (Keep running!) │  (Interactive)   │
│                  │                  │
└──────────────────┴──────────────────┘
```

**Watch Terminal 1 for tool invocation logs!**

---

## 🎨 Tool Categories

**Math Tools:**
- add, subtract, multiply, divide

**Data Tools:**
- validate, transform, analyze

**API Tools:**
- fetch, query, search

**Business Tools:**
- calculate_risk, generate_report

**Your Tools:**
- ___________________________

---

## 📈 Next Steps

After workshop:
1. ✅ Build 2-3 custom tools for your work
2. ✅ Test with different agent instructions
3. ✅ Deploy to Azure Container Apps
4. ✅ Add authentication and monitoring
5. ✅ Share with your team!

---

## 🎯 Learning Path

```
Basic → Intermediate → Advanced
  │          │            │
  ▼          ▼            ▼
Add tool → Test tool → Deploy tool
  │          │            │
  ▼          ▼            ▼
Simple   → Azure     → Production
calculator  agent       multi-agent
```

---

## 🔗 URLs to Bookmark

**Workshop Materials:**
- README.md - Full guide
- SOLUTIONS.md - Code examples
- QUICKSTART.md - Fast start

**External Resources:**
- [MCP for Beginners](https://github.com/microsoft/mcp-for-beginners)
- [Azure AI Foundry Docs](https://learn.microsoft.com/en-us/agent-framework/)

**Your Project:**
- Azure Portal: portal.azure.com
- AI Foundry Studio: ai.azure.com

---

## ✏️ Notes Space

Take notes here during the workshop:

```
Key insights:
_____________________________________________
_____________________________________________
_____________________________________________

Questions:
_____________________________________________
_____________________________________________
_____________________________________________

Custom tool ideas:
_____________________________________________
_____________________________________________
_____________________________________________

Follow-up tasks:
_____________________________________________
_____________________________________________
_____________________________________________
```

---

## 🌟 Pro Tips

1. **Always restart server** after adding tools
2. **Check docstrings** - agents need them!
3. **Watch server logs** to see tool calls
4. **Test locally first** before agent integration
5. **Save your agent ID** for reuse
6. **Simple tools first** then add complexity
7. **Error handling matters** for production

---

## 🎊 Quick Wins

**First 10 minutes:**
- ✅ Server running
- ✅ Test passing

**First 30 minutes:**
- ✅ Agent created
- ✅ First tool call

**By end:**
- ✅ Custom tool built
- ✅ Understanding MCP
- ✅ Ready for production

---

**Save this page for quick reference!**

**Workshop: Building AI Agents with MCP**  
**Version: 1.0**  
**Date: _________________**
