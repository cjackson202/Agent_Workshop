"""
Sequential Orchestration Workshop
==================================
Learn pipeline workflows where agents process tasks in order.

CORE CONCEPTS (Think of these as building blocks):

1. EXECUTORS - The workers in your pipeline
   - Agents (powered by AI) or simple processors (like a calculator)
   - Each executor does one specific job
   - They pass their output to the next executor in line

2. WORKFLOW - The assembly line
   - Connects executors in a specific order
   - Manages the flow of information between executors
   - Like a factory assembly line where each station does its job

3. EVENTS - Status updates along the way
   - Tells you what's happening as the workflow runs
   - Like tracking a package delivery: "Started", "In Progress", "Delivered"
   - Helps you see what each executor is doing in real-time

This workshop demonstrates:
- Building sequential agent pipelines (assembly line style)
- Adding tool calling capabilities to agents (giving them special abilities)
- Using custom executors for specialized tasks (workers that don't need AI)
- Watching events to understand what's happening

EXERCISES:
1. Run the basic demo to see the sequential flow and events
2. Add your own custom tool (see EXERCISE section)
3. Modify agent instructions to change behavior
4. Create a new pipeline with your own agents
"""

import asyncio
import os
import time
from typing import Any, Annotated
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
# 2. DEFINE TOOLS FOR AGENTS
# =============================================================================

def word_counter(
    text: Annotated[str, "The text to analyze"]
) -> str:
    """Count words, characters, and sentences in a text."""
    print(f"\n{'-'*50}\nWord Counter tool invoked\n{'-'*50}\n")
    words = len(text.split())
    chars = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    
    return f"""Text Analysis:
- Words: {words}
- Characters: {chars}
- Sentences: {sentences}
- Average word length: {chars/words:.1f} characters"""


def readability_checker(
    text: Annotated[str, "The text to check for readability"]
) -> str:
    """Check text readability using simple metrics."""
    print(f"\n{'-'*50}\nReadability Checker tool invoked\n{'-'*50}\n")
    words = text.split()
    word_count = len(words)
    sentences = text.count('.') + text.count('!') + text.count('?') or 1
    
    avg_words_per_sentence = word_count / sentences
    long_words = sum(1 for word in words if len(word) > 7)
    
    if avg_words_per_sentence < 15 and long_words < word_count * 0.2:
        level = "Easy to read ✓"
    elif avg_words_per_sentence < 20:
        level = "Moderate"
    else:
        level = "Complex - consider simplifying"
    
    return f"""Readability Check:
- Average words per sentence: {avg_words_per_sentence:.1f}
- Long words (7+ chars): {long_words} ({long_words/word_count*100:.1f}%)
- Readability: {level}"""


def character_limiter(
    text: Annotated[str, "The text to check"],
    limit: Annotated[int, "Character limit (e.g., 280 for Twitter)"]
) -> str:
    """Check if text fits within character limits for social media or ads."""
    print(f"\n{'-'*50}\nCharacter Limiter tool invoked\n{'-'*50}\n")
    char_count = len(text)
    remaining = limit - char_count
    
    if remaining >= 0:
        status = f"✓ Fits! {remaining} characters remaining"
    else:
        status = f"✗ Too long by {abs(remaining)} characters"
    
    return f"""Character Limit Check:
- Text length: {char_count} characters
- Limit: {limit} characters
- Status: {status}"""


# =============================================================================
# EXERCISE: Add sentiment analysis to your pipeline!
# =============================================================================
# Ready-to-use tool - Just uncomment it and add to the Reviewer agent below!

# Sentiment Analyzer Tool
# Uncomment these lines to add sentiment analysis:

# def sentiment_analyzer(
#     text: Annotated[str, "Text to analyze for sentiment"]
# ) -> str:
#     '''Analyze text sentiment - useful for ensuring positive marketing tone.'''
#     print(f"\n{'-'*50}\nSentiment Analyzer tool invoked\n{'-'*50}\n")
#     positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "best"]
#     negative_words = ["bad", "poor", "terrible", "awful", "horrible", "worst", "hate", "disappointing"]
    
#     text_lower = text.lower()
#     pos_count = sum(word in text_lower for word in positive_words)
#     neg_count = sum(word in text_lower for word in negative_words)
    
#     if pos_count > neg_count:
#         sentiment = "Positive ✓"
#     elif neg_count > pos_count:
#         sentiment = "Negative ✗"
#     else:
#         sentiment = "Neutral ○"
    
#     return f"Sentiment: {sentiment} (Positive words: {pos_count}, Negative words: {neg_count})"


