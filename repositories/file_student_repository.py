from interfaces.student_repository import IStudentRepository
from utils.file_manager import read_file, write_file


class FileStudentRepository(IStudentRepository):

    def __init__(self, filepath="students.txt"):
        self.filepath = filepath

    def get_by_id(self, student_id: str):
        students = read_file(self.filepath)
        for s in students:
            if s["user_id"] == student_id:
                return s
        return None

    def save(self, student_data: dict):
        students = read_file(self.filepath)

        if any(s["user_id"] == student_data["user_id"] for s in students):
            raise ValueError("Student ID already exists")

        students.append(student_data)
        write_file(self.filepath, students)
        return student_data

    def get_all(self):
        return read_file(self.filepath)

    def find_by_id(self, student_id: str):
        students = read_file(self.filepath)
        for s in students:
            if s["user_id"] == student_id:
                return s
        return None

    def update(self, student_id: str, updated_data: dict):
        students = read_file(self.filepath)
        updated = False

        for i, student in enumerate(students):
            if student["user_id"] == student_id:
                students[i] = {**student, **updated_data}
                updated = True
                break

        if not updated:
            raise ValueError("Student not found")

        write_file(self.filepath, students)
        return students[i]

    def delete(self, student_id: str):
        students = read_file(self.filepath)
        new_list = [s for s in students if s["user_id"] != student_id]

        if len(new_list) == len(students):
            raise ValueError("Student not found")

        write_file(self.filepath, new_list)
        return True
