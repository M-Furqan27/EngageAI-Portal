"""
frontend/utils/validators.py

Shared validation rules — sab forms yahan se import karte hain,
taake rules consistent rahein aur ek jagah maintain ho.
"""

import re

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))


def is_valid_phone(number: str, required_length: int = 11) -> bool:
    """Number sirf digits ka hona chahiye, aur exact length match karni chahiye."""
    if not number:
        return False
    digits = number.strip()
    return digits.isdigit() and len(digits) == required_length


def is_valid_url(url: str) -> bool:
    if not url:
        return False
    return url.strip().startswith(("http://", "https://"))


def is_valid_password(password: str, min_length: int = 8) -> bool:
    return bool(password) and len(password) >= min_length


def collect_required_errors(fields: dict) -> list[str]:
    """
    fields = {"Field Label": value, ...}
    Khali/missing fields ke liye specific error messages return karta hai.
    """
    errors = []
    for label, value in fields.items():
        if isinstance(value, str):
            if not value.strip():
                errors.append(f"{label} is required.")
        elif not value:
            errors.append(f"{label} is required.")
    return errors