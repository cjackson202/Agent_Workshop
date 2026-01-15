"""
Multi-Agent Handoff Orchestration System
=========================================

This workflow demonstrates dynamic agent routing where control is intelligently transferred
between specialized agents based on the context of user requests, similar to a sophisticated
customer support system with multiple departments.

Architecture Overview:
---------------------
Five specialized agents work together through dynamic handoffs:

1. **Triage Agent (Coordinator)**
   - Front-line agent that receives initial requests
   - Analyzes customer needs and routes to appropriate specialist
   - Provides warm transfers with context explanations

2. **Refund Agent**
   - Handles refunds, returns, and damaged items
   - Uses submit_refund() tool with approval workflow
   - Can handoff to other specialists if needed

3. **Order Agent**
   - Manages shipping, tracking, and delivery issues
   - Uses track_order() and cancel_order() tools
   - Provides real-time order status updates

4. **Account Agent**
   - Handles login, password resets, and account settings
   - Manages subscriptions and security concerns
   - Can escalate to technical support if needed

5. **Technical Agent**
   - Troubleshoots product malfunctions
   - Provides setup and usage guidance
   - Can handoff to refund/order agents for resolutions

Key Features:
------------
**Human-in-the-Loop (HITL) Approval:**
- Sensitive operations (refunds, cancellations) require human approval
- Clear approval prompts with action details
- Users can approve or deny each action

**Dynamic Handoffs:**
- Agents intelligently transfer control based on request type
- Two workflow modes:
  - Basic: Triage routes to specialists (one-way)
  - Advanced: Specialists can route to each other (multi-way)

**Context Preservation:**
- Full conversation history maintained across handoffs
- Specialists receive complete context when taking over
- Seamless user experience despite agent changes

**Interactive Multi-turn Conversations:**
- Real user input throughout the session
- Natural back-and-forth dialogue
- Agents can ask clarifying questions before acting

Workflow Strategies:
-------------------
1. **Basic Handoff** (workflow_basic)
   - Triage agent routes to specialists
   - One-way transfers only
   - Simple, predictable routing

2. **Advanced Handoff** (workflow_advanced)
   - Specialists can handoff to each other
   - Complex multi-agent collaboration
   - Return-to-previous capability enabled

Demo Scenarios:
--------------
1. **Refund Request** - Demonstrates approval workflow for sensitive operations
2. **Order Tracking** - Shows simple tool usage without approval
3. **Complex Multi-Agent** - Multiple handoffs between specialists

Example Flow:
------------
User: "My order 12345 arrived damaged. I need a refund."
  → Triage Agent: Identifies refund need, transfers to Refund Agent
  → Refund Agent: Gathers details, calls submit_refund()
  → System: Prompts human for approval
  → User: Approves refund
  → Refund Agent: Confirms completion and provides timeline

Use Cases:
---------
- Customer support systems with multiple departments
- Help desk escalation workflows
- Expert routing based on problem type
- Financial operations requiring approval
- Medical triage and specialist referrals
- Technical support with tiered expertise levels
"""

import asyncio
import os
from typing import Annotated
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import HandoffBuilder, ai_function
from agent_framework import RequestInfoEvent, HandoffUserInputRequest, WorkflowOutputEvent
from agent_framework import FunctionApprovalRequestContent
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


# =============================================================================
# 1. SET UP AZURE OPENAI CHAT CLIENT
# =============================================================================

if not os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"):
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"

if not os.getenv("AZURE_OPENAI_ENDPOINT"):
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource.openai.azure.com/"

chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())


# =============================================================================
# 2. DEFINE TOOLS WITH APPROVAL REQUIREMENTS
# =============================================================================

@ai_function(approval_mode="always_require")
def submit_refund(
    refund_description: Annotated[str, "Description of the refund reason"],
    amount: Annotated[str, "Refund amount"],
    order_id: Annotated[str, "Order ID for the refund"],
) -> str:
    """Submit a refund request for manual review before processing."""
    return f"✓ Refund approved and processed for order {order_id} (amount: ${amount}): {refund_description}"


@ai_function(approval_mode="always_require")
def cancel_order(
    order_id: Annotated[str, "Order ID to cancel"],
    reason: Annotated[str, "Reason for cancellation"],
) -> str:
    """Cancel an order - requires approval."""
    return f"✓ Order {order_id} has been cancelled. Reason: {reason}"


def track_order(
    order_id: Annotated[str, "Order ID to track"]
) -> str:
    """Track an order status - no approval needed."""
    # Simulated tracking info
    statuses = {
        "12345": "In Transit - Expected delivery: Tomorrow",
        "67890": "Delivered - Signed by: John Doe",
        "default": f"Order {order_id} - Processing at warehouse"
    }
    return statuses.get(order_id, statuses["default"])


# =============================================================================
# 3. DEFINE SPECIALIZED AGENTS
# =============================================================================

