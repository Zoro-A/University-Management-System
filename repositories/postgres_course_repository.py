from interfaces.course_repository import ICourseRepository
from utils.database import get_db_connection, get_db_cursor

class PostgresCourseRepository(ICourseRepository):

    def save(self, course_data: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Check if course already exists
            cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_data["course_id"],))
            if cursor.fetchone():
                raise ValueError("Course ID already exists")
            
            # Insert course
            cursor.execute(
                """INSERT INTO courses (course_id, course_name, credits, prerequisites)
                   VALUES (%s, %s, %s, %s)""",
                (
                    course_data["course_id"],
                    course_data["course_name"],
                    int(course_data.get("credits", 0)),
                    course_data.get("prerequisites") or None
                )
            )
            
            # Handle eligible_faculty (many-to-many relationship)
            eligible_faculty = course_data.get("eligible_faculty", [])
            for faculty_id in eligible_faculty:
                cursor.execute(
                    "INSERT INTO faculty_courses (faculty_id, course_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (faculty_id, course_data["course_id"])
                )
            
            # Note: conn.commit() is handled by the context manager
            return course_data

    def get_all(self):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT c.course_id, c.course_name, c.credits, c.prerequisites,
                          COALESCE(
                              ARRAY_AGG(fc.faculty_id) FILTER (WHERE fc.faculty_id IS NOT NULL),
                              ARRAY[]::VARCHAR[]
                          ) as eligible_faculty
                   FROM courses c
                   LEFT JOIN faculty_courses fc ON c.course_id = fc.course_id
                   GROUP BY c.course_id, c.course_name, c.credits, c.prerequisites"""
            )
            results = cursor.fetchall()
            courses = []
            for row in results:
                course = dict(row)
                # Convert credits to string if needed for compatibility
                if course.get("credits"):
                    course["credits"] = str(course["credits"])
                # Convert PostgreSQL array to Python list if needed
                if 'eligible_faculty' in course and isinstance(course['eligible_faculty'], str):
                    import json
                    try:
                        course['eligible_faculty'] = json.loads(course['eligible_faculty'].replace("'", '"'))
                    except:
                        course['eligible_faculty'] = []
                elif 'eligible_faculty' in course and course['eligible_faculty'] is None:
                    course['eligible_faculty'] = []
                courses.append(course)
            return courses

    def find_by_id(self, course_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT c.course_id, c.course_name, c.credits, c.prerequisites,
                          COALESCE(
                              ARRAY_AGG(fc.faculty_id) FILTER (WHERE fc.faculty_id IS NOT NULL),
                              ARRAY[]::VARCHAR[]
                          ) as eligible_faculty
                   FROM courses c
                   LEFT JOIN faculty_courses fc ON c.course_id = fc.course_id
                   WHERE c.course_id = %s
                   GROUP BY c.course_id, c.course_name, c.credits, c.prerequisites""",
                (course_id,)
            )
            result = cursor.fetchone()
            if result:
                course = dict(result)
                if course.get("credits"):
                    course["credits"] = str(course["credits"])
                # Convert PostgreSQL array to Python list if needed
                if 'eligible_faculty' in course and isinstance(course['eligible_faculty'], str):
                    import json
                    try:
                        course['eligible_faculty'] = json.loads(course['eligible_faculty'].replace("'", '"'))
                    except:
                        course['eligible_faculty'] = []
                elif 'eligible_faculty' in course and course['eligible_faculty'] is None:
                    course['eligible_faculty'] = []
                return course
            return None

    def delete(self, course_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
            if cursor.rowcount == 0:
                raise ValueError("Course not found")
            # Note: conn.commit() is handled by the context manager
            return True

    def update(self, course_id: str, updated_data: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Check if course exists
            cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
            if not cursor.fetchone():
                raise ValueError("Course not found")
            
            # Build update query
            updates = []
            params = []
            
            if "course_name" in updated_data:
                updates.append("course_name = %s")
                params.append(updated_data["course_name"])
            
            if "credits" in updated_data:
                updates.append("credits = %s")
                params.append(int(updated_data["credits"]))
            
            if "prerequisites" in updated_data:
                updates.append("prerequisites = %s")
                params.append(updated_data["prerequisites"] or None)
            
            if updates:
                params.append(course_id)
                cursor.execute(
                    f"UPDATE courses SET {', '.join(updates)} WHERE course_id = %s",
                    params
                )
            
            # Handle eligible_faculty update
            if "eligible_faculty" in updated_data:
                # Delete existing faculty assignments
                cursor.execute("DELETE FROM faculty_courses WHERE course_id = %s", (course_id,))
                # Add new assignments
                for faculty_id in updated_data["eligible_faculty"]:
                    cursor.execute(
                        "INSERT INTO faculty_courses (faculty_id, course_id) VALUES (%s, %s)",
                        (faculty_id, course_id)
                    )
            
            # Note: conn.commit() is handled by the context manager
            
            # Return updated course
            return self.find_by_id(course_id)

