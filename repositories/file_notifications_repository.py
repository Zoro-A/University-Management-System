# repositories/file_notifications_repository.py
from interfaces.notifications_repository import INotificationsRepository
from utils.file_manager import read_file, write_file

NOTIF_FILE = "notifications.txt"

class FileNotificationsRepository(INotificationsRepository):

    def get_all(self):
        return read_file(NOTIF_FILE)

    def save_all(self, notifications_list: list):
        write_file(NOTIF_FILE, notifications_list)
        return True

    def add_notification(self, note: dict):
        notes = read_file(NOTIF_FILE)
        notes.append(note)
        write_file(NOTIF_FILE, notes)
