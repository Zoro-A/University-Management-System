from interfaces.notifications_repository import INotificationsRepository
from utils.database import get_db_connection, get_db_cursor

class PostgresNotificationsRepository(INotificationsRepository):

    def get_all(self):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute(
                "SELECT sender, receiver, message, date FROM notifications ORDER BY created_at DESC"
            )
            results = cursor.fetchall()
            # Convert to match expected format (using 'to' and 'from' instead of 'receiver' and 'sender')
            notifications = []
            for row in results:
                notif = dict(row)
                # Map to expected format
                notif["to"] = notif.pop("receiver")
                notif["from"] = notif.pop("sender")
                notifications.append(notif)
            return notifications

    def save_all(self, notifications_list: list):
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Clear all notifications
            cursor.execute("DELETE FROM notifications")
            
            # Insert all notifications
            for notif in notifications_list:
                # Handle both 'to'/'from' and 'receiver'/'sender' formats
                receiver = notif.get("to") or notif.get("receiver", "all")
                sender = notif.get("from") or notif.get("sender")
                message = notif.get("message", "")
                date = notif.get("date")
                
                cursor.execute(
                    "INSERT INTO notifications (sender, receiver, message, date) VALUES (%s, %s, %s, %s)",
                    (sender, receiver, message, date)
                )
            
            # Note: conn.commit() is handled by the context manager
            return True

