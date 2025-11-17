from models.user import UserModel
from utils.file_manager import read_file, write_file, append_record
from utils.timetable_generator import TimetableGenerator
import datetime

ADMIN_FILE = "admin.txt"
COURSES_FILE = "courses.txt"
STUDENTS_FILE = "students.txt"
FACULTY_FILE = "faculty.txt"
TIMETABLE_FILE = "timetable.txt"


class AdminModel(UserModel):
    FILE = ADMIN_FILE

    @staticmethod
    def get_by_id(admin_id: str):
        records = read_file(ADMIN_FILE)
        rec = next((x for x in records if x["user_id"] == admin_id), None)
        return AdminModel(**rec) if rec else None

    # ------------------------ COURSE MANAGEMENT ------------------------

    def add_course(self, course_id, course_name, eligible_faculty, credits, prerequisites):
        courses = read_file(COURSES_FILE)

        if any(c["course_id"] == course_id for c in courses):
            raise ValueError("Course already exists")

        courses.append({
            "course_id": course_id,
            "course_name": course_name,
            "eligible_faculty": eligible_faculty,
            "credits": credits,
            "prerequisites": prerequisites
        })

        write_file(COURSES_FILE, courses)

    def remove_course(self, course_id):
        courses = read_file(COURSES_FILE)
        new_courses = [c for c in courses if c["course_id"] != course_id]
        write_file(COURSES_FILE, new_courses)

    def list_courses(self):
        return read_file(COURSES_FILE)

    # ------------------------ USER MANAGEMENT ------------------------

    def add_student(self, user_id, name, email, password):
        students = read_file(STUDENTS_FILE)
        if any(s["user_id"] == user_id for s in students):
            raise ValueError("Student already exists")

        append_record(STUDENTS_FILE, {
            "user_id": user_id,
            "name": name,
            "email": email,
            "password": password,
            "enrolled": []
        })

    def add_faculty(self, user_id, name, email, password, courses):
        faculty = read_file(FACULTY_FILE)
        if any(f["user_id"] == user_id for f in faculty):
            raise ValueError("Faculty already exists")

        append_record(FACULTY_FILE, {
            "user_id": user_id,
            "name": name,
            "email": email,
            "password": password,
            "courses": courses
        })

    def remove_user(self, user_id):
        students = read_file(STUDENTS_FILE)
        faculty = read_file(FACULTY_FILE)

        write_file(STUDENTS_FILE, [s for s in students if s["user_id"] != user_id])
        write_file(FACULTY_FILE, [f for f in faculty if f["user_id"] != user_id])

    def list_users(self):
        return {
            "students": read_file(STUDENTS_FILE),
            "faculty": read_file(FACULTY_FILE)
        }

    # ------------------------ TIMETABLE ------------------------

    def generate_timetable(self, rooms):
        courses = read_file(COURSES_FILE)
        faculty = read_file(FACULTY_FILE)

        tg = TimetableGenerator()
        timetable = tg.generate(courses, faculty, rooms)

        write_file(TIMETABLE_FILE, timetable)
        return timetable

    def view_timetable(self):
        return read_file(TIMETABLE_FILE)

