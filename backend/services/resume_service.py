import pdfplumber
import re


def extract_text_from_pdf(file_stream):

    text = ""

    # FIX: use .file for UploadFile
    if hasattr(file_stream, "file"):
        file_stream = file_stream.file

    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    # ---------- CLEANING ----------

    # Add space before capital letters (LeadSoftwareEngineer → Lead Software Engineer)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # Fix missing spaces around brackets
    text = re.sub(r"\(", " ( ", text)
    text = re.sub(r"\)", " ) ", text)

    # Replace special characters with space
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()