import sqlite3

class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.grades = {}

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def calculate_average(self):
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0

class StudentTracker:
    def __init__(self):
        self.students = []
        self.load_students()

    def create_connection(self):
        conn = sqlite3.connect('students.db')
        return conn

    def load_students(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                roll_number TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT,
                subject TEXT,
                grade REAL
            )
        ''')
        conn.commit()

        cursor.execute('SELECT name, roll_number FROM students')
        students_data = cursor.fetchall()
        for name, roll_number in students_data:
            student = Student(name, roll_number)
            cursor.execute('SELECT subject, grade FROM grades WHERE roll_number=?', (roll_number,))
            grades = cursor.fetchall()
            for subject, grade in grades:
                student.add_grade(subject, grade)
            self.students.append(student)
        conn.close()

    def add_student(self, name, roll_number):
        if any(s.roll_number == roll_number for s in self.students):
            return False
        student = Student(name, roll_number)
        self.students.append(student)

        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, roll_number) VALUES (?, ?)', (name, roll_number))
        conn.commit()
        conn.close()
        return True

    def add_grade(self, roll_number, subject, grade):
        student = self.get_student(roll_number)
        if student:
            student.add_grade(subject, grade)

            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO grades (roll_number, subject, grade) VALUES (?, ?, ?)', (roll_number, subject, grade))
            conn.commit()
            conn.close()
            return True
        return False

    def get_student(self, roll_number):
        for student in self.students:
            if student.roll_number == roll_number:
                return student
        return None
