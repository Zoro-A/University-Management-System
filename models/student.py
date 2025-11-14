# models/student.py
from models.user import User
from utils.file_manager import FileManager

COURSES_FILE = "data/courses.txt"
STUDENTS_FILE = "data/students.txt"
GRADES_FILE = "data/grades.txt"
TIMETABLE_FILE = "data/timetable.txt"
NOTIF_FILE = "data/notifications.txt"

class Student(User):
    FILE = STUDENTS_FILE

    def __init__(self, user_id, name, email, password, enrolled=None):
        super().__init__(user_id, name, email, password)
        # stored as list of course_ids
        self.enrolled = enrolled or []

    @staticmethod
    def login():
        email = input("Student email: ").strip()
        password = input("Password: ").strip()
        record = User.authenticate(Student.FILE, email, password)
        if record:
            print(f"Welcome, {record['name']}!")
            return Student(**record)
        else:
            print("Invalid credentials.")
            return None

    def interactive_menu(self):
        while True:
            print(f"\n--- Student: {self.name} ---")
            print("1. View Transcript")
            print("2. View Timetable")
            print("3. View Dashboard")
            print("4. Enroll in Course")
            print("5. Drop Course")
            print("6. View Notifications")
            print("7. Update Profile")
            print("8. Logout")
            c = input("Choice: ").strip()
            if c == "1":
                self.view_transcript()
            elif c == "2":
                self.view_timetable()
            elif c == "3":
                self.view_dashboard()
            elif c == "4":
                self.enroll_course()
            elif c == "5":
                self.drop_course()
            elif c == "6":
                self.view_notifications()
            elif c == "7":
                self.update_profile()
            elif c == "8":
                break
            else:
                print("Invalid choice.")

    def view_transcript(self):
        grades = FileManager.read_file(GRADES_FILE)
        if not grades:
            print("No grades available.")
            return

        my_grades = [g for g in grades if g["student_id"] == self.user_id]

        if not my_grades:
            print("No grades found for your ID.")
            return

        print("\n=== Transcript ===")
        for g in my_grades:
            print(f"{g['course_id']}: {g['grade']}")


    def view_timetable(self):
        tt = FileManager.read_file(TIMETABLE_FILE)
        my_slots = [s for s in tt if s.get("course_id") in (self.enrolled or [])]
        if not my_slots:
            print("No timetable entries found for your courses.")
            return
        print("Timetable entries for your enrolled courses:")
        for s in my_slots:
            print(f"  {s['day']} {s['slot']} - {s['course_id']} ({s['course_name']}) - {s['faculty_name']} - Room {s['room']}")

    def view_dashboard(self):
        print(f"Name: {self.name}")
        print(f"Enrolled courses: {', '.join(self.enrolled) if self.enrolled else 'None'}")
        grades = FileManager.read_file(GRADES_FILE)
        my_grades = [g for g in grades if g.get("student_id") == self.user_id]
        print(f"Courses graded: {len(my_grades)}")

    def enroll_course(self):
        courses = FileManager.read_file(COURSES_FILE)
        grades = FileManager.read_file(GRADES_FILE)

        if not courses:
            print("No courses available.")
            return

        # Show all courses
        print("Available courses:")
        for c in courses:
            print(f"  {c['course_id']}: {c['course_name']}")

        cid = input("Enter course id to enroll: ").strip()

        # Already enrolled?
        if cid in (self.enrolled or []):
            print("Already enrolled in this course.")
            return

        # Find the course
        course = next((c for c in courses if c['course_id'] == cid), None)
        if not course:
            print("Invalid course ID.")
            return

        prereq = course.get("prerequisite", "").strip()

        # No prerequisite → enroll directly
        if prereq == "":
            self.enrolled.append(cid)
            self._persist_self()
            print(f"Enrolled in {cid}.")
            return

        # Otherwise check if the student passed the prerequisite
        prereq_grade = next(
            (g for g in grades if g["student_id"] == self.user_id and g["course_id"] == prereq),
            None
        )

        # Student never took the prerequisite
        if prereq_grade is None:
            print(f"You must complete prerequisite course {prereq} before taking {cid}.")
            return

        # Student took prerequisite but failed
        if prereq_grade["grade"] == "F":
            print(f"You did not pass prerequisite {prereq}. Cannot enroll in {cid}.")
            return

        # Student passed prerequisite → enroll
        self.enrolled.append(cid)
        self._persist_self()
        print(f"Enrolled in {cid}.")
        
    def drop_course(self):
        if not self.enrolled:
            print("You are not enrolled in any courses.")
            return

        print("Your enrolled courses:")
        for c in self.enrolled:
            print(f" - {c}")

        cid = input("Enter course id to drop: ").strip()

        if cid not in self.enrolled:
            print("You are not enrolled in this course.")
            return

        self.enrolled.remove(cid)
        self._persist_self()
        print(f"Dropped course {cid}.")

    def view_notifications(self):
        notifs = FileManager.read_file(NOTIF_FILE)
        mine = [n for n in notifs if n.get("to") in ("all", self.user_id)]
        if not mine:
            print("No notifications.")
            return
        print("Notifications:")
        for n in mine:
            print(f"From {n.get('from')}: {n.get('message')}")

    def update_profile(self):
        new_name = input(f"New name (blank to keep {self.name}): ").strip()
        new_pass = input("New password (blank to keep): ").strip()
        if new_name:
            self.name = new_name
        if new_pass:
            self.password = new_pass
        self._persist_self()
        print("Profile updated.")

    def _persist_self(self):
        all_students = FileManager.read_file(self.FILE)
        for i, s in enumerate(all_students):
            if s.get("user_id") == self.user_id:
                all_students[i] = {
                    "user_id": self.user_id,
                    "name": self.name,
                    "email": self.email,
                    "password": self.password,
                    "enrolled": self.enrolled
                }
                FileManager.write_file(self.FILE, all_students)
                return
        rec = {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "enrolled": self.enrolled
        }
        FileManager.append_record(self.FILE, rec)
