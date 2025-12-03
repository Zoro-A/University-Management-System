"""
Database initialization script
Run this script to create the database schema and optionally migrate data from files.
"""
import os
import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import DB_CONFIG, get_db_connection

def create_database():
    """Create the database if it doesn't exist"""
    # Connect to postgres database to create our database
    temp_config = DB_CONFIG.copy()
    temp_config["database"] = "postgres"
    
    try:
        conn = psycopg2.connect(**temp_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_CONFIG["database"],)
        )
        
        if not cursor.fetchone():
            cursor.execute(f'CREATE DATABASE {DB_CONFIG["database"]}')
            print(f"✓ Database '{DB_CONFIG['database']}' created successfully")
        else:
            print(f"✓ Database '{DB_CONFIG['database']}' already exists")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

def create_schema(force_recreate=False):
    """Create all tables using schema.sql"""
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if tables already exist
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('admin', 'students', 'faculty', 'courses', 'grades')
            """)
            existing_tables = cursor.fetchone()[0]
            
            if existing_tables > 0 and not force_recreate:
                print(f"  ⚠ Found {existing_tables} existing tables in database.")
                response = input("  Do you want to DROP and recreate all tables? This will DELETE ALL DATA! (yes/no): ")
                if response.lower() != 'yes':
                    print("  ✓ Skipping schema creation. Using existing tables.")
                    return
                print("  ⚠ Dropping existing tables...")
            
            cursor.execute(schema_sql)
            conn.commit()
            print("✓ Database schema created successfully")
    except Exception as e:
        print(f"Error creating schema: {e}")
        sys.exit(1)

def migrate_data_from_files(force_overwrite=False):
    """Optionally migrate existing data from JSON files to PostgreSQL"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    
    if not os.path.exists(data_dir):
        print("⚠ No data directory found. Skipping data migration.")
        return
    
    print("\n📦 Migrating data from files to PostgreSQL...")
    
    # Check if data already exists
    if not force_overwrite:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM admin")
                admin_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM students")
                student_count = cursor.fetchone()[0]
                
                if admin_count > 0 or student_count > 0:
                    print(f"  ⚠ Found existing data in database ({admin_count} admins, {student_count} students).")
                    response = input("  Do you want to overwrite existing data? (yes/no): ")
                    if response.lower() != 'yes':
                        print("  ✓ Skipping data migration. Keeping existing data.")
                        return
                    print("  ⚠ Overwriting existing data...")
        except Exception as e:
            # Tables might not exist yet, that's okay
            pass
    
    # Import repositories
    from repositories.postgres_admin_repository import PostgresAdminRepository
    from repositories.postgres_student_repository import PostgresStudentRepository
    from repositories.postgres_faculty_repository import PostgresFacultyRepository
    from repositories.postgres_course_repository import PostgresCourseRepository
    from repositories.postgres_grades_repository import PostgresGradesRepository
    from repositories.postgres_notifications_repository import PostgresNotificationsRepository
    from repositories.postgres_timetable_repository import PostgresTimetableRepository
    
    repos = {
        "admin": PostgresAdminRepository(),
        "students": PostgresStudentRepository(),
        "faculty": PostgresFacultyRepository(),
        "courses": PostgresCourseRepository(),
        "grades": PostgresGradesRepository(),
        "notifications": PostgresNotificationsRepository(),
        "timetable": PostgresTimetableRepository()
    }
    
    # IMPORTANT: Migration order matters because of foreign key constraints.
    # We must insert parent records (courses, students, faculty) before
    # child/related records (enrollments, grades, timetable).
    file_mapping = {
        # Independent tables
        "admin.txt": ("admin", "save"),
        "courses.txt": ("courses", "save"),
        # Depend on courses
        "students.txt": ("students", "save"),
        "faculty.txt": ("faculty", "save"),
        # Depend on students / faculty / courses
        "grades.txt": ("grades", "save_all"),
        "notifications.txt": ("notifications", "save_all"),
        "timetable.txt": ("timetable", "write_all"),
    }
    
    for filename, (repo_key, method) in file_mapping.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                
                repo = repos[repo_key]
                
                # For save_all/write_all methods, clear existing data first if overwriting
                if (method == "save_all" or method == "write_all") and force_overwrite:
                    # Clear existing data
                    if repo_key == "grades":
                        with get_db_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM grades")
                    elif repo_key == "notifications":
                        with get_db_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM notifications")
                    elif repo_key == "timetable":
                        with get_db_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM timetable")
                
                if method == "save_all" or method == "write_all":
                    getattr(repo, method)(data)
                else:
                    for item in data:
                        try:
                            getattr(repo, method)(item)
                        except ValueError as e:
                            # Skip duplicates if not overwriting
                            if "already exists" in str(e) and not force_overwrite:
                                continue
                            raise
                
                print(f"  ✓ Migrated {filename} ({len(data)} records)")
            except Exception as e:
                print(f"  ✗ Error migrating {filename}: {e}")
        else:
            print(f"  ⚠ {filename} not found, skipping")

def main():
    print("🚀 Initializing PostgreSQL Database...\n")
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    create_database()
    
    # Step 2: Create schema
    print("\nStep 2: Creating schema...")
    create_schema()
    
    # Step 3: Migrate data (optional)
    response = input("\nDo you want to migrate existing data from files? (y/n): ")
    if response.lower() == 'y':
        migrate_data_from_files()
    
    print("\n✅ Database initialization complete!")
    print("\nYou can now start your FastAPI application.")
    print("\n💡 Tip: Running this script again will ask before dropping existing tables/data.")

if __name__ == "__main__":
    main()

