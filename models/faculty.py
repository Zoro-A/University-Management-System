from models.user import UserModel
from utils.file_manager import read_file, write_file, append_record

FAC_FILE = "faculty.txt"
STUDENTS_FILE = "students.txt"
GRADES_FILE = "grades.txt"
COURSES_FILE = "courses.txt"
TIMETABLE_FILE = "timetable.txt"
NOTIF_FILE = "notifications.txt"


class FacultyModel(UserModel):
    FILE = FAC_FILE

    def __init__(self, user_id, name, email, password, courses=None):
        super().__init__(user_id, name, email, password)
        self.courses = courses or []

    # ------------------------ STATIC HELPERS ------------------------

    @staticmethod
    def get_by_id(faculty_id: str):
        records = read_file(FAC_FILE)
        rec = next((x for x in records if x["user_id"] == faculty_id), None)
        if not rec:
            return None
        return FacultyModel(**rec)

    # ------------------------ BUSINESS LOGIC ------------------------

    def view_assigned_courses(self):
        return self.courses

    def view_students_for_course(self, course_id: str):
        students = read_file(STUDENTS_FILE)
        enrolled = [s for s in students if course_id in s.get("enrolled", [])]
        return enrolled

    def assign_grade(self, student_id: str, course_id: str, grade: str):
        students = read_file(STUDENTS_FILE)
        student = next((s for s in students if s["user_id"] == student_id), None)

        if not student:
            raise ValueError("Student not found")

        if course_id not in student.get("enrolled", []):
            raise ValueError("Student not enrolled in this course")

        grades = read_file(GRADES_FILE)
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

        write_file(GRADES_FILE, grades)

    def send_notification(self, target: str, message: str):
        notifs = read_file(NOTIF_FILE)
        notifs.append({
            "to": target,
            "from": self.user_id,
            "message": message
        })
        write_file(NOTIF_FILE, notifs)

    def view_timetable(self):
        tt = read_file(TIMETABLE_FILE)
        mine = [x for x in tt if x.get("faculty_id") == self.user_id]
        return mine
