from pathlib import Path

from docx import Document


def parse_docx(file_path: str | Path) -> list[dict]:
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return [
        {
            "page": 1,
            "text": "\n".join(paragraphs),
        }
    ]