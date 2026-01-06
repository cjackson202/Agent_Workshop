# MCP Workshop - Presentation Slides Outline

## Slide 1: Title Slide
**Title:** Building AI Agents with Model Context Protocol (MCP)  
**Subtitle:** Hands-On Workshop - Day 3  
**Duration:** 90 minutes

---

## Slide 2: Workshop Agenda
- 🎯 What is MCP and why it matters
- 🔧 Creating your first MCP server
- 🧪 Testing MCP tools locally
- ☁️ Integrating with Azure AI Foundry agents
- 🚀 Building custom tools for your use cases
- 💡 Best practices and next steps

---

## Slide 3: Recap - Where We Are
**Day 1:** LLMs & Prompt Engineering  
**Day 2:** Azure AI Foundry & Agent Framework  
**Day 3:** ← You are here! MCP + Advanced Integration

**Today's Goal:** Connect everything together with extensible tool hosting

---

## Slide 4: The Tool Problem
### Without MCP:
- ❌ Tools embedded in agent code
- ❌ Hard to share across agents
- ❌ Difficult to secure and version
- ❌ No standardization
- ❌ Language/platform dependent

### With MCP:
- ✅ Tools as separate services
- ✅ Shared across multiple agents
- ✅ Centralized security & governance
- ✅ Standardized protocol
- ✅ Language agnostic

---

## Slide 5: What is MCP?
**Model Context Protocol (MCP)**

A standardized protocol for AI agents to discover and invoke tools

**Key Concepts:**
- **Server:** Hosts tools and resources
- **Client:** Agents that consume tools
- **Tools:** Functions agents can call
- **Resources:** Dynamic content accessible via URIs
- **Transport:** HTTP, SSE, or stdio

**Created by:** Anthropic, adopted by Microsoft

---

## Slide 6: MCP Architecture

```
┌─────────────────────────────────────────┐
│         AI Agent (Client)                │
│  ┌────────────────────────────────────┐ │
│  │  Agent Reasoning & Tool Selection  │ │
│  └────────────────────────────────────┘ │
└──────────────┬──────────────────────────┘
               │ MCP Protocol
               │ (HTTP/JSON)
               ▼
┌─────────────────────────────────────────┐
│         MCP Server                       │
│  ┌────────┐  ┌────────┐  ┌────────┐   │
│  │Tool 1  │  │Tool 2  │  │Tool N  │   │
│  │(add)   │  │(search)│  │(...)   │   │
│  └────────┘  └────────┘  └────────┘   │
└─────────────────────────────────────────┘
```

---

## Slide 7: MCP vs Traditional API Calls

| Aspect | Traditional APIs | MCP |
|--------|------------------|-----|
| Discovery | Manual docs | Auto-discovery |
| Schema | OpenAPI/manual | Built-in schemas |
| Tool selection | Hardcoded | Agent decides |
| Security | Per-API auth | Centralized |
| Versioning | Manual tracking | Server-side |
| Multi-agent | Duplicate code | Shared server |

---

## Slide 8: Workshop Architecture

**What we're building today:**

```
Your Machine                    Azure Cloud
┌──────────────────┐           ┌──────────────────┐
│  MCP Server      │           │ Azure AI Foundry │
│  (localhost:8080)│◄──────────│     Agent        │
│  - add()         │    MCP    │  - GPT-4o-mini   │
│  - subtract()    │           │  - Agent Framework│
│  - custom...     │           └──────────────────┘
└──────────────────┘                    │
         ▲                               │
         │ Test                          │ User Chat
         │                               ▼
    test_mcp.py                    You (via script)
```

---

## Slide 9: Exercise Overview

**Exercise 1:** Understanding MCP (15 min)  
→ Review server code, add a tool

**Exercise 2:** Local Testing (20 min)  
→ Run server, test with test client

**Exercise 3:** Azure Integration (25 min)  
→ Create agent, connect to MCP server

**Exercise 4:** Agent Management (20 min)  
→ Retrieve existing agents, compare approaches

**Exercise 5:** Custom Tools (20 min)  
→ Build real-world tools for your use cases

---

