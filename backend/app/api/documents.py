from pathlib import Path
from uuid import UUID, uuid4
from typing import Annotated
from app.services.retrieval_service import retrieve_chunks
from langgraph.types import Command
import time
from app.services.llm_service import calculate_total_usage
# Cleaned up duplicate/overlapping imports
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models import Finding
from app.database import get_db


from app.parser.loader import parse_document
from app.models import Document, DocumentPage, Pile, Run, Finding
from app.services.chunnk_service import create_document_chunks
from app.services.vector_service import embed_document_chunks
from app.services.rag_service import answer_query
from app.agents.graph import build_graph
from fastapi import Request
router = APIRouter(
    prefix="/piles",
    tags=["Documents"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post(
    "/{pile_id}/documents",
    status_code=status.HTTP_201_CREATED,
)
async def upload_documents(
    pile_id: UUID,
    # FIXED: Replaced standard Annotated list format with explicit File default assignment
    files: list[UploadFile] = File(),
    session: AsyncSession = Depends(get_db),
):
    # Check that the pile exists
    result = await session.execute(
        select(Pile).where(Pile.id == pile_id)
    )
    pile = result.scalar_one_or_none()

    if pile is None:
        raise HTTPException(
            status_code=404,
            detail="Pile not found",
        )

    documents = []

    for upload_file in files:
        document_id = uuid4()

        pile_dir = UPLOAD_DIR / str(pile_id)
        pile_dir.mkdir(parents=True, exist_ok=True)

        file_path = pile_dir / f"{document_id}_{upload_file.filename}"

        with file_path.open("wb") as file:
            while chunk := await upload_file.read(1024 * 1024):
                file.write(chunk)

        document = Document(
            id=document_id,
            pile_id=pile_id,
            filename=upload_file.filename,
            content_type=upload_file.content_type,
            file_path=str(file_path),
        )

        session.add(document)
        documents.append(document)

        pages = parse_document(file_path)

        for page in pages:
            document_page = DocumentPage(
                document_id=document_id,
                page_number=page["page"],
                content=page["text"],
            )

            session.add(document_page)

        await session.flush()

        await create_document_chunks(
            session,
            document_id,
        )
        await embed_document_chunks(
                session,
                document_id,
            )

    await session.commit()

    for document in documents:
        await session.refresh(document)

    return {
        "pile_id": pile_id,
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "content_type": document.content_type,
            }
            for document in documents
        ],
    }

@router.get("/{pile_id}/search")
async def search_documents(
    pile_id: UUID,
    query: str,
    session: AsyncSession = Depends(get_db),
):
    chunks = await retrieve_chunks(
        session=session,
        pile_id=pile_id,
        query=query,
    )

    return {
        "query": query,
        "results": [
            {
                "document_id": chunk.document_id,
                "page": chunk.page_number,
                "chunk": chunk.chunk_index,
                "content": chunk.content,
            }
            for chunk in chunks
        ],
    }

@router.get("/{pile_id}/ask")
async def ask_documents(
    request: Request,
    pile_id: UUID,
    query: str,
    session: AsyncSession = Depends(get_db),
):
    run = Run(
        
        pile_id=pile_id,
        query=query,
        status="running",
        current_stage="started",
    )

    session.add(run)
    await session.commit()
    await session.refresh(run)

    graph =  build_graph(session=session,
    checkpointer=request.app.state.checkpointer,
)
    run_start = time.perf_counter()
    result = await graph.ainvoke(
            {
        "pile_id": str(pile_id),
        "query": query,
        "context": "",
        "answer": "",
        "sources": [],
        "should_generate": False,
        "retry_count": 0,
        "human_approved": False,
        "finding": {},
        "timing": {},
    },
    config={
        "configurable": {
            "thread_id": str(run.id),
        }
    },
        )
    # print("GRAPH RESULT:")
    # print(result)
    usage = result.get("usage", {})

    total_usage = calculate_total_usage(usage)
    total_duration_ms = round(
            (time.perf_counter() - run_start) * 1000,
            2,
        )
    run.usage = {
            "stages": usage,
            "total": total_usage,
        }
    run.timing = {
            "stages": result.get("timing", {}),
            "total_duration_ms": total_duration_ms,
        }
            
    finding_data = result.get("finding", {})
    # print("FINDING DATA:", finding_data)

    if finding_data.get("has_finding"):
        finding = Finding(
            run_id=run.id,
            type=finding_data["type"],
            title=finding_data["title"],
            description=finding_data["description"],
            severity=finding_data["severity"],
            status="pending",
        )

        session.add(finding)
    
    if "__interrupt__" in result:
        run.answer = result["answer"]
        run.status = "waiting_review"
        run.current_stage = "human_review"

        await session.commit()

        return {
            "run_id": str(run.id),
            "status": "waiting_review",
            "answer": result["answer"],
            "sources": result["sources"],
        }

    run.answer = result["answer"]
    run.status = "completed"
    run.current_stage = "completed"

    await session.commit()

    return {
        "run_id": str(run.id),
        "status": "completed",
        "answer": result["answer"],
        "sources": result["sources"],
    }

