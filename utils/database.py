"""
Database connection utility for PostgreSQL
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "university_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres")
}

# Connection pool (optional, but recommended for better performance)
_pool = None

def get_pool():
    """Get or create connection pool"""
    global _pool
    if _pool is None:
        _pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            **DB_CONFIG
        )
    return _pool

@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
    """
    pool = get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        pool.putconn(conn)

def get_db_cursor(conn=None):
    """
    Get a cursor with RealDictCursor (returns dict-like rows).
    If conn is None, creates a new connection.
    """
    if conn is None:
        conn = get_db_connection()
        return conn.cursor(cursor_factory=RealDictCursor), conn
    return conn.cursor(cursor_factory=RealDictCursor)

def init_db():
    """
    Initialize database - create tables if they don't exist.
    This should be called once when the application starts.
    """
    # Read and execute schema.sql
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "schema.sql")
    
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()

def test_connection():
    """Test database connection"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"PostgreSQL connection successful! Version: {version[0]}")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

