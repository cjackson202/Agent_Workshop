# Multi-Agent Orchestration Cheat Sheet

## 🎯 Quick Reference

### Core Concepts (Building Blocks)

Think of building a multi-agent system like setting up a team:

| Concept | Simple Explanation | Real-World Analogy |
|---------|-------------------|-------------------|
| **Executor** | A worker that does a specific job | Team member with a specialty |
| **Workflow** | The plan for how workers collaborate | Project plan or assembly line |
| **Events** | Status updates as work progresses | Email notifications or status reports |
| **Edges** | Connections between workers | Who passes work to whom |

**Executors** - The Workers:
- **AI Agents**: Smart workers who think and make decisions (like a consultant)
- **Custom Executors**: Simple workers who follow rules (like a calculator)
- Each has one job, passes results to the next worker

**Workflows** - The Plan:
- Connects workers in an order (sequential, handoff, or group chat)
- Manages information flow between workers
- Like an assembly line or routing system

**Events** - The Updates:
- Tell you what's happening in real-time
- Like package tracking: "Started", "In Progress", "Completed"
- Help you debug and monitor your system

---

### Orchestration Patterns

| Pattern | Use Case | Key Feature | Example |
|---------|----------|-------------|---------|
| **Sequential** | Step-by-step processing | Linear pipeline | Writer → Reviewer → Editor |
| **Handoff** | Dynamic routing | Specialized agents | Triage → Refund/Order/Account Agent |
| **Group Chat** | Collaboration | Multiple perspectives | Researcher + Writer + FactChecker |

---

## 📦 Installation & Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure Azure OpenAI
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"

# Authenticate
az login --identity
```

---

## 🔄 Sequential Orchestration

### Basic Structure
```python
from agent_framework import SequentialBuilder
from agent_framework.azure import AzureOpenAIChatClient

chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())

# Create agents
agent1 = chat_client.create_agent(instructions="...", name="Agent1")
agent2 = chat_client.create_agent(instructions="...", name="Agent2")

# Build workflow
workflow = SequentialBuilder().participants([agent1, agent2]).build()

# Run
async for event in workflow.run_stream("Your task"):
    if isinstance(event, AgentRunUpdateEvent):
        print(event.data, end="", flush=True)
```

### Key Features
- **Linear flow:** Output → Input chain
- **Full history:** Each agent gets complete conversation
- **Custom executors:** Add non-LLM processing stages

### When to Use
✅ Editorial workflows (write → review → edit)  
✅ Data processing pipelines  
✅ Quality assurance flows  
✅ Multi-stage content creation

---

## 🔀 Handoff Orchestration

### Basic Structure
```python
from agent_framework import HandoffBuilder, HandoffConfig

# Create agents with handoff configs
triage = chat_client.create_agent(
    instructions="Route to appropriate agent",
    name="Triage",
    handoff_config=HandoffConfig([
        HandoffTo(target="RefundAgent", description="Refunds and returns"),
        HandoffTo(target="OrderAgent", description="Tracking and shipping"),
    ])
)

# Build workflow
workflow = HandoffBuilder().participants([triage, refund_agent, order_agent]).build()

# Run with user input
async for event in workflow.run_stream(task="Your request"):
    # Handle streaming, user input, approvals
    pass
```

### Key Features
- **Dynamic routing:** Based on request content
- **Human-in-the-loop:** Approval for sensitive operations
- **Context preservation:** Full history across handoffs
- **Bi-directional:** Can return to previous agents

### When to Use
✅ Customer support systems  
✅ Expert routing scenarios  
✅ Approval workflows  
✅ Multi-department operations

---

## 💬 Group Chat Orchestration

### Basic Structure
```python
from agent_framework import GroupChatBuilder

# Create agents with tools
researcher = chat_client.create_agent(
    instructions="Research and gather information",
    name="Researcher",
    functions=[web_search, get_docs]
)

writer = chat_client.create_agent(
    instructions="Synthesize into document",
    name="Writer",
    functions=[save_document]
)

