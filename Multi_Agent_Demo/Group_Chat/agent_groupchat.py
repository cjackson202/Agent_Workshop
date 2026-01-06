"""
Group Chat Orchestration Demo with Web Search
Demonstrates collaborative multi-agent workflows with actual research capabilities
"""

import asyncio
import os
import json
import time
from typing import cast, Annotated
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatAgent, GroupChatBuilder, GroupChatStateSnapshot
from agent_framework import AgentRunUpdateEvent, Role, WorkflowOutputEvent
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


# =============================================================================
# 1. SET UP AZURE OPENAI CHAT CLIENT
# =============================================================================
# Configuration: Set your Azure OpenAI deployment details
# Option 1: Set environment variables (recommended)
#   - AZURE_OPENAI_CHAT_DEPLOYMENT_NAME (required)
#   - AZURE_OPENAI_ENDPOINT (required)
# Option 2: Pass directly to AzureOpenAIChatClient() below

# Example: Set deployment name and endpoint if not already in environment
if not os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"):
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"  # Change to your deployment name

if not os.getenv("AZURE_OPENAI_ENDPOINT"):
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource.openai.azure.com/"  # Change to your endpoint

# Initialize chat client
# Note: Requires 'az login' to be completed first
chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    # Uncomment to override environment variables:
    # deployment_name="your-deployment-name",
    # endpoint="https://your-resource.openai.azure.com/"
)


# =============================================================================
# 2. DEFINE RESEARCH TOOLS
# =============================================================================

def web_search(query: Annotated[str, "The search query to look up"]) -> str:
    """
    Simulates a web search tool that the researcher can use.
    
    In a real implementation, this would call Bing Search API or similar.
    For demo purposes, returns mock search results.
    """
    # Mock search results for demonstration
    mock_results = {
        "async": {
            "title": "Understanding Async/Await in Python",
            "snippet": "Async/await enables concurrent execution through coroutines. Key benefits: non-blocking I/O operations, improved performance for I/O-bound tasks, better resource utilization than threading, and cleaner syntax for asynchronous code.",
            "source": "python.org/docs"
        },
        "azure": {
            "title": "Azure Services Overview",
            "snippet": "Microsoft Azure provides 200+ cloud services including compute, storage, networking, AI, and databases. Key features: global scale, enterprise security, hybrid capabilities, and pay-as-you-go pricing.",
            "source": "azure.microsoft.com"
        },
        "default": {
            "title": "Search Results",
            "snippet": "Found information related to: " + query,
            "source": "web-search"
        }
    }
    
    # Simple keyword matching for demo
    query_lower = query.lower()
    if "async" in query_lower or "await" in query_lower:
        result = mock_results["async"]
    elif "azure" in query_lower:
        result = mock_results["azure"]
    else:
        result = mock_results["default"]
    
    return json.dumps({
        "query": query,
        "results": [result]
    }, indent=2)


def get_technical_docs(topic: Annotated[str, "The technical topic to get documentation for"]) -> str:
    """
    Simulates retrieving technical documentation.
    
    In a real implementation, this could query a documentation database or API.
    """
    docs = {
        "async": """
Python Async/Await Documentation:
- asyncio provides infrastructure for writing concurrent code using async/await syntax
- Coroutines are declared with async def and awaited with await keyword
- Event loop manages execution of asynchronous tasks
- Performance benefits: handles thousands of concurrent I/O operations efficiently
- Use cases: web servers, database operations, API calls, file I/O
""",
        "python": """
Python Language Features:
- Dynamic typing with optional type hints
- First-class functions and decorators
- List comprehensions and generators
- Context managers (with statement)
- Multiple inheritance and metaclasses
""",
        "azure": """
Azure Key Services:
- Azure Functions: Serverless compute platform
- Azure App Service: Web app hosting
- Azure Storage: Blob, File, Queue, Table storage
- Azure AI Services: Computer Vision, Language, Speech
- Azure Cosmos DB: Globally distributed NoSQL database
"""
    }
    
    topic_lower = topic.lower()
    for key, doc in docs.items():
        if key in topic_lower:
            return doc
    
    return f"Documentation for {topic}: General technical information available."


