"""
Sequential Orchestration Demo
Demonstrates pipeline workflows where agents process tasks in order
"""

import asyncio
import os
import time
from typing import Any
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import SequentialBuilder, ChatMessage, Role
from agent_framework import WorkflowOutputEvent, AgentRunUpdateEvent
from agent_framework import Executor, WorkflowContext, handler
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


# =============================================================================
# 1. SET UP AZURE OPENAI CHAT CLIENT
# =============================================================================

# Configuration
if not os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"):
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"

if not os.getenv("AZURE_OPENAI_ENDPOINT"):
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource.openai.azure.com/"

chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())


# =============================================================================
# 2. DEFINE AGENTS FOR SEQUENTIAL PIPELINE
# =============================================================================

# Stage 1: Writer - Creates initial content
writer = chat_client.create_agent(
    instructions="""You are a creative copywriter. Create compelling, concise marketing content.
    
Guidelines:
- Write a punchy, memorable tagline or short paragraph
- Focus on benefits and emotional appeal
- Keep it brief but impactful
- Use active voice and strong verbs""",
    name="Writer",
)

# Stage 2: Reviewer - Provides constructive feedback
reviewer = chat_client.create_agent(
    instructions="""You are a marketing reviewer. Provide constructive feedback on the content.
    
Your review should:
- Assess clarity, impact, and memorability
- Identify strengths and weaknesses
- Suggest specific improvements
- Rate the content (1-10)
- Be constructive but honest""",
    name="Reviewer",
)

# Stage 3: Editor - Revises based on feedback
editor = chat_client.create_agent(
    instructions="""You are an expert editor. Revise the original content based on the reviewer's feedback.
    
Your responsibilities:
- Read the original content and reviewer feedback carefully
- Make specific improvements addressing the feedback
- Maintain the original intent and voice
- Produce a final, polished version
- Explain what changes you made and why""",
    name="Editor",
)


# =============================================================================
# 3. DEFINE CUSTOM EXECUTOR FOR SPECIALIZED PROCESSING
# =============================================================================

class ContentAnalyzer(Executor):
    """Custom executor that analyzes the conversation without using an LLM."""
    
    @handler
    async def analyze(
        self,
        conversation: list[ChatMessage],
        ctx: WorkflowContext[list[ChatMessage]]
    ) -> None:
        """Analyze conversation statistics and append summary."""
        
        # Count messages by role
        user_msgs = sum(1 for m in conversation if m.role == Role.USER)
        assistant_msgs = sum(1 for m in conversation if m.role == Role.ASSISTANT)
        
        # Calculate word counts
        total_words = sum(len(m.text.split()) for m in conversation)
        
        # Get agent names
        agents = set(m.author_name for m in conversation if m.author_name)
        
        # Create analysis summary
        analysis = f"""
📊 **Content Pipeline Analysis**

**Pipeline Statistics:**
- Total messages: {len(conversation)}
- User queries: {user_msgs}
- Agent responses: {assistant_msgs}
- Agents involved: {', '.join(sorted(agents))}
- Total words generated: {total_words}

**Pipeline Status:** ✓ Complete
**Quality Gate:** All stages processed successfully
"""
        
        # Add analysis message to conversation
        summary_msg = ChatMessage(
            role=Role.ASSISTANT,
            text=analysis.strip(),
            author_name="ContentAnalyzer"
        )
        
        await ctx.send_message(list(conversation) + [summary_msg])


# =============================================================================
# 4. BUILD SEQUENTIAL WORKFLOWS
# =============================================================================

# Basic Sequential: Writer -> Reviewer
workflow_basic = (
    SequentialBuilder()
    .participants([writer, reviewer])
    .build()
)

# Extended Sequential: Writer -> Reviewer -> Editor
workflow_extended = (
    SequentialBuilder()
    .participants([writer, reviewer, editor])
    .build()
)

# Advanced Sequential with Custom Executor: Writer -> Reviewer -> Editor -> Analyzer
content_analyzer = ContentAnalyzer(id="ContentAnalyzer")
workflow_advanced = (
    SequentialBuilder()
    .participants([writer, reviewer, editor, content_analyzer])
    .build()
)


