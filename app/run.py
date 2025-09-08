from flask import Flask, render_template, request, redirect, url_for, flash
from database import StudentTracker  # Changed from app.database to database
import os
import sys
import re

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key-change-in-production')

tracker = StudentTracker()

def validate_input(text, pattern=None, max_length=100):
    """Enhanced input validation and sanitization"""
    if not text or len(text.strip()) == 0:
        return False, "Input cannot be empty"
    
    text = text.strip()
    if len(text) > max_length:
        return False, f"Input too long (max {max_length} characters)"
    
    if pattern and not re.match(pattern, text):
        return False, "Input contains invalid characters"
    
    return True, text

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        
        # Enhanced input validation
        name_valid, name_result = validate_input(name, r'^[a-zA-Z\s.]+$', 50)
        roll_valid, roll_result = validate_input(roll_number, r'^[a-zA-Z0-9\-_]+$', 20)
        
        if not name_valid:
            flash(f'Name error: {name_result}', 'danger')
            return render_template('add_student.html')
        
        if not roll_valid:
            flash(f'Roll number error: {roll_result}', 'danger')
            return render_template('add_student.html')
        
        if tracker.add_student(name_result, roll_result):
            flash('Student added successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Roll number already exists.', 'danger')
    
    return render_template('add_student.html')

@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        subject = request.form.get('subject', '').strip()
        grade_str = request.form.get('grade', '').strip()
        
        # Enhanced validation
        roll_valid, roll_result = validate_input(roll_number, r'^[a-zA-Z0-9\-_]+$', 20)
        subject_valid, subject_result = validate_input(subject, r'^[a-zA-Z\s]+$', 30)
        
        if not roll_valid:
            flash(f'Roll number error: {roll_result}', 'danger')
            return render_template('add_grade.html')
        
        if not subject_valid:
            flash(f'Subject error: {subject_result}', 'danger')
            return render_template('add_grade.html')
        
        try:
            grade = float(grade_str)
        except ValueError:
            flash('Grade must be a valid number between 0 and 100.', 'danger')
            return render_template('add_grade.html')

        if 0 <= grade <= 100:
            if tracker.add_grade(roll_result, subject_result, grade):
                flash('Grade added successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Student not found.', 'danger')
        else:
            flash('Grade must be between 0 and 100.', 'danger')
    
    return render_template('add_grade.html')

@app.route('/update_grade', methods=['GET', 'POST'])
def update_grade():
    """New route for updating existing grades"""
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        subject = request.form.get('subject', '').strip()
        grade_str = request.form.get('grade', '').strip()
        
        # Enhanced validation
        roll_valid, roll_result = validate_input(roll_number, r'^[a-zA-Z0-9\-_]+$', 20)
        subject_valid, subject_result = validate_input(subject, r'^[a-zA-Z\s]+$', 30)
        
        if not roll_valid or not subject_valid:
            flash('Invalid input provided.', 'danger')
            return render_template('update_grade.html')
        
        try:
            grade = float(grade_str)
        except ValueError:
            flash('Grade must be a valid number between 0 and 100.', 'danger')
            return render_template('update_grade.html')

        if 0 <= grade <= 100:
            if tracker.update_grade(roll_result, subject_result, grade):
                flash('Grade updated successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Student or subject not found.', 'danger')
        else:
            flash('Grade must be between 0 and 100.', 'danger')
    
    return render_template('update_grade.html')

@app.route('/delete_student/<roll_number>', methods=['POST'])
def delete_student(roll_number):
    """New route for deleting students"""
    if tracker.delete_student(roll_number):
        flash('Student and all associated grades deleted successfully!', 'success')
    else:
        flash('Student not found.', 'danger')
    return redirect(url_for('view_all_students'))

@app.route('/delete_grade', methods=['POST'])
def delete_grade():
    """New route for deleting specific grades"""
    roll_number = request.form.get('roll_number', '').strip()
    subject = request.form.get('subject', '').strip()
    
    if tracker.delete_grade(roll_number, subject):
        flash('Grade deleted successfully!', 'success')
    else:
        flash('Grade not found.', 'danger')
    return redirect(url_for('view_student', roll_number=roll_number))

@app.route('/view_student/<roll_number>')
def view_student(roll_number):
    student = tracker.get_student(roll_number)
    if student:
        return render_template('view_student.html', student=student)
    else:
        flash('Student not found.', 'danger')
        return redirect(url_for('home'))

@app.route('/view_all_students')
def view_all_students():
    students = tracker.students
    return render_template('view_all_students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
