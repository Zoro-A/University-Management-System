from abc import ABC, abstractmethod

class ITimetableRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass
