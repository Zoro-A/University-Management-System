from interfaces.grades_repository import IGradeRepository
from utils.file_manager import read_file, write_file


class FileGradesRepository(IGradeRepository):

    def __init__(self, filepath="grades.txt"):
        self.filepath = filepath

    def get_all(self):
        return read_file(self.filepath)

    def save(self, grade_record: dict):
        grades = read_file(self.filepath)
        grades.append(grade_record)
        write_file(self.filepath, grades)
        return grade_record

    def save_all(self, grades_list: list):
        write_file(self.filepath, grades_list)
        return True

    def find_grades_for_student(self, student_id: str):
        grades = read_file(self.filepath)
        return [g for g in grades if g["student_id"] == student_id]

    def find_grades_for_course(self, course_id: str):
        grades = read_file(self.filepath)
        return [g for g in grades if g["course_id"] == course_id]
