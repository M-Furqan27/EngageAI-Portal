"""
backend/modules/profile/router.py

REPLACE the existing file. Ek naya endpoint add hua:
POST /profile/organization/complete-onboarding
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from modules.auth.service import get_current_user
from modules.profile import schemas, service
from modules.profile.user_model import User

router = APIRouter()


@router.get("/organization", response_model=schemas.OrganizationOut)
def get_my_organization(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_organization_by_id(db, current_user.organization_id)


@router.put("/organization", response_model=schemas.OrganizationOut)
def update_my_organization(
    payload: schemas.OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.update_organization(db, current_user.organization_id, payload)


@router.post("/organization/complete-onboarding", response_model=schemas.OrganizationOut)
def complete_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Onboarding wizard complete karne pe frontend ye call karta hai."""
    return service.complete_onboarding(db, current_user.organization_id)


@router.get("/user", response_model=schemas.UserProfileOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/user", response_model=schemas.UserProfileOut)
def update_my_profile(
    payload: schemas.UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.update_user_profile(db, current_user, payload)