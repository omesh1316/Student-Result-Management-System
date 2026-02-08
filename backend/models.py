from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    
    marks = db.relationship('Marks', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.roll_no}>'

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    
    marks = db.relationship('Marks', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f'<Teacher {self.teacher_id}>'

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Admin {self.admin_id}>'

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), unique=True, nullable=False)
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    max_marks = db.Column(db.Integer, default=100)
    
    marks = db.relationship('Marks', backref='subject', lazy=True)
    
    def __repr__(self):
        return f'<Subject {self.subject_name}>'

class Marks(db.Model):
    __tablename__ = 'marks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Marks {self.student_id} - {self.subject_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_roll_no': self.student.roll_no,
            'student_name': self.student.name,
            'subject': self.subject.subject_name,
            'marks': self.marks_obtained,
            'max_marks': self.subject.max_marks
        }
