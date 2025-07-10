# app/pdf_utils.py

from PyPDF2 import PdfReader
from langchain.docstore.document import Document

def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return [Document(page_content=text)]
