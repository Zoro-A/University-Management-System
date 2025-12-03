"""
Migration script to convert 'year' column to 'semester' in grades table.
Run this script after updating the schema to migrate existing data.
"""
import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_db_connection, get_db_cursor

def migrate_year_to_semester():
    """
    Migrate existing 'year' data to 'semester' format.
    Converts: 2022 -> "Fall 2022", 2023 -> "Spring 2023", etc.
    """
    print("🔄 Migrating 'year' column to 'semester' in grades table...")
    
    try:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            
            # Check if 'year' column exists (for existing databases)
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='grades' AND column_name='year'
            """)
            
            if cursor.fetchone():
                print("  ✓ Found 'year' column, converting to 'semester'...")
                
                # Add semester column if it doesn't exist
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='grades' AND column_name='semester'
                """)
                
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE grades ADD COLUMN semester VARCHAR(50)")
                    print("  ✓ Added 'semester' column")
                
                # Convert year values to semester format
                # Even years -> Fall, Odd years -> Spring
                cursor.execute("""
                    UPDATE grades 
                    SET semester = CASE 
                        WHEN year % 2 = 0 THEN 'Fall ' || year::TEXT
                        ELSE 'Spring ' || year::TEXT
                    END
                    WHERE semester IS NULL AND year IS NOT NULL
                """)
                
                rows_updated = cursor.rowcount
                print(f"  ✓ Converted {rows_updated} records from year to semester")
                
                # Drop the year column
                cursor.execute("ALTER TABLE grades DROP COLUMN IF EXISTS year")
                print("  ✓ Removed 'year' column")
                
                conn.commit()
                print("✅ Migration completed successfully!")
            else:
                print("  ℹ 'year' column not found. Schema may already be updated.")
                print("  ✓ Migration not needed or already completed.")
                
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    migrate_year_to_semester()

