from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.admin import AdminModel
from repositories.file_admin_repository import FileAdminRepository
from repositories.file_course_repository import FileCourseRepository
from repositories.file_student_repository import FileStudentRepository
from repositories.file_faculty_repository import FileFacultyRepository
from repositories.file_timetable_repository import FileTimetableRepository

router = APIRouter(prefix="/admin", tags=["admin"])

# Repo singletons
repo_admin = FileAdminRepository()
repo_course = FileCourseRepository()
repo_student = FileStudentRepository()
repo_faculty = FileFacultyRepository()
repo_timetable = FileTimetableRepository()


def load_admin(admin_id):
    return AdminModel.load(
        repo_admin, repo_course, repo_student, repo_faculty, repo_timetable, admin_id
    )


# ---------------- REQUEST MODELS ----------------

class CourseRequest(BaseModel):
    admin_id: str
    course_id: str
    name: str
    eligible_faculty: list[str]
    credits: int
    prerequisites: str | None = None


class RemoveCourseRequest(BaseModel):
    admin_id: str
    course_id: str


class StudentCreate(BaseModel):
    admin_id: str
    user_id: str
    name: str
    email: str
    password: str


class FacultyCreate(BaseModel):
    admin_id: str
    user_id: str
    name: str
    email: str
    password: str
    courses: list[str]


class RemoveUserRequest(BaseModel):
    admin_id: str
    user_id: str


class TimetableRequest(BaseModel):
    admin_id: str
    rooms: list[str]


# ---------------- ENDPOINTS ----------------

@router.get("/{admin_id}/dashboard")
def dashboard(admin_id: str):
    admin = load_admin(admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")

    return {
        "user_id": admin.user_id,
        "name": admin.name,
        "email": admin.email,
        "courses": admin.list_courses(),
        "users": admin.list_users(),
        "timetable": admin.view_timetable()
    }


@router.post("/courses/add")
def add_course(req: CourseRequest):
    admin = load_admin(req.admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")

    try:
        admin.add_course(req.course_id, req.name, req.eligible_faculty, req.credits, req.prerequisites)
        return {"status": "ok", "message": "Course added"}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/courses/remove")
def remove_course(req: RemoveCourseRequest):
    admin = load_admin(req.admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")

    admin.remove_course(req.course_id)
    return {"status": "ok", "message": "Course removed"}


@router.get("/{admin_id}/courses")
def list_courses(admin_id: str):
    admin = load_admin(admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")
    return admin.list_courses()


@router.post("/student/add")
def add_student(req: StudentCreate):
    admin = load_admin(req.admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")

    try:
        admin.add_student(req.user_id, req.name, req.email, req.password)
        return {"status": "ok", "message": "Student added"}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/faculty/add")
def add_faculty(req: FacultyCreate):
    admin = load_admin(req.admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")

    try:
        admin.add_faculty(req.user_id, req.name, req.email, req.password, req.courses)
        return {"status": "ok", "message": "Faculty added"}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/user/remove")
def remove_user(req: RemoveUserRequest):
    admin = load_admin(req.admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")

    admin.remove_user(req.user_id)
    return {"status": "ok", "message": "User removed"}


@router.get("/{admin_id}/users")
def list_users(admin_id: str):
    admin = load_admin(admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")
    return admin.list_users()


@router.post("/timetable/generate")
def generate(req: TimetableRequest):
    admin = load_admin(req.admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")

    timetable = admin.generate_timetable(req.rooms)
    return {"status": "ok", "timetable": timetable}


@router.get("/{admin_id}/timetable")
def view_timetable(admin_id: str):
    admin = load_admin(admin_id)
    if not admin:
        raise HTTPException(404, "Admin not found")
    return admin.view_timetable()
