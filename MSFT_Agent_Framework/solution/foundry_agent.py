"""
MSFT Agent Framework Workshop - SOLUTION
========================================
This is the completed solution for the workshop.
"""

import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient, AzureAIClient
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
import os

# Required: Your Azure AI Foundry project endpoint
# Find this in Azure AI Foundry Studio → Project Settings
PROJECT_ENDPOINT = "https://<ai_foundry_resource>.services.ai.azure.com/api/projects/<project_name>"
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = PROJECT_ENDPOINT

# Required: Your model deployment name
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "your-model-deployment-name"

# Your agent ID from Azure AI Foundry
AGENT_ID = "your-agent-id"


async def main():
    """Main function demonstrating agent interaction with tracing."""
    
    async with (
        AzureCliCredential() as credential,
        AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential) as project_client,
        AzureAIClient(project_client=project_client) as client,
        ChatAgent(
            chat_client=AzureAIAgentClient(
                credential=credential,
                agent_id=AGENT_ID
            ),
            name="FoundryAgent",
        ) as agent,
    ):
        # Configure Azure Monitor for OpenTelemetry tracing
        await client.configure_azure_monitor(enable_live_metrics=True)
        
        print("✓ Connected to agent:", AGENT_ID)
        print("✓ Azure Monitor tracing enabled")
        
        # Interactive Chat Loop
        print("\n" + "="*60)
        print("💬 Interactive Chat Mode")
        print("="*60)
        print("Chat with your Contoso Sales Agent")
        print("Type 'exit', 'quit', or 'q' to end")
        print("="*60 + "\n")
        
        # Create a thread to maintain conversation history
        thread = agent.get_new_thread()
        
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
                result = await agent.run(user_input, thread=thread)
                print(result.text)
                print()  # Extra newline for readability
                
            except EOFError:
                # Handle Ctrl+D
                print("\n\n👋 Goodbye!")
                break


if __name__ == "__main__":
    print("🚀 Connecting to Azure AI Foundry Agent...\n")
    asyncio.run(main())