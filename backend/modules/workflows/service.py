import smtplib
from email.mime.text import MIMEText
from datetime import timedelta, datetime, time as dtime
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from core.config import settings
from modules.leads.models import Lead
from modules.profile.user_model import User, UserRole, UserStatus

SCOPES = ["https://www.googleapis.com/auth/calendar"]
BUSINESS_START_HOUR = 9
BUSINESS_END_HOUR = 17
SLOT_STEP_MINUTES = 30
MAX_SEARCH_DAYS = 3



def _get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CALENDAR_CREDENTIALS_FILE, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)


def _get_active_department_employees(db: Session, organization_id, department: str):
    if department not in ("Sales", "Finance", "Support"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid department")

    return (
        db.query(User)
        .filter(
            User.organization_id == organization_id,
            User.role == UserRole(department),
            User.status == UserStatus.Active,
        )
        .all()
    )


def _is_slot_free(calendar_service, employee_email: str, start: datetime, end: datetime) -> bool:
    body = {
        "timeMin": start.isoformat() + "Z",
        "timeMax": end.isoformat() + "Z",
        "items": [{"id": employee_email}],
    }
    try:
        result = calendar_service.freebusy().query(body=body).execute()
        busy_slots = result["calendars"].get(employee_email, {}).get("busy", [])
        return len(busy_slots) == 0
    except Exception:
        return False


def find_available_employee_and_slot(db: Session, organization_id, department: str, preferred_start: datetime, duration_minutes: int):
    employees = _get_active_department_employees(db, organization_id, department)
    if not employees:
        return None, None

    calendar_service = _get_calendar_service()

    search_start = preferred_start
    for day_offset in range(MAX_SEARCH_DAYS):
        day = (search_start + timedelta(days=day_offset)).date()
        start_hour = search_start.hour if day_offset == 0 else BUSINESS_START_HOUR
        slot = datetime.combine(day, dtime(hour=max(start_hour, BUSINESS_START_HOUR)))

        while slot.hour < BUSINESS_END_HOUR:
            slot_end = slot + timedelta(minutes=duration_minutes)
            for employee in employees:
                if _is_slot_free(calendar_service, employee.email, slot, slot_end):
                    return employee, slot
            slot += timedelta(minutes=SLOT_STEP_MINUTES)

    return None, None


def _create_calendar_event(employee: User, lead: Lead, scheduled_time, duration_minutes: int, notes: str) -> str:
    calendar_service = _get_calendar_service()
    end_time = scheduled_time + timedelta(minutes=duration_minutes)

    event = {
        "summary": f"Meeting: {lead.visitor_name or lead.visitor_email} with {employee.first_name} ({employee.role.value})",
        "description": notes,
        "start": {"dateTime": scheduled_time.isoformat(), "timeZone": "Asia/Karachi"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Karachi"},
        # Note: 'attendees' aur 'sendUpdates' hata diya — Service Accounts
        # bina Google Workspace Domain-Wide Delegation ke attendees invite nahi kar sakte.
        # Notification Gmail SMTP se separately jati hai (_send_email function).
    }

    try:
        created_event = calendar_service.events().insert(
            calendarId=employee.email, body=event
        ).execute()
    except Exception as e:
        print(f"[DEBUG] Calendar event FAIL hua. Exact error: {repr(e)}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Calendar event create nahi ho saka: {e}")

    return created_event.get("htmlLink", "")


def _send_email(to_email: str, subject: str, body: str) -> bool:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.GMAIL_SMTP_EMAIL
    msg["To"] = to_email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.GMAIL_SMTP_EMAIL, settings.GMAIL_SMTP_APP_PASSWORD)
            server.sendmail(settings.GMAIL_SMTP_EMAIL, to_email, msg.as_string())
        return True
    except Exception:
        return False


def _execute_booking(db: Session, lead: Lead, employee: User, scheduled_time: datetime, duration_minutes: int = 30, notes: str = ""):
    event_link = _create_calendar_event(employee, lead, scheduled_time, duration_minutes, notes)

    time_str = scheduled_time.strftime("%d %b %Y, %I:%M %p")
    email_sent = False
    if lead.visitor_email:
        email_sent = _send_email(
            lead.visitor_email, "Meeting Confirmed",
            f"Hi {lead.visitor_name or 'there'},\n\nYour meeting with our {employee.role.value} team "
            f"({employee.first_name}) is scheduled for {time_str}.\nCalendar link: {event_link}\n\nThanks,\nEngageAI",
        )
    _send_email(
        employee.email, "New Meeting Booked",
        f"Hi {employee.first_name},\n\nA new meeting has been booked with a customer "
        f"({lead.visitor_name or lead.visitor_email}) for {time_str}.\nCalendar link: {event_link}",
    )

    lead.status = "Contacted"
    db.commit()
    db.refresh(lead)

    return event_link, email_sent


def book_meeting(db: Session, organization_id, data):
    lead = db.query(Lead).filter(Lead.id == data.lead_id, Lead.organization_id == organization_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    employee, slot = find_available_employee_and_slot(db, organization_id, data.department, data.preferred_time, data.duration_minutes)
    if not employee:
        return {
            "lead_id": lead.id, "assigned_employee_email": None, "scheduled_time": None,
            "calendar_event_link": None, "email_sent": False, "lead_status": lead.status,
            "message": f"Agle {MAX_SEARCH_DAYS} din mein {data.department} team ka koi slot free nahi mila.",
        }

    event_link, email_sent = _execute_booking(db, lead, employee, slot, data.duration_minutes, data.notes)
    return {
        "lead_id": lead.id, "assigned_employee_email": employee.email, "scheduled_time": slot,
        "calendar_event_link": event_link, "email_sent": email_sent, "lead_status": lead.status,
        "message": "Meeting booked successfully.",
    }