# =============================================================================
# 5. WORKFLOW EXECUTION
# =============================================================================

async def run_sequential_workflow(workflow, task: str, workflow_name: str = "Sequential Workflow"):
    """
    Execute a sequential workflow and display results.
    
    Args:
        workflow: The configured Sequential workflow
        task: The task to process
        workflow_name: Display name for the workflow
    """
    print(f"\n{'='*80}")
    print(f"{workflow_name.upper()}")
    print(f"{'='*80}")
    print(f"Task: {task}\n")
    print("=" * 80)
    
    output_evt: WorkflowOutputEvent | None = None
    last_executor_id = None
    
    # Run workflow and stream events
    async for event in workflow.run_stream(task):
        if isinstance(event, AgentRunUpdateEvent):
            # Print streaming updates
            eid = event.executor_id
            if eid != last_executor_id:
                if last_executor_id is not None:
                    print()
                    time.sleep(1.5)  # Pause between agents
                print(f"\n[Stage: {eid}]:", end=" ", flush=True)
                last_executor_id = eid
            print(event.data, end="", flush=True)
            time.sleep(0.03)  # Smooth streaming
        elif isinstance(event, WorkflowOutputEvent):
            output_evt = event
    
    # Display final conversation
    if output_evt:
        time.sleep(1)
        print("\n\n" + "=" * 80)
        print("SEQUENTIAL PIPELINE RESULTS")
        print("=" * 80)
        
        messages: list[ChatMessage] | Any = output_evt.data
        for i, msg in enumerate(messages, start=1):
            name = msg.author_name or ("assistant" if msg.role == Role.ASSISTANT else "user")
            print(f"\n{'-' * 80}")
            print(f"Stage {i:02d} [{name}]")
            print(f"{'-' * 80}")
            print(msg.text)
            time.sleep(0.5)
    
    print("\n" + "=" * 80)
    print("Pipeline completed successfully!")
    print("=" * 80)


# =============================================================================
# 6. DEMO SCENARIOS
# =============================================================================

async def demo_basic():
    """Basic sequential workflow: Writer -> Reviewer"""
    task = "Write a tagline for a budget-friendly eBike."
    await run_sequential_workflow(workflow_basic, task, "Basic Sequential Pipeline (Writer → Reviewer)")


async def demo_extended():
    """Extended sequential workflow: Writer -> Reviewer -> Editor"""
    task = "Create a tagline for an eco-friendly meal delivery service."
    await run_sequential_workflow(workflow_extended, task, "Extended Sequential Pipeline (Writer → Reviewer → Editor)")


async def demo_advanced():
    """Advanced workflow with custom executor"""
    task = "Write a compelling tagline for a smart home security system."
    await run_sequential_workflow(workflow_advanced, task, "Advanced Pipeline with Analytics (Writer → Reviewer → Editor → Analyzer)")


async def main():
    """Run the selected demo scenario."""
    
    print("\nAvailable demos:")
    print("1. Basic Pipeline (Writer → Reviewer)")
    print("2. Extended Pipeline (Writer → Reviewer → Editor)")
    print("3. Advanced Pipeline with Analytics (Writer → Reviewer → Editor → Analyzer)")
    
    # Run demo 1 by default (uncomment others to try)
    await demo_extended()
    
    # Uncomment to try other demos:
    # await demo_basic()
    # await demo_advanced()
    
    # Run multiple demos in sequence:
    # await demo_basic()
    # await asyncio.sleep(3)
    # await demo_extended()
    # await asyncio.sleep(3)
    # await demo_advanced()


# =============================================================================
# 7. RUN THE DEMO
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("SEQUENTIAL ORCHESTRATION DEMO")
    print("Pipeline-based Multi-Agent Workflows")
    print("="*80)
    print("\nFeatures:")
    print("  • Sequential processing: Each agent builds on previous output")
    print("  • Multiple pipeline configurations (basic, extended, advanced)")
    print("  • Custom executors for specialized processing")
    print("  • Full conversation history available at each stage")
    print("="*80)
    
    asyncio.run(main())