# Triage/Coordinator Agent - Routes to specialists
triage_agent = chat_client.create_agent(
    instructions="""You are a frontline customer service triage agent. 

Your role:
1. Greet customers warmly
2. Understand their issue quickly
3. Route them to the right specialist using handoff tools:
   - handoff_to_refund_agent: For refunds, damaged items, returns
   - handoff_to_order_agent: For shipping, tracking, delivery issues
   - handoff_to_account_agent: For account, login, password issues
   - handoff_to_technical_agent: For product malfunctions, technical problems

Be friendly, professional, and efficient. Always explain who you're transferring them to and why.""",
    name="triage_agent",
)

# Refund Specialist - Handles refunds with approval tools
refund_agent = chat_client.create_agent(
    instructions="""You are a refund specialist. 

Your responsibilities:
1. Gather refund details: order ID, reason, amount
2. Validate the refund request
3. Use submit_refund() to process the refund (requires approval)
4. Explain the refund timeline (5-10 business days)
5. Offer alternatives if appropriate (replacement, store credit)

Be empathetic and solution-focused. If you can handoff to another specialist that can better help, use the appropriate handoff tool.""",
    name="refund_agent",
    tools=[submit_refund],
)

# Order Specialist - Handles shipping/tracking
order_agent = chat_client.create_agent(
    instructions="""You are an order tracking and shipping specialist.

Your responsibilities:
1. Help customers track their orders using track_order()
2. Resolve delivery issues
3. Arrange reshipments or expedited shipping
4. Use cancel_order() if cancellation is needed (requires approval)

Be proactive and provide specific solutions. If the issue requires a refund, use handoff_to_refund_agent.""",
    name="order_agent",
    tools=[track_order, cancel_order],
)

# Account Specialist
account_agent = chat_client.create_agent(
    instructions="""You are an account and security specialist.

Your responsibilities:
1. Help with login issues and password resets
2. Update account information
3. Manage subscriptions and preferences
4. Handle security concerns

Be security-conscious and verify customer identity when needed. If the issue is related to orders or refunds, use the appropriate handoff tool.""",
    name="account_agent",
)

# Technical Support Specialist
technical_agent = chat_client.create_agent(
    instructions="""You are a technical support specialist.

Your responsibilities:
1. Troubleshoot product malfunctions
2. Provide setup and usage guidance
3. Diagnose technical issues
4. Recommend solutions or repairs

Be patient and thorough. If the issue requires a refund or replacement, use handoff_to_refund_agent or handoff_to_order_agent.""",
    name="technical_agent",
)


# =============================================================================
# 4. BUILD HANDOFF WORKFLOWS
# =============================================================================

# Basic Handoff: Triage routes to specialists
workflow_basic = (
    HandoffBuilder(
        name="customer_support_basic",
        participants=[triage_agent, refund_agent, order_agent, account_agent, technical_agent],
    )
    .set_coordinator(triage_agent)  # Pass the agent instance, not the string name
    .with_termination_condition(
        lambda conv: sum(1 for msg in conv if msg.role.value == "user") >= 15
    )
    .build()
)

# Advanced Handoff: Specialists can also route to each other
workflow_advanced = (
    HandoffBuilder(
        name="customer_support_advanced",
        participants=[triage_agent, refund_agent, order_agent, account_agent, technical_agent],
    )
    .set_coordinator(triage_agent)  # Pass the agent instance, not the string name
    .add_handoff(triage_agent, [refund_agent, order_agent, account_agent, technical_agent])
    .add_handoff(refund_agent, [order_agent, technical_agent])
    .add_handoff(order_agent, [refund_agent, technical_agent])
    .add_handoff(technical_agent, [refund_agent, order_agent])
    .add_handoff(account_agent, [technical_agent])
    .enable_return_to_previous(True)  # User inputs go directly to current agent
    .with_termination_condition(
        lambda conv: sum(1 for msg in conv if msg.role.value == "user") >= 15
    )
    .build()
)


# =============================================================================
# 5. INTERACTIVE WORKFLOW EXECUTION
# =============================================================================

