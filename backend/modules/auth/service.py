# """
# backend/modules/auth/service.py

# REPLACE the existing file. Sirf register_organization_and_owner function
# change hui hai — baaki (verify_password, create_access_token,
# authenticate_user, get_current_user) EXACTLY same hain, copy kar liye
# taake poori file ek sath replace ho sake.
# """

# from datetime import datetime, timedelta
# from passlib.context import CryptContext
# from jose import jwt, JWTError
# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from core.database import get_db
# from core.config import settings
# from modules.profile.organization_model import Organization
# from modules.profile.user_model import User, UserRole

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def create_access_token(user_id, organization_id) -> str:
#     expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     payload = {"sub": str(user_id), "organization_id": str(organization_id), "exp": expire}
#     return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# def register_organization_and_owner(db: Session, data):
#     existing = db.query(User).filter(User.email == data.email).first()
#     if existing:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

#     # Sirf naam se organization shell banti hai — baaki fields (business_type,
#     # website, business_email, business_phone, country, ...) NULL rehte hain
#     # jab tak owner onboarding wizard mein complete na kare.
#     org = Organization(
#         organization_name=data.organization_name,
#         onboarding_completed=False,
#     )
#     db.add(org)
#     db.flush()  # commit se pehle organization_id generate karne ke liye

#     owner = User(
#         organization_id=org.organization_id,
#         first_name=data.first_name,
#         last_name=data.last_name,
#         email=data.email,
#         password_hash=hash_password(data.password),
#         phone=data.phone,
#         role=UserRole.Owner,
#     )
#     db.add(owner)
#     db.commit()
#     db.refresh(owner)

#     token = create_access_token(owner.user_id, owner.organization_id)
#     return token, owner


# def authenticate_user(db: Session, email: str, password: str):
#     user = db.query(User).filter(User.email == email).first()
#     if not user or not verify_password(password, user.password_hash):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

#     if user.role.value != "Owner":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only the organization Owner can log in to the portal.",
#         )

#     if user.status.value == "Inactive":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Your account has been deactivated. Contact your organization admin.",
#         )

#     token = create_access_token(user.user_id, user.organization_id)
#     return token, user


# security = HTTPBearer()


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db),
# ) -> User:
#     """
#     Token decode karke logged-in user return karta hai.
#     Har protected route mein: current_user: User = Depends(get_current_user)
#     """
#     token = credentials.credentials
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

#     user = db.query(User).filter(User.user_id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
#     if user.status.value == "Inactive":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated")

#     return user




from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.database import get_db
from core.config import settings

from modules.profile.organization_model import Organization
from modules.profile.user_model import User, UserRole


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ---------------- PASSWORD ----------------

def hash_password(password: str) -> str:
    """
    bcrypt only supports max 72 bytes
    """
    password = password[:72]
    return pwd_context.hash(password)



def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    plain_password = plain_password[:72]

    return pwd_context.verify(
        plain_password,
        hashed_password
    )



# ---------------- JWT ----------------

def create_access_token(
    user_id,
    organization_id
) -> str:

    expire = (
        datetime.utcnow()
        +
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "organization_id": str(organization_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )



# ---------------- REGISTER ----------------

def register_organization_and_owner(
    db: Session,
    data
):

    existing = (
        db.query(User)
        .filter(
            User.email == data.email
        )
        .first()
    )


    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    org = Organization(
        organization_name=data.organization_name,
        onboarding_completed=False,
    )

    db.add(org)
    db.flush()


    owner = User(
        organization_id=org.organization_id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password_hash=hash_password(data.password),
        phone=data.phone,
        role=UserRole.Owner,
    )


    db.add(owner)

    db.commit()

    db.refresh(owner)


    token = create_access_token(
        owner.user_id,
        owner.organization_id
    )


    return token, owner



# ---------------- LOGIN ----------------

def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )


    if (
        not user
        or not verify_password(
            password,
            user.password_hash
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    if user.role.value != "Owner":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization Owner can login"
        )


    if user.status.value == "Inactive":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated"
        )


    token = create_access_token(
        user.user_id,
        user.organization_id
    )


    return token, user



# ---------------- CURRENT USER ----------------

security = HTTPBearer()



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials


    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )


        user_id = payload.get("sub")


        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    user = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )


    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    return user