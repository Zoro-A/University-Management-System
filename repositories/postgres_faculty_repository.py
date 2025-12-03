from interfaces.faculty_repository import IFacultyRepository
from utils.database import get_db_connection, get_db_cursor

class PostgresFacultyRepository(IFacultyRepository):

    def get_by_id(self, faculty_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT f.user_id, f.name, f.email, f.password,
                          COALESCE(
                              ARRAY_AGG(fc.course_id) FILTER (WHERE fc.course_id IS NOT NULL),
                              ARRAY[]::VARCHAR[]
                          ) as courses
                   FROM faculty f
                   LEFT JOIN faculty_courses fc ON f.user_id = fc.faculty_id
                   WHERE f.user_id = %s
                   GROUP BY f.user_id, f.name, f.email, f.password""",
                (faculty_id,)
            )
            result = cursor.fetchone()
            if result:
                data = dict(result)
                # Convert PostgreSQL array to Python list if needed
                if 'courses' in data and isinstance(data['courses'], str):
                    import json
                    try:
                        data['courses'] = json.loads(data['courses'].replace("'", '"'))
                    except:
                        data['courses'] = []
                elif 'courses' in data and data['courses'] is None:
                    data['courses'] = []
                return data
            return None

    def save(self, faculty_obj: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Check if faculty already exists
            cursor.execute("SELECT user_id FROM faculty WHERE user_id = %s", (faculty_obj["user_id"],))
            if cursor.fetchone():
                # Update existing
                cursor.execute(
                    "UPDATE faculty SET name = %s, email = %s, password = %s WHERE user_id = %s",
                    (faculty_obj["name"], faculty_obj["email"], faculty_obj["password"], faculty_obj["user_id"])
                )
            else:
                # Insert new
                cursor.execute(
                    "INSERT INTO faculty (user_id, name, email, password) VALUES (%s, %s, %s, %s)",
                    (faculty_obj["user_id"], faculty_obj["name"], faculty_obj["email"], faculty_obj["password"])
                )
            
            # Handle courses
            courses = faculty_obj.get("courses", [])
            # Delete existing course assignments
            cursor.execute("DELETE FROM faculty_courses WHERE faculty_id = %s", (faculty_obj["user_id"],))
            # Add new course assignments
            for course_id in courses:
                cursor.execute(
                    "INSERT INTO faculty_courses (faculty_id, course_id) VALUES (%s, %s)",
                    (faculty_obj["user_id"], course_id)
                )
            
            # Note: conn.commit() is handled by the context manager
            return faculty_obj

    def get_all(self):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT f.user_id, f.name, f.email, f.password,
                          COALESCE(
                              ARRAY_AGG(fc.course_id) FILTER (WHERE fc.course_id IS NOT NULL),
                              ARRAY[]::VARCHAR[]
                          ) as courses
                   FROM faculty f
                   LEFT JOIN faculty_courses fc ON f.user_id = fc.faculty_id
                   GROUP BY f.user_id, f.name, f.email, f.password"""
            )
            results = cursor.fetchall()
            faculty_list = []
            for row in results:
                data = dict(row)
                # Convert PostgreSQL array to Python list if needed
                if 'courses' in data and isinstance(data['courses'], str):
                    import json
                    try:
                        data['courses'] = json.loads(data['courses'].replace("'", '"'))
                    except:
                        data['courses'] = []
                elif 'courses' in data and data['courses'] is None:
                    data['courses'] = []
                faculty_list.append(data)
            return faculty_list

    def save_all(self, faculty_list: list):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Clear all faculty and their course assignments
            cursor.execute("DELETE FROM faculty_courses")
            cursor.execute("DELETE FROM faculty")
            
            # Insert all faculty
            for faculty_obj in faculty_list:
                cursor.execute(
                    "INSERT INTO faculty (user_id, name, email, password) VALUES (%s, %s, %s, %s)",
                    (faculty_obj["user_id"], faculty_obj["name"], faculty_obj["email"], faculty_obj["password"])
                )
                
                # Add course assignments
                courses = faculty_obj.get("courses", [])
                for course_id in courses:
                    cursor.execute(
                        "INSERT INTO faculty_courses (faculty_id, course_id) VALUES (%s, %s)",
                        (faculty_obj["user_id"], course_id)
                    )
            
            # Note: conn.commit() is handled by the context manager
            return True

    def delete(self, faculty_id: str):
        """
        Delete a faculty member by user_id.
        Related rows in faculty_courses are removed automatically
        via ON DELETE CASCADE; timetable rows will have faculty_id
        set to NULL via ON DELETE SET NULL.
        """
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("DELETE FROM faculty WHERE user_id = %s", (faculty_id,))
            if cursor.rowcount == 0:
                raise ValueError("Faculty not found")
            # Commit is handled by the context manager
            return True

