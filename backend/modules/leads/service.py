from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from modules.leads.models import Lead


VALID_STATUSES = ("New", "Contacted", "Qualified", "Lost")



def get_organization_leads(db: Session, organization_id):
    return (
        db.query(Lead)
        .filter(Lead.organization_id == organization_id)
        .order_by(Lead.created_at.desc())
        .all()
    )


def update_lead_status(db: Session, organization_id, lead_id, new_status: str):
    if new_status not in VALID_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status value")

    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.organization_id == organization_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    lead.status = new_status
    db.commit()
    db.refresh(lead)
    return lead