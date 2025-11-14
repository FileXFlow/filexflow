from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from .smart_export import smart_export
from .conversion import office_to_pdf, image_to_pdf
from .settings import settings
import os

# ---------------------- APP ----------------------

app = FastAPI(title="FileXFlow API")


# ---------------------- CORS ----------------------

# Permitir Vercel frontend + localhost
origins = [
    "*",  # Si quieres restringir luego, reemplaza este "*" por tu dominio
    "http://localhost:3000",
    "https://filexflow.vercel.app",
    "https://*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------- HELLO / HEALTH ----------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------- DETECTOR DE MIME ----------------------

def ext_for(target: str) -> str:
    return {
        "docx": "docx",
        "xlsx": "xlsx",
        "csv": "csv",
        "html": "html",
        "pptx": "pptx",
        "jpg": "zip",
        "pdf": "pdf"
    }.get(target, "bin")


def mime_for(target: str) -> str:
    return {
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "csv":  "text/csv",
        "html": "text/html",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "jpg":  "application/zip",
        "pdf":  "application/pdf",
    }.get(target, "application/octet-stream")


# ---------------------- RUTA PRINCIPAL DE CONVERSIÓN ----------------------

@app.post("/convert")
async def convert_ep(
    file: UploadFile,
    kind: str = Form(...)
):
    """
    kind puede ser:

    * pdf2docx
    * pdf2xlsx
    * pdf2csv
    * pdf2html
    * pdf2pptx
    * pdf2jpg

    * jpg2pdf
    * docx2pdf
    * xlsx2pdf
    * pptx2pdf
    * html2pdf
    """

    try:
        file_bytes = await file.read()

        # ----------------------------------------------
        # PDF → otros formatos
        # ----------------------------------------------
        if kind.startswith("pdf2"):
            target = kind.replace("pdf2", "")
            out_bytes = smart_export(file_bytes, target)
            return StreamingResponse(
                iter([out_bytes]),
                media_type=mime_for(target),
                headers={
                    "Content-Disposition": f"attachment; filename=output.{ext_for(target)}"
                }
            )

        # ----------------------------------------------
        # JPG → PDF
        # ----------------------------------------------
        if kind == "jpg2pdf":
            out_bytes = image_to_pdf(file_bytes)
            return StreamingResponse(
                iter([out_bytes]),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=output.pdf"}
            )

        # ----------------------------------------------
        # Office / HTML → PDF (LibreOffice)
        # ----------------------------------------------
        if kind in ("docx2pdf", "xlsx2pdf", "pptx2pdf", "html2pdf"):
            ext = kind.replace("2pdf", "")
            out_bytes = office_to_pdf(file_bytes, ext)
            return StreamingResponse(
                iter([out_bytes]),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=output.pdf"}
            )

        raise HTTPException(400, f"Unsupported conversion kind: {kind}")

    except Exception as e:
        raise HTTPException(400, detail=f"conversion_error: {e}")
