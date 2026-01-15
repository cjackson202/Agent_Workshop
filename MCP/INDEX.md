# MCP Workshop - Navigation Guide

> **👋 Welcome!** This guide helps you find exactly what you need.

## 🎯 I want to...

### Learn MCP from scratch
→ Start here: **[README.md](README.md)** (Full workshop guide with 5 exercises)

### Get running in 5 minutes
→ Go here: **[QUICKSTART.md](QUICKSTART.md)** (Minimal setup path)

### See example solutions
→ Check here: **[solutions/SOLUTIONS.md](solutions/SOLUTIONS.md)** (All exercise answers + examples)

### Teach this workshop
→ Read this: **[docs/FACILITATOR_GUIDE.md](docs/FACILITATOR_GUIDE.md)** (Complete teaching runbook)

### Present to a group
→ Use this: **[docs/SLIDES_OUTLINE.md](docs/SLIDES_OUTLINE.md)** (40 slides with notes)

### Understand what this is
→ Read this: **[docs/WORKSHOP_SUMMARY.md](docs/WORKSHOP_SUMMARY.md)** (Overview of everything)

### Fix a problem
→ Check: **README.md → Troubleshooting section** (Common issues & solutions)

---

## 📁 All Workshop Files

### Core Files (Run these)
| File | Purpose | When |
|------|---------|------|
| [server.py](server.py) | MCP server with tools | Start first (Terminal 1) |
| [test_mcp.py](test_mcp.py) | Test MCP locally | After server starts (Terminal 2) |
| [get_agent_mi.py](get_agent_mi.py) | Connect to portal agent | After creating agent in portal |
| [requirements.txt](requirements.txt) | Install dependencies | Run once: `pip install -r requirements.txt --pre` |

### Documentation Files (Read these)
| File | What It's For | Read If... |
|------|---------------|-----------|
| [README.md](README.md) | Main workshop guide | You're doing the workshop |
| [QUICKSTART.md](QUICKSTART.md) | 5-min getting started | You want to start fast |
| [INDEX.md](INDEX.md) | This file | You need navigation help |

### Solutions Folder
| File | What It's For |
|------|---------------|
| [solutions/SOLUTIONS.md](solutions/SOLUTIONS.md) | Exercise answers & examples |

### Facilitator Resources (docs/ folder)
| File | What It's For |
|------|---------------|
| [docs/FACILITATOR_GUIDE.md](docs/FACILITATOR_GUIDE.md) | Teaching guide & runbook |
| [docs/SLIDES_OUTLINE.md](docs/SLIDES_OUTLINE.md) | Presentation deck (40 slides) |
| [docs/WORKSHOP_SUMMARY.md](docs/WORKSHOP_SUMMARY.md) | Workshop overview |
| [docs/DIAGRAMS.md](docs/DIAGRAMS.md) | Architecture diagrams |
| [docs/CHEATSHEET.md](docs/CHEATSHEET.md) | Quick reference card |

### Archive Folder (Ignore)
- `archive/create_agent_sp.py` - Service Principal auth (not used)
- `archive/get_agent_sp.py` - Service Principal retrieval (not used)

---

## 🎓 Workshop Path

```
Step 1: Setup (5 min)
└─→ Install dependencies
    └─→ pip install -r requirements.txt --pre

Step 2: Learn Basics (15 min)
└─→ Read README.md Exercise 1
    └─→ Review server.py code
        └─→ Add multiplication tool

Step 3: Test Locally (20 min)
└─→ README.md Exercise 2
    └─→ python server.py (Terminal 1)
        └─→ python test_mcp.py (Terminal 2)

Step 4: Azure Integration (25 min)
└─→ README.md Exercise 3
    └─→ Create agent in Azure portal
        └─→ Configure get_agent_mi.py
            └─→ python get_agent_mi.py
                └─→ Chat with agent!

Step 5: Advanced (20 min)
└─→ README.md Exercise 4
    └─→ Build custom tools
        └─→ Test with agent
```

---

## 🚨 Quick Troubleshooting

### "Where do I start?"
→ [QUICKSTART.md](QUICKSTART.md) for fast path, or [README.md](README.md) for complete guide

### "My server won't start"
→ Check port 8080 isn't in use: `netstat -ano | findstr :8080`

### "Azure authentication failed"
→ Run: `az login --identity` then `az account show`

