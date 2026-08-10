


from sqlalchemy.ext.asyncio import AsyncSession
import time
from app.agents.state import AgentState
from app.services.embedding_service import generate_embedding

from app.services.llm_service import generate_answer ,generate_finding
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from app.services.mcp_client import call_mcp_tool
async def analyze_node(state: AgentState) -> AgentState:
    if not state["context"].strip():
        return {
            **state,
            "answer": "I could not find relevant information in the documents.",
            "should_generate": False,
        }

    return {
        **state,
        "should_generate": True,
    }
def build_graph(session: AsyncSession, checkpointer):

    
    async def mcp_search_node(state: AgentState) -> AgentState:
        start = time.perf_counter()
        result = await call_mcp_tool(
            "search_documents",
            {
                "query": state["query"],
                "pile_id": state["pile_id"],
            },
        )

        # MCP returns structuredContent when FastMCP wraps the result
        if hasattr(result, "structuredContent") and result.structuredContent:
            chunks = result.structuredContent.get("result", [])
        else:
            chunks = []

        context_parts = []
        sources = []

        for item in chunks:
            context_parts.append(
                f"[Source: {item['filename']}, "
                f"page {item['page']}, "
                f"chunk {item['chunk']}]\n"
                f"{item['content']}"
            )

            sources.append(
                {
                    "document_id": item["document_id"],
                    "filename": item["filename"],
                    "page": item["page"],
                    "chunk": item["chunk"],
                }
            )
        timing = record_stage_timing(
        state,
        "mcp_search",
        start,
    )
        return {
            **state,
            "context": "\n\n".join(context_parts),
            "sources": sources,
            "mcp_result": chunks,
            "timing": timing,
            "retry_count": (
                state["retry_count"] + 1
                if not context_parts
                else state["retry_count"]
            ),
        }
    # async def analyze_node(state: AgentState) -> AgentState:
    #     if not state["context"].strip():
    #         return {
    #             **state,
    #             "answer": "I could not find relevant information in the documents.",
    #             "should_generate": False,
    #         }

    #     return {
    #         **state,
    #         "should_generate": True,
    #     }
    def route_after_analysis(state: AgentState):
        if state["should_generate"]:
            return "generate"

        # if state["retry_count"] < 2:
        #     return "retrieve"

        return END
    async def generate_node(state: AgentState) -> AgentState:
        start = time.perf_counter()

        answer, usage= generate_answer(
            query=state["query"],
            context=state["context"],
        )
        timing = record_stage_timing(
        state,
        "generate",
        start,
    )


        return {
            **state,
            "answer": answer,
             "timing": timing,
             "usage": {
        **(state.get("usage") or {}),
        "generate": usage,
    },
        }
    async def finding_node(state: AgentState) -> AgentState:
        start = time.perf_counter()
        finding,usage = generate_finding(
            query=state["query"],
            context=state["context"],
        )
        timing = record_stage_timing(
        state,
        "finding",
        start,
    )
        return {
            **state,
            "finding": finding,
                "timing": timing,
                 "usage": {
            **(state.get("usage") or {}),
            "finding": usage,
        },
        }
    async def human_review_node(state: AgentState) -> AgentState:
        decision = interrupt(
            {
                "type": "human_review",
                "message": "Please review the generated answer.",
                "answer": state["answer"],
                "sources": state["sources"],
            }
        )

        return {
            **state,
            "human_approved": decision.get("approved", False),
        }
    


    builder = StateGraph(AgentState)

    # builder.add_node("retrieve", retrieve_node)
    builder.add_node("analyze", analyze_node)
    builder.add_node("generate", generate_node)
    builder.add_node("finding", finding_node)
    builder.add_node("human_review", human_review_node)
    builder.add_node("mcp_search", mcp_search_node)
    builder.add_edge(START, "mcp_search")
    builder.add_edge("mcp_search", "analyze")

    builder.add_conditional_edges(
        "analyze",
        route_after_analysis,
        {
            "generate": "generate",
            END: END,
        },
    )

    builder.add_edge("generate", "finding")
    builder.add_edge("finding", "human_review")
    builder.add_edge("human_review", END)
    print("BEFORE CHECKPOINTER")
#     async with AsyncPostgresSaver.from_conn_string(
#     os.environ["CHECKPOINT_DATABASE_URL"]
# ) as checkpointer:
#         print("CHECKPOINTER CONNECTED")
#         # await checkpointer.setup()

#         print("CHECKPOINTER SETUP SUCCESS")

#         return builder.compile(
#             checkpointer=checkpointer
#         )
    return builder.compile(
    checkpointer=checkpointer
)
def record_stage_timing(state: AgentState, stage: str, start: float) -> dict:
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    timing = dict(state.get("timing") or {})
    timing[stage] = {
        "duration_ms": elapsed_ms,
    }

    return timing
  
