from models.user import User
from utils.file_manager import FileManager
from utils.timetable_generator import TimetableGenerator
import datetime
import os

ADMIN_FILE = "data/admin.txt"
COURSES_FILE = "data/courses.txt"
STUDENTS_FILE = "data/students.txt"
FAC_FILE = "data/faculty.txt"
TIMETABLE_FILE = "data/timetable.txt"

class Admin(User):
    FILE = ADMIN_FILE

    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)

    @staticmethod
    def login():
        email = input("Admin email: ").strip()
        password = input("Password: ").strip()
        rec = User.authenticate(Admin.FILE, email, password)
        if rec:
            print(f"Welcome Admin {rec['name']}!")
            return Admin(**rec)
        else:
            print("Invalid credentials.")
            return None

    def interactive_menu(self):
        while True:
            print(f"\n--- Admin: {self.name} ---")
            print("1. Manage Courses")
            print("2. Manage Users (students/faculty)")
            print("3. Generate Timetable")
            print("4. Backup Data")
            print("5. View Timetable")
            print("6. Logout")
            c = input("Choice: ").strip()
            if c == "1":
                self.manage_courses()
            elif c == "2":
                self.manage_users()
            elif c == "3":
                self.generate_timetable()
            elif c == "4":
                self.backup_data()
            elif c == "5":
                self.view_timetable()
            elif c == "6":
                break
            else:
                print("Invalid choice.")

    def manage_courses(self):
        while True:
            print("\n--- Course Management ---")
            print("1. Add Course")
            print("2. Remove Course")
            print("3. List Courses")
            print("4. Back")
            c = input("Choice: ").strip()
            if c == "1":
                self.add_course()
            elif c == "2":
                self.remove_course()
            elif c == "3":
                self.list_courses()
            elif c == "4":
                break
            else:
                print("Invalid.")

    def add_course(self):
        cid = input("Course id: ").strip()
        name = input("Course name: ").strip()
        facs = input("Comma separated eligible faculty ids (optional): ").strip().split(",")
        facs = [f.strip() for f in facs if f.strip()]
        crhrs=input("Enter the credit hours for this course: ").strip()
        preReqs = input("Enter the prerequisite course id (if any): ").strip()
        courses = FileManager.read_file(COURSES_FILE)
        if any(c['course_id'] == cid for c in courses):
            print("Course id already exists.")
            return
        rec = {"course_id": cid, "course_name": name, "eligible_faculty": facs, "credits": crhrs, "prerequisites": preReqs}
        FileManager.append_record(COURSES_FILE, rec)
        print("Course added.")

    def remove_course(self):
        cid = input("Course id to remove: ").strip()
        courses = FileManager.read_file(COURSES_FILE)
        new = [c for c in courses if c['course_id'] != cid]
        FileManager.write_file(COURSES_FILE, new)
        print("Course removed (if existed).")

    def list_courses(self):
        courses = FileManager.read_file(COURSES_FILE)
        if not courses:
            print("No courses.")
            return
        for c in courses:
            print(f"{c['course_id']}: {c['course_name']} Eligible: {','.join(c.get('eligible_faculty',[]))}")

    def manage_users(self):
        while True:
            print("\n--- User Management ---")
            print("1. Add Student")
            print("2. Add Faculty")
            print("3. Remove Student/Faculty")
            print("4. List Students/Faculty")
            print("5. Back")
            c = input("Choice: ").strip()
            if c == "1":
                self.add_student()
            elif c == "2":
                self.add_faculty()
            elif c == "3":
                self.remove_user()
            elif c == "4":
                self.list_users()
            elif c == "5":
                break
            else:
                print("Invalid.")

    def add_student(self):
        sid = input("Student id: ").strip()
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        pwd = input("Password: ").strip()
        students = FileManager.read_file(STUDENTS_FILE)
        if any(s['user_id'] == sid for s in students):
            print("Student id exists.")
            return
        rec = {"user_id": sid, "name": name, "email": email, "password": pwd, "enrolled": []}
        FileManager.append_record(STUDENTS_FILE, rec)
        print("Student added.")

    def add_faculty(self):
        fid = input("Faculty id: ").strip()
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        pwd = input("Password: ").strip()
        courses = input("Comma separated course ids this faculty can teach: ").strip().split(",")
        courses = [c.strip() for c in courses if c.strip()]
        facs = FileManager.read_file(FAC_FILE)
        if any(f['user_id'] == fid for f in facs):
            print("Faculty id exists.")
            return
        rec = {"user_id": fid, "name": name, "email": email, "password": pwd, "courses": courses}
        FileManager.append_record(FAC_FILE, rec)
        print("Faculty added.")

    def remove_user(self):
        uid = input("Enter student or faculty id to remove: ").strip()
        students = FileManager.read_file(STUDENTS_FILE)
        facs = FileManager.read_file(FAC_FILE)
        students = [s for s in students if s.get('user_id') != uid]
        facs = [f for f in facs if f.get('user_id') != uid]
        FileManager.write_file(STUDENTS_FILE, students)
        FileManager.write_file(FAC_FILE, facs)
        print("User removed if existed.")

    def list_users(self):
        students = FileManager.read_file(STUDENTS_FILE)
        facs = FileManager.read_file(FAC_FILE)
        print("Students:")
        for s in students:
            print(f"  {s['user_id']} - {s['name']} enrolled: {len(s.get('enrolled',[]))}")
        print("\nFaculty:")
        for f in facs:
            print(f"  {f['user_id']} - {f['name']} courses: {','.join(f.get('courses',[]))}")

    def generate_timetable(self):
        courses = FileManager.read_file(COURSES_FILE)
        facs = FileManager.read_file(FAC_FILE)
        if not courses or not facs:
            print("Need courses and faculty to generate timetable.")
            return
        rooms = input("Enter comma separated room names to use (default: R101,R102,R103): ").strip()
        rooms = [r.strip() for r in (rooms.split(",") if rooms else ["R101","R102","R103"])]
        tg = TimetableGenerator()
        timetable = tg.generate(courses, facs, rooms)
        FileManager.write_file(TIMETABLE_FILE, timetable)
        print("Timetable generated and saved to data/timetable.txt")

    def backup_data(self):
        src_dir = "data"
        dest = f"backups/backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        FileManager.backup_folder(src_dir, dest)
        print(f"Backup complete -> {dest}")

    def view_timetable(self):
        tt = FileManager.read_file(TIMETABLE_FILE)
        if not tt:
            print("No timetable saved.")
            return
        for s in tt:
            print(f"{s['day']} {s['slot']} - {s['course_id']} ({s['course_name']}) - {s['faculty_name']} - Room {s['room']}")
