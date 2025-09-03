import sqlite3
import os

def upgrade_database():
    """Apply database optimizations"""
    db_path = 'students.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_grades_roll_number ON grades(roll_number);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_roll_number ON students(roll_number);')
        
        # Add created_at columns if they don't exist
        try:
            cursor.execute('ALTER TABLE students ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        try:
            cursor.execute('ALTER TABLE grades ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Add constraints (SQLite doesn't support adding constraints to existing tables easily)
        # So we'll handle validation in the application layer
        
        conn.commit()
        print("Database optimizations applied successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error applying database optimizations: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    upgrade_database()
