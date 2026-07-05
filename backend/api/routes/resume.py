import uuid
import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.resume_chunker import resume_chunker
from backend.services.file_parser_service import (
    extract_text_from_pdf,
    extract_text_from_docx
)
from backend.services.resume_service import analyze_resume_text

from backend.services.embedding_service import embedding_service
from backend.services.vector_store_instance import vector_store
from backend.services.bm25_service import BM25Service
from backend.services.bm25_global import bm25_global

router = APIRouter()


@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        # ----------------------------
        # 1. Extract resume text
        # ----------------------------
        if suffix.lower() == ".pdf":
            resume_text = extract_text_from_pdf(temp_path)

        elif suffix.lower() == ".docx":
            resume_text = extract_text_from_docx(temp_path)

        else:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX supported"
            )

        # ----------------------------
        # 2. LLM resume analysis
        # ----------------------------
        result = analyze_resume_text(
            name="Unknown",
            email="Unknown",
            resume_text=resume_text
        )

        # ----------------------------
        # 3. Chunk resume
        # ----------------------------
        chunks = resume_chunker.chunk_resume(resume_text)
        print("\n[UPLOAD DEBUG] chunks received:", len(chunks)) # debug

        if not chunks:
            raise HTTPException(
                status_code=500,
                detail="Chunking failed: no chunks generated"
            )

        candidate_id = str(uuid.uuid4())

        # ----------------------------
        # 4. Initialize BM25 (per upload for now)
        # ----------------------------
        bm25_service = BM25Service()

        # ----------------------------
        # 5. Index FAISS + attach metadata
        # ----------------------------
        for chunk in chunks:
            print("[UPLOAD DEBUG] indexing section:", chunk["section"]) # debug

            chunk["metadata"].update({
                "candidate_id": candidate_id,
                "candidate_name": "Unknown",
                "email": "Unknown",
                "filename": file.filename
            })

            embedding = embedding_service.get_embedding(chunk["text"])

            vector_store.add(embedding, chunk)

        # ----------------------------
        # 6. Build BM25 index (BATCH)
        # ----------------------------
        bm25_global.index_candidate(candidate_id, chunks)

        # ----------------------------
        # 7. Response
        # ----------------------------
        return {
            "analysis": result,
            "candidate_id": candidate_id,
            "chunks_stored": len(chunks),
            "message": "Resume uploaded and indexed successfully"
        }

    finally:
        os.remove(temp_path)