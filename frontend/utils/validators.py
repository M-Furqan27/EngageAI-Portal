"""
frontend/utils/validators.py

Poori app ke liye ek hi jagah se validation rules — taake har form
(Login, Signup, Onboarding, Profile) mein exact same, professional
validation lage. Naya form banate waqt bas yahan se import karo.
"""

import re

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
URL_PATTERN = re.compile(
    r"^https?://[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9-]+)+(?:[/?#][^\s]*)?$"
)

# Country-specific phone rules. Naya country add karna ho to bas yahan
# entry add kar do — poori app mein khud-ba-khud lagu ho jayega.
PHONE_RULES = {
    "Pakistan": {"length": 11, "starts_with": "0", "example": "03001234567"},
    "India": {"length": 10, "starts_with": None, "example": "9876543210"},
    "United Arab Emirates": {"length": 9, "starts_with": "5", "example": "501234567"},
    "United States/Canada": {"length": 10, "starts_with": None, "example": "2025551234"},
    "United States": {"length": 10, "starts_with": None, "example": "2025551234"},
    "United Kingdom": {"length": 10, "starts_with": None, "example": "7911123456"},
    "Saudi Arabia": {"length": 9, "starts_with": "5", "example": "501234567"},
}

DEFAULT_PHONE_MIN = 7
DEFAULT_PHONE_MAX = 15


# ---------------------------------------------------------------------
# REQUIRED FIELD
# ---------------------------------------------------------------------
def is_required(value: str) -> bool:
    """Khali ya sirf-spaces wali value ko invalid maanta hai."""
    return bool(value and value.strip())


# ---------------------------------------------------------------------
# EMAIL
# ---------------------------------------------------------------------
def is_valid_email(email: str) -> bool:
    if not email or not email.strip():
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))


# ---------------------------------------------------------------------
# WEBSITE / URL
# ---------------------------------------------------------------------
def normalize_website(url: str) -> str:
    """Agar user https:// likhna bhool jaye to khud add kar deta hai."""
    url = (url or "").strip()
    if url and not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    return url


def is_valid_website(url: str) -> bool:
    if not url or not url.strip():
        return False
    return bool(URL_PATTERN.match(url.strip()))


# ---------------------------------------------------------------------
# PHONE — country diya ho to us country ki exact length/format check
# hoti hai (e.g. Pakistan = 11 digits, 0 se shuru). Country na diya ho
# to generic international range (7–15 digits) check hoti hai.
# ---------------------------------------------------------------------
def validate_phone(phone: str, country: str | None = None) -> tuple[bool, str]:
    if not phone or not phone.strip():
        return False, "Phone number is required."

    digits = re.sub(r"\D", "", phone)

    if not digits:
        return False, "Phone number must contain digits only."

    rule = PHONE_RULES.get(country) if country else None

    if rule:
        if len(digits) != rule["length"]:
            return False, (
                f"{country} phone numbers must be exactly {rule['length']} digits "
                f"(e.g. {rule['example']})."
            )
        if rule.get("starts_with") and not digits.startswith(rule["starts_with"]):
            return False, (
                f"{country} phone numbers must start with "
                f"'{rule['starts_with']}' (e.g. {rule['example']})."
            )
        return True, ""

    if not (DEFAULT_PHONE_MIN <= len(digits) <= DEFAULT_PHONE_MAX):
        return False, (
            f"Phone number must be between {DEFAULT_PHONE_MIN} and "
            f"{DEFAULT_PHONE_MAX} digits."
        )

    return True, ""


# ---------------------------------------------------------------------
# TEXT LENGTH
# ---------------------------------------------------------------------
def validate_min_length(value: str, min_len: int, field_name: str) -> tuple[bool, str]:
    if not value or len(value.strip()) < min_len:
        return False, f"{field_name} must be at least {min_len} characters."
    return True, ""


def validate_password(password: str, min_len: int = 8) -> tuple[bool, str]:
    if not password:
        return False, "Password is required."
    if len(password) < min_len:
        return False, f"Password must be at least {min_len} characters long."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
        return False, "Password must contain at least one letter and one number."
    return True, ""