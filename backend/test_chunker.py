from app.parser.chunker import chunk_text


text = """
This is a sample document.
We are testing whether a long document can be divided into smaller pieces.
Each piece will later be converted into an embedding and stored in PostgreSQL.
"""

chunks = chunk_text(
    text,
    chunk_size=50,
    chunk_overlap=10,
)

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {index} ---")
    print(chunk)