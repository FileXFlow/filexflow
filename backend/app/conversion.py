import subprocess, tempfile, os, io, csv, pdfplumber, fitz, img2pdf
from openpyxl import Workbook
LIBREOFFICE_BIN = os.environ.get("LIBREOFFICE_BIN", "soffice")
def pdf_to_docx(pdf_bytes: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp, "in.pdf"); out_dir = tmp
        open(in_path,"wb").write(pdf_bytes)
        subprocess.check_call([LIBREOFFICE_BIN,"--headless","--convert-to","docx",in_path,"--outdir",out_dir])
        return open(os.path.join(out_dir,"in.docx"),"rb").read()
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
    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp,"in.pdf"); open(in_path,"wb").write(pdf_bytes)
        subprocess.check_call([LIBREOFFICE_BIN,"--headless","--convert-to","html",in_path,"--outdir",tmp])
        return open(os.path.join(tmp,"in.html"),"rb").read()
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
