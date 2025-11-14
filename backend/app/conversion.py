import subprocess, tempfile, os, io, csv, pdfplumber, fitz, img2pdf, html
from openpyxl import Workbook
from docx import Document
LIBREOFFICE_BIN = os.environ.get("LIBREOFFICE_BIN", "soffice")
def pdf_to_docx(pdf_bytes: bytes) -> bytes:
    """
    Convierte un PDF en un DOCX simple, solo texto (sin formato avanzado),
    usando pdfplumber + python-docx. No depende de LibreOffice.
    """
    doc = Document()
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        num_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                for line in text.splitlines():
                    doc.add_paragraph(line)
            else:
                # Página sin texto (por ejemplo, escaneada)
                doc.add_paragraph("[Page without extractable text]")
            if i != num_pages:
                doc.add_page_break()

    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()
def pdf_to_csv(pdf_bytes: bytes) -> bytes:
    output = io.StringIO(newline=""); import csv as _csv; writer = _csv.writer(output)
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines(): writer.writerow([line])
    return output.getvalue().encode("utf-8")
def pdf_to_xlsx(pdf_bytes: bytes) -> bytes:
    wb = Workbook(); ws = wb.active; ws.title = "PDF"
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        r = 1
        for i, page in enumerate(pdf.pages, start=1):
            ws.cell(r,1,f"Page {i}"); r+=1
            text = page.extract_text() or ""
            for line in text.splitlines(): ws.cell(r,1,line); r+=1
            r+=1
    bio = io.BytesIO(); wb.save(bio); return bio.getvalue()
def pdf_to_html(pdf_bytes: bytes) -> bytes:
    """
    Convierte PDF a un HTML muy simple: título de página + texto en <pre>.
    No usa LibreOffice, solo pdfplumber.
    """
    parts: list[str] = ["<html><body>"]
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            parts.append(f"<h2>Page {i}</h2>")
            parts.append("<pre>")
            parts.append(html.escape(text))
            parts.append("</pre>")
    parts.append("</body></html>")
    return "\n".join(parts).encode("utf-8")
def pdf_to_pptx(pdf_bytes: bytes) -> bytes:
    from pptx import Presentation; from pptx.util import Inches
    prs = Presentation(); blank = prs.slide_layouts[6]
    doc = fitz.open(stream=pdf_bytes, filetype="pdf"); import tempfile, os, io as _io
    for page in doc:
        slide = prs.slides.add_slide(blank)
        pix = page.get_pixmap(dpi=150); img_bytes = pix.tobytes("png")
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tf:
            tf.write(img_bytes); tmp = tf.name
        slide.shapes.add_picture(tmp, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)
        os.unlink(tmp)
    bio = _io.BytesIO(); prs.save(bio); return bio.getvalue()
def pdf_to_jpg_zip(pdf_bytes: bytes) -> bytes:
    import zipfile
    zbio = io.BytesIO(); doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    with zipfile.ZipFile(zbio,"w",zipfile.ZIP_DEFLATED) as zf:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=150); jpg = pix.tobytes("jpg")
            zf.writestr(f"page-{i}.jpg", jpg)
    return zbio.getvalue()
def image_to_pdf(jpg_bytes: bytes) -> bytes: return img2pdf.convert(jpg_bytes)
def office_to_pdf(file_bytes: bytes, ext: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp,f"in.{ext}"); open(in_path,"wb").write(file_bytes)
        subprocess.check_call([LIBREOFFICE_BIN,"--headless","--convert-to","pdf",in_path,"--outdir",tmp])
        return open(os.path.join(tmp,"in.pdf"),"rb").read()