@router.post("/runs/{run_id}/review")
async def review_run(
    request: Request,
    run_id: UUID,
    approved: bool,
    session: AsyncSession = Depends(get_db),
):
    result = await session.execute(
        select(Run).where(Run.id == run_id)
    )

    run = result.scalar_one_or_none()

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found",
        )

    if run.status != "waiting_review":
        raise HTTPException(
            status_code=400,
            detail=f"Run is not waiting for review. Current status: {run.status}",
        )

    graph = build_graph(
        session=session,
        checkpointer=request.app.state.checkpointer,
    )

    result = await graph.ainvoke(
        Command(
            resume={
                "approved": approved,
            }
        ),
        config={
            "configurable": {
                "thread_id": str(run.id),
            }
        },
    )

    if "__interrupt__" in result:
        run.status = "waiting_review"
        run.current_stage = "human_review"
    else:
        run.answer = result.get("answer", run.answer)
        run.status = "completed"
        run.current_stage = "completed"

    await session.commit()

    return {
        "run_id": str(run.id),
        "status": run.status,
        "answer": run.answer,
        "approved": approved,
        "sources": result.get("sources", []),
    }

@router.get("/runs/{run_id}/findings")
async def get_run_findings(
    run_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    result = await session.execute(
        select(Finding)
        .where(Finding.run_id == run_id)
        .order_by(Finding.created_at.desc())
    )

    findings = result.scalars().all()

    return {
        "run_id": str(run_id),
        "findings": [
            {
                "id": str(finding.id),
                "type": finding.type,
                "title": finding.title,
                "description": finding.description,
                "severity": finding.severity,
                "status": finding.status,
            }
            for finding in findings
        ],
    }

@router.post("/runs/{run_id}/findings/{finding_id}/review")
async def review_finding(
    run_id: UUID,
    finding_id: UUID,
    approved: bool,
    session: AsyncSession = Depends(get_db),
):
    result = await session.execute(
        select(Finding).where(
            Finding.id == finding_id,
            Finding.run_id == run_id,
        )
    )

    finding = result.scalar_one_or_none()

    if finding is None:
        raise HTTPException(
            status_code=404,
            detail="Finding not found",
        )

    if finding.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Finding is already {finding.status}",
        )

    finding.status = "approved" if approved else "rejected"

    run_result = await session.execute(
        select(Run).where(Run.id == run_id)
    )

    run = run_result.scalar_one_or_none()

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found",
        )

    if approved:
        run.status = "completed"
        run.current_stage = "completed"
    else:
        run.status = "rejected"
        run.current_stage = "human_review"

    await session.commit()

    return {
        "finding_id": str(finding.id),
        "run_id": str(run_id),
        "status": finding.status,
    }

@router.get("/runs/{run_id}")
async def get_run(
    run_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    result = await session.execute(
        select(Run).where(Run.id == run_id)
    )

    run = result.scalar_one_or_none()

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found",
        )

    return {
        "run_id": str(run.id),
        "pile_id": str(run.pile_id),
        "query": run.query,
        "status": run.status,
        "current_stage": run.current_stage,
        "answer": run.answer,
        "created_at": run.created_at,
        "updated_at": run.updated_at,
    }

@router.get("/runs/{run_id}/details")
async def get_run_details(
    run_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    result = await session.execute(
        select(Run).where(Run.id == run_id)
    )

    run = result.scalar_one_or_none()

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found",
        )

    finding_result = await session.execute(
        select(Finding)
        .where(Finding.run_id == run.id)
        .order_by(Finding.created_at.desc())
    )

    findings = finding_result.scalars().all()

    return {
        "run_id": str(run.id),
        "pile_id": str(run.pile_id),
        "query": run.query,
        "status": run.status,
        "current_stage": run.current_stage,
        "answer": run.answer,
        "findings": [
            {
                "id": str(f.id),
                "type": f.type,
                "title": f.title,
                "description": f.description,
                "severity": f.severity,
                "status": f.status,
            }
            for f in findings
        ],
        "created_at": run.created_at,
        "updated_at": run.updated_at,
    }