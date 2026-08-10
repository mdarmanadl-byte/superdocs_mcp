from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DocumentChunk
from app.services.embedding_service import generate_embedding


async def embed_document_chunks(
    session: AsyncSession,
    document_id: UUID,
):
    result = await session.execute(
        select(DocumentChunk)
        .where(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index)
    )

    chunks = result.scalars().all()

    for chunk in chunks:
        chunk.embedding = generate_embedding(chunk.content)

    await session.commit()

    return chunks