from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import fitz  # PyMuPDF
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",  # Add the frontend URL(s) from which requests are allowed
    "http://localhost:8080",  # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PdfExtractionRequest(BaseModel):
    pdf_path: str
    start_page: int
    end_page: int

@app.post("/extract-text/")
async def extract_text_from_pdf(pdf_info: PdfExtractionRequest):
    try:
        pdf_document = fitz.open(pdf_info.pdf_path)
        text = ""
        for page_num in range(pdf_info.start_page - 1, pdf_info.end_page):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    try:
        # Save the uploaded file to a specified location (e.g., 'uploads/')
        with open(f"uploads/{file.filename}", "wb") as f:
            f.write(file.file.read())
        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