## Slide 10: Key Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `server.py` | MCP server | Run continuously |
| `test_mcp.py` | Local test client | Before agent integration |
| `get_agent_mi.py` | Connect to portal agent | After creating agent in portal |
| `requirements.txt` | Dependencies | Install once |

---

## Slide 11: Prerequisites Check

Before we start, ensure you have:
- ✅ Python 3.10+
- ✅ Azure CLI (`az login` completed)
- ✅ Azure AI Foundry project
- ✅ GPT model deployment
- ✅ Code editor (VS Code recommended)
- ✅ Dependencies installed (`pip install -r requirements.txt --pre`)

**Demo:** Quick environment check

---

## Slide 12: Live Demo - Server Startup

**What we'll see:**
1. Starting the MCP server
2. Server logs and output
3. Available endpoints
4. Tool registration

**Command:**
```powershell
python server.py
```

**Expected Output:** Server running on port 8080

---

## Slide 13: Live Demo - Local Testing

**What we'll see:**
1. Connecting to MCP server
2. Discovering available tools
3. Testing tool invocations
4. Reading results

**Command:**
```powershell
python test_mcp.py
```

**Expected Output:** Tool list and test results

---

## Slide 14: Live Demo - Azure Agent

**What we'll see:**
1. Creating agent in Azure portal
2. Copying agent ID
3. Configuring connection script
4. Interactive chat with MCP tools

**Steps:**
1. Create agent in portal
2. Update `get_agent_mi.py`
3. Run: `python get_agent_mi.py`

**Try:** "What is 25 + 17?"

---

## Slide 15: Understanding Tool Decorators

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""  # ← Required! Used by agent
    return a + b
```

**Key elements:**
1. `@mcp.tool()` - Registers the function as a tool
2. Type hints - Define parameter types
3. Docstring - Tells agent what the tool does
4. Return type - What the agent gets back

**Without these, tools won't work!**

---

## Slide 16: Tool Design Best Practices

✅ **DO:**
- Clear, descriptive docstrings
- Type hints on all parameters
- Return simple types (str, int, float, bool)
- Handle errors gracefully
- Log tool invocations

❌ **DON'T:**
- Assume parameter values
- Return complex objects
- Perform destructive operations without safeguards
- Skip error handling
- Forget docstrings

---

## Slide 17: Authentication - Managed Identity vs Service Principal

**Managed Identity (MI)** - What we use in this workshop
- ✅ Simpler setup
- ✅ No credentials to manage
- ✅ Azure CLI authentication
- ✅ Good for development
- ❌ Requires Azure context

**Service Principal (SP)**
- ✅ Works anywhere
- ✅ Fine-grained permissions
- ✅ Production-ready
- ❌ More complex setup
- ❌ Credentials to secure

**Workshop choice:** MI (simpler, matches documentation)

---

## Slide 18: Portal-First Workflow

**Why Create Agent in Portal?**
- ✅ Visible in Azure UI
- ✅ Easier management and monitoring
- ✅ Production-ready pattern
- ✅ No confusion about agent location

**Workflow:**
1. Create agent in Azure AI Foundry portal
2. Copy agent ID
3. Use `get_agent_mi.py` to connect and add MCP tools
4. Chat with your agent

**Best Practice:** Portal for creation, code for tool integration

---

## Slide 19: Debugging Tips

**Server not responding?**
- Check if `python server.py` is running
- Verify port 8080 is not in use
- Check firewall settings

**Agent not using tools?**
- Restart server after adding tools
- Verify tool has `@mcp.tool()` decorator
- Check docstring is present
- Review agent instructions

**Azure auth errors?**
- Run `az login`
- Verify: `az account show`
- Check endpoint URL is correct

---

## Slide 20: Extension Ideas

**Real-World Tools:**
1. 🌤️ Weather API integration
2. 📊 Database queries
3. 📧 Email operations
4. 📁 File management
5. 🔍 Web search
6. 📈 Data analysis
7. 🗣️ Language translation
8. 🔐 Secret management

**Your Ideas?**
- What tools would help your use case?
- What APIs do you need to integrate?

---

## Slide 21: Security Considerations

**MCP Server Security:**
- 🔒 Authentication & authorization
- 🛡️ Input validation
- 🚫 Rate limiting
- 📝 Audit logging
- 🔑 API key management

**Production Checklist:**
- [ ] HTTPS transport
- [ ] API authentication
- [ ] Input sanitization
- [ ] Error handling
- [ ] Monitoring & alerts
- [ ] Access controls

---

## Slide 22: Deployment Options

**Development:** Localhost (what we use today)

**Testing/Staging:**
- Azure Container Apps
- Azure App Service
- Docker container

**Production:**
- Azure Container Apps with scaling
- Azure Kubernetes Service (AKS)
- Azure Functions (for simple tools)
- Behind API Management

---

## Slide 23: Multi-Agent Scenarios

**One MCP Server, Many Agents:**

```
MCP Server (Port 8080)
    ├── Agent 1 (Customer Service)
    ├── Agent 2 (Data Analysis)
    ├── Agent 3 (Report Generation)
    └── Agent 4 (Monitoring)
