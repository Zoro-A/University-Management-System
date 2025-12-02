from abc import ABC, abstractmethod

class INotificationsRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass
