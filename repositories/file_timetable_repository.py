from interfaces.timetable_repository import ITimetableRepository
from utils.file_manager import read_file, write_file

TIMETABLE_FILE = "timetable.txt"

class FileTimetableRepository(ITimetableRepository):

    def __init__(self):
        pass
    def get_all(self):
        return read_file(TIMETABLE_FILE)

    def write_all(self, timetable_list: list):
        write_file(TIMETABLE_FILE, timetable_list)
        return True
