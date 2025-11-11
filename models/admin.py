# 📂 models/admin.py
from models.user import User
from utils.file_manager import FileManager

class Admin(User):
    FILE = "data/admin.txt"

    @staticmethod
    def login():
        email = input("Enter email: ")
        password = input("Enter password: ")
        record = User.authenticate(Admin.FILE, email, password)
        if record:
            print(f"Welcome Admin {record['name']}!")
            return Admin(**record)
        else:
            print("Invalid credentials.")
            return None

    def menu(self):
        print("\n--- Admin Menu ---")
        print("1. Manage Courses")
        print("2. Generate Timetable")
        print("3. View Reports")
        print("4. Logout")

        choice = input("Enter choice: ")
        if choice == "1":
            print("Managing courses (placeholder).")
        elif choice == "2":
            print("Generating timetable (placeholder).")
        elif choice == "3":
            print("Viewing reports (placeholder).")
