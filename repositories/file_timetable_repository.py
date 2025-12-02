# repositories/file_timetable_repository.py
from interfaces.timetable_repository import ITimetableRepository
from utils.file_manager import read_file

TIMETABLE_FILE = "timetable.txt"

class FileTimetableRepository(ITimetableRepository):

    def get_all(self):
        return read_file(TIMETABLE_FILE)
