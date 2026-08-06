"""
frontend/utils/api_client.py

Streamlit frontend API client.
Uses Render backend URL from Streamlit secrets.
"""

import requests
import streamlit as st


BASE_URL = st.secrets.get(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)


def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}



# ---------------- AUTH + PROFILE ----------------

def register_organization_and_owner(payload: dict):
    """
    Backend endpoint:
    POST /register
    """

    res = requests.post(
        f"{BASE_URL}/register",
        json=payload
    )

    res.raise_for_status()

    return res.json()



def login(email: str, password: str):
    """
    Backend endpoint:
    POST /login
    """

    res = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": email,
            "password": password
        }
    )

    res.raise_for_status()

    return res.json()



def get_organization_profile():

    res = requests.get(
        f"{BASE_URL}/profile/organization",
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



# ---------------- ADMIN ----------------


def get_organization_users():

    res = requests.get(
        f"{BASE_URL}/admin/users",
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def toggle_user_status(user_id: str, new_status: str):

    res = requests.patch(
        f"{BASE_URL}/admin/users/{user_id}/status",
        json={
            "status": new_status
        },
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def create_employee(payload: dict):

    res = requests.post(
        f"{BASE_URL}/admin/employees",
        json=payload,
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



# ---------------- DASHBOARD ----------------


def get_dashboard_summary():

    res = requests.get(
        f"{BASE_URL}/summary",
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def get_leads_over_time(days: int = 30):

    res = requests.get(
        f"{BASE_URL}/leads-over-time",
        params={
            "days": days
        },
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



# ---------------- KNOWLEDGE ----------------


def upload_knowledge_text(content: str):

    res = requests.post(
        f"{BASE_URL}/text",
        json={
            "content": content
        },
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def upload_knowledge_url(url: str):

    res = requests.post(
        f"{BASE_URL}/url",
        json={
            "url": url
        },
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def upload_knowledge_pdf(file):

    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf"
        )
    }

    res = requests.post(
        f"{BASE_URL}/pdf",
        files=files,
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def list_knowledge():

    res = requests.get(
        f"{BASE_URL}/",
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



# ---------------- PROFILE ----------------


def update_organization_profile(payload: dict):

    res = requests.put(
        f"{BASE_URL}/profile/organization",
        json=payload,
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def get_my_user_profile():

    res = requests.get(
        f"{BASE_URL}/profile/user",
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def update_my_user_profile(payload: dict):

    res = requests.put(
        f"{BASE_URL}/profile/user",
        json=payload,
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



# ---------------- ONBOARDING ----------------


def complete_onboarding():

    res = requests.post(
        f"{BASE_URL}/profile/organization/complete-onboarding",
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



# ---------------- REPRESENTATIVES ----------------


def create_representative(payload: dict):

    res = requests.post(
        f"{BASE_URL}/representatives",
        json=payload,
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()



def list_representatives():

    res = requests.get(
        f"{BASE_URL}/representatives",
        headers=_headers()
    )

    res.raise_for_status()

    return res.json()