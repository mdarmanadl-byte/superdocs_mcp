from pathlib import Path

from app.parser.docx_parser import parse_docx
from app.parser.pdf_parser import parse_pdf
from app.parser.text_parser import parse_text


def parse_document(file_path: str | Path) -> list[dict]:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        return parse_pdf(path)

    if extension == ".docx":
        return parse_docx(path)

    if extension == ".txt":
        return parse_text(path)

    raise ValueError(
        f"Unsupported document format: {extension}"
    )