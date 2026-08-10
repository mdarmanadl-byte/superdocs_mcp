import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("TOOLS:")
            for tool in tools.tools:
                print(tool.name)

            result = await session.call_tool(
                "ask_document",
                arguments={
                    "query": "which technology used in skolist",
                    "pile_id": "c67a15e1-7c7f-4e22-934f-360aea68aafb",
                },
            )

            print("\nRESULT:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())