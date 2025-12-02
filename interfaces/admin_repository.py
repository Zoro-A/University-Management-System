# backend/repositories/interfaces/admin_repository.py

from abc import ABC, abstractmethod


class IAdminRepository(ABC):

    @abstractmethod
    def get_by_id(self, admin_id: str):
        pass

    @abstractmethod
    def save(self, data: dict):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete(self, admin_id: str):
        pass
