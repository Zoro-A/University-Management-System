# utils/file_manager.py
import json
import os
import shutil

class FileManager:
    @staticmethod
    def ensure_file(filename):
        dirpath = os.path.dirname(filename)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                f.write("[]")

    @staticmethod
    def read_file(filename):
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def write_file(filename, data):
        dirpath = os.path.dirname(filename)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def append_record(filename, record):
        data = FileManager.read_file(filename)
        data.append(record)
        FileManager.write_file(filename, data)

    @staticmethod
    def backup_folder(src_folder, dest_folder):
        os.makedirs(dest_folder, exist_ok=True)
        for name in os.listdir(src_folder):
            full = os.path.join(src_folder, name)
            if os.path.isfile(full):
                shutil.copy(full, dest_folder)
