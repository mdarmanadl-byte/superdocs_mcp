import asyncio
import os
from uuid import uuid4

import pytest
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.agents.graph import build_graph
from app.database import AsyncSessionLocal


async def run_graph(checkpointer, pile_id, query, run_id):
    async with AsyncSessionLocal() as session:

        graph = build_graph(
            session=session,
            checkpointer=checkpointer,
        )

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
            },
            config={
                "configurable": {
                    "thread_id": str(run_id),
                }
            },
        )

        return result


@pytest.mark.asyncio
async def test_two_runs_are_isolated():

    pile_id = uuid4()

    run_1 = uuid4()
    run_2 = uuid4()

    async with AsyncPostgresSaver.from_conn_string(
        os.environ["CHECKPOINT_DATABASE_URL"]
    ) as checkpointer:

        await checkpointer.setup()

        result_1, result_2 = await asyncio.gather(
            run_graph(
                checkpointer,
                pile_id,
                "What technology is used?",
                run_1,
            ),
            run_graph(
                checkpointer,
                pile_id,
                "What is the project name?",
                run_2,
            ),
        )

    assert run_1 != run_2
    assert result_1 is not None
    assert result_2 is not None