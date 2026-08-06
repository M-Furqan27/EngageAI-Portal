from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from modules.auth.service import get_current_user
from modules.dashboard import schemas, service
from modules.profile.user_model import User

router = APIRouter()


@router.get("/summary", response_model=schemas.DashboardSummary)
def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_summary(db, current_user.organization_id)


@router.get("/leads-over-time", response_model=schemas.LeadsOverTimeResponse)
def leads_over_time(
    days: int = Query(30, ge=1, le=90),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    points = service.get_leads_over_time(db, current_user.organization_id, days)
    return {"points": points}

