from pathlib import Path
from docx import Document
from pypdf import PdfReader


ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def validate_upload(filename: str, size: int, max_mb: int) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF, TXT, and DOCX files are supported.")
    if size > max_mb * 1024 * 1024:
        raise ValueError(f"File exceeds {max_mb} MB limit.")


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        doc = Document(str(path))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    raise ValueError("Unsupported file type.")
