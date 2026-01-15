# Multi-Agent Orchestration Workshop

> **Learn to build collaborative AI systems using Microsoft Agent Framework**

This hands-on workshop teaches you how to build multi-agent systems using three key orchestration patterns: Sequential, Handoff, and Group Chat.

---

## 🧩 Core Concepts (Building Blocks)

Before diving in, understand these simple concepts:

### 1. Executors - Your Workers
Think of executors as team members, each with a specific job:
- **AI Agents**: Smart workers who think and make decisions (like a consultant)
- **Custom Executors**: Simple workers who follow rules (like a calculator)

**Example**: A Writer agent creates content, while a calculator executor does math.

### 2. Workflows - Your Plan
A workflow is like a project plan that connects workers:
- Defines who does what and in what order
- Manages how information flows between workers
- Like an assembly line or org chart

**Example**: Writer creates → Reviewer checks → Editor polishes

### 3. Events - Your Status Updates
Events tell you what's happening in real-time:
- Like package tracking: "Started", "In Progress", "Delivered"
- Helps you see what each worker is doing
- Useful for debugging and monitoring

**Example**: "Writer is working...", "Reviewer completed", "All done!"

---

## 🎯 Learning Objectives

By the end of this workshop, you will:
- ✅ Understand three multi-agent orchestration patterns
- ✅ Build sequential pipelines (Write → Review → Edit)
- ✅ Implement dynamic agent handoffs (triage and routing)
- ✅ Create collaborative group chat workflows
- ✅ Add tool calling to extend agent capabilities
- ✅ Choose the right pattern for your use case

---

## 📋 Prerequisites

- **Python 3.10+** installed
- **Azure OpenAI** access with GPT-4 or GPT-4o deployment
- **Azure CLI** installed (`az` command)
- **Git** (to clone repository)
- Basic understanding of async/await in Python
- Familiarity with AI agents (Day 1 & 2 of workshop series)

---

## 🚀 Quick Start

```bash
# Setup
cd Multi_Agent_Workshop
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure Azure
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"

# Authenticate
az login --identity

# Run first demo
cd Sequential
python agent_sequential.py
```

📖 **Full setup:** See [docs/QUICKSTART.md](docs/QUICKSTART.md)

---

## 🔄 Orchestration Patterns

### 1. Sequential Orchestration
**Location:** `Sequential/agent_sequential.py`

Pipeline workflows where agents process tasks in order. Output from one agent becomes input for the next.

**Example:** Writer → Reviewer → Editor

**Use Cases:**
- Editorial workflows
- Data processing pipelines
- Quality assurance flows
- Multi-stage content creation

**Features:**
- ✅ Tool calling (calculator, word counter)
- ✅ Custom executors for analytics
- ✅ Multiple pipeline configurations

**Run:**
```bash
cd Sequential
python agent_sequential.py
```

**Exercise: Add Sentiment Analyzer Tool**

The sentiment analyzer tool is already written but commented out. Here's how to enable it:

**Step 1: Uncomment the tool function**
- Open `Sequential/agent_sequential.py`
- Go to lines 141-157
- Remove the triple quotes `"""` before and after the `sentiment_analyzer` function

**Step 2: Add it to the Reviewer agent**
- Find the Reviewer agent definition (around line 212)
- Change: `tools=[word_counter, readability_checker]`
- To: `tools=[word_counter, readability_checker, sentiment_analyzer]`

**Step 3: Update instructions**
- In the Reviewer agent's instructions (lines 197-211), add:
  ```python
  3. THIRD: Call sentiment_analyzer to check emotional tone
  ```

**Step 4: Test it**
```bash
python agent_sequential.py
```

The Reviewer will now analyze sentiment for marketing content!

---

### 2. Handoff Orchestration
**Location:** `Handoff/agent_handoff.py`

Dynamic routing where agents transfer control based on request type. Like a customer support system with specialized departments.

**Example:** Triage → Refund/Order/Account/Technical Agent

**Use Cases:**
- Customer support systems
- Expert routing
- Approval workflows
- Multi-department operations

**Features:**
- ✅ Dynamic agent selection
- ✅ Human-in-the-loop approval
- ✅ Context preservation across handoffs
- ✅ Interactive user input

**Run:**
```bash
cd Handoff
python agent_handoff.py
```

**Try:** "My order 12345 arrived damaged. I need a refund."

---

### 3. Group Chat Orchestration
**Location:** `Group_Chat/agent_groupchat.py`

Collaborative workflows where multiple agents work together with intelligent speaker selection.

**Example:** Researcher + Writer + FactChecker

