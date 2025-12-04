from interfaces.timetable_repository import ITimetableRepository
from utils.database import get_db_connection, get_db_cursor

class PostgresTimetableRepository(ITimetableRepository):

    def get_all(self):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                """SELECT course_id, course_name, faculty_id, faculty_name, day, slot, room
                   FROM timetable
                   ORDER BY day, slot, course_id"""
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def write_all(self, timetable_list: list):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Clear all timetable entries
            cursor.execute("DELETE FROM timetable")
            
            # Insert all timetable entries
            for entry in timetable_list:
                cursor.execute(
                    """INSERT INTO timetable (course_id, course_name, faculty_id, faculty_name, day, slot, room)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        entry.get("course_id"),
                        entry.get("course_name", ""),
                        entry.get("faculty_id"),
                        entry.get("faculty_name"),
                        entry.get("day"),
                        entry.get("slot"),
                        entry.get("room")
                    )
                )
            
            # Note: conn.commit() is handled by the context manager
            return True

