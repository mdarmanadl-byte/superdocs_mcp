from typing import TypedDict


class AgentState(TypedDict):
    pile_id: str
    query: str
    context: str
    answer: str
    sources: list[dict]
    should_generate: bool
    retry_count: int
    human_approved: bool
    finding: dict
    mcp_result: object
    timing: dict
    usage: dict