# repositories/file_course_repository.py

from interfaces.course_repository import ICourseRepository
from utils.file_manager import read_file, write_file


class FileCourseRepository(ICourseRepository):

    def __init__(self, filepath="courses.txt"):
        self.filepath = filepath

        # Ensures file exists with empty list

    def save(self, course_data: dict):
        courses = read_file(self.filepath)

        # Check duplicate course_id
        if any(c["course_id"] == course_data["course_id"] for c in courses):
            raise ValueError("Course ID already exists")

        courses.append(course_data)
        write_file(self.filepath, courses)
        return course_data

    def get_all(self):
        return read_file(self.filepath)

    def find_by_id(self, course_id: str):
        courses = read_file(self.filepath)
        for course in courses:
            if course["course_id"] == course_id:
                return course
        return None

    def delete(self, course_id: str):
        courses = read_file(self.filepath)
        new_courses = [c for c in courses if c["course_id"] != course_id]

        if len(courses) == len(new_courses):
            raise ValueError("Course not found")

        write_file(self.filepath, new_courses)
        return True

    def update(self, course_id: str, updated_data: dict):
        courses = read_file(self.filepath)
        updated = False

        for i, course in enumerate(courses):
            if course["course_id"] == course_id:
                courses[i] = {**course, **updated_data}
                updated = True
                break

        if not updated:
            raise ValueError("Course not found")

        write_file(self.filepath, courses)
        return courses[i]
