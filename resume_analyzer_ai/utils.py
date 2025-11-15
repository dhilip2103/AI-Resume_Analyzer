import pdfplumber
from docx import Document

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    text = ""
    doc = Document(docx_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip()

def extract_resume_text(file_path, file_extension):
    """Detects file type and extracts text accordingly."""
    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return None