# Build workflow (simple sequential)
workflow = (
    GroupChatBuilder()
    .participants([researcher, writer, fact_checker])
    .speaker_selection_simple_sequential()
    .build()
)

# Or agent-based manager
workflow = (
    GroupChatBuilder()
    .participants([researcher, writer, fact_checker])
    .speaker_selection_agent_based(manager_agent)
    .build()
)

# Run
async for event in workflow.run_stream("Research question"):
    # Handle events
    pass
```

### Speaker Selection Strategies

| Strategy | How It Works | Best For |
|----------|--------------|----------|
| **Simple Sequential** | Fixed order (A → B → C) | Predictable workflows |
| **Agent-Based** | Manager selects next speaker | Complex routing |
| **Iterative** | Quality checks, can loop back | Refinement needed |

### When to Use
✅ Research and synthesis  
✅ Peer review workflows  
✅ Collaborative brainstorming  
✅ Multi-perspective analysis

---

## 🎭 Understanding Events (Status Updates)

Events are like notifications that tell you what's happening. Here are the main types:

### Common Event Types (in simple terms)

| Event | What It Means | When You See It |
|-------|---------------|-----------------|
| **AgentRunUpdateEvent** | Agent is thinking/writing | Text appears as agent works |
| **WorkflowOutputEvent** | Job complete, here's the result | At the very end |
| **RequestInfoEvent** | Agent needs more information | During handoff workflows |

**Think of it like ordering food:**
- `AgentRunUpdateEvent`: "Your order is being prepared" (ongoing updates)
- `WorkflowOutputEvent`: "Your order is ready!" (final result)
- `RequestInfoEvent`: "What size drink would you like?" (needs input)

### Watching Events in Code

```python
async for event in workflow.run_stream(task):
    if isinstance(event, AgentRunUpdateEvent):
        # Agent is working - show progress
        print(event.data, end="", flush=True)
    
    elif isinstance(event, WorkflowOutputEvent):
        # All done - show final result
        final_result = event.data
```

---

## 🔧 Tool Calling

### Define a Tool
```python
from typing import Annotated

def calculator(
    operation: Annotated[str, "The operation: add, subtract, multiply, divide"],
    a: Annotated[float, "First number"],
    b: Annotated[float, "Second number"]
) -> str:
    """Perform basic arithmetic operations."""
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = a / b if b != 0 else "Error: Division by zero"
    return f"Result: {result}"
```

### Register Tool with Agent
```python
agent = chat_client.create_agent(
    instructions="You can use the calculator tool for math",
    name="MathAgent",
    functions=[calculator]
)
```

### Tool Requirements
- Type annotations with `Annotated[type, "description"]`
- Docstring describing the tool's purpose
- Return string or JSON serializable data
- Handle errors gracefully

---

## 🎭 Event Handling

### Common Event Types
```python
async for event in workflow.run_stream(task):
    if isinstance(event, AgentRunUpdateEvent):
        # Streaming text from agent
        print(event.data, end="", flush=True)
    
    elif isinstance(event, WorkflowOutputEvent):
        # Final conversation result
        messages = event.data
    
    elif isinstance(event, UserInputRequestedEvent):
        # User input needed
        user_input = input(event.data)
        await workflow.send_user_input(user_input)
    
    elif isinstance(event, ActionRequested):
        # Approval needed
        approval = input(f"Approve? (y/n): ")
        await workflow.respond_to_action(event.id, approval == "y")
```

---

## 📝 Agent Instructions Best Practices

### Structure
```
You are a [ROLE].

Your responsibilities:
- [Task 1]
- [Task 2]
- [Task 3]

Guidelines:
- [Guideline 1]
- [Guideline 2]

[Additional context or constraints]
```

### Examples

**Good Instructions:**
```
You are a technical writer specializing in API documentation.

Your responsibilities:
- Create clear, concise documentation
- Include code examples
- Follow REST API conventions

