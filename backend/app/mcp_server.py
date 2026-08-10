from fastmcp import FastMCP

from app.database import AsyncSessionLocal
from app.services.retrieval_service import retrieve_chunks

mcp = FastMCP("SuperDocs")


@mcp.tool()
async def search_documents(query: str, pile_id: str) -> list[dict]:
    """Search a SuperDocs pile and return relevant document chunks."""

    async with AsyncSessionLocal() as session:
        chunks = await retrieve_chunks(
            session=session,
            pile_id=pile_id,
            query=query,
            limit=5,
        )

        return [
            {
                "document_id": str(document.id),
                "filename": document.filename,
                "page": chunk.page_number,
                "chunk": chunk.chunk_index,
                "content": chunk.content,
            }
            for chunk, document in chunks
        ]

@mcp.tool()
async def ask_document(query: str, pile_id: str) -> dict:
    """Ask a question about documents in a SuperDocs pile."""

    async with AsyncSessionLocal() as session:
        chunks = await retrieve_chunks(
            session=session,
            pile_id=pile_id,
            query=query,
            limit=5,
        )

        context_parts = []

        sources = []

        for chunk, document in chunks:
            context_parts.append(
                f"[Source: {document.filename}, "
                f"page {chunk.page_number}, "
                f"chunk {chunk.chunk_index}]\n"
                f"{chunk.content}"
            )

            sources.append(
                {
                    "document_id": str(document.id),
                    "filename": document.filename,
                    "page": chunk.page_number,
                    "chunk": chunk.chunk_index,
                }
            )

        context = "\n\n".join(context_parts)

        from app.services.llm_service import generate_answer

        answer = generate_answer(
            query=query,
            context=context,
        )

        return {
            "query": query,
            "answer": answer,
            "sources": sources,
        }
if __name__ == "__main__":
    mcp.run()