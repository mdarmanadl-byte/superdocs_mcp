from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Pile


router = APIRouter(
    prefix="/piles",
    tags=["Piles"],
)


class CreatePileRequest(BaseModel):
    name: str


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_pile(
    data: CreatePileRequest,
    session: AsyncSession = Depends(get_db),
):
    pile = Pile(name=data.name)

    session.add(pile)
    await session.commit()
    await session.refresh(pile)

    return {
        "id": pile.id,
        "name": pile.name,
        "created_at": pile.created_at,
    }