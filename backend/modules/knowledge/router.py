from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from modules.auth.service import get_current_user
from modules.knowledge import schemas, service
from modules.profile.user_model import User

router = APIRouter()


@router.post("/text", response_model=schemas.KnowledgeBaseOut)
def upload_text(
    payload: schemas.TextSourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.add_text_source(db, current_user.organization_id, payload.content)


@router.post("/url", response_model=schemas.KnowledgeBaseOut)
def upload_url(
    payload: schemas.UrlSourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.add_url_source(db, current_user.organization_id, payload.url)


@router.post("/pdf", response_model=schemas.KnowledgeBaseOut)
def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.add_pdf_source(db, current_user.organization_id, file)


@router.get("/", response_model=List[schemas.KnowledgeBaseOut])
def list_knowledge(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_organization_knowledge(db, current_user.organization_id)



    
    
# ============================================================
# Delete Knowledge Source
# ============================================================


@router.delete("/{knowledge_base_id}")
def delete_knowledge(
    knowledge_base_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return service.delete_knowledge_source(
        db,
        knowledge_base_id,
        current_user.organization_id
    )    