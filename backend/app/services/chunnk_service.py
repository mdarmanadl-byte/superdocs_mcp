from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DocumentChunk, DocumentPage
from app.parser.chunker import chunk_text


async def create_document_chunks(
    session: AsyncSession,
    document_id: UUID,
):
    result = await session.execute(
        select(DocumentPage)
        .where(DocumentPage.document_id == document_id)
        .order_by(DocumentPage.page_number)
    )

    pages = result.scalars().all()

    chunks = []

    for page in pages:
        page_chunks = chunk_text(page.content)

        for chunk_index, content in enumerate(page_chunks):
            chunk = DocumentChunk(
                document_id=document_id,
                page_number=page.page_number,
                chunk_index=chunk_index,
                content=content,
            )

            session.add(chunk)
            chunks.append(chunk)

    await session.commit()

    return chunks