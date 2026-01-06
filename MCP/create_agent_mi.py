"""
Create Azure AI Foundry Agent with MCP Tools
==============================================

This script creates a NEW Azure AI Foundry agent and connects it to your
local MCP server. The agent can then use the tools exposed by the MCP server.

Prerequisites:
1. MCP server running (python server.py in another terminal)
2. Azure CLI authenticated (az login)
3. Azure AI Foundry project created
4. Model deployment available (GPT-4o or GPT-4o-mini)

Workshop Usage:
1. Update the environment variables below with your Azure project details
2. Make sure server.py is running (in a separate terminal)
3. Run this script: python create_agent_mi.py
4. Start chatting with your agent!
"""

import os
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureAIAgentClient
import asyncio
from agent_framework import MCPStreamableHTTPTool

# ============================================================================
# CONFIGURATION - Update these with your Azure AI Foundry project details
# ============================================================================
# Find these values in Azure AI Foundry Studio:
# 1. Go to your project settings
# 2. Copy the project endpoint URL
# 3. Note your model deployment name

os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://YOUR-PROJECT.services.ai.azure.com/api/projects/YOUR-PROJECT-NAME"
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"

# Example:
# os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://camerjackson-9533-resource.services.ai.azure.com/api/projects/camerjackson-9533"
# os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"
# ============================================================================


async def basic_foundry_mcp_example():
    """
    Main function: Creates an Azure AI Foundry agent with MCP tool integration
    
    Steps:
    1. Authenticate using Azure CLI credentials (Managed Identity)
    2. Create an Azure AI Agent client
    3. Configure MCP tool pointing to local server
    4. Create agent with instructions and tools
    5. Start interactive chat loop
    """
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(credential=credential) as chat_client,
    ):
        # Optional: Enable Azure AI observability for monitoring
        # Uncomment the line below to enable tracing and logging
        # await chat_client.setup_azure_ai_observability()

        # ===================================================================
        # STEP 1: Configure MCP Tool
        # ===================================================================
        # This connects your agent to the local MCP server
        # The server must be running at http://localhost:8080/mcp
        mcp_tool = MCPStreamableHTTPTool(
            name="Custom MCP Server2",  # Friendly name for the tool
            url="http://localhost:8080/mcp",  # URL where your MCP server is running
            chat_client=chat_client  # Agent client for making requests
        )
        print("✓ MCP tool configured for localhost:8080")

        # ===================================================================
        # STEP 2: Create Agent
        # ===================================================================
        # This creates a NEW agent in Azure AI Foundry
        # Note: Each run creates a new agent. See get_agent_mi.py to reuse agents.
        agent = chat_client.create_agent(
            name="MicrosoftLearnAgent",  # Name that appears in Azure
            instructions="You answer questions by using the available tools only.",  # System prompt
            tools=mcp_tool,  # MCP tools available to the agent
        )
        print("✓ Agent created with MCP tool")
        print(f"✓ Agent ID: {agent.id}")  # Save this ID to reuse the agent later!
        
        # ===================================================================
        # STEP 3: Interactive Chat Loop
        # ===================================================================
        # The agent is ready! Now you can chat with it and it will use the
        # MCP tools when needed to answer your questions.
        
        try:
            print("\n" + "="*60)
            print("💬 Interactive Chat Mode")
            print("="*60)
            print("Ask math questions and watch the agent use your MCP tools!")
            print("Type 'exit', 'quit', or 'q' to end")
            print("="*60 + "\n")
            
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
                    
                    # Run the agent with user's query
                    # The agent will automatically decide which tools to use
                    print("\n🤖 Assistant: ", end="", flush=True)
                    result = await agent.run(user_input)
                    print(result.text)
                    print()  # Extra newline for readability
                    
                except EOFError:
                    # Handle Ctrl+D
                    print("\n\n👋 Goodbye!")
                    break
                    
        finally:
            # ===================================================================
            # CLEANUP: Close MCP connection
            # ===================================================================
            # Always cleanup async resources properly
            await mcp_tool.close()
            print("\n✓ MCP tool connection closed")

# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    print("🚀 Starting Azure AI Foundry Agent with MCP...")
    print("📝 Make sure your MCP server is running (python server.py)\n")
    asyncio.run(basic_foundry_mcp_example())