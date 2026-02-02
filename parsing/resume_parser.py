import io
import re
import fitz  # PyMuPDF
import pdfplumber
from docx import Document


def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def _extract_pdf_pymupdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def _extract_pdf_pdfplumber(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def _extract_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_resume_text(file) -> str:
    file_bytes = file.read()
    try:
        filename = file.name.lower()
    except AttributeError:
        # Fallback for dummy objects in testing, if any
        if hasattr(file, "name"):
             filename = file.name.lower()
        else:
            raise ValueError("File object missing name attribute")

    if filename.endswith(".pdf"):
        text = _extract_pdf_pymupdf(file_bytes)
        if len(text.strip()) < 200:
            text = _extract_pdf_pdfplumber(file_bytes)

    elif filename.endswith(".docx"):
        text = _extract_docx(file_bytes)

    else:
        raise ValueError("Unsupported file type")

    return _clean_text(text)

if __name__ == "__main__":
    # Basic sanity check
    try:
        with open("sample_resume.pdf", "rb") as f:
            class Dummy:
                name = "sample_resume.pdf"
                def read(self): return f.read()

            text = extract_resume_text(Dummy())
            print("--- Extracted Text Preview ---")
            print(text[:1000])
            print("--- End Preview ---")
    except FileNotFoundError:
        print("sample_resume.pdf not found. Skipping local test.")
