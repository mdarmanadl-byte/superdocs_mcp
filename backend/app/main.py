from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import create_tables, get_db
from app.exceptions import AppException

from app.api.piles import router as piles_router
from app.api.documents import router as documents_router
from sqlalchemy import select
import os
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.models import DocumentPage
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    async with AsyncPostgresSaver.from_conn_string(
        os.environ["CHECKPOINT_DATABASE_URL"]
    ) as checkpointer:

        await checkpointer.setup()

        app.state.checkpointer = checkpointer

        yield

app = FastAPI(
    title="DocTask",
    lifespan=lifespan,
)
app.include_router(piles_router)
app.include_router(documents_router)
app.openapi_schema = None
@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors(),
            },
        },
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    # Don't expose raw database errors to the client.
    print(f"Database error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred.",
            },
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    print(f"Unexpected error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred.",
            },
        },
    )


@app.get("/")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def database_health(
    session: AsyncSession = Depends(get_db),
):
    result = await session.execute(text("SELECT 1"))

    return {
        "database": result.scalar(),
    }

@app.get("/documents/{document_id}/pages")
async def get_document_pages(
    document_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    result = await session.execute(
        select(DocumentPage)
        .where(DocumentPage.document_id == document_id)
        .order_by(DocumentPage.page_number)
    )

    pages = result.scalars().all()

    return {
        "document_id": document_id,
        "pages": [
            {
                "page": page.page_number,
                "content": page.content,
            }
            for page in pages
        ],
    }