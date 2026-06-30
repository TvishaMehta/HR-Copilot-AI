from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.schemas.resume import ResumeRequest
from backend.services.resume_service import (
    analyze_resume,
    analyze_resume_text
)
from backend.services.file_parser_service import (
    extract_text_from_pdf,
    extract_text_from_docx
)

# ✅ NEW IMPORTS (FAISS integration)
from backend.services.embedding_service import embedding_service
from backend.services.vector_store_instance import vector_store

import tempfile
import os

router = APIRouter()

# -----------------------------
# JSON-based analysis endpoint
# -----------------------------
@router.post("/resume/analyze")
def resume_analyze(req: ResumeRequest):
    return analyze_resume(req)


# -----------------------------
# FILE UPLOAD + FAISS STORAGE
# -----------------------------
@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:

        # -------------------------
        # 1. Extract text
        # -------------------------
        if suffix.lower() == ".pdf":
            resume_text = extract_text_from_pdf(temp_path)

        elif suffix.lower() == ".docx":
            resume_text = extract_text_from_docx(temp_path)

        else:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX are supported"
            )

        # -------------------------
        # 2. AI analysis (existing)
        # -------------------------
        result = analyze_resume_text(
            name="Unknown",
            email="Unknown",
            resume_text=resume_text
        )

        # -------------------------
        # 3. FAISS INTEGRATION (NEW)
        # -------------------------
        embedding = embedding_service.get_embedding(resume_text)

        vector_store.add(
            embedding,
            {
                "resume_text": resume_text,
                "filename": file.filename
            }
        )

        # -------------------------
        # 4. Return response
        # -------------------------
        return {
            "analysis": result,
            "message": "Resume uploaded + stored in vector DB"
        }

    finally:
        os.remove(temp_path)