def save_to_document(
    title: Annotated[str, "The title of the document"],
    content: Annotated[str, "The main content/answer to save"],
    author: Annotated[str, "The author name"] = "AI Research Team"
) -> str:
    """
    Saves the final answer to a professional markdown document.
    
    Creates a well-formatted document with metadata, proper formatting,
    and saves it to the output directory.
    """
    import datetime
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename from title
    safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    safe_title = safe_title.replace(' ', '_')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_title}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Create professional document content
    document_content = f"""# {title}

---

**Author:** {author}  
**Date:** {datetime.datetime.now().strftime("%B %d, %Y")}  
**Generated by:** Multi-Agent Research Team

---

## Executive Summary

This document provides a comprehensive answer to the question: "{title}"

---

## Detailed Analysis

{content}

---

## Document Information

- **File:** {filename}
- **Generated:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Version:** 1.0

---

*This document was generated by an AI-powered multi-agent research team utilizing web search, technical documentation, and collaborative review processes.*
"""
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(document_content)
    
    return f"✓ Document saved successfully to: {filepath}\n\nFile contains {len(content.split())} words across {len(content.split(chr(10)))} lines."


# =============================================================================
# 3. DEFINE SPECIALIZED AGENTS WITH TOOLS
# =============================================================================

# Researcher Agent - With web search and documentation tools
researcher = ChatAgent(
    name="Researcher",
    description="Collects relevant background information using web search and documentation tools.",
    instructions="""You are a research specialist. Your job is to gather accurate, relevant information to answer questions.

Steps to follow:
1. Use web_search() to find current information about the topic
2. Use get_technical_docs() to retrieve detailed technical documentation
3. Synthesize the findings into clear, factual bullet points
4. Cite your sources (web search results or documentation)

Keep your research concise but comprehensive. Focus on facts and data.""",
    tools=[web_search, get_technical_docs],
    chat_client=chat_client,
)

# Writer Agent - Synthesizes polished answers and saves to document
writer = ChatAgent(
    name="Writer",
    description="Synthesizes polished answers using gathered information and saves to professional documents.",
    instructions="""You are a technical writer. Your job is to create clear, well-structured answers and save them to professional documents.

Guidelines:
1. Review the research provided by the Researcher
2. Organize information into a logical structure with clear sections:
   - Introduction/Overview
   - Key Points (with subheadings)
   - Examples or Use Cases
   - Conclusion or Summary
3. Write in a clear, professional tone using markdown formatting
4. Use proper markdown: ## for headings, **bold** for emphasis, - for bullets, ``` for code
5. After composing your answer, ALWAYS use save_to_document() to create the final document
6. Call save_to_document with:
   - title: The question being answered
   - content: Your complete, well-formatted answer
   - author: "AI Research Team"

Make your response comprehensive, well-formatted, and professional.""",
    tools=[save_to_document],
    chat_client=chat_client,
)

# Fact Checker Agent - Validates information accuracy
fact_checker = ChatAgent(
    name="FactChecker",
    description="Validates the accuracy and completeness of information.",
    instructions="""You are a fact checker and quality assurance specialist. Your job is to VALIDATE the work done by the team, not restate it.

Your responsibilities:

1. **Verify Research Usage**: Check if the Writer correctly used the Researcher's findings
   - Are all key points from the research included?
   - Is any information misrepresented or exaggerated?
   - Are the sources/citations accurate?

2. **Check Completeness**: Identify what's missing
   - Did the Writer address all aspects of the original question?
   - Are there important details from the research that were omitted?
   - Should any additional context be provided?

3. **Validate Document Creation**: Confirm the document was saved
   - Did the Writer call save_to_document()?
   - Was the document creation successful?

4. **Identify Issues**: Point out specific problems if found
   - Factual errors or contradictions
   - Unclear explanations
   - Missing information

5. **Provide Clear Verdict**: End with one of these:
   - "✓ APPROVED: Answer is accurate, complete, and well-documented."
   - "⚠ NEEDS REVISION: [specific issues found]"
   - "✗ REJECTED: [critical problems that require complete rework]"

Be critical but constructive. Don't just summarize - VALIDATE.""",
    chat_client=chat_client,
)


