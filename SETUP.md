## 🚀 Quick Start Guide

### Step 1️⃣: Install Dependencies (One-time setup)

Open PowerShell or Command Prompt in the `backend` folder and run:

```powershell
pip install -r requirements.txt
```

**Output should show:** ✅ Successfully installed Flask, Flask-SQLAlchemy, Flask-Cors, Werkzeug

---

### Step 2️⃣: Start the Backend Server

**Windows (Easy):**
Double-click `run_backend.bat` in the root folder.

**Or manually:**
In PowerShell/Command Prompt:
```powershell
cd backend
python app.py
```

**You should see:**
```
Running on http://127.0.0.1:5000
WARNING in app.run_simple: This is a development server.
```

✅ **Keep this terminal open** - Don't close it!

---

### Step 3️⃣: Open the Frontend

Open your browser and navigate to:
```
file:///C:/Users/omesh/Desktop/Desktop/Student_Result_management/frontend/index.html
```

Or simply drag-and-drop `index.html` into your browser.

---

## 🧑‍💻 Test the System

### 1️⃣ Test Student Login
- Click "Student Login" on home page
- Roll No: `S001`
- Password: `pass123`
- Click Login → View Results

### 2️⃣ Test Teacher Login
- Go back, click "Teacher Login"
- Teacher ID: `T001`
- Password: `pass123`
- Enter marks for students

### 3️⃣ Test Admin Login
- Go back, click "Admin Login"
- Admin ID: `admin1`
- Password: `admin123`
- Manage students, teachers, view all results

---

## ❌ If Something Goes Wrong

### Error: "Error connecting to server"
✅ **Solution:** Make sure `python app.py` is running in backend folder

### Error: Port 5000 already in use
✅ **Solution:** Edit `backend/app.py` line 48:
```python
app.run(debug=True, port=5001)  # Change to 5001 or another port
```

### Error: Module not found
✅ **Solution:** Run `pip install -r requirements.txt` again

### Database issues
✅ **Solution:** Delete `backend/database.db` file, then restart server

---

## 📊 Database Auto-Creation

The first time you start the backend:
- ✅ `database.db` is created automatically
- ✅ Default admin (admin1) is added
- ✅ 5 subjects are added (Math, English, Science, History, Geography)
- ✅ You can add more students/teachers via Admin panel

---

## 🎯 What You Can Do

### As Student:
- ✓ Login with roll number
- ✓ View subject-wise marks
- ✓ See total marks and percentage
- ✓ Check grades (A+, A, B+, etc.)
- ✓ See Pass/Fail status

### As Teacher:
- ✓ Login with teacher ID
- ✓ Enter marks for students (0-100)
- ✓ Update marks anytime
- ✓ View all marks entered

### As Admin:
- ✓ Add/Remove students
- ✓ Add/Remove teachers
- ✓ View all student results
- ✓ View all subjects
- ✓ Full database control

---

## 🌐 Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python Flask |
| Frontend | HTML5 + Tailwind CSS |
| Database | SQLite |
| API | RESTful JSON |
| Authentication | Session-based (localStorage) |

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application & all APIs |
| `models.py` | Database models (Student, Teacher, Admin, etc.) |
| `index.html` | Home page with feature overview |
| `*_login.html` | Login pages for each role |
| `*_dashboard.html` | Main interface for each role |
| `requirements.txt` | Python dependencies |
| `README.md` | Complete documentation |
| `run_backend.bat` | Quick start script for Windows |

---

## ✨ Next Steps

1. ✅ Install dependencies
2. ✅ Run backend server
3. ✅ Open frontend in browser
4. ✅ Test all 3 roles with demo credentials
5. ✅ Explore the admin panel to add custom data
6. ✅ Customize passwords, subjects, and grades as needed

---

**Enjoy your Student Result Management System! 🎓**
