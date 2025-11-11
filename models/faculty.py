# 📂 models/faculty.py
from models.user import User
from utils.file_manager import FileManager

class Faculty(User):
    FILE = "data/faculty.txt"

    @staticmethod
    def login():
        email = input("Enter email: ")
        password = input("Enter password: ")
        record = User.authenticate(Faculty.FILE, email, password)
        if record:
            print(f"Welcome, Prof. {record['name']}!")
            return Faculty(**record)
        else:
            print("Invalid credentials.")
            return None

    def menu(self):
        print("\n--- Faculty Menu ---")
        print("1. Assign Grades")
        print("2. Send Notifications")
        print("3. Logout")

        choice = input("Enter choice: ")
        if choice == "1":
            print("Assign grades (placeholder).")
        elif choice == "2":
            print("Send notifications (placeholder).")
