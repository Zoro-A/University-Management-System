from models.user import User
from utils.file_manager import FileManager

FAC_FILE = "data/faculty.txt"
GRADES_FILE = "data/grades.txt"
COURSES_FILE = "data/courses.txt"
NOTIF_FILE = "data/notifications.txt"
TIMETABLE_FILE = "data/timetable.txt"
STUDENTS_FILE = "data/students.txt"

class Faculty(User):
    FILE = FAC_FILE

    def __init__(self, user_id, name, email, password, courses=None):
        super().__init__(user_id, name, email, password)
        self.courses = courses or []

    @staticmethod
    def login():
        email = input("Faculty email: ").strip()
        password = input("Password: ").strip()
        rec = User.authenticate(Faculty.FILE, email, password)
        if rec:
            print(f"Welcome, Prof. {rec['name']}!")
            return Faculty(**rec)
        else:
            print("Invalid credentials.")
            return None

    def interactive_menu(self):
        while True:
            print(f"\n--- Faculty: {self.name} ---")
            print("1. View Assigned Courses")
            print("2. View Students (for a course)")
            print("3. Assign/Edit Grade")
            print("4. Send Notification")
            print("5. View Timetable")
            print("6. Logout")
            c = input("Choice: ").strip()
            if c == "1":
                self.view_assigned_courses()
            elif c == "2":
                self.view_students_for_course()
            elif c == "3":
                self.assign_grade()
            elif c == "4":
                self.send_notification()
            elif c == "5":
                self.view_timetable()
            elif c == "6":
                break
            else:
                print("Invalid choice.")

    def view_assigned_courses(self):
        print("Courses you can teach:", ", ".join(self.courses) if self.courses else "None")

    def view_students_for_course(self):
        cid = input("Course id: ").strip()
        students = FileManager.read_file(STUDENTS_FILE)
        enrolled_students = [s for s in students if cid in (s.get("enrolled") or [])]
        if not enrolled_students:
            print("No students enrolled or course not found.")
            return
        print(f"Students in {cid}:")
        for s in enrolled_students:
            print(f"  {s['user_id']} - {s['name']}")

    def assign_grade(self):
        cid = input("Course id: ").strip()
        sid = input("Student id: ").strip()
        grade = input("Grade (e.g., A, B+, 78): ").strip()
        students = FileManager.read_file(STUDENTS_FILE)
        student = next((s for s in students if s.get("user_id") == sid), None)
        if not student or cid not in (student.get("enrolled") or []):
            print("Student not enrolled in this course or not found.")
            return
        grades = FileManager.read_file(GRADES_FILE)
        updated = False
        for g in grades:
            if g.get("student_id") == sid and g.get("course_id") == cid:
                g["grade"] = grade
                updated = True
                break
        if not updated:
            grades.append({"student_id": sid, "course_id": cid, "grade": grade})
        FileManager.write_file(GRADES_FILE, grades)
        print("Grade assigned/updated.")

    def send_notification(self):
        target = input("Send to (student_id/all): ").strip()
        message = input("Message: ").strip()
        notifs = FileManager.read_file(NOTIF_FILE)
        if target.lower() == "all":
            notifs.append({"to": "all", "from": self.user_id, "message": message})
        else:
            notifs.append({"to": target, "from": self.user_id, "message": message})
        FileManager.write_file(NOTIF_FILE, notifs)
        print("Notification sent.")

    def view_timetable(self):
        tt = FileManager.read_file(TIMETABLE_FILE)
        mine = [s for s in tt if s.get("faculty_id") == self.user_id]
        if not mine:
            print("No timetable entries assigned.")
            return
        for s in mine:
            print(f"{s['day']} {s['slot']} - {s['course_id']} ({s['course_name']}) - Room {s['room']}")
