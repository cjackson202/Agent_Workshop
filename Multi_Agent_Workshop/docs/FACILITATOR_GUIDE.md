# Workshop Facilitator Guide - Multi-Agent Orchestration

## 🎯 Workshop Overview

**Title:** Multi-Agent Orchestration with Microsoft Agent Framework  
**Duration:** 90 minutes  
**Audience:** Developers with Python and basic AI agent experience  
**Level:** Intermediate  
**Format:** Instructor-led with hands-on exercises

## 📋 Pre-Workshop Checklist

### 1 Week Before
- [ ] Send pre-requisites email to participants
- [ ] Verify all participants have Azure OpenAI access
- [ ] Test all scripts with latest agent-framework package
- [ ] Prepare backup materials

### 1 Day Before
- [ ] Test all three orchestration patterns
- [ ] Prepare demo environment
- [ ] Load documentation in browser tabs

### 1 Hour Before
- [ ] Start VS Code with all files open
- [ ] Test each script runs successfully
- [ ] Open Azure OpenAI portal for troubleshooting

## 🎓 Workshop Agenda (90 minutes)

### Part 1: Introduction (10 min)
- **0:00-0:05** Welcome & why multi-agent?
- **0:05-0:10** Overview of three patterns

**Facilitator Notes:**
- Keep intro brief - show real-world examples
- Quick poll: "Who has built agents before?"

### Part 2: Sequential Orchestration (30 min)
- **0:10-0:20** Demo: Sequential pipeline (Writer → Reviewer → Editor)
- **0:20-0:35** Exercise 1: Run and modify sequential workflows
- **0:35-0:40** Exercise 2: Add a custom tool

**Demo Script:**
```bash
cd Multi_Agent_Workshop/Sequential
python -m venv .venv
.venv\Scripts\activate
pip install -r ../requirements.txt

# Set environment variables
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"

# Run demo
python agent_sequential.py
```

### Part 3: Handoff Orchestration (25 min)
- **0:40-0:50** Demo: Dynamic agent routing
- **0:50-1:00** Exercise 3: Test handoff scenarios
- **1:00-1:05** Discussion: When to use handoffs

**Demo Script:**
```bash
cd ../Handoff
python agent_handoff.py
# Try: "My order 12345 arrived damaged. I need a refund."
```

### Part 4: Group Chat Orchestration (20 min)
- **1:05-1:15** Demo: Collaborative research team
- **1:15-1:25** Exercise 4: Run different workflow strategies

**Demo Script:**
```bash
cd ../Group_Chat
python agent_groupchat.py
# Try: "What are the key benefits of async/await in Python?"
# Check output/ folder for generated files
```

### Part 5: Wrap-up (5 min)
- **1:25-1:30** Pattern comparison and Q&A

## 📚 Exercise Details

### Exercise 1: Sequential Patterns (15 min)

**Objective:** Understand sequential pipelines

**Instructions:**
1. Open `agent_sequential.py`
2. Run the basic, extended, and advanced workflows
3. Modify agent instructions
4. Observe how each agent receives full conversation history

**Common Issues:**
| Issue | Solution |
|-------|----------|
| Azure auth fails | Run `az login --identity` |
| Module not found | Activate venv and install dependencies |
| No output | Check Azure OpenAI endpoint and deployment name |

### Exercise 2: Add Custom Tool (10 min)

**Objective:** Add tool calling to agents

**Instructions:**
1. Open the "EXERCISE" section in `agent_sequential.py` (around line 100)
2. Remove the triple quotes (""") around the sentiment_analyzer tool
3. Scroll to the Reviewer agent definition (around line 245)
4. Add sentiment_analyzer to the functions list
5. Test with the provided prompt

**Step-by-Step:**
```python
# After uncommenting sentiment_analyzer, update Reviewer agent:
reviewer = chat_client.create_agent(
    instructions="...",
    name="Reviewer",
    functions=[word_counter, readability_checker, sentiment_analyzer]  # Add here
)
```

**Test Prompt:**
"Write a positive tagline for a new smartphone and check its sentiment"

**What They'll Learn:**
- How sentiment analysis ensures positive marketing tone
- How to uncomment and register a tool
- See the tool being called automatically by the agent

### Exercise 3: Handoff Patterns (10 min)

**Objective:** Understand dynamic routing

**Instructions:**
1. Open `agent_handoff.py`
2. Run with different scenarios
3. Observe approval workflows
4. Note how context is preserved

**Test Scenarios:**
- Refund request (requires approval)
- Order tracking (no approval)
- Multi-agent: "I can't log in and need to track my order"

### Exercise 4: Group Chat Workflows (10 min)

**Objective:** Explore collaborative patterns

**Instructions:**
1. Open `agent_groupchat.py`
2. Run each workflow strategy (simple, iterative, agent-managed)
3. Compare outputs
4. Check generated markdown files in output/

## 💡 Key Concepts to Emphasize

1. **Pattern Selection:**
   - Sequential: Step-by-step processing
   - Handoff: Dynamic routing by request type
   - Group Chat: Collaborative problem-solving

2. **Tool Calling:**
   - Functions extend agent capabilities
   - Requires proper type annotations
   - Tools can be shared across agents

3. **Context Flow:**
   - Full conversation history available at each stage
   - Agents build on previous outputs

## 🔧 Troubleshooting Guide

**Problem:** Dependencies won't install
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Problem:** Azure authentication fails
```bash
az login --identity
az account show
```

**Problem:** Agent doesn't respond
- Check endpoint URL ends with `/`
- Verify deployment name
- Test with simple prompt first

**Problem:** Tools not being called
- Check type annotations
- Verify tool is registered
- Add explicit instruction to use tools

## 📊 Success Metrics

By end of workshop, participants should:
- [ ] Explain three orchestration patterns
- [ ] Build a sequential pipeline
- [ ] Add tools to agents
- [ ] Implement handoff workflows
- [ ] Choose appropriate pattern for use case

## 📚 Resources

- [Agent Framework Docs](https://learn.microsoft.com/agent-framework)
- [Sequential Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/sequential)
- [Group Chat Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/group-chat)
- [Handoff Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/handoff)

