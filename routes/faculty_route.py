from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.faculty import FacultyModel

from repositories.postgres_faculty_repository import PostgresFacultyRepository
from repositories.postgres_student_repository import PostgresStudentRepository
from repositories.postgres_grades_repository import PostgresGradesRepository
from repositories.postgres_course_repository import PostgresCourseRepository
from repositories.postgres_notifications_repository import PostgresNotificationsRepository
from repositories.postgres_timetable_repository import PostgresTimetableRepository

router = APIRouter(prefix="/faculty", tags=["faculty"])

# -----------------------
# Repo Singletons - Using PostgreSQL repositories
# -----------------------
repo_faculty = PostgresFacultyRepository()
repo_student = PostgresStudentRepository()
repo_grades = PostgresGradesRepository()
repo_course = PostgresCourseRepository()
repo_notes = PostgresNotificationsRepository()
repo_time = PostgresTimetableRepository()

def load_faculty(fid):
    return FacultyModel.load(repo_faculty, repo_student, repo_grades, repo_course, repo_notes, repo_time, fid)

# -----------------------
# Request Models
# -----------------------

class GradeRequest(BaseModel):
    faculty_id: str
    student_id: str
    course_id: str
    grade: str

class NotificationRequest(BaseModel):
    faculty_id: str
    target: str
    message: str

# -----------------------
# Routes
# -----------------------

@router.get("/{faculty_id}")
def get_faculty(faculty_id: str):
    fac = load_faculty(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    return {
        "user_id": fac.user_id,
        "name": fac.name,
        "email": fac.email,
        "courses": fac.courses
    }

@router.get("/{faculty_id}/courses")
def courses(faculty_id: str):
    fac = load_faculty(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    return fac.view_assigned_courses()

@router.get("/{faculty_id}/students/{course_id}")
def students(faculty_id: str, course_id: str):
    fac = load_faculty(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    return fac.view_students_for_course(course_id)

@router.post("/assign-grade")
def assign_grade(req: GradeRequest):
    fac = load_faculty(req.faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    try:
        fac.assign_grade(req.student_id, req.course_id, req.grade)
        return {"status": "ok", "message": "Grade assigned"}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/notify")
def notify(req: NotificationRequest):
    fac = load_faculty(req.faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    fac.send_notification(req.target, req.message)
    return {"status": "ok", "message": "Notification sent"}

@router.get("/{faculty_id}/timetable")
def timetable(faculty_id: str):
    fac = load_faculty(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    return fac.view_timetable()