**Use Cases:**
- Research and synthesis
- Peer review workflows
- Collaborative problem-solving
- Multi-perspective analysis

**Features:**
- ✅ Web search and documentation tools
- ✅ Document generation
- ✅ Multiple workflow strategies (sequential, iterative, agent-managed)
- ✅ Quality validation and refinement

**Run:**
```bash
cd Group_Chat
python agent_groupchat.py
```

**Output:** Check `output/` folder for generated markdown files

---

### Group Chat Exercises

**Understanding the Two Group Chat Workflow Strategies**

Group Chat supports multiple orchestration approaches. We'll focus on two advanced patterns (Sequential orchestration is covered in the Sequential module):

| Workflow | Speaker Selection | Iteration | Best For |
|----------|------------------|-----------|----------|
| **Agent-Based Manager** | Coordinator agent decides | Limited by termination condition | Complex questions needing adaptive routing |
| **Iterative Refinement** | Smart function with feedback analysis | Yes - loops until approved | Quality-critical work requiring validation |

**Key Differences Explained:**

**1. Agent-Based Manager (`workflow_agent_manager`)**
- Uses Coordinator agent to intelligently select next speaker
- LLM decides who speaks based on conversation context
- Can adapt to conversation needs
- More flexible but uses extra LLM calls for coordination
- Think: Project manager delegating tasks dynamically

**2. Iterative Refinement (`workflow_iterative`)**
- Uses `iterative_selector()` function that analyzes FactChecker feedback
- Routes back to Writer or Researcher based on specific issues found
- Continues until FactChecker approves or max rounds reached
- Ensures quality through revision loops
- Think: Editorial process with multiple draft revisions

---

### Group Chat Exercises

**Understanding the Two Group Chat Workflow Strategies**

Group Chat supports multiple orchestration approaches. We'll focus on two advanced patterns (Sequential orchestration is covered in the Sequential module):

| Workflow | Speaker Selection | Iteration | Best For |
|----------|------------------|-----------|----------|
| **Agent-Based Manager** | Coordinator agent decides | Limited by termination condition | Complex questions needing adaptive routing |
| **Iterative Refinement** | Smart function with feedback analysis | Yes - loops until approved | Quality-critical work requiring validation |

**Key Differences Explained:**

**1. Agent-Based Manager (`workflow_agent_manager`)**
- Uses Coordinator agent to intelligently select next speaker
- LLM decides who speaks based on conversation context
- Can adapt to conversation needs
- More flexible but uses extra LLM calls for coordination
- Think: Project manager delegating tasks dynamically

**2. Iterative Refinement (`workflow_iterative`)**
- Uses `iterative_selector()` function that analyzes FactChecker feedback
- Routes back to Writer or Researcher based on specific issues found
- Continues until FactChecker approves or max rounds reached
- Ensures quality through revision loops
- Think: Editorial process with multiple draft revisions

---

**Exercise 1: Run Agent-Based Manager Workflow (10 min)**

Try the intelligent coordinator approach.

**Steps:**
1. Open [agent_groupchat.py](Group_Chat/agent_groupchat.py)
2. In `main()` function (around line 590), uncomment:
   ```python
   # 1. Agent-based manager (intelligent coordination) - uncomment to try
   await run_group_chat(workflow_agent_manager, tasks[0], "Agent-Based Manager Workflow")
   ```
3. Comment out the iterative workflow line
4. Run: `python agent_groupchat.py`

**Observe:**
- Coordinator agent decides which specialist to call next
- More adaptive than simple sequential patterns
- Context-aware speaker selection
- **Key Insight**: Watch the Coordinator's reasoning in brackets. It's using an LLM to make intelligent routing decisions instead of following hardcoded rules.

---

**Exercise 2: Run Iterative Refinement Workflow (10 min)**

Try the feedback-based revision approach with default agent behavior.

**Steps:**
1. In `main()` function (around line 590), ensure this line is uncommented:
   ```python
   # 2. Iterative refinement (allows multiple rounds if FactChecker finds issues)
   await run_group_chat(workflow_iterative, tasks[0], "Iterative Refinement Workflow")
   ```
2. Comment out the agent-based manager workflow line
3. Run: `python agent_groupchat.py`

**Observe:**
- Linear flow: Researcher → Writer → FactChecker
- FactChecker reads the saved document using `read_saved_document()` tool
- Workflow analyzes FactChecker's verdict
- If approved, workflow ends; if issues found, routes back to Writer or Researcher
- **Key Insight**: The `iterative_selector()` function uses deterministic keyword parsing (not LLM) to route based on FactChecker feedback

**Compare with Exercise 1:**
- Agent-based Manager: LLM-based coordination, adaptive but more token usage
- Iterative Refinement: Rule-based routing on keywords, predictable and efficient for quality loops

