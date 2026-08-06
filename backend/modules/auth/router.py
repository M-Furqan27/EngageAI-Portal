from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from modules.auth import schemas, service

router = APIRouter()


@router.post("/register", response_model=schemas.RegisterResponse)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    token, owner = service.register_organization_and_owner(db, payload)
    return {"token": token, "user": owner}


@router.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    token, user = service.authenticate_user(db, payload.email, payload.password)
    return {"token": token, "user": user}