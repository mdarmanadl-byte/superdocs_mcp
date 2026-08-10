from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm_service import generate_answer
from app.services.retrieval_service import retrieve_chunks


async def answer_query(
    session: AsyncSession,
    pile_id: UUID,
    query: str,
):
    chunks = await retrieve_chunks(
        session=session,
        pile_id=pile_id,
        query=query,
        limit=5,
    )

    if not chunks:
        return {
            "answer": "I could not find relevant information in the documents.",
            "sources": [],
        }

    context_parts = []

    for chunk, document in chunks:
        context_parts.append(
            f"[Source: document={document.id}, "
            f"filename={document.filename}, "
            f"page={chunk.page_number}, "
            f"chunk={chunk.chunk_index}]\n"
            f"{chunk.content}"
        )

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        query=query,
        context=context,
    )

    sources = [
        {
            "document_id": document.id,
            "filename": document.filename,
            "page": chunk.page_number,
            "chunk": chunk.chunk_index,
        }
        for chunk, document in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }