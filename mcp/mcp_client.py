from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.sse import sse_client


class ContainerLookup:
    """A client for interacting with Container Lookup through MCP (Model Context Protocol) server.
    
    This client establishes and manages a connection to an MCP server using Server-Sent Events (SSE),
    allowing for tool discovery and execution of container lookup operations.
    
    Attributes:
        session (Optional[ClientSession]): The active client session with the MCP server.
        exit_stack (AsyncExitStack): Context manager for handling async resources.
    """
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        
    async def connect_to_server(self, server_url):
        """Establishes an async connection to the MCP server using SSE transport.
        
        Args:
            server_url (str): The URL endpoint of the MCP server to connect to.
            
        Returns:
            ClientSession: The established client session object.
            
        Raises:
            ConnectionError: If the connection to the server cannot be established.
        """
        # Connect using SSE transport
        sse_transport = await self.exit_stack.enter_async_context(
            sse_client(server_url)
        )
        read, write = sse_transport
        
        # Create the client session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        
        # Initialize the session
        await self.session.initialize()       
                
        return self.session
    
    async def get_tools(self):
        """Retrieves and formats available tools from the MCP server.
        
        Fetches the list of available tools from the connected MCP server and converts
        them into agent-compatible function schemas.
        
        Returns:
            list[dict]: A list of tool definitions in agent function calling format.
            Each tool is represented as a dictionary containing:
                - type: The type of the tool (always "function")
                - function: Dictionary containing name, description, and parameters schema
                
        Raises:
            RuntimeError: If called before establishing a server connection.
        """
        response = await self.session.list_tools()
        tool_names = [tool.name for tool in response.tools]
        print(f'Available Server Tools: {tool_names}')
        
        agent_tools_schema = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]
        
        return agent_tools_schema
    
    async def get_container_lookup(self, container_id: Optional[str] = None):
        """Retrieves container color information.
        
        Args:
            container_id (Optional[str]): The container ID to lookup (unused in this simple implementation).
            
        Returns:
            str: Container color information.
        """
        return "Container is Red"
    
    async def get_container_location(self, container_id: Optional[str] = None):
        """Retrieves container location information.
        
        Args:
            container_id (Optional[str]): The container ID to lookup (unused in this simple implementation).
            
        Returns:
            str: Container location information.
        """
        return "Container in China"
    
    async def disconnect(self):
        """Cleanly disconnects from the MCP server.
        
        Closes the async exit stack and cleans up the client session.
        After disconnection, the client will need to reconnect before making
        further server requests.
        """
        await self.exit_stack.aclose()
        self.session = None


# Example usage
async def main():
    """Example usage of the ContainerLookup client."""
    client = ContainerLookup()
    
    # Example of using the simple tools without server connection
    color_info = await client.get_container_lookup("CONT123")
    print(color_info)  # Output: Container is Red
    
    location_info = await client.get_container_location("CONT123")
    print(location_info)  # Output: Container in China
    
    # If you need to connect to an actual MCP server:
    # await client.connect_to_server("http://your-mcp-server-url")
    # tools = await client.get_tools()
    # await client.disconnect()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())