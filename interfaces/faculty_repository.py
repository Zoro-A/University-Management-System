# interfaces/faculty_repository.py
from abc import ABC, abstractmethod

class IFacultyRepository(ABC):

    @abstractmethod
    def get_by_id(self, faculty_id: str):
        raise NotImplementedError

    @abstractmethod
    def save(self, faculty_obj: dict):
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def save_all(self, faculty_list: list):
        raise NotImplementedError
    
    
