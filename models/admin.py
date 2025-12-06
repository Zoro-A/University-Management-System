# backend/models/admin_model.py

from models.user import UserModel


class AdminModel(UserModel):
    def __init__(
        self,
        repo_admin,
        repo_courses,
        repo_students,
        repo_faculty,
        repo_timetable,
        user_id,
        name,
        email,
        password
    ):
        super().__init__(user_id, name, email, password)

        self.admin_repo = repo_admin
        self.course_repo = repo_courses
        self.student_repo = repo_students
        self.faculty_repo = repo_faculty
        self.timetable_repo = repo_timetable

    # -----------------------------
    # FACTORY LOAD
    # -----------------------------
    @classmethod
    def load(cls, repo_admin, repo_courses, repo_students, repo_faculty, repo_timetable, admin_id):
        user = repo_admin.get_by_id(admin_id)
        if not user:
            return None

        return cls(
            repo_admin, repo_courses, repo_students, repo_faculty, repo_timetable,
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            password=user["password"],
        )

    # -----------------------------
    # INTERNAL SAVE
    # -----------------------------
    def _save_self(self):
        self.admin_repo.save({
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        })

    # -----------------------------
    # BUSINESS LOGIC
    # -----------------------------

    # COURSES
    def add_course(self, course_id, name, eligible_faculty, credits, prerequisites):
        courses = self.course_repo.get_all()

        if any(c["course_id"] == course_id for c in courses):
            raise ValueError("Course already exists")

        self.course_repo.save({
            "course_id": course_id,
            "course_name": name,
            "eligible_faculty": eligible_faculty,
            "credits": credits,
            "prerequisites": prerequisites
        })

    def remove_course(self, course_id):
        self.course_repo.delete(course_id)

    def list_courses(self):
        return self.course_repo.get_all()

    # USERS
    def add_student(self, user_id, name, email, password):
        if self.student_repo.get_by_id(user_id):
            raise ValueError("Student already exists")

        self.student_repo.save({
            "user_id": user_id,
            "name": name,
            "email": email,
            "password": password,
            "enrolled": []
        })

    def add_faculty(self, user_id, name, email, password, courses):
        if self.faculty_repo.get_by_id(user_id):
            raise ValueError("Faculty already exists")

        self.faculty_repo.save({
            "user_id": user_id,
            "name": name,
            "email": email,
            "password": password,
            "courses": courses
        })

    def remove_user(self, user_id):
        self.student_repo.delete(user_id)
        #self.faculty_repo.delete(user_id)

    def list_users(self):
        students = self.student_repo.get_all() or []
        faculty = self.faculty_repo.get_all() or []

        # Helper to sort IDs like S1, S2, ..., S10 by their numeric part
        def _id_key(user):
            uid = user.get("user_id", "") or ""
            # Extract trailing digits; fallback to 0 if none
            num = ""
            for ch in uid:
                if ch.isdigit():
                    num += ch
            return int(num) if num.isdigit() else 0

        students_sorted = sorted(students, key=_id_key)
        faculty_sorted = sorted(faculty, key=_id_key)

        return {
            "students": students_sorted,
            "faculty": faculty_sorted,
        }

    # TIMETABLE
    def generate_timetable(self, rooms):
        courses = self.course_repo.get_all()
        faculty = self.faculty_repo.get_all()

        # You still use your existing generator
        from utils.timetable_generator import TimetableGenerator
        tg = TimetableGenerator()
        timetable = tg.generate(courses, faculty, rooms)

        self.timetable_repo.write_all(timetable)
        return timetable

    def view_timetable(self):
        return self.timetable_repo.get_all()
