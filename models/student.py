# backend/models/student_model.py

from models.user import UserModel
from utils.file_manager import read_file, write_file

STUDENTS_FILE = "students.txt"
GRADES_FILE = "grades.txt"
COURSES_FILE = "courses.txt"
NOTIFICATIONS_FILE = "notifications.txt"
TIMETABLE_FILE = "timetable.txt"


class StudentModel(UserModel):

    def __init__(self, user_id, name, email, password, enrolled=None):
        super().__init__(user_id, name, email, password)
        self.enrolled = enrolled or []

    # ------------------------------------------------------
    # STATIC LOADERS
    # ------------------------------------------------------
    @staticmethod
    def get_by_id(student_id: str):
        data = read_file(STUDENTS_FILE)
        user = next((u for u in data if u["user_id"] == student_id), None)
        if not user:
            return None

        return StudentModel(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            password=user["password"],
            enrolled=user.get("enrolled", [])
        )

    @staticmethod
    def _save_all(students):
        write_file(STUDENTS_FILE, students)

    # ------------------------------------------------------
    # INTERNAL SAVE METHOD
    # ------------------------------------------------------
    def _save_self(self):
        all_data = read_file(STUDENTS_FILE)
        for s in all_data:
            if s["user_id"] == self.user_id:
                s["name"] = self.name
                s["email"] = self.email
                s["password"] = self.password
                s["enrolled"] = self.enrolled
                break

        write_file(STUDENTS_FILE, all_data)

    # ------------------------------------------------------
    # 1. ENROLL IN COURSE
    # ------------------------------------------------------
    def enroll(self, course_id):
        courses = read_file(COURSES_FILE)
        grades = read_file(GRADES_FILE)

        # Already enrolled?
        if course_id in self.enrolled:
            raise ValueError("Already enrolled in this course")

        # Check if course exists
        course = next((c for c in courses if c["course_id"] == course_id), None)
        if not course:
            raise ValueError("Invalid course")

        # Check prerequisites (correct key: prerequisites)
        prereq = course.get("prerequisites", "")
        if prereq:
            passed = False
            for g in grades:
                if (
                    g["student_id"] == self.user_id and
                    g["course_id"] == prereq and
                    g["grade"] != "F"
                ):
                    passed = True
                    break

            if not passed:
                raise ValueError(f"Prerequisite required: {prereq}")

        # Add enrollment
        self.enrolled.append(course_id)
        self._save_self()
        return True

    # ------------------------------------------------------
    # 2. DROP COURSE
    # ------------------------------------------------------
    def drop(self, course_id):
        if course_id not in self.enrolled:
            raise ValueError("You are not enrolled in this course")

        self.enrolled.remove(course_id)
        self._save_self()
        return True

    # ------------------------------------------------------
    # 3. TRANSCRIPT
    # ------------------------------------------------------
    def get_transcript(self):
        grades = read_file(GRADES_FILE)
        return [g for g in grades if g["student_id"] == self.user_id]

    # ------------------------------------------------------
    # 4. NOTIFICATIONS
    # ------------------------------------------------------
    def get_notifications(self):
        notes = read_file(NOTIFICATIONS_FILE)
        # notifications stored as {to: student_id/all, message, from}
        return [
            n for n in notes
            if n.get("to") == self.user_id or n.get("to") == "all"
        ]

    # ------------------------------------------------------
    # 5. TIMETABLE
    # ------------------------------------------------------
    def get_timetable(self):
        timetable = read_file(TIMETABLE_FILE)
        return [t for t in timetable if t["course_id"] in self.enrolled]

    # ------------------------------------------------------
    # 6. UPDATE PROFILE
    # ------------------------------------------------------
    def update_profile(self, name=None, email=None, password=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = password

        self._save_self()

        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password_updated": bool(password)
        }
