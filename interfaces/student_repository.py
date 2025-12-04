from abc import ABC, abstractmethod

class IStudentRepository(ABC):

    @abstractmethod
    def save(self, student_data: dict):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def find_by_id(self, student_id: str):
        pass

    @abstractmethod
    def update(self, student_id: str, updated_data: dict):
        pass

    @abstractmethod
    def delete(self, student_id: str):
        pass
    
    @abstractmethod
    def get_by_id(self, student_id: str):
        pass
