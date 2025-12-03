from interfaces.grades_repository import IGradeRepository
from utils.database import get_db_connection, get_db_cursor

class PostgresGradesRepository(IGradeRepository):

    def get_all(self):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT student_id, course_id, grade, year FROM grades ORDER BY year DESC, student_id, course_id"
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def save(self, grade_record: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """INSERT INTO grades (student_id, course_id, grade, year)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (student_id, course_id)
                   DO UPDATE SET grade = EXCLUDED.grade, year = EXCLUDED.year, updated_at = CURRENT_TIMESTAMP""",
                (
                    grade_record["student_id"],
                    grade_record["course_id"],
                    grade_record["grade"],
                    grade_record.get("year")
                )
            )
            # Note: conn.commit() is handled by the context manager
            return grade_record

    def save_all(self, grades_list: list):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Clear all grades
            cursor.execute("DELETE FROM grades")
            
            # Insert all grades
            for grade_record in grades_list:
                cursor.execute(
                    "INSERT INTO grades (student_id, course_id, grade, year) VALUES (%s, %s, %s, %s)",
                    (
                        grade_record["student_id"],
                        grade_record["course_id"],
                        grade_record["grade"],
                        grade_record.get("year")
                    )
                )
            
            # Note: conn.commit() is handled by the context manager
            return True

    def find_grades_for_student(self, student_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT student_id, course_id, grade, year FROM grades WHERE student_id = %s ORDER BY year DESC, course_id",
                (student_id,)
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def find_grades_for_course(self, course_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT student_id, course_id, grade, year FROM grades WHERE course_id = %s ORDER BY student_id, year DESC",
                (course_id,)
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

