"""
Simple MCP Client to Test Server Locally

This script connects to the MCP server running locally and:
1. Lists available tools
2. Tests the 'add' and 'subtract' functions

Usage:
1. Start the MCP server: python server.py
2. In another terminal, run: python test_mcp_client.py
"""

import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_mcp_server():
    """Test the MCP server running locally"""
    
    # Server endpoint
    server_url = "http://localhost:8080/mcp"
    
    print("=" * 60)
    print("MCP Server Test Client")
    print("=" * 60)
    print(f"Connecting to: {server_url}\n")
    
    streams = None
    session = None
    
    try:
        # Connect to MCP server using streamable HTTP transport
        print("🔌 Initializing MCP session...")
        print("-" * 60)
        
        streams_ctx = streamablehttp_client(server_url)
        streams = await streams_ctx.__aenter__()
        session_ctx = ClientSession(streams[0], streams[1])
        session = await session_ctx.__aenter__()
        await session.initialize()
        
        print("✅ Session initialized successfully\n")
        
        # Test 1: List available tools
        print("📋 Fetching available tools...")
        print("-" * 60)
        
        response = await session.list_tools()
        tools = response.tools
        
        print(f"✅ Found {len(tools)} tool(s):\n")
        
        for i, tool in enumerate(tools, 1):
            print(f"{i}. Tool: {tool.name}")
            print(f"   Description: {tool.description or 'N/A'}")
            if tool.inputSchema:
                print(f"   Input Schema:")
                schema = tool.inputSchema
                if 'properties' in schema:
                    for prop_name, prop_info in schema['properties'].items():
                        prop_type = prop_info.get('type', 'unknown')
                        prop_desc = prop_info.get('description', '')
                        print(f"      - {prop_name} ({prop_type}): {prop_desc}")
                if 'required' in schema:
                    print(f"   Required: {', '.join(schema['required'])}")
            print()
        
        # Test 2: Test the 'add' tool
        print("=" * 60)
        print("🧮 Testing 'add' tool (5 + 3)...")
        print("-" * 60)
        
        result = await session.call_tool("add", {"a": 5, "b": 3})
        
        if result.content:
            content = result.content[0]
            if hasattr(content, 'text'):
                print(f"✅ Result: {content.text}")
            else:
                print(f"✅ Result: {content}")
        else:
            print(f"✅ Result: {result}")
        
        # Test 3: Test the 'subtract' tool
        print("=" * 60)
        print("🧮 Testing 'subtract' tool (5 - 3)...")
        print("-" * 60)
        
        result = await session.call_tool("subtract", {"a": 5, "b": 3})
        
        if result.content:
            content = result.content[0]
            if hasattr(content, 'text'):
                print(f"✅ Result: {content.text}")
            else:
                print(f"✅ Result: {content}")
        else:
            print(f"✅ Result: {result}")

        
        # Test 4: List available resources
        print("\n" + "=" * 60)
        print("📚 Fetching available resources...")
        print("-" * 60)
        
        try:
            resources_response = await session.list_resources()
            resources = resources_response.resources
            
            if resources:
                print(f"✅ Found {len(resources)} resource(s):\n")
                
                for i, resource in enumerate(resources, 1):
                    print(f"{i}. Resource URI: {resource.uri}")
                    print(f"   Name: {resource.name or 'N/A'}")
                    print(f"   Description: {resource.description or 'N/A'}")
                    print(f"   MIME Type: {resource.mimeType or 'N/A'}")
                    print()
            else:
                print("ℹ️  No resources found (this is normal if server doesn't expose any)")
        except Exception as e:
            print(f"⚠️  Could not list resources: {e}")
        
        # Test 5: Test greeting resource (if available)
        print("\n" + "=" * 60)
        print("👋 Testing 'greeting' resource...")
        print("-" * 60)
        
        try:
            # Try to read the greeting resource with a sample name
            resource_uri = "greeting://World"
            print(f"Reading resource: {resource_uri}")
            
            resource_result = await session.read_resource(resource_uri)
            
            if resource_result.contents:
                content = resource_result.contents[0]
                if hasattr(content, 'text'):
                    print(f"✅ Greeting: {content.text}")
                else:
                    print(f"✅ Result: {content}")
            else:
                print(f"✅ Result: {resource_result}")
        except Exception as e:
            print(f"ℹ️  Greeting resource not available or error occurred: {e}")
            print("   (This is expected if the greeting resource is not defined in the server)")

        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if session:
            try:
                await session_ctx.__aexit__(None, None, None)
            except:
                pass
        if streams:
            try:
                await streams_ctx.__aexit__(None, None, None)
            except:
                pass


if __name__ == "__main__":
    asyncio.run(test_mcp_server())