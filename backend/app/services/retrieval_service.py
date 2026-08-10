from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import desc
from uuid import UUID

from app.models import Document, DocumentChunk
from app.services.embedding_service import generate_embedding


async def retrieve_chunks(
    session: AsyncSession,
    pile_id: UUID,
    query: str,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    )

    result = await session.execute(
        select(DocumentChunk, Document)
        .join(Document)
        .where(Document.pile_id == pile_id)
        .order_by(distance)
        .limit(limit)
)

    return result.all()

    