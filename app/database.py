import sqlite3
import logging
import threading
from contextlib import contextmanager
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

class Student:
    """Represents a student with grades tracking"""
    
    def __init__(self, name: str, roll_number: str):
        self.name = name.strip()
        self.roll_number = roll_number.strip()
        self.grades = {}
    
    def add_grade(self, subject: str, grade: float) -> None:
        """Add or update a grade for a subject"""
        self.grades[subject.strip()] = grade
    
    def calculate_average(self) -> float:
        """Calculate the average grade across all subjects"""
        if not self.grades:
            return 0.0
        return round(sum(self.grades.values()) / len(self.grades), 2)
    
    def get_grade_count(self) -> int:
        """Get the number of subjects with grades"""
        return len(self.grades)

class StudentTracker:
    """Manages student records and grades with SQLite backend"""
    
    def __init__(self, db_path: str = 'students.db'):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._initialize_database()
        logger.info(f"StudentTracker initialized with database: {db_path}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _initialize_database(self) -> None:
        """Create database tables if they don't exist - COMPATIBLE WITH EXISTING SCHEMA"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create students table (same as original)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    roll_number TEXT UNIQUE
                )
            ''')
            
            # Create grades table (same as original)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_number TEXT,
                    subject TEXT,
                    grade REAL
                )
            ''')
            
            # Create indexes for better performance (safe to add)
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_roll_number ON students (roll_number)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_grades_roll_number ON grades (roll_number)')
            
            conn.commit()
            logger.info("Database tables initialized successfully")
    
    def add_student(self, name: str, roll_number: str) -> Tuple[bool, str]:
        """Add a new student to the database"""
        with self._lock:
            try:
                name = name.strip()
                roll_number = roll_number.strip()
                
                if not name or not roll_number:
                    return False, "Name and roll number cannot be empty"
                
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'INSERT INTO students (name, roll_number) VALUES (?, ?)',
                        (name, roll_number)
                    )
                    conn.commit()
                    logger.info(f"Student added: {name} ({roll_number})")
                    return True, "Student added successfully"
                    
            except sqlite3.IntegrityError:
                return False, "Roll number already exists"
            except Exception as e:
                logger.error(f"Error adding student: {e}")
                return False, "Database error occurred"
    
    def add_grade(self, roll_number: str, subject: str, grade: float) -> Tuple[bool, str]:
        """Add or update a grade for a student"""
        with self._lock:
            try:
                roll_number = roll_number.strip()
                subject = subject.strip()
                
                if not all([roll_number, subject]):
                    return False, "Roll number and subject cannot be empty"
                
                if not (0 <= grade <= 100):
                    return False, "Grade must be between 0 and 100"
                
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Check if student exists
                    cursor.execute('SELECT 1 FROM students WHERE roll_number = ?', (roll_number,))
                    if not cursor.fetchone():
                        return False, "Student not found"
                    
                    # Check if grade already exists for this subject
                    cursor.execute(
                        'SELECT id FROM grades WHERE roll_number = ? AND subject = ?',
                        (roll_number, subject)
                    )
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Update existing grade
                        cursor.execute(
                            'UPDATE grades SET grade = ? WHERE roll_number = ? AND subject = ?',
                            (grade, roll_number, subject)
                        )
                        action = "updated"
                    else:
                        # Insert new grade
                        cursor.execute(
                            'INSERT INTO grades (roll_number, subject, grade) VALUES (?, ?, ?)',
                            (roll_number, subject, grade)
                        )
                        action = "added"
                    
                    conn.commit()
                    logger.info(f"Grade {action}: {roll_number} - {subject}: {grade}")
                    return True, f"Grade {action} successfully"
                    
            except Exception as e:
                logger.error(f"Error adding grade: {e}")
                return False, "Database error occurred"
    
    def get_student(self, roll_number: str) -> Optional[Student]:
        """Retrieve a student with all their grades"""
        try:
            roll_number = roll_number.strip()
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get student info
                cursor.execute('SELECT name, roll_number FROM students WHERE roll_number = ?', (roll_number,))
                student_data = cursor.fetchone()
                
                if not student_data:
                    return None
                
                # Create student object
                student = Student(student_data[0], student_data[1])
                
                # Get all grades for this student
                cursor.execute('SELECT subject, grade FROM grades WHERE roll_number = ?', (roll_number,))
                grades = cursor.fetchall()
                
                for subject, grade in grades:
                    student.add_grade(subject, grade)
                
                return student
                
        except Exception as e:
            logger.error(f"Error retrieving student {roll_number}: {e}")
            return None
    
    def get_all_students(self) -> List[Student]:
        """Retrieve all students with their grades"""
        try:
            students = []
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get all students
                cursor.execute('SELECT name, roll_number FROM students ORDER BY name')
                students_data = cursor.fetchall()
                
                for name, roll_number in students_data:
                    student = Student(name, roll_number)
                    
                    # Get grades for this student
                    cursor.execute('SELECT subject, grade FROM grades WHERE roll_number = ?', (roll_number,))
                    grades = cursor.fetchall()
                    
                    for subject, grade in grades:
                        student.add_grade(subject, grade)
                    
                    students.append(student)
            
            return students
            
        except Exception as e:
            logger.error(f"Error retrieving all students: {e}")
            return []
    
    def delete_student(self, roll_number: str) -> Tuple[bool, str]:
        """Delete a student and all their grades"""
        with self._lock:
            try:
                roll_number = roll_number.strip()
                
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Delete grades first (no foreign key constraints in original schema)
                    cursor.execute('DELETE FROM grades WHERE roll_number = ?', (roll_number,))
                    
                    # Delete student
                    cursor.execute('DELETE FROM students WHERE roll_number = ?', (roll_number,))
                    
                    if cursor.rowcount == 0:
                        return False, "Student not found"
                    
                    conn.commit()
                    logger.info(f"Student deleted: {roll_number}")
                    return True, "Student deleted successfully"
                    
            except Exception as e:
                logger.error(f"Error deleting student: {e}")
                return False, "Database error occurred"
    
    def get_statistics(self) -> dict:
        """Get basic statistics about the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get student count
                cursor.execute('SELECT COUNT(*) FROM students')
                student_count = cursor.fetchone()[0]
                
                # Get total grades
                cursor.execute('SELECT COUNT(*) FROM grades')
                grade_count = cursor.fetchone()[0]
                
                # Get average grade across all students
                cursor.execute('SELECT AVG(grade) FROM grades')
                overall_average = cursor.fetchone()[0] or 0
                
                return {
                    'total_students': student_count,
                    'total_grades': grade_count,
                    'overall_average': round(overall_average, 2)
                }
                
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {'total_students': 0, 'total_grades': 0, 'overall_average': 0}
