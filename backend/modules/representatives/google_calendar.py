from uuid import UUID


from fastapi import HTTPException


from google_auth_oauthlib.flow import Flow


from google.oauth2.credentials import Credentials


from googleapiclient.discovery import build


from core.config import settings


from core.security import decrypt_token

from datetime import datetime, timedelta




GOOGLE_SCOPES = [

    "https://www.googleapis.com/auth/calendar",

]







def create_google_flow(
    state: str | None = None,
) -> Flow:


    client_config = {

        "web": {

            "client_id":
                settings.google_client_id,


            "client_secret":
                settings.google_client_secret,


            "auth_uri":
                "https://accounts.google.com/o/oauth2/auth",


            "token_uri":
                "https://oauth2.googleapis.com/token",


            "redirect_uris": [

                settings.google_redirect_uri,

            ],

        }

    }



    flow = Flow.from_client_config(

        client_config=client_config,

        scopes=GOOGLE_SCOPES,

        state=state,

        autogenerate_code_verifier=False,

    )



    flow.redirect_uri = (
        settings.google_redirect_uri
    )



    return flow








def get_representative_or_404(
    db,
    representative_id: UUID,
):

    from modules.representatives.models import Representative



    representative = db.get(

        Representative,

        representative_id,

    )


    if not representative:

        raise HTTPException(

            status_code=404,

            detail="Representative not found.",

        )


    return representative







def verify_google_calendar_access(
    connection,
):


    if not connection.encrypted_refresh_token:

        raise Exception(
            "Refresh token missing"
        )



    credentials = Credentials(

        token=decrypt_token(

            connection.encrypted_access_token

        ),


        refresh_token=decrypt_token(

            connection.encrypted_refresh_token

        ),


        token_uri=(

            "https://oauth2.googleapis.com/token"

        ),


        client_id=
            settings.google_client_id,


        client_secret=
            settings.google_client_secret,


    )



    service = build(

        "calendar",

        "v3",

        credentials=credentials,

    )



    service.calendarList().list(

        maxResults=1

    ).execute()



    return True


def get_calendar_service(connection):
    if not connection.encrypted_refresh_token:
        raise HTTPException(
            status_code=400,
            detail="Representative calendar is not connected.",
        )

    credentials = Credentials(
        token=(
            decrypt_token(connection.encrypted_access_token)
            if connection.encrypted_access_token
            else None
        ),
        refresh_token=decrypt_token(
            connection.encrypted_refresh_token
        ),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
    )

    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )


def get_available_slots(
    connection,
    time_min: datetime,
    time_max: datetime,
    duration_minutes: int = 30,
    offset: int = 0,
    limit: int = 3,
):
    service = get_calendar_service(connection)

    response = service.freebusy().query(
        body={
            "timeMin": time_min.isoformat(),
            "timeMax": time_max.isoformat(),
            "items": [
                {
                    "id": connection.google_calendar_id,
                }
            ],
        }
    ).execute()

    calendar_data = response["calendars"].get(
        connection.google_calendar_id,
        {},
    )

    busy_periods = calendar_data.get("busy", [])

    duration = timedelta(minutes=duration_minutes)

    free_slots = []
    current = time_min

    for busy in busy_periods:
        busy_start = datetime.fromisoformat(
            busy["start"].replace("Z", "+00:00")
        )

        busy_end = datetime.fromisoformat(
            busy["end"].replace("Z", "+00:00")
        )

        if busy_start > current:
            slot_start = current

            while slot_start + duration <= busy_start:
                slot_end = slot_start + duration

                free_slots.append(
                    {
                        "start": slot_start.isoformat(),
                        "end": slot_end.isoformat(),
                    }
                )

                slot_start = slot_end

        if busy_end > current:
            current = busy_end

    while current + duration <= time_max:
        slot_end = current + duration

        free_slots.append(
            {
                "start": current.isoformat(),
                "end": slot_end.isoformat(),
            }
        )

        current = slot_end

    selected_slots = free_slots[
        offset:offset + limit
    ]

    next_offset = offset + len(selected_slots)

    return {
        "busy_periods": busy_periods,
        "free_slots": selected_slots,
        "next_offset": next_offset,
        "has_more": next_offset < len(free_slots),
    }
    
    
def create_calendar_event(
    connection,
    summary: str,
    description: str,
    start_time: datetime,
    end_time: datetime,
    attendee_email: str | None = None,
):
    service = get_calendar_service(connection)

    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
        },
        "end": {
            "dateTime": end_time.isoformat(),
        },
    }

    if attendee_email:
        event["attendees"] = [
            {
                "email": attendee_email,
            }
        ]

    return service.events().insert(
        calendarId=connection.google_calendar_id,
        body=event,
        sendUpdates="all",
    ).execute()