from interfaces.admin_repository import IAdminRepository
from utils.database import get_db_connection, get_db_cursor

class PostgresAdminRepository(IAdminRepository):

    def get_by_id(self, admin_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT user_id, name, email, password FROM admin WHERE user_id = %s",
                (admin_id,)
            )
            result = cursor.fetchone()
            if result:
                return dict(result)
            return None

    def get_all(self):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT user_id, name, email, password FROM admin")
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def save(self, data: dict):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            # Use INSERT ... ON CONFLICT to handle updates
            cursor.execute(
                """INSERT INTO admin (user_id, name, email, password)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (user_id) 
                   DO UPDATE SET name = EXCLUDED.name, email = EXCLUDED.email, password = EXCLUDED.password""",
                (data["user_id"], data["name"], data["email"], data["password"])
            )
            # Note: conn.commit() is handled by the context manager
            return data

    def delete(self, admin_id: str):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("DELETE FROM admin WHERE user_id = %s", (admin_id,))
            if cursor.rowcount == 0:
                raise ValueError("Admin not found")
            # Note: conn.commit() is handled by the context manager
            return True

