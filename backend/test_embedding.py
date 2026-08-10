from app.services.embedding_service import generate_embedding


text = "This is a test document chunk."

embedding = generate_embedding(text)

print("Dimensions:", len(embedding))
print("First 5 values:", embedding[:5])