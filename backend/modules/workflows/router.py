from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from modules.auth.service import get_current_user
from modules.workflows import schemas, service
from modules.profile.user_model import User

router = APIRouter()


@router.post("/meetings", response_model=schemas.MeetingResponse)
def book_meeting(
    payload: schemas.MeetingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.book_meeting(db, current_user.organization_id, payload)