import asyncio

from app.services.mcp_client import call_mcp_tool


async def main():
    result = await call_mcp_tool(
        "search_documents",
        {
            "query": "which technology used in skolist",
            "pile_id": "c67a15e1-7c7f-4e22-934f-360aea68aafb",
        },
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())