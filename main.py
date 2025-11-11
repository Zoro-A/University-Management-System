# main.py
from models.student import Student
from models.faculty import Faculty
from models.admin import Admin
from utils.file_manager import FileManager
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def ensure_sample_data():
    FileManager.ensure_file("data/students.txt")
    FileManager.ensure_file("data/faculty.txt")
    FileManager.ensure_file("data/admin.txt")
    FileManager.ensure_file("data/courses.txt")
    FileManager.ensure_file("data/grades.txt")
    FileManager.ensure_file("data/timetable.txt")
    FileManager.ensure_file("data/notifications.txt")

def seed_admin_if_missing():
    admins = FileManager.read_file("data/admin.txt")
    if not admins:
        admin = {
            "user_id": "A1",
            "name": "superadmin",
            "email": "admin@uni.edu",
            "password": "admin123"
        }
        FileManager.append_record("data/admin.txt", admin)
        print("Created default admin (email=admin@uni.edu password=admin123)")

def main():
    ensure_sample_data()
    seed_admin_if_missing()

    while True:
        print("\n=== University Management System ===")
        print("1. Student Login")
        print("2. Faculty Login")
        print("3. Admin Login")
        print("4. Exit")

        choice = input("Select your role: ").strip()
        if choice == "1":
            s = Student.login()
            if s:
                s.interactive_menu()
        elif choice == "2":
            f = Faculty.login()
            if f:
                f.interactive_menu()
        elif choice == "3":
            a = Admin.login()
            if a:
                a.interactive_menu()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
