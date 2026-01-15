# Quick Start Guide - Multi-Agent Orchestration Workshop

## 🎯 What You'll Learn (In Simple Terms)

**Core Concepts:**
1. **Executors** = Workers (AI agents or simple programs that do specific jobs)
2. **Workflows** = Plans (how workers collaborate to complete a project)
3. **Events** = Status updates (notifications about what's happening)

**Three Ways to Organize Workers:**
- **Sequential**: Workers line up and pass work down the line (assembly line)
- **Handoff**: A coordinator routes work to the right specialist (help desk)
- **Group Chat**: Workers collaborate and discuss (research team)

---

## 🚀 Getting Started in 5 Minutes

### 1️⃣ Setup Environment (2 min)

```bash
cd Multi_Agent_Workshop
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2️⃣ Configure Azure OpenAI (1 min)

```bash
# Windows PowerShell
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"

# Mac/Linux
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"
```

Or create `.env` file:
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

### 3️⃣ Authenticate (30 seconds)

```bash
az login --identity
az account show
```

### 4️⃣ Test Sequential (1 min)

```bash
cd Sequential
python agent_sequential.py
```

✅ **Success:** Pipeline executes Writer → Reviewer → Editor

### 5️⃣ Test Handoff (1 min)

```bash
cd ../Handoff
python agent_handoff.py
```

Try: `"My order 12345 arrived damaged. I need a refund."`

### 6️⃣ Test Group Chat (1 min)

```bash
cd ../Group_Chat
python agent_groupchat.py
```

---

## 📋 Workshop Exercises

### Exercise 1: Sequential Patterns (15 min)
**File:** `Sequential/agent_sequential.py`

**Tasks:**
1. Run basic, extended, and advanced pipelines
2. Modify agent instructions
3. Observe conversation flow

**Test prompts:**
- "Write a tagline for a budget-friendly eBike"
- "Create a tagline for an eco-friendly meal delivery service"

### Exercise 2: Add a Custom Tool (10 min)
**File:** `Sequential/agent_sequential.py`

**Tasks:**
1. Find the "EXERCISE" section (around line 100)
2. Remove the triple quotes (""") around the sentiment_analyzer tool
3. Scroll to the Reviewer agent (around line 245)
4. Add sentiment_analyzer to the functions list: `functions=[word_counter, readability_checker, sentiment_analyzer]`
5. Test with: "Write a positive tagline for a new smartphone and check its sentiment"

**What it does:**
Analyzes whether your marketing content has a positive, negative, or neutral tone - essential for ensuring your messaging resonates well with customers.

### Exercise 3: Handoff Patterns (10 min)
**File:** `Handoff/agent_handoff.py`

**Test scenarios:**
- Refund request (with approval)
- Order tracking (no approval)
- Multi-agent interaction

### Exercise 4: Group Chat Workflows (10 min)
**File:** `Group_Chat/agent_groupchat.py`

**Tasks:**
1. Run simple sequential workflow
2. Run iterative refinement workflow
3. Compare outputs
4. Check output/ folder for generated files

---

## 🎯 Pattern Selection Guide

| Pattern | Use When | Example |
|---------|----------|---------|
| **Sequential** | Step-by-step process | Write → Review → Edit |
| **Handoff** | Dynamic routing | Customer support triage |
| **Group Chat** | Collaboration needed | Research team |

---

## 🆘 Troubleshooting

### "Module not found"
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Azure auth fails
```bash
az login --identity
az account show
```

### Agent doesn't respond
- Check endpoint ends with `/`
- Verify deployment name
- Check Azure quota

### Tools not called
- Verify type annotations
- Check tool is registered
- Add instruction: "Use available tools"

---

## ✅ Workshop Checklist

- [ ] Configure Azure OpenAI
- [ ] Build sequential pipeline
- [ ] Add tools to agents
- [ ] Test handoff workflows
- [ ] Explore group chat patterns
- [ ] Choose right pattern for use case

---

## 📚 Next Steps

- [Agent Framework Docs](https://learn.microsoft.com/agent-framework)
- [Sequential Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/sequential)
- [Group Chat Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/group-chat)
- [Handoff Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/handoff)

---

**Workshop Time:** ~75 minutes  
**Prerequisites:** Python 3.10+, Azure OpenAI access, Azure CLI


### Prerequisites
- Python 3.10 or higher
- Azure OpenAI access with GPT-4 or GPT-4o deployment
- Azure CLI installed
- Git (to clone repository)

### 1️⃣ Setup Environment (3 min)

```bash
# Clone repository (if not already done)
cd Agent_Workshop/Multi_Agent_Workshop

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure Azure OpenAI (2 min)

**Option 1: Environment Variables (Recommended)**
```bash
# Windows PowerShell
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"

# Mac/Linux
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"
```

**Option 2: .env File**
Create a `.env` file in the root directory:
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

### 3️⃣ Authenticate with Azure (1 min)

```bash
az login --identity
az account show  # Verify correct subscription
```

### 4️⃣ Test Sequential Orchestration (2 min)

```bash
cd Sequential
python agent_sequential.py
```

✅ **You should see:** A pipeline executing Writer → Reviewer → Editor with streaming output

### 5️⃣ Test Handoff Orchestration (2 min)

```bash
cd ../Handoff
python agent_handoff.py
```

**Try this prompt:** "My order 12345 arrived damaged. I need a refund."

✅ **You should see:** Triage agent routing to Refund agent with approval workflow

### 6️⃣ Test Group Chat Orchestration (2 min)

```bash
cd ../Group_Chat
python agent_groupchat.py
```

✅ **You should see:** Researcher, Writer, and FactChecker collaborating

---

## 📋 Workshop Exercise Path

Follow these exercises in order:

### Exercise 1: Sequential Patterns (15 min)
**File:** `Sequential/agent_sequential.py`

**What you'll learn:**
- How sequential pipelines work
- Different pipeline configurations
- Custom executors vs agents

**Tasks:**
1. Run the basic pipeline (Writer → Reviewer)
2. Run the extended pipeline (Writer → Reviewer → Editor)
3. Run the advanced pipeline (with ContentAnalyzer)
4. Compare the outputs and execution patterns

**Test prompts:**
- "Write a tagline for a budget-friendly eBike"
- "Create a tagline for an eco-friendly meal delivery service"
- "Write a compelling tagline for a smart home security system"

### Exercise 2: Adding Tools (10 min)
**File:** `Sequential/agent_sequential.py`

**What you'll learn:**
- How to define tools as Python functions
- Tool registration with agents
- Tool calling in pipelines

**Tasks:**
1. Find the "EXERCISE 2" section in the code
2. Define a calculator tool
3. Register it with the Writer agent
4. Test with: "Write a tagline mentioning that our product saves users $1234 minus 200 dollars annually"

### Exercise 3: Handoff Patterns (10 min)
**File:** `Handoff/agent_handoff.py`

**What you'll learn:**
- Dynamic agent routing
- Human-in-the-loop approval
- Multi-agent collaboration

**Tasks:**
1. Run scenario 1: Refund request (with approval)
2. Run scenario 2: Order tracking (no approval)
3. Run scenario 3: Complex multi-agent interaction
4. Observe how context is preserved across handoffs

**Test prompts:**
- "My order 12345 arrived damaged. I need a refund."
- "Where is my order 67890?"
- "I can't log in and need to track my order 54321"

### Exercise 4: Group Chat Workflows (15 min)
**File:** `Group_Chat/agent_groupchat.py`

**What you'll learn:**
- Collaborative agent systems
- Speaker selection strategies
- Iterative refinement

**Tasks:**
1. Run simple sequential workflow
2. Run agent-managed workflow
3. Run iterative refinement workflow
4. Compare outputs for the same question

**Test prompts:**
- "What are the key benefits of async/await in Python?"
- "Explain the CAP theorem in distributed systems"
- "What are best practices for API design?"

### Exercise 5: Custom Tools (5 min)
**File:** `Group_Chat/agent_groupchat.py`

**What you'll learn:**
- Creating custom tools
- Tool integration in group chat
- Tool usage across multiple agents

**Tasks:**
1. Find the "EXERCISE 5" section
2. Add a new custom tool (e.g., calculator, translator)
3. Test with appropriate prompts
4. Observe which agents use the tool

---

## 🎯 Orchestration Pattern Decision Guide

### Use Sequential When:
- ✅ Clear step-by-step process
- ✅ Each stage builds on previous output
- ✅ Linear workflow (write → review → edit)
- ✅ Data processing pipelines

**Examples:** Content creation, data transformation, quality assurance

### Use Handoff When:
- ✅ Dynamic routing based on request type
- ✅ Specialized agents for different tasks
- ✅ Customer support / triage scenarios
- ✅ Need human approval for specific operations

**Examples:** Support ticketing, expert routing, approval workflows

### Use Group Chat When:
- ✅ Multiple perspectives needed
- ✅ Collaborative problem-solving
- ✅ Iterative refinement required
- ✅ Research and synthesis tasks

**Examples:** Research teams, peer review, brainstorming

---

## 🆘 Quick Troubleshooting

### Problem: "Module not found" errors
**Solution:** 
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Azure authentication errors
**Solution:**
```bash
az login --identity
az account show  # Verify correct subscription is selected
```

### Problem: "AZURE_OPENAI_ENDPOINT not found"
**Solution:**
- Set environment variables (see step 2 above)
- Or create a `.env` file in the root directory
- Verify endpoint URL ends with `/`

### Problem: Agent doesn't respond
**Solution:**
- Check deployment name matches exactly
- Verify Azure OpenAI endpoint is correct
- Check TPM/RPM quota in Azure portal
- Test with Azure OpenAI Studio first

### Problem: Tools not being called
**Solution:**
- Verify function has proper type annotations
- Check tool is registered with agent
- Add explicit instruction: "Use the available tools"
- Check function signature matches expected format

### Problem: Streaming output too fast/slow
**Solution:**
- Adjust `time.sleep()` values in the code
- Add `flush=True` to print statements

---

## 📊 Workshop Completion Checklist

By the end of this workshop, you should be able to:

- [ ] Configure Azure OpenAI for multi-agent systems
- [ ] Build sequential pipelines with multiple agents
- [ ] Implement dynamic agent handoffs
- [ ] Create collaborative group chat workflows
- [ ] Add tool calling to any agent
- [ ] Choose the right orchestration pattern for your use case
- [ ] Debug common multi-agent issues
- [ ] Implement human-in-the-loop approval workflows

---

## 📚 Next Steps

### Explore Advanced Topics
- Custom executors with complex logic
- Nested workflows (e.g., group chat within sequential)
- Streaming optimization techniques
- Error handling and retry logic
- Production deployment patterns

### Build Your Own
Choose a use case and build a multi-agent system:
- **Content Creation:** Writer → SEO Optimizer → Fact Checker → Publisher
- **Customer Support:** Triage → Product Expert → Billing → Technical → Escalation
- **Research System:** Searcher → Analyzer → Synthesizer → Validator
- **Code Review:** Coder → Security Reviewer → Performance Reviewer → Approver

### Additional Resources
- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/agent-framework)
- [Sequential Orchestration Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/sequential)
- [Group Chat Orchestration Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/group-chat)
- [Handoff Orchestration Guide](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/handoff)
- [GitHub Examples](https://github.com/microsoft/agent-framework/tree/main/samples)

---

## 📞 Support

If you encounter issues during the workshop:
1. Check this troubleshooting guide
2. Review the error message carefully
3. Check Azure portal for quota/authentication issues
4. Ask your workshop facilitator
5. Consult the official documentation

---

## ⏱️ Time Estimates

- **Environment Setup:** 5 minutes
- **Sequential Exercises:** 25 minutes
- **Handoff Exercises:** 10 minutes
- **Group Chat Exercises:** 20 minutes
- **Custom Tools:** 5 minutes
- **Q&A and Wrap-up:** 10 minutes

**Total Workshop Time:** ~75-90 minutes
