from pathlib import Path
import fitz
import hashlib

def extract_pdf(path: str):
    pages = []
    doc = fitz.open(path)
    for idx, page in enumerate(doc, start=1):
        text = page.get_text("text")
        pages.append({"page_number": idx, "text": text or ""})
    return pages

def file_hash(path: str):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
