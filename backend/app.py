from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Student, Teacher, Admin, Subject, Marks
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize extensions
db.init_app(app)
CORS(app)

# ==================== INITIALIZATION ====================
@app.before_request
def init_db():
    if not os.path.exists(os.path.join(basedir, 'database.db')):
        with app.app_context():
            db.create_all()
            # Add default admin
            admin = Admin.query.filter_by(admin_id='admin1').first()
            if not admin:
                admin = Admin(admin_id='admin1', name='Admin User', password='admin123', email='admin@school.com')
                db.session.add(admin)
                
                # Add sample subjects
                subjects = [
                    Subject(subject_name='SOFTWARE TESTING', subject_code='316314', max_marks=150),
                    Subject(subject_name='MANAGEMENT', subject_code='315301', max_marks=125),
                    Subject(subject_name='EMERGING TRENDS', subject_code='316313', max_marks=125),
                    Subject(subject_name='CLIENT SIDE SCRIPTING', subject_code='316005', max_marks=50),
                    Subject(subject_name='MOBILE APPLICATION DEVELOPMENT', subject_code='316006', max_marks=75),
                    Subject(subject_name='CAPSTONE PROJECT', subject_code='316004', max_marks=150),
                    Subject(subject_name='DIGITAL FORENSICS AND HACKING TECHNIQUES', subject_code='316315', max_marks=175),
                ]
                for subject in subjects:
                    db.session.add(subject)
                db.session.commit()

# ==================== STUDENT ROUTES ====================
@app.route('/api/student/login', methods=['POST'])
def student_login():
    data = request.json
    roll_no = data.get('roll_no')
    password = data.get('password')
    
    student = Student.query.filter_by(roll_no=roll_no, password=password).first()
    
    if student:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'student_id': student.id,
            'student_name': student.name,
            'roll_no': student.roll_no,
            'class': student.class_name
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/student/results/<int:student_id>', methods=['GET'])
def get_student_results(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    marks = Marks.query.filter_by(student_id=student_id).all()
    
    if not marks:
        return jsonify({'success': False, 'message': 'No marks found'}), 404
    
    total_marks = 0
    max_marks = 0
    results = []
    
    for mark in marks:
        total_marks += mark.marks_obtained
        max_marks += mark.subject.max_marks
        results.append({
            'subject': mark.subject.subject_name,
            'marks': mark.marks_obtained,
            'max_marks': mark.subject.max_marks
        })
    
    percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
    
    # Grade calculation
    if percentage >= 90:
        grade = 'A+'
    elif percentage >= 80:
        grade = 'A'
    elif percentage >= 70:
        grade = 'B+'
    elif percentage >= 60:
        grade = 'B'
    elif percentage >= 50:
        grade = 'C'
    elif percentage >= 40:
        grade = 'D'
    else:
        grade = 'F'
    
    status = 'Pass' if percentage >= 40 else 'Fail'
    
    return jsonify({
        'success': True,
        'student_name': student.name,
        'roll_no': student.roll_no,
        'class': student.class_name,
        'results': results,
        'total_marks': total_marks,
        'max_marks': max_marks,
        'percentage': round(percentage, 2),
        'grade': grade,
        'status': status
    }), 200

# ==================== TEACHER ROUTES ====================
@app.route('/api/teacher/login', methods=['POST'])
def teacher_login():
    data = request.json
    teacher_id = data.get('teacher_id')
    password = data.get('password')
    
    teacher = Teacher.query.filter_by(teacher_id=teacher_id, password=password).first()
    
    if teacher:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'teacher_id': teacher.id,
            'teacher_name': teacher.name,
            'subject': teacher.subject
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/teacher/students', methods=['GET'])
def get_students_for_teacher():
    students = Student.query.all()
    
    student_list = [{
        'id': s.id,
        'roll_no': s.roll_no,
        'name': s.name,
        'class': s.class_name
    } for s in students]
    
    return jsonify({
        'success': True,
        'students': student_list
    }), 200

@app.route('/api/teacher/enter-marks', methods=['POST'])
def enter_marks():
    data = request.json
    student_id = data.get('student_id')
    teacher_id = data.get('teacher_id')
    subject_id = data.get('subject_id')
    marks_obtained = data.get('marks_obtained')
    
    # Get subject to validate marks
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'success': False, 'message': 'Subject not found'}), 404
    
    # Validation - marks must be between 0 and subject's max_marks
    if marks_obtained < 0 or marks_obtained > subject.max_marks:
        return jsonify({'success': False, 'message': f'Marks must be between 0 and {subject.max_marks}'}), 400
    
    # Check if mark already exists
    existing_mark = Marks.query.filter_by(
        student_id=student_id,
        teacher_id=teacher_id,
        subject_id=subject_id
    ).first()
    
    if existing_mark:
        existing_mark.marks_obtained = marks_obtained
        existing_mark.date_updated = datetime.utcnow()
    else:
        mark = Marks(
            student_id=student_id,
            teacher_id=teacher_id,
            subject_id=subject_id,
            marks_obtained=marks_obtained
        )
        db.session.add(mark)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Marks saved successfully'
    }), 201