Guidelines:
- Use active voice
- Keep examples practical
- Include error handling
```

**Poor Instructions:**
```
Write documentation.
```

### Tips
✅ Be specific about role and scope  
✅ Provide clear guidelines  
✅ Include examples when helpful  
✅ Set tone/style expectations  
❌ Don't be vague or generic  
❌ Don't include conflicting instructions

---

## 🐛 Common Issues & Solutions

### Problem: Agent doesn't respond
```python
# Check: 
# 1. Endpoint URL ends with /
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://resource.openai.azure.com/"

# 2. Deployment name is correct
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"

# 3. Authentication works
az login --identity
az account show
```

### Problem: Tools not being called
```python
# Ensure proper annotations
def my_tool(
    param: Annotated[str, "Description"]  # Required!
) -> str:
    """Tool description"""  # Required!
    return "result"

# Add explicit instruction
instructions = "Use the available tools to complete tasks."
```

### Problem: Streaming not working
```python
# Add flush=True
print(event.data, end="", flush=True)

# Add small delay for smooth output
time.sleep(0.03)
```

### Problem: Azure authentication fails
```bash
# Re-authenticate
az login --identity
az account set --subscription "your-subscription-id"
```

---

## 📊 Performance Tips

### Optimize Streaming
```python
# Buffer updates
last_update_time = 0
buffer = ""

async for event in workflow.run_stream(task):
    if isinstance(event, AgentRunUpdateEvent):
        buffer += event.data
        current_time = time.time()
        
        if current_time - last_update_time > 0.05:  # 50ms
            print(buffer, end="", flush=True)
            buffer = ""
            last_update_time = current_time
```

### Reduce Token Usage
```python
# Truncate conversation history for long workflows
def truncate_history(messages, max_messages=10):
    return messages[-max_messages:]
```

### Parallel Tool Calls
```python
# Agent framework automatically handles parallel tool calls
# when multiple tools are needed simultaneously
```

---

## 🔐 Security Best Practices

### Environment Variables
```python
# Use environment variables for secrets
from dotenv import load_dotenv
load_dotenv()

# Never hardcode credentials
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # ✅ Good
endpoint = "https://my-resource.openai.azure.com/"  # ❌ Bad
```

### Human Approval
```python
# Require approval for sensitive operations
action_config = ActionConfiguration(
    description="Approve refund",
    requires_approval=True
)

# Check approval in tool
if not approved:
    return "Operation cancelled by user"
```

### Input Validation
```python
def process_order(order_id: Annotated[str, "Order ID"]) -> str:
    # Validate input
    if not order_id.isalnum():
        return "Invalid order ID format"
    
    # Sanitize before using
    order_id = order_id.strip()
    # ... process
```

---

## 📚 Key Imports

```python
# Core framework
from agent_framework import (
    SequentialBuilder,
    HandoffBuilder,
    GroupChatBuilder,
    ChatMessage,
    Role,
    WorkflowOutputEvent,
    AgentRunUpdateEvent,
    UserInputRequestedEvent
)

# Azure OpenAI
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential, DefaultAzureCredential

# Tool calling
from typing import Annotated

# Utilities
import asyncio
import os
from dotenv import load_dotenv
```

---

## 🎓 Learning Path

1. **Start:** Sequential orchestration (simplest)
2. **Next:** Add tool calling to agents
3. **Then:** Explore handoff patterns
4. **Advanced:** Group chat with multiple strategies
5. **Expert:** Custom executors and nested workflows

---

## 📞 Resources

- [Official Documentation](https://learn.microsoft.com/agent-framework)
- [GitHub Repository](https://github.com/microsoft/agent-framework)
- [Sample Code](https://github.com/microsoft/agent-framework/tree/main/samples)
- [API Reference](https://learn.microsoft.com/agent-framework/api)

---

## 💡 Quick Tips

✅ Start simple, add complexity gradually  
✅ Test each agent individually first  
✅ Use descriptive agent names  
✅ Log events for debugging  
✅ Handle errors gracefully  
✅ Validate tool inputs  
✅ Use environment variables for config  
✅ Test with small examples first  
❌ Don't nest too many agents  
❌ Don't make instructions too long  
❌ Don't skip error handling