---

**Exercise 3: Testing the Fact Checker with Deliberate Errors (Advanced, 20 min)**

Now that you've seen both workflows, test the iterative refinement's error-correction capabilities by deliberately introducing errors.

**Learning Objectives:**
- Validate that quality control agents actually work (not just rubber stamps)
- See multi-round revision loops in action
- Learn how to write effective agent instructions with emphasis
- Understand instruction design principles for agent behavior modification

**Prerequisites:** Complete Exercises 1 and 2 first to understand both orchestration approaches.

**Step 1: Verify iterative workflow is enabled**

Ensure the `main()` function (around line 590) has the iterative workflow uncommented:

```python
# 2. Iterative refinement (allows multiple rounds if FactChecker finds issues)
await run_group_chat(workflow_iterative, tasks[0], "Iterative Refinement Workflow")
```

**Step 2: Add the testing instruction to Writer agent**

Find the Writer agent definition (around line 325) and replace the instructions with this enhanced version that deliberately produces wrong answers first:

```python
instructions="""You are a technical writer. Your job is to create clear, well-structured answers and save them to professional documents.

⚠️ CRITICAL INSTRUCTION - MUST FOLLOW ON FIRST DRAFT:
ON YOUR FIRST DRAFT, you MUST intentionally write the OPPOSITE or INCORRECT version of what the Researcher provided.
This is a testing mechanism to ensure the FactChecker properly validates information.
Examples:
- If Researcher says "async/await improves performance" → Write "async/await decreases performance"
- If Researcher says "Python 3.x" → Write "Python 2.x"
- If Researcher provides benefits → Write drawbacks instead
You will be asked to revise after the FactChecker reviews. This is intentional and expected.

Guidelines:
1. Review the research provided by the Researcher
2. Organize information into a logical structure with clear sections:
   - Introduction/Overview
   - Key Points (with subheadings)
   - Examples or Use Cases (if applicable)
   - Sources/References
   - Conclusion or Summary
3. Write in a clear, professional tone using markdown formatting
4. Use proper markdown: ## for headings, **bold** for emphasis, - for bullets, ``` for code
5. IMPORTANT: Show your complete answer in your response FIRST, so the FactChecker can review it
6. After showing your answer, call save_to_document() with:
   - title: The question being answered
   - content: Your complete, well-formatted answer (the same content you just showed)
   - author: "AI Research Team"
7. Report the result of the save operation

**CRITICAL SOURCE ATTRIBUTION RULES:**
- ONLY cite sources that the Researcher explicitly provided
- DO NOT add, invent, or hallucinate additional sources
- Copy the exact source citations from the Researcher's findings
- If the Researcher provided limited sources, that's fine - use only those
- Never add links or references that weren't in the Researcher's output

Format your response like this:
---
[Your complete formatted answer here with all sections]
---
I've saved this answer using save_to_document().

Make your response comprehensive and well-formatted, but use ONLY the research and sources provided by the Researcher.

