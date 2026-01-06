import asyncio
from agent_framework import MCPStreamableHTTPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import ClientSecretCredential
import os

# Required environment variables
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://<ai_foundry_resource>.services.ai.azure.com/api/projects/<project_name>"
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "your-model-deployment-name"

# Service Principal credentials (set these environment variables)
# Create SP in commercial Azure: az ad sp create-for-rbac --name "aml-to-ai-foundry" --role "Azure AI Developer" --scopes /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<ai-project>
TENANT_ID = os.environ.get("AZURE_COMMERCIAL_TENANT_ID")  # Your commercial Azure tenant ID
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")  # Service principal app ID
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")  # Service principal password

# Debug: Print to verify env vars are set
print(f"TENANT_ID: {TENANT_ID}")
print(f"CLIENT_ID: {CLIENT_ID}")
print(f"CLIENT_SECRET: {'***' if CLIENT_SECRET else 'NOT SET'}")

async def basic_foundry_mcp_example():
    """Basic example of Azure AI Foundry agent with hosted MCP tools.
    
    Uses Service Principal authentication to bypass Conditional Access device policies.
    Cross-cloud scenario: Azure Gov AML -> Commercial Azure AI Foundry
    """
    
    # Use ClientSecretCredential - works across clouds and bypasses device policies
    async with ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ) as credential:
        print("✓ Credential created")
        async with AzureAIAgentClient(credential=credential) as chat_client:
            print("✓ AzureAIAgentClient initialized")
            
            # Enable Azure AI observability (optional but recommended)
            # await chat_client.setup_azure_ai_observability()
            
            # Create MCP tool for local testing (client-side connection)
            mcp_tool = MCPStreamableHTTPTool(
                name="Custom MCP Server",
                url="http://localhost:8080/mcp",
                chat_client=chat_client
            )
            print("✓ MCP tool configured for localhost:8080")
            
            try:
                # Create agent with local MCP tool
                agent = chat_client.create_agent(
                    name="CustomMCPAgent", 
                    instructions="""You are a helpful assistant with access to MCP tools and resources.
                    
                    You have access to:
                    - Tools: Functions you can call (like add, subtract)
                    - Resources: Data you can read using URIs (like greeting://[name] for personalized greetings)
                    
                    When asked about available capabilities, mention both tools AND resources.
                    To access a resource, read it using its URI format (e.g., greeting://John).
                    """,
                    tools=mcp_tool,
                )
                print(f"✓ Agent created with local MCP tool")

                # Interactive chat loop
                print("\n" + "="*60)
                print("Interactive Chat Mode - Type 'exit', 'quit', or 'q' to end")
                print("="*60 + "\n")
                
                while True:
                    try:
                        # Get user input
                        user_input = input("You: ").strip()
                        
                        # Check for exit commands
                        if user_input.lower() in ['exit', 'quit', 'q']:
                            print("\nGoodbye!")
                            break
                        
                        # Skip empty inputs
                        if not user_input:
                            continue
                        
                        # Run the agent with user's query
                        print("\nAssistant: ", end="", flush=True)
                        result = await agent.run(user_input)
                        print(result)
                        print()  # Extra newline for readability
                        
                    except EOFError:
                        # Handle Ctrl+D
                        print("\n\nGoodbye!")
                        break
            finally:
                # Properly close the MCP tool to cleanup async resources
                await mcp_tool.close()

if __name__ == "__main__":
    try:
        asyncio.run(basic_foundry_mcp_example())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")