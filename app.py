from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from pydantic import BaseModel
import fitz  # PyMuPDF
from fastapi.middleware.cors import CORSMiddleware
from embeddings import result, create_chunks
import tempfile

app = FastAPI()

def get_temp_dir():
    # Create a temporary directory and return its path
    return tempfile.TemporaryDirectory()


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
    start_page: int
    end_page: int

import tempfile
from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI()

FILE_PATH =  ""

@app.post("/uploadfile/")
async def upload_file(file: UploadFile, temp_dir: tempfile.TemporaryDirectory = Depends(get_temp_dir)):
    try:
        global FILE_PATH
        # The 'temp_dir' parameter is automatically injected by FastAPI's Dependency Injection
        file_path = f"temp/{file.filename}"
        FILE_PATH = file_path

        # Save the uploaded file to the temporary directory
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return {"filename": file.filename, "message": "File uploaded successfully", "file_path": file_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-text/")
async def extract_text_from_pdf(pdf_info: PdfExtractionRequest):
    try:
        pdf_document = fitz.open(FILE_PATH)
        text = ""
        for page_num in range(pdf_info.start_page - 1, pdf_info.end_page):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        response = create_chunks(text)
        if response:
            return {"message": "Chunks Created Successfully"}
        else:
            return {"message": "Error in creating chunks"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/")
async def receive_query(query: str):
    res = ''
    response = result(query)
    docs = response["documents"]
    for sublist in docs:
        for string in sublist:
            res += string
    return {"response": res}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
