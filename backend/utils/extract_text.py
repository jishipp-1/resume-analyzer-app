import io
from PyPDF2 import PdfReader
import docx

async def extract_text_from_upload(upload_file):
    contents = await upload_file.read()
    filename = (upload_file.filename or "").lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf_bytes(contents)
    elif filename.endswith(".docx") or filename.endswith(".doc"):
        return extract_text_from_docx_bytes(contents)
    else:
        try:
            return contents.decode("utf-8", errors="ignore")
        except Exception:
            return ""

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    text = ""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        for p in reader.pages:
            text += p.extract_text() or ""
    except Exception:
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except:
            return ""
    return text

def extract_text_from_docx_bytes(file_bytes: bytes) -> str:
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except:
            return ""
    return text
