from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.faculty import FacultyModel

from repositories.postgres_faculty_repository import PostgresFacultyRepository
from repositories.postgres_student_repository import PostgresStudentRepository
from repositories.postgres_grades_repository import PostgresGradesRepository
from repositories.postgres_course_repository import PostgresCourseRepository
from repositories.postgres_notifications_repository import PostgresNotificationsRepository
from repositories.postgres_timetable_repository import PostgresTimetableRepository
from repositories.postgres_attendance_repository import PostgresAttendanceRepository

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
repo_attendance = PostgresAttendanceRepository()

def load_faculty(fid):
    return FacultyModel.load(repo_faculty, repo_student, repo_grades, repo_course, repo_notes, repo_time, repo_attendance, fid)

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

class AttendanceRequest(BaseModel):
    faculty_id: str
    student_id: str
    course_id: str
    date: str  # Format: YYYY-MM-DD
    status: str = "Present"  # Present, Absent, Late, Excused

class AttendanceItem(BaseModel):
    student_id: str
    status: str = "Present"

class BulkAttendanceRequest(BaseModel):
    faculty_id: str
    course_id: str
    date: str  # Format: YYYY-MM-DD
    attendance_list: list[AttendanceItem]  # List of {student_id, status}

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

@router.post("/mark-attendance")
def mark_attendance(req: AttendanceRequest):
    """
    Mark attendance for a single student in a course.
    """
    fac = load_faculty(req.faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    try:
        fac.mark_attendance(req.student_id, req.course_id, req.date, req.status)
        return {"status": "ok", "message": "Attendance marked successfully"}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/mark-attendance-bulk")
def mark_attendance_bulk(req: BulkAttendanceRequest):
    """
    Mark attendance for multiple students in a course at once.
    """
    fac = load_faculty(req.faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    
    results = []
    errors = []
    
    for attendance_item in req.attendance_list:
        student_id = attendance_item.student_id
        status = attendance_item.status
        
        try:
            fac.mark_attendance(student_id, req.course_id, req.date, status)
            results.append({"student_id": student_id, "status": "success"})
        except ValueError as e:
            errors.append({"student_id": student_id, "error": str(e)})
    
    return {
        "status": "ok",
        "message": f"Processed {len(req.attendance_list)} students",
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }

@router.get("/{faculty_id}/attendance/{course_id}/{date}")
def get_attendance(faculty_id: str, course_id: str, date: str):
    """
    Get attendance records for all students in a course on a specific date.
    """
    fac = load_faculty(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    try:
        attendance_records = fac.get_attendance_for_course_date(course_id, date)
        return {
            "course_id": course_id,
            "date": date,
            "attendance": attendance_records
        }
    except ValueError as e:
        raise HTTPException(400, str(e))
