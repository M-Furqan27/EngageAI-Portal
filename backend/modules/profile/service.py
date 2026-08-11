"""
backend/modules/profile/service.py

REPLACE the existing file. Ek naya function add hua: complete_onboarding.
"""
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from modules.profile.organization_model import Organization
from modules.profile.user_model import User
import requests


def get_organization_by_id(db: Session, organization_id):
    org = db.query(Organization).filter(Organization.organization_id == organization_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org


def update_organization(db: Session, organization_id, data):
    org = get_organization_by_id(db, organization_id)
    updates = data.dict(exclude_unset=True)
    for field, value in updates.items():
        setattr(org, field, value)
    db.commit()
    db.refresh(org)
    return org


import os

def complete_onboarding(db, organization_id):
    org = get_organization_by_id(db, organization_id)

    org.onboarding_completed = True

    db.commit()
    db.refresh(org)

    requests.post(
    f"{os.getenv('AGENT_BACKEND_URL')}/pipeline/setup",
        json={
            "organization_id": str(organization_id)
        }
    )

    return org


def update_user_profile(db: Session, user: User, data):
    updates = data.dict(exclude_unset=True)
    for field, value in updates.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user