⚠️ REMINDER: On FIRST DRAFT, write INCORRECT/OPPOSITE information to test the FactChecker!""",
```

**Step 3: Run and observe**

```bash
python agent_groupchat.py
```

Watch carefully:
1. **Researcher** gathers accurate information about async/await benefits
2. **Writer** intentionally writes WRONG information (e.g., "decreases performance")
3. **FactChecker** calls `read_saved_document()` and identifies specific errors
4. **Writer** gets a second chance and produces the correct version
5. **FactChecker** approves the corrected content

**Step 4: Key observations**

Notice how the instruction works:
- ⚠️ emoji and "CRITICAL INSTRUCTION" at the top grab attention
- Concrete examples show exactly what "opposite" means
- Reminder at the end reinforces the behavior
- Placement matters: prominent instructions override general guidelines

**Why this matters:**
- **Validates workflows**: Proves the FactChecker actually catches errors
- **Tests iteration**: Demonstrates multi-round refinement works
- **Instruction design**: Shows how to write emphatic agent instructions
- **Production readiness**: Ensures QA agents aren't rubber stamps

**Expected output:**
- Round 1: Wrong answer saved to document
- FactChecker: "⚠ NEEDS REVISION: [lists specific errors]"
- Round 2: Correct answer saved
- FactChecker: "✓ APPROVED: Answer is accurate, complete, and well-structured."

**Compare with Exercises 1 & 2:**
- Agent-based Manager: LLM coordination, could iterate but relies on Coordinator's judgment
- Iterative Refinement (normal): Typically completes in one pass when content is good
- Iterative Refinement (with errors): **Demonstrates revision loops** - catches errors and routes back for fixes

**Key Insight**: The `iterative_selector()` function parses FactChecker responses for keywords like "NEEDS REVISION", "missing", "incomplete". When found, it intelligently routes back to Writer (for content issues) or Researcher (for missing information). This is deterministic logic that ensures quality validation actually happens.

**Bonus challenges:**
1. Change the critical instruction to introduce different types of errors (formatting, missing sections, etc.)
2. Modify the FactChecker to be more or less strict
3. Test what happens with 3+ revision rounds
4. Try removing the prominent formatting - does it still work?

---

## 📚 Workshop Structure

| Time | Module | Activity |
|------|--------|----------|
| 10 min | Introduction | Why multi-agent? Pattern overview |
| 30 min | Sequential | Build pipelines, add tools |
| 25 min | Handoff | Dynamic routing, approvals |
| 20 min | Group Chat | Collaborative workflows |
| 5 min | Wrap-up | Pattern comparison, Q&A |

**Total:** ~90 minutes

---

## 📖 Documentation

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[FACILITATOR_GUIDE.md](docs/FACILITATOR_GUIDE.md)** - For workshop leaders
- **[CHEATSHEET.md](docs/CHEATSHEET.md)** - Quick reference guide
- **[solutions/](solutions/)** - Completed exercise code

---

## 🎓 Exercises

### Exercise 1: Sequential Patterns (15 min)
Run and modify sequential workflows. Observe how each agent builds on previous output.

### Exercise 2: Add Custom Tool (10 min)
Create a new tool (e.g., temperature converter) and register it with an agent.

### Exercise 3: Handoff Scenarios (10 min)
Test different routing scenarios with approval workflows.

### Exercise 4: Group Chat Strategies (10 min)
Compare simple sequential, iterative, and agent-managed workflows.

---

## 🎯 Pattern Decision Guide

**Choose Sequential when:**
- Clear step-by-step process
- Each stage builds on previous output
- Example: Write → Review → Edit

**Choose Handoff when:**
- Dynamic routing based on request type
- Specialized agents for different tasks
- Example: Support ticket routing

**Choose Group Chat when:**
- Multiple perspectives needed
- Collaborative problem-solving
- Example: Research team

---

## 🔧 Configuration

### Environment Variables

Create `.env` file or set:
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

### Requirements

```
agent-framework
azure-identity
python-dotenv
```

Install: `pip install -r requirements.txt`

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Activate venv: `.venv\Scripts\activate` |
| Azure auth fails | Run `az login --identity` |
| Agent no response | Check endpoint ends with `/` |
| Tools not called | Verify type annotations |

See [QUICKSTART.md](docs/QUICKSTART.md) for more troubleshooting.

---

## 📊 What You'll Build

### Sequential Pipeline
```
User Request
    ↓
Writer Agent (with calculator tool)
    ↓
Reviewer Agent (with word counter)
    ↓
Editor Agent
    ↓
Final Output
```

### Handoff System
```
User Request
    ↓
Triage Agent
    ↓
Dynamic routing to:
- Refund Agent (with approval)
- Order Agent (tracking tool)
- Account Agent
- Technical Agent
```

### Group Chat Team
```
Research Question
    ↓
Researcher (web search + docs)
    ↓
Writer (document creation)
    ↓
FactChecker (validation)
    ↓
Professional Markdown Document
```

---

## 📚 Additional Resources

**Microsoft Documentation:**
- [Agent Framework Overview](https://learn.microsoft.com/agent-framework)
- [Sequential Orchestration](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/sequential)
- [Group Chat Orchestration](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/group-chat)
- [Handoff Orchestration](https://learn.microsoft.com/agent-framework/user-guide/workflows/orchestrations/handoff)

**Code Samples:**
- [Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Multi-Agent Examples](https://github.com/microsoft/agent-framework/tree/main/samples)

---

## 🤝 Contributing

This workshop is part of the Agent Workshop series:
1. Azure AI Foundry Agents (Day 1)
2. Model Context Protocol - MCP (Day 2)
3. **Multi-Agent Orchestration (Day 3)** ← You are here

---

## 📝 Next Steps

After completing this workshop:
1. Build a multi-agent system for your use case
2. Explore nested workflows (combine patterns)
3. Add custom executors for specialized processing
4. Implement error handling and retry logic
5. Deploy to production

---

## ⏱️ Time Estimates

- **Environment Setup:** 5 min
- **Sequential Exercises:** 25 min
- **Handoff Exercises:** 25 min
- **Group Chat Exercises:** 20 min
- **Q&A:** 5 min

**Total:** 80-90 minutes