from .conversion import pdf_to_docx, pdf_to_xlsx, pdf_to_html, pdf_to_pptx, pdf_to_jpg_zip
def smart_export(pdf_bytes: bytes, target: str) -> bytes:
    if target == "docx": return pdf_to_docx(pdf_bytes)
    if target == "xlsx": return pdf_to_xlsx(pdf_bytes)
    if target == "html": return pdf_to_html(pdf_bytes)
    if target == "pptx": return pdf_to_pptx(pdf_bytes)
    if target == "jpg":  return pdf_to_jpg_zip(pdf_bytes)
    raise ValueError("Unsupported target")