```

**Benefits:**
- Shared tool library
- Centralized updates
- Consistent behavior
- Easier governance

---

## Slide 24: Monitoring & Observability

**What to monitor:**
- Tool invocation frequency
- Error rates
- Response times
- Token usage
- Cost per tool call

**How:**
- Azure Application Insights
- Custom logging
- MCP server metrics
- Agent Framework telemetry

**Demo:** Look at server logs during agent execution

---

## Slide 25: MCP Resources (Beyond Tools)

**Resources:** Dynamic content accessible via URIs

```python
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
```

**Use cases:**
- Configuration data
- Static content
- Templates
- Documentation
- Knowledge bases

**Access:** `greeting://John` → "Hello, John!"

---

## Slide 26: Error Handling Patterns

**Good error handling:**

```python
@mcp.tool()
def divide(a: float, b: float) -> str:
    """Divide two numbers"""
    if b == 0:
        return "Error: Cannot divide by zero"
    return f"{a} / {b} = {a/b}"
```

**What the agent sees:**
- Clear error messages
- Actionable information
- No crashes
- Can retry or use alternative

---

## Slide 27: Testing Strategy

**3 Levels of Testing:**

1. **Unit Tests:** Individual functions
   ```python
   assert add(2, 3) == 5
   ```

2. **Integration Tests:** MCP client (`test_mcp.py`)
   - Verifies tools are discoverable
   - Tests tool invocation

3. **E2E Tests:** Full agent workflow
   - Agent + MCP server
   - Real conversations
   - Tool chaining

---

## Slide 28: Performance Optimization

**Slow tools = Slow agents**

**Optimize:**
- ⚡ Cache expensive operations
- 🔄 Use async where possible
- 📦 Batch API calls
- 💾 Database connection pooling
- 🎯 Limit result sizes

**Example:** Cache weather data for 15 minutes

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_weather(city: str):
    # Cached for reuse
    return fetch_weather_api(city)
```

---

## Slide 29: Workshop Checkpoints

By now you should be able to:
- ✅ Explain what MCP is
- ✅ Create an MCP server
- ✅ Add custom tools
- ✅ Test tools locally
- ✅ Connect agents to MCP servers
- ✅ Create and retrieve agents
- ✅ Debug tool invocations

**Questions?** Ask now before we move to advanced topics!

---

## Slide 30: Advanced: Tool Chaining

**Agents can chain multiple tools:**

User: "What's 10 + 5, then multiply by 2?"

Agent reasoning:
1. Call `add(10, 5)` → 15
2. Call `multiply(15, 2)` → 30
3. Respond: "The result is 30"

**You don't code this!** The agent framework handles it automatically.

---

## Slide 31: Advanced: Prompt Engineering for Tools

**Better instructions = Better tool usage**

❌ **Vague:**
```python
instructions="Answer questions"
```

✅ **Specific:**
```python
instructions="""You are a math assistant. 
Always use the available calculation tools.
Show your work step by step.
If a calculation fails, explain why."""
```

**Test different instructions!**

---

## Slide 32: Integration with Day 2 Content

**Connecting it all:**

```
Azure AI Search (Day 2)
    ↓
Azure AI Foundry Agent (Day 2)
    ↓
Agent Framework (Day 2)
    ↓
MCP Server (Today!) ← Custom tools
    ↓
