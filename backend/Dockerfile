FROM python:3.11-slim
RUN apt-get update && apt-get install -y libreoffice && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY app /app/app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir fastapi uvicorn[standard] python-multipart pydantic-settings pdfplumber openpyxl img2pdf pymupdf python-pptx
ENV PORT=8000 HOST=0.0.0.0
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]