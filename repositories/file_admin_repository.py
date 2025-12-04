# backend/repositories/file_admin_repository.py

from interfaces.admin_repository import IAdminRepository
from utils.file_manager import read_file, write_file

ADMIN_FILE = "admin.txt"


class FileAdminRepository(IAdminRepository):

    def get_by_id(self, admin_id: str):
        items = read_file(ADMIN_FILE)
        return next((x for x in items if x["user_id"] == admin_id), None)

    def get_all(self):
        return read_file(ADMIN_FILE)

    def save(self, data: dict):
        items = read_file(ADMIN_FILE)

        # remove existing record
        items = [i for i in items if i["user_id"] != data["user_id"]]
        items.append(data)

        write_file(ADMIN_FILE, items)

    def delete(self, admin_id: str):
        items = read_file(ADMIN_FILE)
        items = [i for i in items if i["user_id"] != admin_id]
        write_file(ADMIN_FILE, items)
