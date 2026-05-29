from fastapi import APIRouter, UploadFile, File
from app.services.ingestion_service import ingest_document

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Create file path
    file_path = f"data/{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Ingest uploaded PDF
    ingest_document(file_path, file.filename)

    return {
        "message": f"{file.filename} uploaded and processed successfully"
    }