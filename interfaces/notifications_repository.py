from abc import ABC, abstractmethod

class INotificationsRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save_all(self, notifications_list: list):
        pass
