# repositories/course_repository.py

from abc import ABC, abstractmethod

class ICourseRepository(ABC):

    @abstractmethod
    def save(self, course_data: dict):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def find_by_id(self, course_id: str):
        pass

    @abstractmethod
    def delete(self, course_id: str):
        pass

    @abstractmethod
    def update(self, course_id: str, updated_data: dict):
        pass