# TO COMPLETE THE EXERCISE:
# 1. Remove the triple quotes (""") above and below the sentiment_analyzer function
# 2. Scroll down to the Reviewer agent definition (around line 270)
# 3. Add sentiment_analyzer to the functions list:
#    functions=[word_counter, readability_checker, sentiment_analyzer]
# 4. Test with: "Write a positive tagline for a new smartphone and check its sentiment"
# =============================================================================


# =============================================================================
# 3. DEFINE AGENTS FOR SEQUENTIAL PIPELINE
# =============================================================================
# NOTE: To add a tool you uncommented above, add it to the functions list!
# Example: functions=[calculator, word_counter, temperature_converter]

# Stage 1: Writer - Creates initial content with tools
writer = chat_client.create_agent(
    instructions="""You are a creative copywriter. Create compelling, concise marketing content.
    
Guidelines:
- Write a punchy, memorable tagline or short paragraph
- Focus on benefits and emotional appeal
- Keep it brief but impactful
- Use active voice and strong verbs

IMPORTANT - ALWAYS use these tools:
1. FIRST: Call word_counter with your draft to analyze it
2. SECOND: Call readability_checker with your draft to ensure it's easy to read
3. IF creating content for a specific platform: Call character_limiter to verify it fits

You MUST call these functions - don't just describe the metrics, actually invoke the tools!""",
    name="Writer",
    tools=[word_counter, readability_checker, character_limiter]  # Tools registered here
)

