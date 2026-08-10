from pathlib import Path


def parse_text(file_path: str | Path) -> list[dict]:
    text = Path(file_path).read_text(
        encoding="utf-8",
        errors="replace",
    )

    return [
        {
            "page": 1,
            "text": text,
        }
    ]