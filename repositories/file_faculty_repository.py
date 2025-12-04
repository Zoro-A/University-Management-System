from interfaces.faculty_repository import IFacultyRepository
from utils.file_manager import read_file, write_file

class FileFacultyRepository(IFacultyRepository):

    def __init__(self, filepath="faculty.txt"):
        self.filepath = filepath

    def get_all(self):
        """Return list of all faculty members"""
        return read_file(self.filepath)

    def save(self, faculty_record: dict):
        faculty = read_file(self.filepath)
        faculty.append(faculty_record)
        write_file(self.filepath, faculty)
        return faculty_record

    def save_all(self, faculty_list: list):
        write_file(self.filepath, faculty_list)
        return True

    def get_by_id(self, faculty_id: str):
        faculty = read_file(self.filepath)
        for f in faculty:
            if f.get("user_id") == faculty_id:
                return f
        return None
