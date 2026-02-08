# 📚 Student Result Management System

A complete web-based system for managing student results with role-based access control. Built with **Flask (Python) backend** and **HTML/Tailwind CSS frontend**.

## 🎯 Features

### 📋 Role-Based Access Control
- **👨‍🎓 Student Login** - View your marks, percentage, grades, and result status
- **👨‍🏫 Teacher Login** - Enter and update student marks for your subjects
- **🛡️ Admin Login** - Complete system management with full database access

### 📊 Auto Result Calculation
- Total marks calculation
- Percentage calculation
- Grade assignment (A+, A, B+, B, C, D, F)
- Pass/Fail status (Pass: 40%, Fail: <40%)

### 💾 Database Features
- SQLite database for secure data storage
- Student management (add/remove)
- Teacher management (add/remove)
- Subject management
- Marks tracking with date stamps

### 🔐 Security
- Role-based authentication
- Secure password storage
- Session management via localStorage
- Input validation on all forms

---

## 🚀 Project Structure

```
Student_Result_management/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── models.py               # Database models
│   ├── requirements.txt         # Python dependencies
│   └── database.db             # SQLite database (auto-created)
│
├── frontend/
│   ├── index.html              # Home page
│   ├── student_login.html       # Student login page
│   ├── student_dashboard.html   # Student results view
│   ├── teacher_login.html       # Teacher login page
│   ├── teacher_dashboard.html   # Teacher marks entry
│   ├── admin_login.html         # Admin login page
│   ├── admin_dashboard.html     # Admin control panel
│   ├── css/                     # CSS files (Tailwind via CDN)
│   └── js/                      # JavaScript files
│
└── README.md                   # This file
```

---

## 📋 Installation & Setup

### Prerequisites
- **Python 3.7+** installed
- **pip** (Python package manager)
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Install Python Dependencies

Navigate to the backend folder and install required packages:

```bash
cd backend
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Flask==2.3.3
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Cors==4.0.0
pip install Werkzeug==2.3.7
```

### Step 2: Run the Flask Server

In the `backend` folder, run:

```bash
python app.py
```

You should see:
```
WARNING in app.run_simple: This is a development server. Do not use it in production applications.
Running on http://127.0.0.1:5000
```

**Keep this terminal open** - the server needs to be running!

### Step 3: Open the Frontend

In your browser, navigate to:
```
file:///path/to/Student_Result_management/frontend/index.html
```

Or open the `index.html` file directly from the frontend folder.

---

## 🧑‍💻 Demo Credentials

Use these credentials to test the system:

### Student Login
- **Roll No:** `S001`
- **Password:** `pass123`

### Teacher Login
- **Teacher ID:** `T001`
- **Password:** `pass123`

### Admin Login
- **Admin ID:** `admin1`
- **Password:** `admin123`

---

## 🎮 Usage Guide

### 👨‍🎓 For Students

1. Go to **Student Login** page
2. Enter Roll No: `S001` and Password: `pass123`
3. View your:
   - Subject-wise marks
   - Total marks and max marks
   - Percentage
   - Grade
   - Pass/Fail status

### 👨‍🏫 For Teachers

1. Go to **Teacher Login** page
2. Enter Teacher ID: `T001` and Password: `pass123`
3. Use the **Enter Marks** tab to:
   - Select a student
   - Select a subject
   - Enter marks (0-100)
   - Save marks
4. Use the **View Marks** tab to see all marks you've entered

### 🛡️ For Admin

1. Go to **Admin Login** page
2. Enter Admin ID: `admin1` and Password: `admin123`
3. Access four main sections:
   - **Students** - Add/remove students
   - **Teachers** - Add/remove teachers
   - **Results** - View all student results
   - **Subjects** - View all available subjects

---

## 🌐 API Endpoints

### Student APIs
```
POST   /api/student/login              - Login student
GET    /api/student/results/<id>       - Get student results
```

### Teacher APIs
```
POST   /api/teacher/login              - Login teacher
GET    /api/teacher/students           - Get all students
POST   /api/teacher/enter-marks        - Enter/update marks
GET    /api/teacher/marks/<id>         - Get teacher's marks
```

### Admin APIs
```
POST   /api/admin/login                - Login admin
POST   /api/admin/add-student          - Add new student
POST   /api/admin/add-teacher          - Add new teacher
DELETE /api/admin/delete-student/<id>  - Delete student
DELETE /api/admin/delete-teacher/<id>  - Delete teacher
GET    /api/admin/students             - Get all students
GET    /api/admin/teachers             - Get all teachers
GET    /api/admin/all-results          - Get all results
```

### General APIs
```
GET    /api/subjects                   - Get all subjects
```

---

## 🗄️ Database Schema

### Students Table
```
id, roll_no, name, password, class_name, email
```

### Teachers Table
```
id, teacher_id, name, password, subject, email
```

### Admins Table
```
id, admin_id, name, password, email
```

### Subjects Table
```
id, subject_name, subject_code, max_marks
```

### Marks Table
```
id, student_id, teacher_id, subject_id, marks_obtained, date_created, date_updated
```

---

## 📝 Sample Data

The system comes pre-loaded with:
- **5 Subjects:** Mathematics, English, Science, History, Geography
- **1 Admin:** admin1 (password: admin123)
- **Demo credentials for testing**

To add more:
1. Use Admin Dashboard to add students and teachers
2. Teachers can enter marks for students

---

## 🔧 Customization

### Change API Port
In `backend/app.py`, change:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change 5000 to your port
```

### Modify Grade Calculation
In `backend/app.py`, update the grade logic in `get_student_results()`:
```python
if percentage >= 90:
    grade = 'A+'
elif percentage >= 80:
    grade = 'A'
# ... modify thresholds as needed
```

### Update Passing Percentage
Change `40` to your desired threshold:
```python
status = 'Pass' if percentage >= 40 else 'Fail'
```

---

## 🚨 Troubleshooting

### "Error connecting to server"
- Ensure Flask backend is running on `http://localhost:5000`
- Check if backend terminal shows no errors
- Clear browser cache and refresh

### CORS Errors
- Flask-CORS is already configured in the backend
- If issues persist, ensure Flask is running

### Database Issues
- Delete `database.db` to reset the database
- Database will be recreated on next backend start

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill the process using port 5000

---

## 📱 Browser Support
- Chrome/Chromium (Recommended)
- Firefox
- Safari
- Edge

---

## 🔐 Security Notes

⚠️ **This is a development project. For production:**
- Change the `SECRET_KEY` in `app.py`
- Use proper password hashing (bcrypt)
- Enable HTTPS
- Deploy using a production WSGI server (Gunicorn, etc.)
- Use a production database (PostgreSQL, MySQL)
- Implement JWT tokens instead of localStorage

---

## 📞 Support

If you encounter issues:
1. Check the browser console for errors (F12)
2. Check Flask backend terminal for error messages
3. Ensure all dependencies are installed
4. Try clearing browser cache
5. Restart both browser and backend server

---

## 📄 License

This project is for educational purposes.

---

**Built with ❤️ for Education Management**
