# models/user.py
from utils.file_manager import FileManager

class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def authenticate(filename, email, password):
        data = FileManager.read_file(filename)
        for entry in data:
            if entry.get("email") == email and entry.get("password") == password:
                return entry
        return None
