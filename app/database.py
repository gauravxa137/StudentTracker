import sqlite3
import threading
from contextlib import contextmanager

class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.grades = {}

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def update_grade(self, subject, grade):
        """Update existing grade or add new one"""
        self.grades[subject] = grade

    def delete_grade(self, subject):
        """Remove a specific grade"""
        if subject in self.grades:
            del self.grades[subject]
            return True
        return False

    def calculate_average(self):
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0

class StudentTracker:
    def __init__(self):
        self.students = []
        self._lock = threading.Lock()  # Thread safety for database operations
        self.db_name = 'students.db'
        self.init_database()
        self.load_students()

    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections - improves resource management"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.execute('PRAGMA foreign_keys = ON')  # Enable foreign key constraints
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def init_database(self):
        """Initialize database with proper constraints"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Students table with constraints
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL CHECK(LENGTH(name) > 0),
                    roll_number TEXT UNIQUE NOT NULL CHECK(LENGTH(roll_number) > 0)
                )
            ''')
            
            # Grades table with foreign key constraint
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_number TEXT NOT NULL,
                    subject TEXT NOT NULL CHECK(LENGTH(subject) > 0),
                    grade REAL NOT NULL CHECK(grade >= 0 AND grade <= 100),
                    FOREIGN KEY (roll_number) REFERENCES students (roll_number) ON DELETE CASCADE,
                    UNIQUE(roll_number, subject)
                )
            ''')
            conn.commit()

    def load_students(self):
        """Load students from database with improved error handling"""
        with self._lock:
            self.students.clear()
            
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT name, roll_number FROM students ORDER BY name')
                students_data = cursor.fetchall()
                
                for name, roll_number in students_data:
                    student = Student(name, roll_number)
                    cursor.execute(
                        'SELECT subject, grade FROM grades WHERE roll_number=? ORDER BY subject', 
                        (roll_number,)
                    )
                    grades = cursor.fetchall()
                    for subject, grade in grades:
                        student.add_grade(subject, grade)
                    self.students.append(student)

    def add_student(self, name, roll_number):
        """Add student with improved error handling"""
        with self._lock:
            if any(s.roll_number == roll_number for s in self.students):
                return False
            
            try:
                with self.get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'INSERT INTO students (name, roll_number) VALUES (?, ?)', 
                        (name, roll_number)
                    )
                    conn.commit()
                    
                    student = Student(name, roll_number)
                    self.students.append(student)
                    return True
                    
            except sqlite3.IntegrityError:
                return False

    def add_grade(self, roll_number, subject, grade):
        """Add grade with duplicate handling"""
        student = self.get_student(roll_number)
        if not student:
            return False
        
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO grades (roll_number, subject, grade) VALUES (?, ?, ?)',
                    (roll_number, subject, grade)
                )
                conn.commit()
                student.add_grade(subject, grade)
                return True
        except sqlite3.IntegrityError:
            return False  # Duplicate subject for student

    def update_grade(self, roll_number, subject, grade):
        """Update existing grade or create new one"""
        student = self.get_student(roll_number)
        if not student:
            return False
        
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO grades (roll_number, subject, grade) VALUES (?, ?, ?)',
                (roll_number, subject, grade)
            )
            conn.commit()
            student.update_grade(subject, grade)
            return True

    def delete_student(self, roll_number):
        """Delete student and all associated grades"""
        with self._lock:
            student = self.get_student(roll_number)
            if not student:
                return False
            
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM students WHERE roll_number=?', (roll_number,))
                cursor.execute('DELETE FROM grades WHERE roll_number=?', (roll_number,))
                conn.commit()
                
                self.students.remove(student)
                return True

    def delete_grade(self, roll_number, subject):
        """Delete specific grade"""
        student = self.get_student(roll_number)
        if not student or subject not in student.grades:
            return False
        
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM grades WHERE roll_number=? AND subject=?',
                (roll_number, subject)
            )
            conn.commit()
            student.delete_grade(subject)
            return True

    def get_student(self, roll_number):
        """Get student by roll number"""
        for student in self.students:
            if student.roll_number == roll_number:
                return student
        return None
