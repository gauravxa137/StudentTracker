import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify  # Add to imports
from database import StudentTracker
from flask import Flask, render_template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key') 

# Use environment variable for secret key with fallback for development
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize tracker with error handling
try:
    tracker = StudentTracker()
    logger.info("StudentTracker initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize StudentTracker: {e}")
    raise

@app.route('/')
def home():
    """Homepage route"""
    return render_template('home.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add new student with validation"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            roll_number = request.form.get('roll_number', '').strip()
            
            # Input validation
            if not name or not roll_number:
                flash('Name and roll number are required.', 'danger')
                return render_template('add_student.html')
            
            if len(name) > 100 or len(roll_number) > 20:
                flash('Name or roll number too long.', 'danger')
                return render_template('add_student.html')
            
            # Attempt to add student
            success, message = tracker.add_student(name, roll_number)
            if success:
                flash('Student added successfully!', 'success')
                logger.info(f"Student added: {name} ({roll_number})")
                return redirect(url_for('home'))
            else:
                flash(message, 'danger')
                
        except Exception as e:
            logger.error(f"Error adding student: {e}")
            flash('An error occurred while adding the student.', 'danger')
    
    return render_template('add_student.html')

@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    """Add grade with comprehensive validation"""
    if request.method == 'POST':
        try:
            roll_number = request.form.get('roll_number', '').strip()
            subject = request.form.get('subject', '').strip()
            grade_str = request.form.get('grade', '').strip()
            
            # Input validation
            if not all([roll_number, subject, grade_str]):
                flash('All fields are required.', 'danger')
                return render_template('add_grade.html')
            
            if len(subject) > 50:
                flash('Subject name too long.', 'danger')
                return render_template('add_grade.html')
            
            # Parse and validate grade
            try:
                grade = float(grade_str)
            except ValueError:
                flash('Grade must be a valid number.', 'danger')
                return render_template('add_grade.html')
            
            if not (0 <= grade <= 100):
                flash('Grade must be between 0 and 100.', 'danger')
                return render_template('add_grade.html')
            
            # Attempt to add grade
            success, message = tracker.add_grade(roll_number, subject, grade)
            if success:
                flash('Grade added successfully!', 'success')
                logger.info(f"Grade added: {roll_number} - {subject}: {grade}")
                return redirect(url_for('home'))
            else:
                flash(message, 'danger')
                
        except Exception as e:
            logger.error(f"Error adding grade: {e}")
            flash('An error occurred while adding the grade.', 'danger')
    
    return render_template('add_grade.html')

@app.route('/view_student/<roll_number>')  # Fixed: Added URL parameter
def view_student(roll_number):
    """View individual student details"""
    try:
        roll_number = roll_number.strip()
        student = tracker.get_student(roll_number)
        
        if student:
            return render_template('view_student.html', student=student)
        else:
            flash('Student not found.', 'danger')
            logger.warning(f"Student not found: {roll_number}")
            return redirect(url_for('home'))
            
    except Exception as e:
        logger.error(f"Error viewing student {roll_number}: {e}")
        flash('An error occurred while retrieving student information.', 'danger')
        return redirect(url_for('home'))

@app.route('/view_all_students')
def view_all_students():
    """View all students"""
    try:
        students = tracker.get_all_students()
        return render_template('view_all_students.html', students=students)
    except Exception as e:
        logger.error(f"Error viewing all students: {e}")
        flash('An error occurred while retrieving student list.', 'danger')
        return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    flash('Page not found.', 'danger')
    return redirect(url_for('home'))

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    flash('An internal error occurred. Please try again.', 'danger')
    return redirect(url_for('home'))




# Add this route
@app.route('/api/statistics')
def api_statistics():
    """API endpoint for system statistics"""
    try:
        stats = tracker.get_statistics()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")
        return jsonify({
            'total_students': 0,
            'total_grades': 0,
            'overall_average': 0,
            'error': 'Failed to load statistics'
        }), 500


@app.route('/delete_student/<roll_number>', methods=['POST'])
def delete_student_route(roll_number):
    """Delete a student and all their grades"""
    try:
        success, message = tracker.delete_student(roll_number)
        if success:
            flash('Student deleted successfully!', 'success')
            logger.info(f"Student deleted: {roll_number}")
        else:
            flash(message, 'danger')
        return redirect(url_for('view_all_students'))
    except Exception as e:
        logger.error(f"Error deleting student: {e}")
        flash('An error occurred while deleting the student.', 'danger')
        return redirect(url_for('view_all_students'))

if __name__ == '__main__':
    # Only enable debug mode if explicitly set
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting Flask app on port {port}, debug={debug_mode}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

