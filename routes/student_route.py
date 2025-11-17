# backend/routers/student.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.student import StudentModel

router = APIRouter(prefix="/student", tags=["student"])


# --------------------
# Request Models
# --------------------
class EnrollRequest(BaseModel):
    student_id: str
    course_id: str

class DropRequest(BaseModel):
    student_id: str
    course_id: str

class UpdateProfileRequest(BaseModel):
    student_id: str
    name: str | None = None
    email: str | None = None
    password: str | None = None


# --------------------
# 1. View Dashboard
# --------------------
@router.get("/{student_id}/dashboard")
def dashboard(student_id: str):
    student = StudentModel.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "user_id": student.user_id,
        "name": student.name,
        "email": student.email,
        "enrolled_courses": student.enrolled,
        "notifications": student.get_notifications(),
        "timetable": student.get_timetable()
    }


# --------------------
# 2. View Transcript
# --------------------
@router.get("/{student_id}/transcript")
def transcript(student_id: str):
    student = StudentModel.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student.get_transcript()


# --------------------
# 3. View Timetable
# --------------------
@router.get("/{student_id}/timetable")
def timetable(student_id: str):
    student = StudentModel.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.get_timetable()


# --------------------
# 4. Enroll in Course
# --------------------
@router.post("/enroll")
def enroll(req: EnrollRequest):
    student = StudentModel.get_by_id(req.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        student.enroll(req.course_id)
        return {"status": "ok", "message": f"Enrolled in {req.course_id}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------------------
# 5. Drop Course
# --------------------
@router.post("/drop")
def drop_course(req: DropRequest):
    student = StudentModel.get_by_id(req.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        student.drop(req.course_id)
        return {"status": "ok", "message": f"Dropped {req.course_id}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------------------
# 6. View Notifications
# --------------------
@router.get("/{student_id}/notifications")
def notifications(student_id: str):
    student = StudentModel.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.get_notifications()


# --------------------
# 7. Update Profile
# --------------------
@router.put("/update-profile")
def update_profile(req: UpdateProfileRequest):
    student = StudentModel.get_by_id(req.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    updated = student.update_profile(
        name=req.name,
        email=req.email,
        password=req.password
    )

    return {"status": "ok", "message": "Profile updated", "updated": updated}


# --------------------
# 8. Logout
# --------------------
@router.post("/logout/{student_id}")
def logout(student_id: str):
    # For now this is a dummy endpoint because you're not using JWT yet.
    # In the future, you'll invalidate the token here.
    return {"status": "ok", "message": "Logged out"}
