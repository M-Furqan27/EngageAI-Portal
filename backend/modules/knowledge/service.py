import os
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from modules.knowledge.models import KnowledgeBase, SourceType, ProcessingStatus

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================
# Knowledge upload (PostgreSQL)
# ============================================================

def add_text_source(db: Session, organization_id, content: str):
    kb = KnowledgeBase(
        organization_id=organization_id,
        source_type=SourceType.Text,
        source_path=content,
        processing_status=ProcessingStatus.Completed,
    )

    db.add(kb)
    db.commit()
    db.refresh(kb)
    return kb


def add_url_source(db: Session, organization_id, url: str):
    kb = KnowledgeBase(
        organization_id=organization_id,
        source_type=SourceType.URL,
        source_path=url,
        processing_status=ProcessingStatus.Completed,
    )

    db.add(kb)
    db.commit()
    db.refresh(kb)
    return kb


def add_pdf_source(db: Session, organization_id, file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    safe_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    kb = KnowledgeBase(
        organization_id=organization_id,
        source_type=SourceType.PDF,
        source_path=file_path,
        processing_status=ProcessingStatus.Completed,
    )

    db.add(kb)
    db.commit()
    db.refresh(kb)
    return kb



def get_organization_knowledge(db: Session, organization_id):
    return (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.organization_id == organization_id)
        .order_by(KnowledgeBase.created_at.desc())
        .all()
    )