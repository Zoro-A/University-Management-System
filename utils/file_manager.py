# 📂 utils/file_manager.py
import json
import os

class FileManager:
    @staticmethod
    def read_file(filename):
        if not os.path.exists(filename):
            return []
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def write_file(filename, data):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def append_record(filename, record):
        data = FileManager.read_file(filename)
        data.append(record)
        FileManager.write_file(filename, data)
