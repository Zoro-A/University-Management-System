from abc import ABC, abstractmethod

class ITimetableRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def write_all(self, timetable_list: list):
        pass
