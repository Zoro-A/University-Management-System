from abc import ABC, abstractmethod

class IAttendanceRepository(ABC):

    @abstractmethod
    def save(self, attendance_record: dict):
        pass

    @abstractmethod
    def get_attendance_for_student_course(self, student_id: str, course_id: str):
        pass

    @abstractmethod
    def get_attendance_for_course_date(self, course_id: str, date: str):
        pass

    @abstractmethod
    def get_attendance_for_student(self, student_id: str):
        pass

    @abstractmethod
    def update_attendance(self, student_id: str, course_id: str, date: str, status: str):
        pass

