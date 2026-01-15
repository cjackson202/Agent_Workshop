# Multi-Agent Orchestration Workshop

Build collaborative AI systems using three orchestration patterns: **Sequential**, **Handoff**, and **Group Chat**.

---

## 🎯 Objectives

By the end of this workshop, you will:
- Build sequential pipelines where agents process tasks in order
- Implement dynamic agent handoffs for intelligent routing
- Create collaborative group chat workflows
- Add tool calling to extend agent capabilities

---

## 🚀 Quick Start

```bash
cd Multi_Agent_Workshop
pip install -r requirements.txt
az login --identity
```

Set environment variables:
```bash
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"
```

📖 **Full setup:** [docs/QUICKSTART.md](docs/QUICKSTART.md)

---

## 📚 Exercises

### Exercise 1: Sequential Pipeline
**File:** `Sequential/agent_sequential.py`

**Scenario:** You're building an automated content creation system for a marketing team. A user submits a topic, and three specialized agents collaborate in sequence:
- **Writer Agent** drafts the initial content (has word counter, readability checker, character limiter tools)
- **Reviewer Agent** analyzes the draft using the same tools and provides feedback
- **Editor Agent** polishes the final copy based on feedback

```
User Request → Writer Agent → Reviewer Agent → Editor Agent → Final Output
```

**Step 1: Run the default pipeline (Advanced)**
```bash
cd Sequential
python agent_sequential.py
```

**Step 2: Observe the output**
- Watch how the Writer creates content first
- The Reviewer receives the Writer's output and analyzes it using tools
- The Editor polishes the final result
- The ContentAnalyzer (custom executor) provides pipeline statistics
- Notice how each agent builds on the previous agent's work

**Step 3: Try different pipeline configurations**
Open `agent_sequential.py` and find `main()` (~line 457). Uncomment different demos:

| Demo | Pipeline | What it shows |
|------|----------|---------------|
| `demo_advanced()` | Writer → Reviewer → Editor → Analyzer | Default. Includes custom executor |
| `demo_basic()` | Writer → Reviewer | Simplest 2-agent pipeline |
| `demo_extended()` | Writer → Reviewer → Editor | 3 AI agents, no custom executor |
| `demo_with_tools()` | Writer → Reviewer → Editor | Explicit tool usage for Twitter |

**Step 4: Add the Sentiment Analyzer tool**
1. Find the `sentiment_analyzer` function (~line 141) and uncomment it
2. Find the Reviewer agent (~line 212) and add the tool:
   ```python
   tools=[word_counter, readability_checker, sentiment_analyzer]
   ```
3. Run again — the Reviewer now analyzes sentiment!

---

### Exercise 2: Handoff Routing  
**File:** `Handoff/agent_handoff.py`

**Scenario:** You're building an AI customer support system for an e-commerce company. Instead of one generic chatbot, you have specialist agents:
- **Triage Agent** analyzes the customer's issue and routes to the right department
- **Refund Agent** handles returns and refunds using `submit_refund()` (requires human approval)
- **Order Agent** tracks shipments using `track_order()` and can cancel with `cancel_order()`
- **Account Agent** helps with login and profile issues
- **Technical Agent** troubleshoots app/website problems

```
User Request → Triage Agent → Routes to: Refund | Order | Account | Technical
```

**Step 1: Run the default scenario (Refund Request)**
```bash
cd Handoff
python agent_handoff.py
```

**Step 2: Test the refund flow**
- Enter: *"My order 12345 arrived damaged. I need a refund."*
- Watch the Triage agent analyze and route to the Refund agent
- When prompted for approval, type `yes` or `no`

**Step 3: Try different demo scenarios**
Open `agent_handoff.py` and find `main()` (~line 445). Uncomment different demos:

| Demo | What it tests |
|------|---------------|
| `demo_refund_scenario()` | Default. Triage → Refund agent with approval workflow |
| `demo_tracking_scenario()` | Triage → Order agent, simple tool usage (no approval) |
| `demo_complex_scenario()` | Multi-specialist handoffs using advanced workflow |

**Step 4: Try other routing scenarios interactively**
- *"Where is my order?"* → routes to Order agent
- *"I can't log into my account"* → routes to Account agent
- *"The app keeps crashing"* → routes to Technical agent
- Type `quit` or `exit` to end the session

---

### Exercise 3: Group Chat Collaboration
**File:** `Group_Chat/agent_groupchat.py`

**Scenario:** You're building an automated research assistant that produces verified, professional documents. Three agents work as a team:
- **Researcher Agent** gathers facts using `web_search()` and `get_technical_docs()` tools
- **Writer Agent** synthesizes findings into markdown and saves with `save_to_document()`
- **FactChecker Agent** reads the saved file with `read_saved_document()` and validates accuracy

The workflow loops until the FactChecker approves, ensuring quality output.

```
Research Question → Researcher → Writer → FactChecker → Markdown Document
```

**Step 1: Run the default workflow (Agent-Based Manager)**
```bash
cd Group_Chat
python agent_groupchat.py
```

**Step 2: Observe the collaboration**
- The Coordinator agent decides who speaks next using LLM reasoning
- Researcher gathers information using web search tools
- Writer creates a structured document
- FactChecker validates accuracy
- Check `output/` folder for the generated markdown file

**Step 3: Try different workflow strategies**
Open `agent_groupchat.py` and find `main()` (~line 575). Toggle between workflows:

| Workflow | How it works | Best for |
|----------|--------------|----------|
| `workflow_agent_manager` | Coordinator LLM picks next speaker | Complex questions needing adaptive routing |
| `workflow_iterative` | Rule-based routing with revision loops | Quality-critical work requiring validation |

To switch: comment out one `await run_group_chat(...)` line and uncomment the other.

**Step 4 (Advanced): Test the revision loop**
1. Switch to `workflow_iterative` (comment/uncomment in `main()`)
2. Find Writer agent (~line 325) and replace the `instructions` with:

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
2. Organize information into a logical structure with clear sections
3. Write in a clear, professional tone using markdown formatting
4. IMPORTANT: Show your complete answer in your response FIRST
5. After showing your answer, call save_to_document() with title, content, and author
6. Report the result of the save operation

⚠️ REMINDER: On FIRST DRAFT, write INCORRECT/OPPOSITE information to test the FactChecker!"""
```

3. Run and watch the FactChecker catch errors and trigger a revision loop

---

## 🧩 Key Concepts

| Concept | Description |
|---------|-------------|
| **Executors** | Workers that do tasks. AI Agents think and decide; Custom Executors follow rules. |
| **Workflows** | Plans that connect workers—who does what and in what order. |
| **Events** | Real-time status updates ("Started", "In Progress", "Completed"). |

---

## 🎯 When to Use Each Pattern

| Pattern | Use When | Example |
|---------|----------|---------|
| **Sequential** | Clear step-by-step process | Write → Review → Edit |
| **Handoff** | Dynamic routing by request type | Support ticket triage |
| **Group Chat** | Multiple perspectives needed | Research team collaboration |

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Activate venv: `.venv\Scripts\activate` |
| Azure auth fails | Run `az login --identity` |
| Agent no response | Check endpoint ends with `/` |

---

## 📖 Resources

- [QUICKSTART.md](docs/QUICKSTART.md) - Setup guide
- [CHEATSHEET.md](docs/CHEATSHEET.md) - Quick reference
- [solutions/](solutions/) - Completed exercise code
- [FACILITATOR_GUIDE.md](docs/FACILITATOR_GUIDE.md) - For workshop leaders