# =============================================================================
# 4. SPEAKER SELECTION STRATEGIES
# =============================================================================

def simple_selector(state: GroupChatStateSnapshot) -> str | None:
    """
    Simple workflow: Researcher → Writer → FactChecker → Done
    
    Args:
        state: Contains task, participants, conversation, history, and round_index
    
    Returns:
        Name of next speaker, or None to finish
    """
    round_idx = state["round_index"]
    history = state["history"]
    
    # Maximum 6 rounds for safety
    if round_idx >= 6:
        return None
    
    # Start with Researcher
    if round_idx == 0:
        return "Researcher"
    
    last_speaker = history[-1].speaker if history else None
    
    # Workflow: Researcher → Writer → FactChecker → Done
    if last_speaker == "Researcher":
        return "Writer"
    elif last_speaker == "Writer":
        return "FactChecker"
    elif last_speaker == "FactChecker":
        return None  # End the conversation
    
    return "Researcher"  # Fallback


def iterative_selector(state: GroupChatStateSnapshot) -> str | None:
    """
    Iterative refinement: Researcher → Writer → FactChecker → (optional round 2) → Done
    
    Args:
        state: Contains task, participants, conversation, history, and round_index
    
    Returns:
        Name of next speaker, or None to finish
    """
    round_idx = state["round_index"]
    conversation = state["conversation"]
    history = state["history"]
    
    # Maximum 8 rounds (allows for 2 full cycles if needed)
    if round_idx >= 8:
        return None
    
    # First round: always start with researcher
    if round_idx == 0:
        return "Researcher"
    
    last_speaker = history[-1].speaker if history else None
    last_message = conversation[-1] if conversation else None
    last_text = getattr(last_message, "text", "").lower() if last_message else ""
    
    # After Researcher: go to Writer
    if last_speaker == "Researcher" and round_idx <= 3:
        return "Writer"
    
    # After Writer: go to FactChecker for review
    if last_speaker == "Writer" and round_idx <= 4:
        return "FactChecker"
    
    # After FactChecker: check if additional research is needed
    if last_speaker == "FactChecker":
        if "missing" in last_text or "need more" in last_text or "incomplete" in last_text:
            return "Researcher"  # Do another round
        else:
            return None  # All good, finish
    
    # Default: end the conversation
    return None


# Coordinator Agent - For agent-based manager approach
coordinator = ChatAgent(
    name="Coordinator",
    description="Coordinates multi-agent collaboration by selecting speakers",
    instructions="""You coordinate a research team to solve the user's task.

Team members:
- Researcher: Uses web search and documentation tools to gather information
- Writer: Creates polished, well-structured answers
- FactChecker: Validates accuracy and completeness

Selection guidelines:
1. Always start with Researcher to gather information using available tools
2. After research is complete, have Writer create the answer
3. Have FactChecker review for accuracy
4. If FactChecker finds issues, send back to Researcher for more info
5. Finish when answer is complete and validated

Consider the conversation context and task requirements when selecting speakers.""",
    chat_client=chat_client,
)


# =============================================================================
# 5. BUILD WORKFLOWS
# =============================================================================

# Option A: Simple sequential workflow (Researcher → Writer → FactChecker)
workflow_simple = (
    GroupChatBuilder()
    .set_select_speakers_func(simple_selector, display_name="SimpleOrchestrator")
    .participants([researcher, writer, fact_checker])
    .build()
)

# Option B: Agent-based manager (intelligent coordination)
workflow_agent_manager = (
    GroupChatBuilder()
    .set_manager(coordinator, display_name="Orchestrator")
    .with_termination_condition(
        lambda messages: sum(1 for msg in messages if msg.role == Role.ASSISTANT) >= 6
    )
    .participants([researcher, writer, fact_checker])
    .build()
)

