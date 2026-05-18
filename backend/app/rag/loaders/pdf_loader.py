from io import BytesIO

from pypdf import PdfReader


def load_pdf_text(content: bytes, _filename: str) -> str:
    reader = PdfReader(BytesIO(content))
    texts: list[str] = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts).strip()
