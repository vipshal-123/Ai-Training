import fitz
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return text


def parse_date_safe(date_str: str):
    
    for suffix in ["st", "nd", "rd", "th"]:
        date_str = date_str.replace(suffix, "")
    try:
        return datetime.strptime(date_str.strip(), "%d %B %Y").date()
    except ValueError:
        return None