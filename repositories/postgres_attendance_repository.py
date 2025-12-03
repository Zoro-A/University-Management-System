from interfaces.attendance_repository import IAttendanceRepository
from utils.database import get_db_connection, get_db_cursor
from datetime import datetime

class PostgresAttendanceRepository(IAttendanceRepository):

    def save(self, attendance_record: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """INSERT INTO attendance (student_id, course_id, faculty_id, date, status)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (student_id, course_id, date)
                   DO UPDATE SET status = EXCLUDED.status, updated_at = CURRENT_TIMESTAMP""",
                (
                    attendance_record["student_id"],
                    attendance_record["course_id"],
                    attendance_record.get("faculty_id"),
                    attendance_record.get("date") or datetime.now().date(),
                    attendance_record.get("status", "Present")
                )
            )
            # Note: conn.commit() is handled by the context manager
            return attendance_record

    def get_attendance_for_student_course(self, student_id: str, course_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT student_id, course_id, date, status, faculty_id
                   FROM attendance
                   WHERE student_id = %s AND course_id = %s
                   ORDER BY date DESC""",
                (student_id, course_id)
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def get_attendance_for_course_date(self, course_id: str, date: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT student_id, course_id, date, status, faculty_id
                   FROM attendance
                   WHERE course_id = %s AND date = %s
                   ORDER BY student_id""",
                (course_id, date)
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def get_attendance_for_student(self, student_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT student_id, course_id, date, status, faculty_id
                   FROM attendance
                   WHERE student_id = %s
                   ORDER BY date DESC, course_id""",
                (student_id,)
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def update_attendance(self, student_id: str, course_id: str, date: str, status: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """UPDATE attendance
                   SET status = %s, updated_at = CURRENT_TIMESTAMP
                   WHERE student_id = %s AND course_id = %s AND date = %s""",
                (status, student_id, course_id, date)
            )
            if cursor.rowcount == 0:
                raise ValueError("Attendance record not found")
            # Note: conn.commit() is handled by the context manager
            return True

