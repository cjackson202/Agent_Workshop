"""
MCP Server - Calculator Tools
==============================

This is a Model Context Protocol (MCP) server that provides mathematical
calculation tools to AI agents. The server exposes tools that agents can
discover and invoke to perform calculations.

Workshop: Add your own tools by following the pattern below!
"""

# server.py
from mcp.server.fastmcp import FastMCP
import uvicorn

# Create an MCP server
# This server will be accessible at http://localhost:8080/mcp
mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",  # Listen on all network interfaces (localhost for dev)
    port=8080,  # Port number - must match what clients connect to
)


# ============================================================================
# TOOLS - Add your custom tools below using the @mcp.tool() decorator
# ============================================================================

# Tool 1: Addition
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        The sum of a and b
    """
    print('-'*50)
    print(f"Add tool being used for sum of:")
    print(a)
    print('+')
    print(b)
    print('-'*50)
    return a + b

# Tool 2: Subtraction
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers
    
    Args:
        a: Number to subtract from
        b: Number to subtract
        
    Returns:
        The difference (a - b)
    """
    print('-'*50)
    print(f"Subtract tool being used for difference of:")
    print(a)
    print('-')
    print(b)
    print('-'*50)
    return a - b

# ============================================================================
# Additional Tool "Multiplication" can be added here. 
# ============================================================================

# ============================================================================
# RESOURCES - Dynamic content accessible via URI patterns
# Resources are different from tools - they provide data/content rather than
# performing actions. Agents can request resources by URI.
# ============================================================================

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting
    
    This resource can be accessed via URI: greeting://YourName
    
    Args:
        name: The name to include in the greeting
        
    Returns:
        A personalized greeting message
    """
    print('-'*50)
    print(f"Greeting resource being used for:")
    print(name)
    print('-'*50)
    return f"Hello, {name}!"


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    """Main entry point - starts the MCP server"""
    print("="*60)
    print("🚀 Starting MCP Server")
    print("="*60)
    print("Transport: HTTP Streamable")
    print("Endpoint: http://0.0.0.0:8080/mcp") 
    print("\nAvailable Tools:")
    print("  - add(a, b): Add two numbers")
    print("  - subtract(a, b): Subtract two numbers")
    print("  - multiply(a, b): Multiply two numbers")
    print("\nAvailable Resources:")
    print("  - greeting://{name}: Get personalized greeting")
    print("="*60)
    print("\n⚡ Server is running... (Press CTRL+C to stop)\n")
    
    # Get the streamable HTTP ASGI app from FastMCP and run it
    app = mcp.streamable_http_app
    uvicorn.run(app, host="0.0.0.0", port=8080)