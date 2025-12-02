# models/faculty_model.py

from models.user import UserModel

class FacultyModel(UserModel):
    def __init__(
        self,
        repo_faculty,
        repo_student,
        repo_grades,
        repo_course,
        repo_notifications,
        repo_timetable,
        user_id,
        name,
        email,
        password,
        courses=None
    ):
        super().__init__(user_id, name, email, password)

        self.faculty_repo = repo_faculty
        self.student_repo = repo_student
        self.grades_repo = repo_grades
        self.course_repo = repo_course
        self.notifications_repo = repo_notifications
        self.timetable_repo = repo_timetable

        self.courses = courses or []

    # -----------------------------
    # LOAD FACULTY (FACTORY METHOD)
    # -----------------------------
    @classmethod
    def load(cls, repo_faculty, repo_student, repo_grades, repo_course, repo_notifications, repo_timetable, faculty_id):
        user = repo_faculty.get_by_id(faculty_id)
        if not user:
            return None

        return cls(
            repo_faculty, repo_student, repo_grades, repo_course, repo_notifications, repo_timetable,
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            password=user["password"],
            courses=user.get("courses", [])
        )

    # -----------------------------
    # SAVE
    # -----------------------------
    def _save_self(self):
        self.faculty_repo.save({
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "courses": self.courses
        })

    # -----------------------------
    # BUSINESS LOGIC
    # -----------------------------

    def view_assigned_courses(self):
        return self.courses

    def view_students_for_course(self, course_id):
        students = self.student_repo.get_all()
        return [s for s in students if course_id in s.get("enrolled", [])]

    def assign_grade(self, student_id, course_id, grade):
        students = self.student_repo.get_all()
        student = next((s for s in students if s["user_id"] == student_id), None)
        if not student:
            raise ValueError("Student not found")

        if course_id not in student.get("enrolled", []):
            raise ValueError("Student not enrolled in this course")

        grades = self.grades_repo.get_all()
        updated = False

        for g in grades:
            if g["student_id"] == student_id and g["course_id"] == course_id:
                g["grade"] = grade
                updated = True
                break

        if not updated:
            grades.append({
                "student_id": student_id,
                "course_id": course_id,
                "grade": grade
            })

        self.grades_repo.save_all(grades)

    def send_notification(self, target, message):
        notes = self.notifications_repo.get_all()
        notes.append({
            "to": target,
            "from": self.user_id,
            "message": message
        })
        self.notifications_repo.save_all(notes)

    def view_timetable(self):
        tt = self.timetable_repo.get_all()
        return [t for t in tt if t.get("faculty_id") == self.user_id]
