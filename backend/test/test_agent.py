import pytest

from app.agents.graph import analyze_node
from app.services.llm_service import generate_finding
from app.services.llm_service import parse_finding_response


@pytest.mark.asyncio
async def test_analyze_with_empty_context():
    state = {
        "pile_id": "test-pile",
        "query": "What is Arman's salary?",
        "context": "",
        "answer": "",
        "sources": [],
        "should_generate": False,
        "retry_count": 0,
        "human_approved": False,
        "finding": {},
    }

    result = await analyze_node(state)

    assert result["should_generate"] is False
    assert result["answer"] == (
        "I could not find relevant information in the documents."
    )


@pytest.mark.asyncio
async def test_analyze_with_context():
    state = {
        "pile_id": "test-pile",
        "query": "Which technology does Skolist use?",
        "context": "Skolist uses Next.js, Node.js and PostgreSQL.",
        "answer": "",
        "sources": [],
        "should_generate": False,
        "retry_count": 0,
        "human_approved": False,
        "finding": {},
    }

    result = await analyze_node(state)

    assert result["should_generate"] is True

def test_finding_response_has_required_fields():
    context = """
    Arman has 2 years of software development experience.
    Later in the document it says Arman has 5 years of software
    development experience.
    """

    result,usage = generate_finding(
        query="What is Arman's experience?",
        context=context,
    )

    assert "has_finding" in result
    assert "type" in result
    assert "title" in result
    assert "description" in result
    assert "severity" in result
    assert usage["total_tokens"] > 0

def test_parse_finding():
    response = """
    {
        "has_finding": true,
        "type": "conflict",
        "title": "Conflicting experience information",
        "description": "The document says 2 years and 5 years.",
        "severity": "high"
    }
    """

    result = parse_finding_response(response)

    assert result["has_finding"] is True
    assert result["type"] == "conflict"
    assert result["severity"] == "high"


def test_parse_no_finding():
    response = """
    {
        "has_finding": false,
        "type": "",
        "title": "",
        "description": "",
        "severity": ""
    }
    """

    result = parse_finding_response(response)

    assert result["has_finding"] is False
    assert result["type"] == ""


def test_parse_markdown_json():
    response = """```json
    {
        "has_finding": true,
        "type": "conflict",
        "title": "Conflict",
        "description": "Two different values.",
        "severity": "medium"
    }
    ```"""

    result = parse_finding_response(response)

    assert result["has_finding"] is True
    assert result["severity"] == "medium"
def test_parse_invalid_json():
    response = "This is not valid JSON."

    result = parse_finding_response(response)

    assert result["has_finding"] is False
    assert result["type"] == ""
    assert result["title"] == ""
    assert result["description"] == ""
    assert result["severity"] == ""