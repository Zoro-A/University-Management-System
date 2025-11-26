import json
import os
import shutil

# -----------------------------------------
# BASE PROJECT DIRECTORY
# utils/file_manager.py → go one level up → project root
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------------------
# DATA DIRECTORY INSIDE PROJECT ROOT
# Example: D:/University-Management-System/data
# -----------------------------------------
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------------------
# READ JSON FILE
# -----------------------------------------
def read_file(path):
    full_path = os.path.join(DATA_DIR, path)

    if not os.path.exists(full_path):
        return []

    try:
        with open(full_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON in {full_path}")
        return []


# -----------------------------------------
# WRITE JSON FILE
# -----------------------------------------
def write_file(path, data):
    full_path = os.path.join(DATA_DIR, path)
    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------------
# APPEND TO JSON FILE
# -----------------------------------------
def append_record(path, record):
    data = read_file(path)

    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")

    data.append(record)
    write_file(path, data)


# -----------------------------------------
# UPDATE RECORD
# -----------------------------------------
def update_record(path, key, value, new_data: dict):
    data = read_file(path)
    updated = False

    for item in data:
        if item.get(key) == value:
            item.update(new_data)
            updated = True
            break

    if updated:
        write_file(path, data)

    return updated


# -----------------------------------------
# DELETE RECORD
# -----------------------------------------
def delete_record(path, key, value):
    data = read_file(path)
    data = [item for item in data if item.get(key) != value]
    write_file(path, data)
    return True