async def run_interactive_handoff(workflow, initial_message: str, workflow_name: str = "Handoff Workflow"):
    """
    Run an interactive handoff workflow with user input and tool approval handling.
    
    Args:
        workflow: The configured Handoff workflow
        initial_message: Initial user message to start the workflow
        workflow_name: Display name for the workflow
    """
    print(f"\n{'='*80}")
    print(f"{workflow_name.upper()}")
    print(f"{'='*80}")
    print("\n💬 Starting customer support session...")
    print(f"You: {initial_message}\n")
    
    # Start workflow with initial message
    pending_requests = []
    async for event in workflow.run_stream(initial_message):
        if isinstance(event, RequestInfoEvent):
            pending_requests.append(event)
        elif isinstance(event, WorkflowOutputEvent):
            # Workflow terminated
            print("\n" + "="*80)
            print("Session ended by system.")
            return
    
    # Interactive loop
    turn_count = 0
    while pending_requests and turn_count < 20:  # Safety limit
        responses = {}
        
        for request in pending_requests:
            if isinstance(request.data, HandoffUserInputRequest):
                # Agent needs user input
                print(f"\n{'─'*80}")
                print(f"🤖 {request.data.awaiting_agent_id}:")
                print(f"{'─'*80}")
                
                # Show recent conversation
                for msg in request.data.conversation[-2:]:
                    if msg.author_name and msg.author_name != "user":
                        print(f"{msg.text}\n")
                
                # Get user input
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Ending support session. Thank you!")
                    return
                
                responses[request.request_id] = user_input
                turn_count += 1
                
            elif isinstance(request.data, FunctionApprovalRequestContent):
                # Agent wants to call a tool that requires approval
                func_call = request.data.function_call
                args = func_call.parse_arguments() or {}
                
                print(f"\n{'═'*80}")
                print(f"⚠️  APPROVAL REQUIRED")
                print(f"{'═'*80}")
                print(f"Tool: {func_call.name}")
                print(f"Arguments:")
                for key, value in args.items():
                    print(f"  • {key}: {value}")
                print(f"{'─'*80}")
                
                approval_input = input("Approve this action? (yes/no): ").strip().lower()
                approved = approval_input in ['yes', 'y']
                
                if approved:
                    print("✓ Approved")
                else:
                    print("✗ Denied")
                
                responses[request.request_id] = request.data.create_response(approved=approved)
        
        # Send all responses and collect new requests
        pending_requests = []
        async for event in workflow.send_responses_streaming(responses):
            if isinstance(event, RequestInfoEvent):
                pending_requests.append(event)
            elif isinstance(event, WorkflowOutputEvent):
                print("\n" + "="*80)
                print("✓ Support session completed successfully!")
                print("="*80)
                return
    
    if turn_count >= 20:
        print("\n⚠️  Maximum turns reached. Ending session.")


# =============================================================================
# 6. DEMO SCENARIOS
# =============================================================================

async def demo_refund_scenario():
    """Demo: Customer needs a refund for damaged item"""
    print("\n" + "="*80)
    print("DEMO SCENARIO 1: Refund Request with Approval")
    print("="*80)
    print("\nScenario: Customer received a damaged item and needs a refund")
    print("This demonstrates:")
    print("  • Triage routing to specialist")
    print("  • Tool approval workflow")
    print("  • Multi-turn conversation")
    print("="*80)
    
    await run_interactive_handoff(
        workflow_basic,
        "My order 12345 arrived damaged. I need a refund.",
        "Customer Support - Refund Request"
    )


async def demo_tracking_scenario():
    """Demo: Customer wants to track their order"""
    print("\n" + "="*80)
    print("DEMO SCENARIO 2: Order Tracking")
    print("="*80)
    print("\nScenario: Customer wants to check order status")
    print("This demonstrates:")
    print("  • Simple tool usage (no approval needed)")
    print("  • Specialist expertise")
    print("="*80)
    
    await run_interactive_handoff(
        workflow_basic,
        "Where is my order 67890?",
        "Customer Support - Order Tracking"
    )


async def demo_complex_scenario():
    """Demo: Multi-specialist handoff"""
    print("\n" + "="*80)
    print("DEMO SCENARIO 3: Complex Multi-Agent Handoff")
    print("="*80)
    print("\nScenario: Issue requires multiple specialists")
    print("This demonstrates:")
    print("  • Agent-to-agent handoffs")
    print("  • Context preservation")
    print("  • Dynamic routing")
    print("="*80)
    
    await run_interactive_handoff(
        workflow_advanced,
        "I have a problem with my recent order",
        "Customer Support - Advanced Handoff"
    )


async def main():
    """Run the selected demo scenario."""
    
    print("\n" + "="*80)
    print("INTERACTIVE HANDOFF ORCHESTRATION DEMO")
    print("="*80)
    
    print("\nAvailable scenarios:")
    print("1. Refund Request (with approval workflow)")
    print("2. Order Tracking (simple tool usage)")
    print("3. Complex Multi-Agent Handoff")
    print("\nTip: Type 'quit' or 'exit' at any time to end the session")
    print("="*80)
    
    # Run a demo (uncomment to try different scenarios)
    await demo_refund_scenario()
    
    # Uncomment to try other scenarios:
    # await demo_tracking_scenario()
    # await demo_complex_scenario()


# =============================================================================
# 7. RUN THE DEMO
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("HANDOFF ORCHESTRATION DEMO")
    print("Dynamic Agent Routing with Specialized Expertise")
    print("="*80)
    print("\nFeatures:")
    print("  • Dynamic routing: Agents transfer control based on context")
    print("  • Specialized agents: Refund, Order, Account, Technical")
    print("  • Tool approval: Sensitive operations require human approval")
    print("  • Interactive: Real user input and multi-turn conversations")
    print("  • Context preservation: Full conversation history maintained")
    print("="*80)
    
    asyncio.run(main())
