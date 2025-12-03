# backend/routers/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.postgres_student_repository import PostgresStudentRepository
from repositories.postgres_admin_repository import PostgresAdminRepository
from repositories.postgres_faculty_repository import PostgresFacultyRepository

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str
    role: str  # "student", "admin", "faculty"

# Repository instances
repo_student = PostgresStudentRepository()
repo_admin = PostgresAdminRepository()
repo_faculty = PostgresFacultyRepository()

ROLE_REPO_MAP = {
    "student": repo_student,
    "admin": repo_admin,
    "faculty": repo_faculty
}

@router.post("/login")
def login(payload: LoginRequest):
    role = payload.role.lower()

    if role not in ROLE_REPO_MAP:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Get the appropriate repository
    repo = ROLE_REPO_MAP[role]
    
    # Get all users from the repository
    users = repo.get_all()

    # Search user
    user = next((
        u for u in users
        if u.get("email") == payload.email and u.get("password") == payload.password
    ), None)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Successful login
    return {
        "status": "ok",
        "role": role,
        "user": {
            "user_id": user["user_id"],
            "name": user.get("name"),
            "email": user.get("email")
        }
    }
