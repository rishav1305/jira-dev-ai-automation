import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from dotenv import load_dotenv

async def inspect_server():
    load_dotenv()
    url = os.getenv("MCP_SERVER_URL", "http://unified-mcp-server:8080/sse")
    print(f"Connecting to MCP Server at: {url}")

    try:
        async with sse_client(url=url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                
                # List Tools
                result = await session.list_tools()
                print("\n--- Available Tools ---")
                confluence_tools = []
                for tool in result.tools:
                    print(f"- {tool.name}: {tool.description}")
                    if tool.name in ["get_page", "create_page", "update_page", "search_pages", "get_page_id", "create_space"]:
                        confluence_tools.append(tool.name)
                
                print("\n--- Verification ---")
                if confluence_tools:
                    print(f"✅ Found {len(confluence_tools)} Confluence tools: {', '.join(confluence_tools)}")
                else:
                    print(f"❌ No Confluence tools found!")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(inspect_server())
