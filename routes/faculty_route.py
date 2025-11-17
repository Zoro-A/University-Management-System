from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.faculty import FacultyModel

router = APIRouter(prefix="/faculty", tags=["faculty"])


class GradeRequest(BaseModel):
    faculty_id: str
    student_id: str
    course_id: str
    grade: str


class NotificationRequest(BaseModel):
    faculty_id: str
    target: str
    message: str


@router.get("/{faculty_id}")
def get_faculty(faculty_id: str):
    fac = FacultyModel.get_by_id(faculty_id)
    if not fac:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return {"user_id": fac.user_id, "name": fac.name, "email": fac.email, "courses": fac.courses}


@router.get("/{faculty_id}/courses")
def get_assigned_courses(faculty_id: str):
    fac = FacultyModel.get_by_id(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    return fac.view_assigned_courses()


@router.get("/{faculty_id}/students/{course_id}")
def get_students(faculty_id: str, course_id: str):
    fac = FacultyModel.get_by_id(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    return fac.view_students_for_course(course_id)


@router.post("/assign-grade")
def assign_grade(req: GradeRequest):
    fac = FacultyModel.get_by_id(req.faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")

    try:
        fac.assign_grade(req.student_id, req.course_id, req.grade)
        return {"status": "ok", "message": "Grade assigned"}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/notify")
def notify(req: NotificationRequest):
    fac = FacultyModel.get_by_id(req.faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    fac.send_notification(req.target, req.message)
    return {"status": "ok", "message": "Notification sent"}


@router.get("/{faculty_id}/timetable")
def timetable(faculty_id: str):
    fac = FacultyModel.get_by_id(faculty_id)
    if not fac:
        raise HTTPException(404, "Faculty not found")
    return fac.view_timetable()
