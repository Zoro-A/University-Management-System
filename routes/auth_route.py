# backend/routers/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.file_manager import read_file

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str
    role: str  # "student", "admin", "faculty"


ROLE_FILE_MAP = {
    "student": "students.txt",
    "admin": "admin.txt",
    "faculty": "faculty.txt"
}

@router.post("/login")
def login(payload: LoginRequest):
    role = payload.role.lower()

    if role not in ROLE_FILE_MAP:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Load only the relevant file
    users = read_file(ROLE_FILE_MAP[role])

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