# Stage 2: Reviewer - Provides constructive feedback
reviewer = chat_client.create_agent(
    instructions="""You are a marketing reviewer. Provide constructive feedback on the content.
    
Your review should:
- Assess clarity, impact, and memorability
- Identify strengths and weaknesses
- Suggest specific improvements
- Rate the content (1-10)
- Be constructive but honest

IMPORTANT - ALWAYS use these tools:
1. FIRST: Call word_counter on the content to get objective metrics
2. SECOND: Call readability_checker to analyze complexity
3. THIRD: Call sentiment_analyzer to check emotional tone
4. THEN: Provide your review based on the tool results

You MUST call these functions - don't just guess the metrics!""",
    name="Reviewer",
    tools=[word_counter, readability_checker]
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
# 4. DEFINE CUSTOM EXECUTOR FOR SPECIALIZED PROCESSING
# =============================================================================
# IMPORTANT CONCEPT: When to use Custom Executors vs AI Agents
#
# Use CUSTOM EXECUTOR when:
#   ✓ Task is deterministic (same input = same output)
#   ✓ No reasoning or creativity needed
#   ✓ You want instant results (no API calls)
#   ✓ Examples: Formatting data, validating JSON, counting, math operations
#
# Use AI AGENT when:
#   ✓ Task requires understanding context or nuance
#   ✓ Creative output or decision-making needed
#   ✓ Examples: Writing content, reviewing quality, making recommendations
#
# BENEFITS:
#   • Cost: Custom executors are FREE (no AI API calls)
#   • Speed: Instant processing (no network latency)
#   • Reliability: Predictable, testable logic
#   • Mix & Match: Combine both in the same pipeline!

class ContentAnalyzer(Executor):
    """Custom executor that analyzes conversation without using an LLM.
    
    REAL-WORLD USE CASES (like what you'll build in your POC):
    - Data validation: Check if output meets requirements before proceeding
    - Metrics collection: Track pipeline performance and quality
    - Format conversion: Transform data between pipeline stages
    - Business rules: Apply deterministic logic (pricing, filtering, routing)
    
    This example shows how to add a "quality gate" step that runs after AI agents
    to collect metrics about what they produced. No AI needed - just counting!
    """
    
    @handler
    async def analyze(
        self,
        conversation: list[ChatMessage],
        ctx: WorkflowContext[list[ChatMessage]]
    ) -> None:
        """Analyze conversation statistics and append summary.
        
        NOTE: This executor receives the ENTIRE conversation history from
        all previous stages (Writer, Reviewer, Editor). It can access everything
        that happened before it in the pipeline.
        """
        
        # Count messages by role (simple counting logic - no AI needed)
        user_msgs = sum(1 for m in conversation if m.role == Role.USER)
        assistant_msgs = sum(1 for m in conversation if m.role == Role.ASSISTANT)
        
        # Calculate word counts (deterministic math)
        total_words = sum(len(m.text.split()) for m in conversation)
        
        # Get agent names involved in the pipeline
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

💡 **Why a Custom Executor Here?**
This analysis doesn't require AI - it's just counting and formatting.
Using a custom executor makes it instant and free!
"""
        
        # Add analysis message to conversation
        summary_msg = ChatMessage(
            role=Role.ASSISTANT,
            text=analysis.strip(),
            author_name="ContentAnalyzer"
        )
        
        # Pass the conversation + summary to next stage (or as final output)
        await ctx.send_message(list(conversation) + [summary_msg])


# =============================================================================
# 5. BUILD SEQUENTIAL WORKFLOWS
# =============================================================================
# Basic Sequential: Writer -> Reviewer (simplest pipeline)
workflow_basic = (
    SequentialBuilder()
    .participants([writer, reviewer])
    .build()
)

# Extended Sequential: Writer -> Reviewer -> Editor (all AI agents)
workflow_extended = (
    SequentialBuilder()
    .participants([writer, reviewer, editor])
    .build()
)

# Advanced Sequential: Mixing AI Agents + Custom Executor
# Shows how to add non-AI processing steps to your pipeline!
# Pipeline: AI → AI → AI → Simple Code
#           Writer → Reviewer → Editor → ContentAnalyzer
#
# USE THIS PATTERN IN YOUR POC when you need to:
# - Validate AI output meets requirements
# - Format data for the next system
# - Apply business rules after AI processing
# - Add quality gates or metrics collection
content_analyzer = ContentAnalyzer(id="ContentAnalyzer")
workflow_advanced = (
    SequentialBuilder()
    .participants([writer, reviewer, editor, content_analyzer])
    .build()
)


# =============================================================================
# 6. WORKFLOW EXECUTION WITH EVENT MONITORING
# =============================================================================
# Events are like status updates. They tell you what's happening at each step.
# Think of it like tracking a delivery: "Package picked up", "Out for delivery", "Delivered"

async def run_sequential_workflow(workflow, task: str, workflow_name: str = "Sequential Workflow"):
    """
    Execute a sequential workflow and display results with event monitoring.
    
    This function watches for different types of events:
    - AgentRunUpdateEvent: Shows what the agent is thinking/writing (like live updates)
    - WorkflowOutputEvent: The final result when everything is done
    
    Args:
        workflow: The configured Sequential workflow (your assembly line)
        task: The task to process (the work order)
        workflow_name: Display name for the workflow
    """
    print(f"\n{'='*80}")
    print(f"{workflow_name.upper()}")
    print(f"{'='*80}")
    print(f"Task: {task}\n")
    print("=" * 80)
    print("\n📊 Watching for events (status updates)...\n")
    
    output_evt: WorkflowOutputEvent | None = None
    last_executor_id = None
    
    # Run workflow and stream events (listen for status updates)
    async for event in workflow.run_stream(task):
        # EVENT TYPE 1: Agent is actively working and streaming output
        if isinstance(event, AgentRunUpdateEvent):
            # Print streaming updates (like watching someone type)
            eid = event.executor_id
            if eid != last_executor_id:
                if last_executor_id is not None:
                    print()
                    time.sleep(1.5)  # Pause between agents
                print(f"\n[Stage: {eid}]:", end=" ", flush=True)
                last_executor_id = eid
            print(event.data, end="", flush=True)
            time.sleep(0.03)  # Smooth streaming
        
        # EVENT TYPE 2: Workflow has completed and produced final output
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
# 7. DEMO SCENARIOS
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
    """Advanced workflow demonstrating custom executor integration.
    
    This demo shows the key concept you'll use in your POC:
    Mixing AI agents with custom executors in the same pipeline.
    
    The ContentAnalyzer adds a quality gate that validates and reports
    on the AI-generated content without needing another AI call.
    """
    task = "Write a compelling tagline for a smart home security system."
    await run_sequential_workflow(workflow_advanced, task, "Advanced Pipeline with Custom Executor (Writer → Reviewer → Editor → Analyzer)")


async def demo_with_tools():
    """Demo showing tool usage in pipeline"""
    task = "Write a Twitter-friendly tagline (under 280 characters) for a project management tool that improves team productivity. Check readability and character count."
    await run_sequential_workflow(workflow_extended, task, "Tool-Enhanced Pipeline (with Content Analysis Tools)")


async def main():
    """Run the sequential pipeline demos.
    
    TIP: Try demo_advanced() to see custom executors in action!
    This concept will be important for your proof of concept.
    """
    
    # Run advanced demo by default (shows tools + custom executor)
    await demo_advanced()
    
    # Uncomment to try other demos:
    # await demo_basic()  # Simplest: just Writer → Reviewer
    # await demo_extended()  # Writer → Reviewer → Editor (no custom executor)
    # await demo_with_tools()  # Explicit tool usage prompts


# =============================================================================
# 8. RUN THE DEMO
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
