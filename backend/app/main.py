from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings
from .conversion import pdf_to_csv, image_to_pdf, office_to_pdf
from .smart_export import smart_export

app = FastAPI(title="FilexFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_BASE, "http://localhost:3000", "https://filexflow.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Kinds = { 'pdf2docx','pdf2xlsx','pdf2csv','pdf2pptx','pdf2html','pdf2jpg','jpg2pdf','docx2pdf','xlsx2pdf','pptx2pdf','html2pdf' }

def ext_for(kind: str) -> str:
    return { 'pdf2docx':'docx','pdf2xlsx':'xlsx','pdf2csv':'csv','pdf2pptx':'pptx','pdf2html':'html','pdf2jpg':'zip','jpg2pdf':'pdf','docx2pdf':'pdf','xlsx2pdf':'pdf','pptx2pdf':'pdf','html2pdf':'pdf' }[kind]

@app.get("/health", response_class=PlainTextResponse)
def health(): return "ok"

@app.post("/convert")
async def convert_ep(file: UploadFile, kind: str = Form("pdf2docx")):
    if kind not in Kinds: raise HTTPException(400, "kind not supported")
    data = await file.read()
    try:
        if kind.startswith('pdf2'):
            if kind == 'pdf2csv':
                out_bytes = pdf_to_csv(data); mime = 'text/csv'
            else:
                target = ext_for(kind)
                out_bytes = smart_export(data, target)
                mime = (
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if target=="docx" else
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if target=="xlsx" else
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation" if target=="pptx" else
                    "text/html" if target=="html" else
                    "application/zip"
                )
        else:
            if kind == 'jpg2pdf': out_bytes = image_to_pdf(data)
            elif kind == 'docx2pdf': out_bytes = office_to_pdf(data, 'docx')
            elif kind == 'xlsx2pdf': out_bytes = office_to_pdf(data, 'xlsx')
            elif kind == 'pptx2pdf': out_bytes = office_to_pdf(data, 'pptx')
            elif kind == 'html2pdf': out_bytes = office_to_pdf(data, 'html')
            else: raise HTTPException(400, 'kind not supported')
            mime = 'application/pdf'
    except Exception as e:
        raise HTTPException(400, f"conversion_error: {e}")
    return StreamingResponse(iter([out_bytes]), media_type=mime, headers={ 'Content-Disposition': f'attachment; filename=output.{ext_for(kind)}' })
