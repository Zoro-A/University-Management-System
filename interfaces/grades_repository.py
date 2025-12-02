from abc import ABC, abstractmethod

class IGradeRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, grade_record: dict):
        pass

    @abstractmethod
    def save_all(self, grades_list: list):
        pass

    @abstractmethod
    def find_grades_for_student(self, student_id: str):
        pass

    @abstractmethod
    def find_grades_for_course(self, course_id: str):
        pass
