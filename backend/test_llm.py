from app.services.llm_service import generate_answer


context = """
Arman worked as a Founding Engineer at Skolist.
He built a full-stack platform using Next.js, Node.js,
and PostgreSQL.
"""

answer = generate_answer(
    query="What technologies did Arman use at Skolist?",
    context=context,
)

print(answer)