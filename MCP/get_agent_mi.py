"""
Retrieve Existing Azure AI Foundry Agent with MCP Tools
========================================================

This script retrieves an EXISTING Azure AI Foundry agent (by ID) and adds
MCP tools to it. Use this instead of create_agent_mi.py when you want to
reuse an agent you've already created.

Prerequisites:
1. An existing agent (created by create_agent_mi.py or in Azure portal)
2. The agent's ID (found in create script output or Azure portal)
3. MCP server running (python server.py in another terminal)
4. Azure CLI authenticated (az login)

Workshop Usage:
1. Copy your agent ID from the create_agent_mi.py output or Azure portal
2. Update AGENT_ID variable below
3. Update Azure project environment variables
4. Make sure server.py is running (in a separate terminal)
5. Run this script: python get_agent_mi.py
6. Start chatting with your existing agent!
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
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://YOUR-PROJECT.services.ai.azure.com/api/projects/YOUR-PROJECT-NAME"

# Required: Your model deployment name
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"

# Required: Your existing agent ID
# Get this from:
# 1. Output of create_agent_mi.py (look for "Agent ID: asst_xxxxx")
# 2. Azure AI Foundry Studio → Agents → Your Agent → Copy ID
AGENT_ID = "asst_N22njo9VdpIH29OqPiN4CJIA"  # ← REPLACE THIS with your agent ID

# Example:
# os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://camerjackson-9533-resource.services.ai.azure.com/api/projects/camerjackson-9533"
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
        # STEP 1: Get Existing Agent
        # ===================================================================
        # Connect to an existing agent by ID instead of creating a new one
        # This is useful for:
        # - Reusing agents across sessions
        # - Production deployments
        # - Avoiding duplicate agents
        
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
    print("🚀 Retrieving existing Azure AI Foundry Agent...")
    print("📝 Make sure your MCP server is running (python server.py)\n")
    asyncio.run(main())