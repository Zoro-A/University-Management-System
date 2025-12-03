from interfaces.student_repository import IStudentRepository
from utils.database import get_db_connection, get_db_cursor

class PostgresStudentRepository(IStudentRepository):

    def get_by_id(self, student_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT s.user_id, s.name, s.email, s.password,
                          COALESCE(
                              ARRAY_AGG(sc.course_id) FILTER (WHERE sc.course_id IS NOT NULL),
                              ARRAY[]::VARCHAR[]
                          ) as enrolled
                   FROM students s
                   LEFT JOIN student_courses sc ON s.user_id = sc.student_id
                   WHERE s.user_id = %s
                   GROUP BY s.user_id, s.name, s.email, s.password""",
                (student_id,)
            )
            result = cursor.fetchone()
            if result:
                data = dict(result)
                # Convert PostgreSQL array to Python list if needed
                if 'enrolled' in data and isinstance(data['enrolled'], str):
                    # Handle case where array might be returned as string
                    import json
                    try:
                        data['enrolled'] = json.loads(data['enrolled'].replace("'", '"'))
                    except:
                        data['enrolled'] = []
                elif 'enrolled' in data and data['enrolled'] is None:
                    data['enrolled'] = []
                return data
            return None

    def save(self, student_data: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Check if student already exists
            cursor.execute("SELECT user_id FROM students WHERE user_id = %s", (student_data["user_id"],))
            if cursor.fetchone():
                raise ValueError("Student ID already exists")
            
            # Insert student
            cursor.execute(
                "INSERT INTO students (user_id, name, email, password) VALUES (%s, %s, %s, %s)",
                (student_data["user_id"], student_data["name"], student_data["email"], student_data["password"])
            )
            
            # Handle enrolled courses
            enrolled = student_data.get("enrolled", [])
            if enrolled:
                for course_id in enrolled:
                    cursor.execute(
                        "INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (student_data["user_id"], course_id)
                    )
            
            # Note: conn.commit() is handled by the context manager
            return student_data

    def get_all(self):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT s.user_id, s.name, s.email, s.password,
                          COALESCE(
                              ARRAY_AGG(sc.course_id) FILTER (WHERE sc.course_id IS NOT NULL),
                              ARRAY[]::VARCHAR[]
                          ) as enrolled
                   FROM students s
                   LEFT JOIN student_courses sc ON s.user_id = sc.student_id
                   GROUP BY s.user_id, s.name, s.email, s.password"""
            )
            results = cursor.fetchall()
            students = []
            for row in results:
                data = dict(row)
                # Convert PostgreSQL array to Python list if needed
                if 'enrolled' in data and isinstance(data['enrolled'], str):
                    import json
                    try:
                        data['enrolled'] = json.loads(data['enrolled'].replace("'", '"'))
                    except:
                        data['enrolled'] = []
                elif 'enrolled' in data and data['enrolled'] is None:
                    data['enrolled'] = []
                students.append(data)
            return students

    def find_by_id(self, student_id: str):
        return self.get_by_id(student_id)

    def update(self, student_id: str, updated_data: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Check if student exists
            cursor.execute("SELECT user_id FROM students WHERE user_id = %s", (student_id,))
            if not cursor.fetchone():
                raise ValueError("Student not found")
            
            # Build update query dynamically
            updates = []
            params = []
            for key, value in updated_data.items():
                if key != "enrolled" and value is not None:
                    updates.append(f"{key} = %s")
                    params.append(value)
            
            if updates:
                params.append(student_id)
                cursor.execute(
                    f"UPDATE students SET {', '.join(updates)} WHERE user_id = %s",
                    params
                )
            
            # Handle enrolled courses update
            if "enrolled" in updated_data:
                # Delete existing enrollments
                cursor.execute("DELETE FROM student_courses WHERE student_id = %s", (student_id,))
                # Add new enrollments
                for course_id in updated_data["enrolled"]:
                    cursor.execute(
                        "INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)",
                        (student_id, course_id)
                    )
            
            conn.commit()
            
            # Return updated student
            return self.get_by_id(student_id)

    def delete(self, student_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("DELETE FROM students WHERE user_id = %s", (student_id,))
            if cursor.rowcount == 0:
                raise ValueError("Student not found")
            # Note: conn.commit() is handled by the context manager
            return True

