from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from modules.profile.user_model import User, UserRole, UserStatus
from modules.auth.service import hash_password


def ensure_owner(current_user: User):
    if current_user.role.value != "Owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the organization Owner can access employee management.",
        )


def get_employees(db: Session, organization_id):
    return (
        db.query(User)
        .filter(User.organization_id == organization_id, User.role != UserRole.Owner)
        .all()
    )


def create_employee(db: Session, organization_id, data):
    if data.role not in ("Sales", "Finance", "Support"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be Sales, Finance, or Support")

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    employee = User(
        organization_id=organization_id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password_hash=hash_password(data.password),
        phone=data.phone,
        role=UserRole(data.role),
        status=UserStatus.Active,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee_status(db: Session, organization_id, user_id, new_status: str):
    if new_status not in ("Active", "Inactive"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status value")

    employee = (
        db.query(User)
        .filter(User.user_id == user_id, User.organization_id == organization_id)
        .first()
    )
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    if employee.role.value == "Owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Owner status cannot be changed here")

    employee.status = UserStatus(new_status)
    db.commit()
    db.refresh(employee)
    return employee