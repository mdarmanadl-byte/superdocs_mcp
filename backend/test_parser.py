from app.parser.loader import parse_document


file_path = (
    "uploads/edb71393-61ef-46c1-806e-57bec81411be/"
    "07621913-6102-4944-ae94-7c746ca684c9_document.pdf"
)

pages = parse_document(file_path)

for page in pages:
    print(f"\n--- PAGE {page['page']} ---")
    print(page["text"])