Your Business Logic
```

**Result:** Agents with RAG + Custom Tools!

---

## Slide 33: Real-World Use Case: ERM

**Example: Enterprise Risk Management Agent**

**MCP Tools:**
- `query_risk_database()` - Search risk data
- `calculate_risk_score()` - Compute scores
- `generate_compliance_report()` - Create reports
- `check_regulatory_requirements()` - Validate compliance
- `escalate_to_human()` - Human-in-loop

**Agent Instructions:** "You are an ERM assistant..."

---

## Slide 34: Next Steps After Workshop

**Immediate (This Week):**
1. Customize tools for your use case
2. Add error handling and logging
3. Test with different agent instructions
4. Document your tools

**Short Term (This Month):**
1. Deploy MCP server to Azure
2. Add authentication
3. Connect multiple agents
4. Monitor and optimize

**Long Term:**
1. Build tool libraries
2. Multi-agent workflows
3. Production deployment
4. Integration with existing systems

---

## Slide 35: Resources & Documentation

**Microsoft Resources:**
- [MCP for Beginners](https://github.com/microsoft/mcp-for-beginners)
- [Azure Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-services/)

**Workshop Materials:**
- README.md - Full workshop guide
- QUICKSTART.md - 5-minute setup
- SOLUTIONS.md - Exercise solutions

**Community:**
- Azure AI Discord
- Stack Overflow
- GitHub Issues

---

## Slide 36: Questions & Discussion

**Common Questions:**
1. How do I secure my MCP server?
2. Can I use MCP with other agent frameworks?
3. What's the performance overhead of MCP?
4. How do I version my tools?
5. Can agents discover new tools dynamically?

**Your Questions?**
- Ask anything!
- Share your ideas
- Discuss challenges

---

## Slide 37: Hands-On Time!

**Now it's your turn:**

Choose your path:
1. 🎯 **Guided:** Follow Exercise 5 (Advanced Customization)
2. 🚀 **Challenge:** Build a tool for your specific use case
3. 🤝 **Collaborate:** Work with others on shared tools

**Instructors are here to help!**

⏰ Time: 30 minutes

---

## Slide 38: Share Your Work

**Show and Tell:**
- What tool did you build?
- What challenges did you face?
- What did you learn?
- Ideas for production use?

**Volunteers to demo?**

---

## Slide 39: Workshop Wrap-Up

**What we covered:**
- ✅ MCP fundamentals
- ✅ Server & client architecture
- ✅ Azure AI Foundry integration
- ✅ Custom tool development
- ✅ Testing & debugging
- ✅ Best practices

**Key Takeaway:** MCP enables extensible, maintainable, and secure AI agent tools!

---

## Slide 40: Day 3 Complete! 🎉

**Three-Day Journey:**
- Day 1: LLM fundamentals
- Day 2: Azure AI Foundry
- Day 3: MCP & Custom Tools ✓

**You now have the skills to:**
- Build production AI agents
- Create custom tool ecosystems
- Integrate with Azure services
- Design multi-agent systems

**Next:** Apply these to your ERM use cases with Kidambi!

**Thank you!** 🚀

---

## Bonus Slide: Troubleshooting Cheat Sheet

```powershell
# Check if server is running
netstat -ano | findstr :8080

# Test Azure auth
az login
az account show

# Reinstall dependencies
pip install -r requirements.txt --pre --force-reinstall

# View server logs
# (Watch Terminal 1 while agent runs)

# Find agent ID
# Look in create_agent_mi.py output
# Or: Azure AI Foundry Studio → Agents

# Test tool locally
python test_mcp.py
```

---

## Instructor Notes (Not for slides)

**Timing:**
- Slides 1-11: 15 min (intro & setup)
- Slides 12-14: 15 min (live demos)
- Slides 15-29: 30 min (concepts & best practices)
- Slides 30-36: 15 min (advanced topics & Q&A)
- Slide 37: 30 min (hands-on work)
- Slides 38-40: 15 min (wrap-up)

**Total:** ~2 hours (with buffer for questions)

**Tips:**
- Do demos early to build excitement
- Pause for questions after each major section
- Have backup examples ready
- Monitor chat for common issues
- Save last 30 min for hands-on practice
