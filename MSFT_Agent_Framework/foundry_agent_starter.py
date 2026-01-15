"""
MSFT Agent Framework Workshop - Starter Script
==============================================
This script demonstrates how to:
1. Connect to an Azure AI Foundry agent from code
2. Configure OpenTelemetry tracing for monitoring
3. Create an interactive chatbot experience

Prerequisites:
- Completed the Azure AI Foundry Agents workshop (created an agent)
- Installed requirements: pip install -r requirements.txt
- Logged in via Azure CLI: az login --identity
"""

import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient, AzureAIClient
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
import os

# ============================================================================
# EXERCISE 1: Configure Your Azure AI Foundry Project
# ============================================================================
# TODO: Replace with YOUR Azure AI Foundry project endpoint
# Find this in Azure AI Foundry Studio → Project Settings → Project Endpoint
# Example format: "https://<account-name>.services.ai.azure.com/api/projects/<project-name>"

PROJECT_ENDPOINT = "https://<ai_foundry_resource>.services.ai.azure.com/api/projects/<project_name>"  # <-- REPLACE THIS
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = PROJECT_ENDPOINT

# Set your model deployment name (usually "gpt-4o" if using default deployment)
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "your-model-deployment-name"


# ============================================================================
# EXERCISE 2: Connect to Your Foundry Agent
# ============================================================================
# TODO: Replace with YOUR agent ID from Azure AI Foundry
# Find this in Azure AI Foundry Studio → Agents → Select your agent → Copy Agent ID
# Example format: "asst_xxxxxxxxxxxxxxxxxxxx"

AGENT_ID = "your-agent-id"  # <-- REPLACE THIS


async def main():
    """Main function demonstrating agent interaction with tracing."""
    
    async with (
        # Azure CLI credential for authentication
        AzureCliCredential() as credential,
        
        # AI Project client for connecting to your Foundry project
        AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential) as project_client,
        
        # Azure AI Client wrapper from agent framework
        AzureAIClient(project_client=project_client) as client,
        
        # Your Foundry Agent - pulled from Azure AI Foundry
        ChatAgent(
            chat_client=AzureAIAgentClient(
                credential=credential,
                agent_id=AGENT_ID  # Your agent ID from Foundry
            ),
            name="FoundryAgent",  # Friendly name for traces
        ) as agent,
    ):
        # ====================================================================
        # EXERCISE 3: Configure OpenTelemetry Tracing
        # ====================================================================
        # TODO: Uncomment the line below to enable Azure Monitor tracing
        # This sends traces to your Foundry project's Application Insights
        # allowing you to monitor agent performance, latency, and usage
        
        # await client.configure_azure_monitor(enable_live_metrics=True)
        
        print("✓ Connected to agent:", AGENT_ID)
        
        # ====================================================================
        # Interactive Chat Loop
        # ====================================================================
        print("\n" + "="*60)
        print("💬 Interactive Chat Mode")
        print("="*60)
        print("Chat with your Contoso Sales Agent")
        print("Type 'exit', 'quit', or 'q' to end")
        print("="*60 + "\n")
        
        # ====================================================================
        # EXERCISE 4: Enable Conversation Threading
        # ====================================================================
        # TODO: Uncomment the line below to create a thread for conversation history
        # This allows the agent to remember previous messages in the conversation
        
        # thread = agent.get_new_thread()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Send message to your Foundry agent
                print("\n🤖 Assistant: ", end="", flush=True)
                
                # TODO: After completing Exercise 4, change this line to:
                # result = await agent.run(user_input, thread=thread)
                result = await agent.run(user_input)
                
                print(result.text)
                print()  # Extra newline for readability
                
            except EOFError:
                # Handle Ctrl+D
                print("\n\n👋 Goodbye!")
                break


if __name__ == "__main__":
    print("🚀 Connecting to Azure AI Foundry Agent...")
    print("📝 Make sure you've completed Exercises 1 & 2 (endpoint + agent ID)\n")
    asyncio.run(main())
