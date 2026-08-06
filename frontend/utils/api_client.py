"""
frontend/utils/api_client.py

REPLACE the existing file. Neeche end mein 3 naye functions add hain:
complete_onboarding, create_representative, list_representatives.
Baaki sab EXACTLY same hai jo pehle se tha.
"""

import requests
import streamlit as st

BASE_URL = "http://localhost:8000"   # backend ka real URL/port yahan set karo


def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


# ---------------- AUTH + PROFILE ----------------

def register_organization_and_owner(payload: dict):
    res = requests.post(f"{BASE_URL}/auth/register", json=payload)
    res.raise_for_status()
    return res.json()


def login(email: str, password: str):
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    res.raise_for_status()
    return res.json()


def get_organization_profile():
    res = requests.get(f"{BASE_URL}/profile/organization", headers=_headers())
    res.raise_for_status()
    return res.json()


# ---------------- ADMIN (status toggle within own organization) ----------------

def get_organization_users():
    res = requests.get(f"{BASE_URL}/admin/users", headers=_headers())
    res.raise_for_status()
    return res.json()


def toggle_user_status(user_id: str, new_status: str):
    res = requests.patch(
        f"{BASE_URL}/admin/users/{user_id}/status",
        json={"status": new_status},
        headers=_headers(),
    )
    res.raise_for_status()
    return res.json()

def create_employee(payload: dict):
    """
    payload = {
        "first_name", "last_name", "email", "phone", "password", "role"
    }
    role: "Sales" / "Finance" / "Support"
    """
    res = requests.post(f"{BASE_URL}/admin/employees", json=payload, headers=_headers())
    res.raise_for_status()
    return res.json()

# ---------------- DASHBOARD ----------------

def get_dashboard_summary():
    res = requests.get(f"{BASE_URL}/dashboard/summary", headers=_headers())
    res.raise_for_status()
    return res.json()


def get_leads_over_time(days: int = 30):
    res = requests.get(f"{BASE_URL}/dashboard/leads-over-time", params={"days": days}, headers=_headers())
    res.raise_for_status()
    return res.json()

# ---------------- KNOWLEDGE ----------------

def upload_knowledge_text(content: str):
    res = requests.post(f"{BASE_URL}/knowledge/text", json={"content": content}, headers=_headers())
    res.raise_for_status()
    return res.json()


def upload_knowledge_url(url: str):
    res = requests.post(f"{BASE_URL}/knowledge/url", json={"url": url}, headers=_headers())
    res.raise_for_status()
    return res.json()


def upload_knowledge_pdf(file):
    files = {"file": (file.name, file.getvalue(), "application/pdf")}
    res = requests.post(f"{BASE_URL}/knowledge/pdf", files=files, headers=_headers())
    res.raise_for_status()
    return res.json()


def list_knowledge():
    res = requests.get(f"{BASE_URL}/knowledge/", headers=_headers())
    res.raise_for_status()
    return res.json()




# ---------------- PROFILE (updates) ----------------

def update_organization_profile(payload: dict):
    res = requests.put(f"{BASE_URL}/profile/organization", json=payload, headers=_headers())
    res.raise_for_status()
    return res.json()


def get_my_user_profile():
    res = requests.get(f"{BASE_URL}/profile/user", headers=_headers())
    res.raise_for_status()
    return res.json()


def update_my_user_profile(payload: dict):
    res = requests.put(f"{BASE_URL}/profile/user", json=payload, headers=_headers())
    res.raise_for_status()
    return res.json()



# ---------------- ONBOARDING ----------------

def complete_onboarding():
    """Onboarding wizard ke 'Finish Setup' button pe call hota hai."""
    res = requests.post(f"{BASE_URL}/profile/organization/complete-onboarding", headers=_headers())
    res.raise_for_status()
    return res.json()


# ---------------- REPRESENTATIVES ----------------

def create_representative(payload: dict):
    """
    payload = {
        "representative_name", "service", "service_description", "company_email"
    }
    """
    res = requests.post(f"{BASE_URL}/representatives/", json=payload, headers=_headers())
    res.raise_for_status()
    return res.json()


def list_representatives():
    res = requests.get(f"{BASE_URL}/representatives/", headers=_headers())
    res.raise_for_status()
    return res.json()