@app.route('/api/teacher/marks/<int:teacher_id>', methods=['GET'])
def get_teacher_marks(teacher_id):
    marks = Marks.query.filter_by(teacher_id=teacher_id).all()
    
    marks_list = [mark.to_dict() for mark in marks]
    
    return jsonify({
        'success': True,
        'marks': marks_list
    }), 200

# ==================== ADMIN ROUTES ====================
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    admin_id = data.get('admin_id')
    password = data.get('password')
    
    admin = Admin.query.filter_by(admin_id=admin_id, password=password).first()
    
    if admin:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'admin_id': admin.id,
            'admin_name': admin.name
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# Add Student
@app.route('/api/admin/add-student', methods=['POST'])
def add_student():
    data = request.json
    
    existing = Student.query.filter_by(roll_no=data.get('roll_no')).first()
    if existing:
        return jsonify({'success': False, 'message': 'Roll no already exists'}), 400
    
    student = Student(
        roll_no=data.get('roll_no'),
        name=data.get('name'),
        password=data.get('password'),
        class_name=data.get('class_name'),
        email=data.get('email')
    )
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Student added successfully'}), 201

# Add Teacher
@app.route('/api/admin/add-teacher', methods=['POST'])
def add_teacher():
    data = request.json
    
    existing = Teacher.query.filter_by(teacher_id=data.get('teacher_id')).first()
    if existing:
        return jsonify({'success': False, 'message': 'Teacher ID already exists'}), 400
    
    teacher = Teacher(
        teacher_id=data.get('teacher_id'),
        name=data.get('name'),
        password=data.get('password'),
        subject=data.get('subject'),
        email=data.get('email')
    )
    db.session.add(teacher)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Teacher added successfully'}), 201

# Get all students
@app.route('/api/admin/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    
    student_list = [{
        'id': s.id,
        'roll_no': s.roll_no,
        'name': s.name,
        'class': s.class_name,
        'email': s.email
    } for s in students]
    
    return jsonify({'success': True, 'students': student_list}), 200

# Get all teachers
@app.route('/api/admin/teachers', methods=['GET'])
def get_all_teachers():
    teachers = Teacher.query.all()
    
    teacher_list = [{
        'id': t.id,
        'teacher_id': t.teacher_id,
        'name': t.name,
        'subject': t.subject,
        'email': t.email
    } for t in teachers]
    
    return jsonify({'success': True, 'teachers': teacher_list}), 200

# Delete student
@app.route('/api/admin/delete-student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    # Delete related marks
    Marks.query.filter_by(student_id=student_id).delete()
    db.session.delete(student)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Student deleted successfully'}), 200

# Delete teacher
@app.route('/api/admin/delete-teacher/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    
    if not teacher:
        return jsonify({'success': False, 'message': 'Teacher not found'}), 404
    
    # Delete related marks
    Marks.query.filter_by(teacher_id=teacher_id).delete()
    db.session.delete(teacher)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Teacher deleted successfully'}), 200

# Get subjects
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    
    subject_list = [{
        'id': s.id,
        'name': s.subject_name,
        'code': s.subject_code,
        'max_marks': s.max_marks
    } for s in subjects]
    
    return jsonify({'success': True, 'subjects': subject_list}), 200

# Get all results (Admin)
@app.route('/api/admin/all-results', methods=['GET'])
def admin_all_results():
    students = Student.query.all()
    all_results = []
    
    for student in students:
        marks = Marks.query.filter_by(student_id=student.id).all()
        
        if marks:
            total_marks = sum(m.marks_obtained for m in marks)
            max_marks = sum(m.subject.max_marks for m in marks)
            percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
            
            if percentage >= 40:
                status = 'Pass'
            else:
                status = 'Fail'
            
            all_results.append({
                'roll_no': student.roll_no,
                'name': student.name,
                'class': student.class_name,
                'total_marks': total_marks,
                'max_marks': max_marks,
                'percentage': round(percentage, 2),
                'status': status
            })
    
    return jsonify({'success': True, 'results': all_results}), 200

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
