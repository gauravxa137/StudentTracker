from flask import Flask, render_template, request, redirect, url_for, flash
from app.database import StudentTracker
import os
import sys
print(sys.path)

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

tracker = StudentTracker()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        if tracker.add_student(name, roll_number):
            flash('Student added successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Roll number already exists.', 'danger')
    return render_template('add_student.html')

@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        subject = request.form['subject']
        try:
            grade = float(request.form['grade'])
        except ValueError:
            flash('Grade must be a number between 0 and 100.', 'danger')
            return redirect(url_for('add_grade'))

        if 0 <= grade <= 100:
            if tracker.add_grade(roll_number, subject, grade):
                flash('Grade added successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Student not found.', 'danger')
        else:
            flash('Grade must be between 0 and 100.', 'danger')
    return render_template('add_grade.html')

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