### "I'm stuck on Exercise X"
→ See [SOLUTIONS.md](SOLUTIONS.md) for complete code

### "The agent isn't using my tool"
→ Restart server, check `@mcp.tool()` decorator, verify docstring exists

### "What's the difference between create and get?"
→ [README.md Exercise 4](README.md) explains this in detail

---

## 🎯 Quick Reference

### Commands
```bash
# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate

# Install
pip install -r requirements.txt --pre

# Start Server
python server.py

# Test
python test_mcp.py

# Connect to Portal Agent
python get_agent_mi.py

# Azure Login (Managed Identity for Azure ML)
az login --identity --identity
az account show
```

### Ports
- **8080** - MCP server (default)
- Change in server.py if needed

### Azure Configuration
Update in `get_agent_mi.py`:
```python
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://YOUR-PROJECT.services.ai.azure.com/..."
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"
AGENT_ID = "asst_YOUR_AGENT_ID"  # Copy from Azure portal
```

---

## 🎭 Role-Specific Guides

### I'm a Participant
1. Read [QUICKSTART.md](QUICKSTART.md) to get running fast
2. Follow [README.md](README.md) exercises in order
3. Reference [SOLUTIONS.md](SOLUTIONS.md) when stuck
4. Ask questions in workshop!

### I'm an Instructor
1. Read [FACILITATOR_GUIDE.md](FACILITATOR_GUIDE.md) first
2. Review [SLIDES_OUTLINE.md](SLIDES_OUTLINE.md) for presentation
3. Test all scripts before workshop
4. Have [SOLUTIONS.md](SOLUTIONS.md) ready for questions

### I'm Self-Learning
1. Start with [README.md](README.md) Exercise 1
2. Work through at your own pace
3. Use [SOLUTIONS.md](SOLUTIONS.md) to check your work
4. Experiment with custom tools!

### I'm Reviewing Code
1. Check [WORKSHOP_SUMMARY.md](WORKSHOP_SUMMARY.md) for overview
2. Look at server.py for implementation
3. See [SOLUTIONS.md](SOLUTIONS.md) for advanced examples

---

## 📊 File Sizes & Estimates

| File | Lines | Read Time | Purpose |
|------|-------|-----------|---------|
| README.md | ~500 | 30 min | Main guide |
| QUICKSTART.md | ~150 | 5 min | Fast start |
| SOLUTIONS.md | ~400 | 20 min | Examples |
| FACILITATOR_GUIDE.md | ~500 | 30 min | Teaching |
| SLIDES_OUTLINE.md | ~600 | 40 min | Slides |
| server.py | ~100 | 10 min | Code |

**Total Documentation:** ~2,500 lines  
**Total Workshop Time:** 90-120 minutes

---

## 🔗 External Links

### Microsoft Documentation
- [MCP for Beginners](https://github.com/microsoft/mcp-for-beginners/tree/main)
- [Azure AI Foundry Agents](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/azure-ai-foundry-agent?pivots=programming-language-python)
- [Using MCP with Foundry](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents?pivots=programming-language-python)

### Tools & Resources
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [Azure AI Discord](https://discord.gg/azure-ai)
- [Stack Overflow - Azure AI](https://stackoverflow.com/questions/tagged/azure-ai)

---

## ✅ Pre-Workshop Checklist

Before starting, ensure you have:
- [ ] Access to Azure ML Notebooks
- [ ] Python 3.10 or higher in Azure ML
- [ ] Azure CLI available in notebook environment
- [ ] Azure account with AI Foundry project
- [ ] GPT-4o or GPT-4o-mini deployed
- [ ] Repository cloned to Azure ML workspace
- [ ] Internet connection

Test with:
```bash
python --version  # Should be 3.10+
az --version      # Should show Azure CLI
az login --identity --identity  # Authenticate with managed identity
```

---

## 🎊 You're Ready!

Everything you need is here. Pick your path:

- **Fast:** [QUICKSTART.md](QUICKSTART.md)
- **Complete:** [README.md](README.md)
- **Teaching:** [FACILITATOR_GUIDE.md](FACILITATOR_GUIDE.md)

**Questions?** Check the troubleshooting sections in each guide.

**Let's build some AI agents! 🚀**

---

*Last Updated: Workshop Creation*  
*Version: 1.0*  
*Status: Ready for Use*