# Option C: Iterative refinement workflow (allows for multiple rounds if needed)
workflow_iterative = (
    GroupChatBuilder()
    .set_select_speakers_func(iterative_selector, display_name="IterativeOrchestrator")
    .participants([researcher, writer, fact_checker])
    .build()
)


# =============================================================================
# 6. WORKFLOW EXECUTION
# =============================================================================

async def run_group_chat(workflow, task: str, workflow_name: str = "Group Chat"):
    """
    Execute a group chat workflow and display results.
    
    Args:
        workflow: The configured GroupChat workflow
        task: The question/task to process
        workflow_name: Display name for the workflow
    """
    print(f"\n{'='*80}")
    print(f"{workflow_name.upper()}")
    print(f"{'='*80}")
    print(f"Task: {task}\n")
    print("=" * 80)
    
    final_conversation = []
    last_executor_id = None
    
    # Run the workflow and stream events
    async for event in workflow.run_stream(task):
        if isinstance(event, AgentRunUpdateEvent):
            # Print streaming agent updates
            eid = event.executor_id
            if eid != last_executor_id:
                if last_executor_id is not None:
                    print()
                    # Pause between agent transitions for demo visibility
                    time.sleep(2)
                print(f"\n[{eid}]:", end=" ", flush=True)
                last_executor_id = eid
            print(event.data, end="", flush=True)
            # Small delay for readability during streaming
            time.sleep(0.05)
        elif isinstance(event, WorkflowOutputEvent):
            # Workflow completed - data is a list of ChatMessage
            final_conversation = cast(list, event.data)
    
    # Display final conversation
    if final_conversation:
        time.sleep(1)  # Pause before showing summary
        print("\n\n" + "=" * 80)
        print("Final Conversation Summary:")
        for msg in final_conversation:
            author = getattr(msg, "author_name", "Unknown")
            text = getattr(msg, "text", str(msg))
            print(f"\n[{author}]\n{text}")
            print("-" * 80)
            time.sleep(0.5)  # Brief pause between messages in summary
    
    print("\nWorkflow completed.")
    time.sleep(1)  # Final pause before returning


async def main():
    """
    Main execution function demonstrating different workflow configurations.
    """
    # Sample tasks demonstrating the enhanced capabilities
    tasks = [
        "What are the key benefits of async/await in Python?",
        # "What are the main Azure AI services and their use cases?",
        # "Explain the difference between microservices and monolithic architecture.",
    ]
    
    # Choose which workflow to run (uncomment one):
    
    # 1. Simple sequential workflow (Researcher → Writer → FactChecker)
    await run_group_chat(workflow_simple, tasks[0], "Simple Sequential Workflow with Research Tools")
    
    # 2. Agent-based manager (intelligent coordination) - uncomment to try
    # await run_group_chat(workflow_agent_manager, tasks[0], "Agent-Based Manager Workflow")
    
    # 3. Iterative refinement (allows multiple rounds) - uncomment to try
    # await run_group_chat(workflow_iterative, tasks[0], "Iterative Refinement Workflow")
    
    # Try multiple tasks in sequence (uncomment to run all)
    # for i, task in enumerate(tasks, 1):
    #     print(f"\n\n{'='*80}")
    #     print(f"RUNNING TASK {i}/{len(tasks)}")
    #     print(f"{'='*80}\n")
    #     await run_group_chat(workflow_simple, task, f"Task {i}")
    #     await asyncio.sleep(2)  # Brief pause between tasks


# =============================================================================
# 7. RUN THE DEMO
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("Multi-Agent Research Team with Tools")
    print("="*80)
    print("\nFeatures:")
    print("  • Researcher agent with web search & documentation tools")
    print("  • Writer agent for polished responses")
    print("  • FactChecker agent for validation")
    print("="*80)
    
    # Run the async main function
    asyncio.run(main())
