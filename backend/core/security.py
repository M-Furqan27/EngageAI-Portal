import hashlib
import secrets

from cryptography.fernet import Fernet


from core.config import settings





# =========================
# TOKEN ENCRYPTION
# =========================


fernet = Fernet(
    settings.token_encryption_key.encode()
)





def encrypt_token(
    value: str,
) -> str:

    return (
        fernet
        .encrypt(
            value.encode()
        )
        .decode()
    )





def decrypt_token(
    value: str,
) -> str:

    return (
        fernet
        .decrypt(
            value.encode()
        )
        .decode()
    )





# =========================
# INVITATION TOKEN
# =========================


def create_invitation_token():

    raw_token = (
        secrets
        .token_urlsafe(32)
    )


    token_hash = (
        hash_invitation_token(
            raw_token
        )
    )


    return (
        raw_token,
        token_hash,
    )





def hash_invitation_token(
    token: str,
):

    return hashlib.sha256(

        token.encode()

    ).hexdigest()