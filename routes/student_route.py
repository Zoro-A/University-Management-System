from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.student import StudentModel
from repositories.postgres_student_repository import PostgresStudentRepository
from repositories.postgres_course_repository import PostgresCourseRepository
from repositories.postgres_grades_repository import PostgresGradesRepository
from repositories.postgres_notifications_repository import PostgresNotificationsRepository
from repositories.postgres_timetable_repository import PostgresTimetableRepository

router = APIRouter(prefix="/student", tags=["student"])

# Repos (singletons) - Using PostgreSQL repositories
repo_student = PostgresStudentRepository()
repo_course = PostgresCourseRepository()
repo_grades = PostgresGradesRepository()
repo_notes = PostgresNotificationsRepository()
repo_time = PostgresTimetableRepository()

def load_student(student_id):
    return StudentModel.load(repo_student, repo_course, repo_grades, repo_notes, repo_time, student_id)


# --------------------
# Request Models
# --------------------sa
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
# Dashboard
# --------------------
@router.get("/{student_id}/dashboard")
def dashboard(student_id: str):
    student = load_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    return {
        "user_id": student.user_id,
        "name": student.name,
        "email": student.email,
        "enrolled_courses": student.enrolled,
        "notifications": student.get_notifications(),
        "timetable": student.get_timetable()
    }


# Transcript
@router.get("/{student_id}/transcript")
def transcript(student_id: str):
    student = load_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student.get_transcript()


# Timetable
@router.get("/{student_id}/timetable")
def timetable(student_id: str):
    student = load_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student.get_timetable()


# Enrolled Courses
@router.get("/{student_id}/courses")
def enrolled_courses(student_id: str):
    """
    Return a simple list of course IDs the student is currently enrolled in.
    """
    student = load_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    return {
        "student_id": student.user_id,
        "enrolled_courses": student.enrolled,
    }


# Enroll
@router.post("/enroll")
def enroll(req: EnrollRequest):
    student = load_student(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    try:
        student.enroll(req.course_id)
        return {"status": "ok", "message": f"Enrolled in {req.course_id}"}
    except ValueError as e:
        raise HTTPException(400, str(e))


# Drop
@router.post("/drop")
def drop(req: DropRequest):
    student = load_student(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    try:
        student.drop(req.course_id)
        return {"status": "ok", "message": f"Dropped {req.course_id}"}
    except ValueError as e:
        raise HTTPException(400, str(e))


# Notifications
@router.get("/{student_id}/notifications")
def notifications(student_id: str):
    student = load_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student.get_notifications()


# Update Profile
@router.put("/update-profile")
def update_profile(req: UpdateProfileRequest):
    student = load_student(req.student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    updated = student.update_profile(req.name, req.email, req.password)
    return {"status": "ok", "message": "Profile updated", "updated": updated}


# Logout
@router.post("/logout/{student_id}")
def logout(student_id: str):
    return {"status": "ok", "message": "Logged out"}
