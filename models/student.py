# backend/models/student_model.py

from models.user import UserModel

class StudentModel(UserModel):
    def __init__(self, repo_student, repo_course, repo_grades, repo_notifications, repo_timetable,
                 user_id, name, email, password, enrolled=None):

        super().__init__(user_id, name, email, password)

        self.student_repo = repo_student
        self.course_repo = repo_course
        self.grades_repo = repo_grades
        self.notifications_repo = repo_notifications
        self.timetable_repo = repo_timetable

        self.enrolled = enrolled or []

    # -----------------------------
    # LOAD STUDENT (FACTORY METHOD)
    # -----------------------------
    @classmethod
    def load(cls, repo_student, repo_course, repo_grades, repo_notifications, repo_timetable, student_id):
        user = repo_student.get_by_id(student_id)
        if not user:
            return None
        
        return cls(
            repo_student, repo_course, repo_grades, repo_notifications, repo_timetable,
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            password=user["password"],
            enrolled=user.get("enrolled", [])
        )

    # -----------------------------
    # PERSIST CHANGES
    # -----------------------------
    def _save_self(self):
        """
        Persist the current state of the student.

        The student record itself is created once via the admin "add student"
        flow. After that, any changes (enrollment, drop, profile update) should
        UPDATE the existing record instead of trying to create a new one.

        Previously this method called `save`, which is meant for creation and
        enforces unique student IDs. That caused "Student ID already exists"
        whenever a student tried to enroll/drop/update, because it attempted to
        insert a duplicate row. We now delegate to `update` instead.
        """
        self.student_repo.update(
            self.user_id,
            {
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "enrolled": self.enrolled,
            },
        )

    # ---------------------------------
    # BUSINESS LOGIC (UNCHANGED OUTPUT)
    # ---------------------------------

    def enroll(self, course_id):
        courses = self.course_repo.get_all()
        grades = self.grades_repo.get_all()

        if course_id in self.enrolled:
            raise ValueError("Already enrolled in this course")

        course = next((c for c in courses if c["course_id"] == course_id), None)
        if not course:
            raise ValueError("Invalid course")

        prereq = course.get("prerequisites", "")
        if prereq:
            passed = any(
                g["student_id"] == self.user_id and 
                g["course_id"] == prereq and 
                g["grade"] != "F"
                for g in grades
            )
            if not passed:
                raise ValueError(f"Prerequisite required: {prereq}")

        self.enrolled.append(course_id)
        self._save_self()
        return True

    def drop(self, course_id):
        if course_id not in self.enrolled:
            raise ValueError("You are not enrolled in this course")

        self.enrolled.remove(course_id)
        self._save_self()
        return True

    def get_transcript(self):
        grades = self.grades_repo.get_all()
        student_grades = [g for g in grades if g["student_id"] == self.user_id]

        transcript = {}

        for g in student_grades:
            semester = str(g.get("semester", "Unknown"))
            transcript.setdefault(semester, []).append({
                "course": g["course_id"],
                "grade": g["grade"]
            })
        return transcript

    def get_notifications(self):
        notes = self.notifications_repo.get_all()
        return [
            n for n in notes
            if n.get("to") == self.user_id or n.get("to") == "all"
        ]

    def get_timetable(self):
        timetable = self.timetable_repo.get_all()
        return [t for t in timetable if t["course_id"] in self.enrolled]

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
