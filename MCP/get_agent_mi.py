"""
Connect to Azure AI Foundry Agent with MCP Tools
=================================================

This script connects to an Azure AI Foundry agent (created in the portal) 
and adds your custom MCP tools to it, allowing the agent to use your 
local MCP server capabilities.

Prerequisites:
1. An existing agent created in Azure AI Foundry portal
2. The agent's ID (copy from portal: Agents → Your Agent → Agent ID)
3. MCP server running (python server.py in another terminal)
4. Azure CLI authenticated (az login --identity)

Workshop Usage:
1. First, create your agent in Azure AI Foundry portal:
   - Go to Azure AI Foundry Studio
   - Navigate to "Agents" section
   - Click "Create Agent"
   - Give it a name and instructions
   - Copy the Agent ID
2. Update AGENT_ID variable below with your agent's ID
3. Update Azure project environment variables
4. Make sure server.py is running (in a separate terminal)
5. Run this script: python get_agent_mi.py
6. Start chatting with your agent using your MCP tools!
"""

import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import MCPStreamableHTTPTool
import os

# ============================================================================
# CONFIGURATION - Update these with your details
# ============================================================================

# Required: Your Azure AI Foundry project endpoint
# Find this in Azure AI Foundry Studio → Project Settings
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://<ai_foundry_resource>.services.ai.azure.com/api/projects/<project_name>"

# Required: Your model deployment name
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "your-model-deployment-name"

# Required: Your existing agent ID
# Get this from Azure AI Foundry Studio:
# 1. Navigate to "Agents" in the left sidebar
# 2. Click on your agent
# 3. Copy the Agent ID from the details
AGENT_ID = "your-agent-id"  # ← REPLACE THIS with your agent ID from the portal

# Example:
# os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://mcpworkshopdemo0000.services.ai.azure.com/api/projects/proj1"
# os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"
# AGENT_ID = "asst_abc123xyz456"
# ============================================================================


async def main():
    """
    Main function: Retrieves existing agent and adds MCP tool integration
    
    Steps:
    1. Authenticate using Azure CLI credentials (Managed Identity)
    2. Create Azure AI Agent client with existing agent ID
    3. Configure MCP tool pointing to local server
    4. Create ChatAgent wrapper with MCP tools
    5. Start interactive chat loop
    """
    async with AzureCliCredential() as credential:
        # ===================================================================
        # STEP 1: Connect to Your Agent
        # ===================================================================
        # Connect to the agent you created in Azure AI Foundry portal
        # This allows you to add your custom MCP tools to an existing agent
        # 
        # Benefits of this approach:
        # - See and manage your agent in the Azure portal
        # - Reuse the same agent across multiple sessions
        # - Update agent settings in the portal UI
        # - Production-ready deployment pattern
        
        chat_client = AzureAIAgentClient(
            credential=credential,
            agent_id=AGENT_ID  # The ID of your existing agent
        )
        print(f"✓ Connected to existing agent: {AGENT_ID}")
        
        # ===================================================================
        # STEP 2: Configure MCP Tool
        # ===================================================================
        # Add MCP tools to the existing agent
        # The server must be running at http://localhost:8080/mcp
        
        mcp_tool = MCPStreamableHTTPTool(
            name="Custom MCP Server",  # Friendly name for the tool
            url="http://localhost:8080/mcp",  # URL where your MCP server is running
            chat_client=chat_client  # Agent client for making requests
        )
        print("✓ MCP tool configured for localhost:8080")
        
        # ===================================================================
        # STEP 3: Create ChatAgent Wrapper
        # ===================================================================
        # Wrap the agent client in a ChatAgent for easier interaction
        
        async with ChatAgent(
            chat_client=chat_client,
            tools=mcp_tool,  # Add MCP tools to the agent
        ) as agent:
            print("✓ Agent ready with MCP tools")
            
            # ===================================================================
            # STEP 4: Interactive Chat Loop
            # ===================================================================
            # Chat with your existing agent using the MCP tools
            
            try:
                print("\n" + "="*60)
                print("💬 Interactive Chat Mode")
                print("="*60)
                print("Chatting with your existing agent + MCP tools")
                print("Type 'exit', 'quit', or 'q' to end")
                print("="*60 + "\n")

                # ==================================================================
                # CREATE A NEW THREAD FOR CONTEXTUAL CHAT HERE
                # ==================================================================
                
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
                        # The agent will automatically use MCP tools when needed
                        print("\n🤖 Assistant: ", end="", flush=True)
                        result = await agent.run(user_input) # add thread id here if needed (`thread_id=thread_id`)
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
    print("🚀 Retrieving existing Azure AI Foundry Agent...")
    print("📝 Make sure your MCP server is running (python server.py)\n")
    asyncio.run(main())