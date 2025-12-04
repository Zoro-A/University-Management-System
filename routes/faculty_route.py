from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.faculty import FacultyModel

from repositories.file_faculty_repository import FileFacultyRepository
from repositories.file_student_repository import FileStudentRepository
from repositories.file_grades_repository import FileGradesRepository
from repositories.file_course_repository import FileCourseRepository
from repositories.file_notifications_repository import FileNotificationsRepository
from repositories.file_timetable_repository import FileTimetableRepository

router = APIRouter(prefix="/faculty", tags=["faculty"])

# -----------------------
# Repo Singletons
# -----------------------
repo_faculty = FileFacultyRepository()
repo_student = FileStudentRepository()
repo_grades = FileGradesRepository()
repo_course = FileCourseRepository()
repo_notes = FileNotificationsRepository()
repo_time = FileTimetableRepository()

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
