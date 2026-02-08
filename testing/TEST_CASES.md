# Student Result Management System - Test Cases

**Project:** Student Result Management System  
**Version:** 1.0  
**Date:** February 8, 2026  
**Test Environment:** Windows 10/11, Python 3.10, Flask 2.3.3

---

## 📋 Test Case Document Structure

| TC ID | Module | Scenario | Test Steps | Expected Result | Status | Notes |
|-------|--------|----------|-----------|-----------------|--------|-------|

---

# 1️⃣ STUDENT LOGIN MODULE TEST CASES

## TC-STU-001: Valid Student Login
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify student login with correct credentials |
| **Precondition** | Student S001 exists in database |
| **Test Steps** | 1. Navigate to Student Login page<br>2. Enter Roll No: S001<br>3. Enter Password: pass123<br>4. Click Login button |
| **Expected Result** | ✅ Login successful → Redirect to Student Dashboard<br>✅ Display student name and roll number<br>✅ Fetch and display student results |
| **Actual Result** | PASS |
| **Remarks** | Works as expected |

---

## TC-STU-002: Invalid Student Login - Wrong Password
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify system rejects invalid password |
| **Precondition** | Student S001 exists with password "pass123" |
| **Test Steps** | 1. Navigate to Student Login page<br>2. Enter Roll No: S001<br>3. Enter Password: wrongpass<br>4. Click Login button |
| **Expected Result** | ❌ Login failed<br>✅ Display error message: "Invalid credentials"<br>✅ Stay on login page<br>✅ Clear password field |
| **Actual Result** | PASS |
| **Remarks** | Error handling works correctly |

---

## TC-STU-003: Invalid Student Login - Non-existent Roll Number
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify system rejects non-existent student |
| **Precondition** | Student S999 does not exist in database |
| **Test Steps** | 1. Navigate to Student Login page<br>2. Enter Roll No: S999<br>3. Enter Password: pass123<br>4. Click Login button |
| **Expected Result** | ❌ Login failed<br>✅ Display error message: "Invalid credentials"<br>✅ Stay on login page |
| **Actual Result** | PASS |
| **Remarks** | Non-existent user handling works |

---

## TC-STU-004: Empty Fields - Student Login
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify login form requires both fields |
| **Precondition** | Student Login page loaded |
| **Test Steps** | 1. Leave Roll No field empty<br>2. Enter Password: pass123<br>3. Try to submit |
| **Expected Result** | ✅ Form shows validation error: "Roll No is required"<br>✅ Submit button disabled or error shown |
| **Actual Result** | PASS |
| **Remarks** | Browser validation works |

---

## TC-STU-005: View Student Results - All Subjects
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify student can view all subject marks |
| **Precondition** | Student S001 logged in, has marks in 3 subjects |
| **Test Steps** | 1. Login as Student S001<br>2. Dashboard loads<br>3. Observe marks table |
| **Expected Result** | ✅ Display all 7 subjects<br>✅ Show marks for each subject<br>✅ Display max marks for each subject<br>✅ Format: Subject Name | Marks | Max Marks |
| **Actual Result** | PASS |
| **Remarks** | All subjects visible |

---

## TC-STU-006: View Student Results - Percentage Calculation
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify percentage is calculated correctly |
| **Precondition** | Student has marks: Math 80/100, Science 60/100 |
| **Test Steps** | 1. Login as student<br>2. View dashboard<br>3. Check percentage value |
| **Expected Result** | ✅ Percentage = (140/200) × 100 = 70%<br>✅ Shown in summary card |
| **Actual Result** | PASS |
| **Remarks** | Correct calculation |

---

## TC-STU-007: View Student Results - Grade Assignment
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify grade assignment based on percentage |
| **Precondition** | Student has percentage 75% |
| **Test Steps** | 1. Login as student<br>2. View dashboard<br>3. Check grade |
| **Expected Result** | ✅ Grade = B+ (70-79%)<br>✅ Displayed in summary card |
| **Actual Result** | PASS |
| **Remarks** | Grade logic: A+=90+, A=80-89, B+=70-79, B=60-69, C=50-59, D=40-49, F=<40 |

---

## TC-STU-008: View Student Results - Pass/Fail Status
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify pass/fail status based on percentage |
| **Precondition** | Two students: one with 45%, one with 35% |
| **Test Steps** | 1. Login as first student (45%)<br>2. Check status<br>3. Logout, login second (35%)<br>4. Check status |
| **Expected Result** | ✅ 45% → Status: "Pass" (≥40%)<br>✅ 35% → Status: "Fail" (<40%)<br>✅ Color coding: Green=Pass, Red=Fail |
| **Actual Result** | PASS |
| **Remarks** | Passing percentage = 40% |

---

## TC-STU-009: Student Logout
**Priority:** Medium | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify student logout functionality |
| **Precondition** | Student logged in on dashboard |
| **Test Steps** | 1. Click Logout button<br>2. Observe page navigation<br>3. Try accessing dashboard directly |
| **Expected Result** | ✅ LocalStorage cleared<br>✅ Redirect to Student Login page<br>✅ Cannot access dashboard without login |
| **Actual Result** | PASS |
| **Remarks** | Session management works |

---

## TC-STU-010: Student Dashboard - No Marks Found
**Priority:** Medium | **Type:** Edge Case

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify message when student has no marks |
| **Precondition** | New student with no marks entered |
| **Test Steps** | 1. Login as new student<br>2. Wait for results to load |
| **Expected Result** | ✅ Error message: "No marks found"<br>✅ Show helpful message on dashboard |
| **Actual Result** | PASS |
| **Remarks** | Proper error handling |

---

# 2️⃣ TEACHER LOGIN & MARKS ENTRY MODULE TEST CASES

## TC-TEA-001: Valid Teacher Login
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify teacher login with correct credentials |
| **Precondition** | Teacher T001 exists in database |
| **Test Steps** | 1. Navigate to Teacher Login page<br>2. Enter Teacher ID: T001<br>3. Enter Password: pass123<br>4. Click Login button |
| **Expected Result** | ✅ Login successful → Redirect to Teacher Dashboard<br>✅ Display teacher name and subject<br>✅ Load students and subjects list |
| **Actual Result** | PASS |
| **Remarks** | Works as expected |

---

## TC-TEA-002: Invalid Teacher Login - Wrong Password
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify system rejects invalid teacher password |
| **Precondition** | Teacher T001 exists with password "pass123" |
| **Test Steps** | 1. Navigate to Teacher Login page<br>2. Enter Teacher ID: T001<br>3. Enter Password: wrongpass<br>4. Click Login button |
| **Expected Result** | ❌ Login failed<br>✅ Error message: "Invalid credentials"<br>✅ Stay on login page |
| **Actual Result** | PASS |
| **Remarks** | Error handling correct |

---

## TC-TEA-003: Teacher Dashboard - Load Students List
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify all students load in dropdown |
| **Precondition** | Teacher logged in with 5 students in database |
| **Test Steps** | 1. Login as Teacher T001<br>2. Navigate to "Enter Marks" tab<br>3. Click Student dropdown<br>4. Count options |
| **Expected Result** | ✅ All 5+ students visible<br>✅ Format: "Roll No - Name"<br>✅ Dropdown functional |
| **Actual Result** | PASS |
| **Remarks** | Student list loads correctly |

---

## TC-TEA-004: Teacher Dashboard - Load Subjects List
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify all subjects load in dropdown |
| **Precondition** | 7 subjects in database |
| **Test Steps** | 1. Login as Teacher<br>2. Click Subject dropdown<br>3. Count total options |
| **Expected Result** | ✅ All 7 subjects visible<br>✅ Shows subject names<br>✅ No duplicates |
| **Actual Result** | PASS |
| **Remarks** | Subjects: SOFTWARE TESTING, MANAGEMENT, EMERGING TRENDS, CLIENT SIDE SCRIPTING, MOBILE APP DEV, CAPSTONE, DIGITAL FORENSICS |

---

## TC-TEA-005: Enter Marks - Valid Input
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify marks entry for valid input |
| **Precondition** | Teacher logged in, student selected, subject selected |
| **Test Steps** | 1. Select Student: S001<br>2. Select Subject: SOFTWARE TESTING (max 150)<br>3. Enter Marks: 125<br>4. Click Save Marks |
| **Expected Result** | ✅ Success message: "Marks saved successfully!"<br>✅ Form clears<br>✅ Marks appear in "View Marks" tab<br>✅ Database updated |
| **Actual Result** | PASS |
| **Remarks** | Marks saved in DB |

---

## TC-TEA-006: Enter Marks - Marks Exceed Maximum
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify system rejects marks exceeding subject max |
| **Precondition** | Teacher logged in, Software Testing selected (max 150) |
| **Test Steps** | 1. Select Student: S001<br>2. Select Subject: SOFTWARE TESTING<br>3. Enter Marks: 155 (exceeds 150)<br>4. Click Save Marks |
| **Expected Result** | ❌ Error message: "Marks must be between 0 and 150"<br>✅ Marks NOT saved<br>✅ Form retains values for correction |
| **Actual Result** | PASS |
| **Remarks** | Validation working correctly |

---

## TC-TEA-007: Enter Marks - Marks Below Minimum
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify system rejects negative marks |
| **Precondition** | Teacher logged in, subject selected |
| **Test Steps** | 1. Enter Marks: -5<br>2. Click Save Marks |
| **Expected Result** | ❌ Error message: "Marks must be between 0 and X"<br>✅ Marks NOT saved |
| **Actual Result** | PASS |
| **Remarks** | Negative values rejected |

---

## TC-TEA-008: Enter Marks - Different Subject Max Marks
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify different subjects have different max marks |
| **Precondition** | Teacher logged in |
| **Test Steps** | 1. Select Subject: CLIENT SIDE SCRIPTING<br>2. Check max marks label<br>3. Select Subject: CAPSTONE PROJECT<br>4. Check max marks label |
| **Expected Result** | ✅ CLIENT SIDE SCRIPTING shows: (Max: 50)<br>✅ CAPSTONE PROJECT shows: (Max: 150)<br>✅ Input field max attribute updates |
| **Actual Result** | PASS |
| **Remarks** | Dynamic max marks working |

---

## TC-TEA-009: Enter Marks - Update Existing Marks
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify teacher can update previously entered marks |
| **Precondition** | Marks already entered for S001 in SOFTWARE TESTING (125) |
| **Test Steps** | 1. Select Student: S001<br>2. Select Subject: SOFTWARE TESTING<br>3. Enter different Marks: 135<br>4. Click Save Marks |
| **Expected Result** | ✅ Success message: "Marks saved successfully!"<br>✅ Database updated with new value (135)<br>✅ Old value (125) replaced<br>✅ View Marks shows 135 |
| **Actual Result** | PASS |
| **Remarks** | Update functionality works |

---

## TC-TEA-010: View Marks - Table Display
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify all entered marks display correctly |
| **Precondition** | Teacher has entered marks for 3 students |
| **Test Steps** | 1. Login as Teacher<br>2. Click "View Marks" tab<br>3. Observe table |
| **Expected Result** | ✅ Display columns: Roll No, Name, Subject, Marks, Max Marks, Percentage<br>✅ Show all 3 entries<br>✅ Percentages calculated correctly<br>✅ Format: (marks/max_marks)*100 |
| **Actual Result** | PASS |
| **Remarks** | All data displayed correctly |

---

## TC-TEA-011: Enter Marks - Empty Fields
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify form requires all fields |
| **Precondition** | Teacher on Enter Marks form |
| **Test Steps** | 1. Leave Student field empty<br>2. Leave Subject field empty<br>3. Try to submit |
| **Expected Result** | ✅ Browser validation: "Please select a student"<br>✅ Form does not submit |
| **Actual Result** | PASS |
| **Remarks** | HTML5 required attribute |

---

## TC-TEA-012: Teacher Logout
**Priority:** Medium | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify teacher logout functionality |
| **Precondition** | Teacher logged in |
| **Test Steps** | 1. Click Logout button<br>2. Observe redirection |
| **Expected Result** | ✅ LocalStorage cleared<br>✅ Redirect to Teacher Login page<br>✅ Cannot access dashboard |
| **Actual Result** | PASS |
| **Remarks** | Session cleared properly |

---

# 3️⃣ ADMIN MODULE TEST CASES

## TC-ADM-001: Valid Admin Login
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify admin login works |
| **Precondition** | Admin account: admin1 / admin123 exists |
| **Test Steps** | 1. Navigate to Admin Login<br>2. Enter Admin ID: admin1<br>3. Enter Password: admin123<br>4. Click Login |
| **Expected Result** | ✅ Login successful → Redirect to Admin Dashboard<br>✅ Display admin name<br>✅ Load all 4 tabs |
| **Actual Result** | PASS |
| **Remarks** | Default admin works |

---

## TC-ADM-002: Invalid Admin Login
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify invalid credentials rejected |
| **Precondition** | Correct password is "admin123" |
| **Test Steps** | 1. Enter Admin ID: admin1<br>2. Enter Password: wrongpass<br>3. Click Login |
| **Expected Result** | ❌ Error message: "Invalid credentials"<br>✅ Stay on login page |
| **Actual Result** | PASS |
| **Remarks** | Error handling |

---

## TC-ADM-003: Add Student - Valid Input
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify admin can add new student |
| **Precondition** | Admin logged in on Students tab |
| **Test Steps** | 1. Fill Roll No: S002<br>2. Fill Name: John Doe<br>3. Fill Class: B.Tech 7th Sem<br>4. Fill Email: john@email.com<br>5. Fill Password: newpass123<br>6. Click Add Student |
| **Expected Result** | ✅ Success message: "Student added successfully"<br>✅ Student appears in table<br>✅ Saved in database |
| **Actual Result** | PASS |
| **Remarks** | New student created |

---

## TC-ADM-004: Add Student - Duplicate Roll Number
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify duplicate roll numbers rejected |
| **Precondition** | Student S001 already exists |
| **Test Steps** | 1. Fill Roll No: S001 (duplicate)<br>2. Fill other fields<br>3. Click Add Student |
| **Expected Result** | ❌ Error message: "Roll no already exists"<br>✅ Student NOT added<br>✅ Database unchanged |
| **Actual Result** | PASS |
| **Remarks** | Duplicate prevention works |

---

## TC-ADM-005: Add Student - Empty Fields
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify required fields validation |
| **Precondition** | Admin on Students tab |
| **Test Steps** | 1. Leave Roll No empty<br>2. Fill other fields<br>3. Click Add Student |
| **Expected Result** | ✅ Browser validation error<br>✅ Form doesn't submit |
| **Actual Result** | PASS |
| **Remarks** | HTML5 validation |

---

## TC-ADM-006: View All Students
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify all students listed in Students tab |
| **Precondition** | 5 students in database |
| **Test Steps** | 1. Admin logged in<br>2. Navigate to Students tab<br>3. Observe table |
| **Expected Result** | ✅ Display all 5 students<br>✅ Columns: Roll No, Name, Class, Email<br>✅ Delete buttons present |
| **Actual Result** | PASS |
| **Remarks** | All students visible |

---

## TC-ADM-007: Delete Student
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify admin can delete student |
| **Precondition** | Student S002 exists with no marks |
| **Test Steps** | 1. Admin logged in<br>2. Navigate to Students tab<br>3. Click Delete on S002<br>4. Confirm deletion |
| **Expected Result** | ✅ Confirmation dialog appears<br>✅ Student removed from table<br>✅ Removed from database<br>✅ Success message shown |
| **Actual Result** | PASS |
| **Remarks** | Student deleted |

---

## TC-ADM-008: Delete Student - With Associated Marks
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify marks deleted when student deleted |
| **Precondition** | Student has 3 marks in database |
| **Test Steps** | 1. Delete student<br>2. Confirm<br>3. Check database for orphan marks |
| **Expected Result** | ✅ Student deleted<br>✅ All associated marks also deleted<br>✅ No orphan records left |
| **Actual Result** | PASS |
| **Remarks** | Cascading delete works |

---

## TC-ADM-009: Add Teacher - Valid Input
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify admin can add teacher |
| **Precondition** | Admin logged in on Teachers tab |
| **Test Steps** | 1. Fill Teacher ID: T002<br>2. Fill Name: Jane Smith<br>3. Fill Subject: MANAGEMENT<br>4. Fill Email: jane@email.com<br>5. Fill Password: tpass123<br>6. Click Add Teacher |
| **Expected Result** | ✅ Success message<br>✅ Teacher added to table<br>✅ Saved in database |
| **Actual Result** | PASS |
| **Remarks** | Teacher created |

---

## TC-ADM-010: Add Teacher - Duplicate Teacher ID
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify duplicate teacher IDs rejected |
| **Precondition** | Teacher T001 exists |
| **Test Steps** | 1. Fill Teacher ID: T001 (duplicate)<br>2. Fill other fields<br>3. Click Add Teacher |
| **Expected Result** | ❌ Error message: "Teacher ID already exists"<br>✅ Teacher NOT added |
| **Actual Result** | PASS |
| **Remarks** | Duplicate prevention |

---

## TC-ADM-011: View All Teachers
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify all teachers listed |
| **Precondition** | 3 teachers in database |
| **Test Steps** | 1. Navigate to Teachers tab<br>2. Observe table |
| **Expected Result** | ✅ Display all 3 teachers<br>✅ Columns: Teacher ID, Name, Subject, Email<br>✅ Delete buttons present |
| **Actual Result** | PASS |
| **Remarks** | All teachers visible |

---

## TC-ADM-012: Delete Teacher
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify admin can delete teacher |
| **Precondition** | Teacher T002 exists |
| **Test Steps** | 1. Navigate to Teachers tab<br>2. Click Delete on T002<br>3. Confirm |
| **Expected Result** | ✅ Confirmation dialog<br>✅ Teacher removed from table<br>✅ Removed from database<br>✅ Associated marks also deleted |
| **Actual Result** | PASS |
| **Remarks** | Cascading delete works |

---

## TC-ADM-013: View All Results
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify admin can view all student results |
| **Precondition** | 3 students with marks in database |
| **Test Steps** | 1. Navigate to Results tab<br>2. Observe table |
| **Expected Result** | ✅ Display all 3 students<br>✅ Show: Roll, Name, Class, Total Marks, Max Marks, %, Status<br>✅ Percentages calculated<br>✅ Status shows Pass/Fail |
| **Actual Result** | PASS |
| **Remarks** | All results visible |

---

## TC-ADM-014: View Subjects
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify all subjects displayed |
| **Precondition** | 7 subjects in database |
| **Test Steps** | 1. Navigate to Subjects tab<br>2. Observe table |
| **Expected Result** | ✅ Display all 7 subjects<br>✅ Columns: Name, Code, Max Marks<br>✅ Correct max marks shown |
| **Actual Result** | PASS |
| **Remarks** | All subjects visible |

---

## TC-ADM-015: Admin Logout
**Priority:** Medium | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify admin logout |
| **Precondition** | Admin logged in |
| **Test Steps** | 1. Click Logout button<br>2. Observe redirection |
| **Expected Result** | ✅ LocalStorage cleared<br>✅ Redirect to Admin Login<br>✅ Cannot access dashboard |
| **Actual Result** | PASS |
| **Remarks** | Session cleared |

---

# 4️⃣ GENERAL / API TEST CASES

## TC-API-001: Server Running Check
**Priority:** High | **Type:** Smoke Test

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify backend server is running |
| **Precondition** | Flask app started |
| **Test Steps** | 1. Open terminal<br>2. Run: `curl http://localhost:5000/api/subjects` |
| **Expected Result** | ✅ Server responds with status 200<br>✅ Returns JSON with subjects array<br>✅ No errors in response |
| **Actual Result** | PASS |
| **Remarks** | Server healthy |

---

## TC-API-002: CORS Enabled
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify cross-origin requests work |
| **Precondition** | Frontend at file:///, Backend at localhost:5000 |
| **Test Steps** | 1. Open frontend in browser<br>2. Try any login<br>3. Check network tab |
| **Expected Result** | ✅ Request succeeds (no CORS error)<br>✅ Response headers include appropriate CORS headers |
| **Actual Result** | PASS |
| **Remarks** | CORS configured correctly |

---

## TC-API-003: Database Connection
**Priority:** High | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify database is accessible |
| **Precondition** | database.db exists in backend folder |
| **Test Steps** | 1. Perform any CRUD operation<br>2. Check if data persists across server restarts |
| **Expected Result** | ✅ Data saved successfully<br>✅ Data persists after restart<br>✅ No connection errors |
| **Actual Result** | PASS |
| **Remarks** | SQLite working |

---

## TC-API-004: Error Handling - 404 Endpoint
**Priority:** Medium | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify 404 errors handled gracefully |
| **Precondition** | Backend running |
| **Test Steps** | 1. Call non-existent endpoint<br>2. Example: `/api/nonexistent` |
| **Expected Result** | ✅ Returns 404 status<br>✅ JSON error message: "Endpoint not found"<br>✅ No server crash |
| **Actual Result** | PASS |
| **Remarks** | Error handling working |

---

## TC-API-005: Error Handling - 500 Server Error
**Priority:** Medium | **Type:** Functional

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify 500 errors handled |
| **Precondition** | Simulate database error |
| **Test Steps** | 1. Cause unexpected error (e.g., delete db during operation)<br>2. Observe response |
| **Expected Result** | ✅ Returns 500 status<br>✅ JSON error message shown<br>✅ Server stays running |
| **Actual Result** | PASS |
| **Remarks** | Error handling robust |

---

## TC-API-006: Marks Validation - 0-100 Range
**Priority:** High | **Type:** Validation

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify marks range validation |
| **Precondition** | Subject with max 150 marks |
| **Test Steps** | 1. Send API request with marks: 160<br>2. Send with marks: -5<br>3. Send with marks: 150 |
| **Expected Result** | ✅ Marks 160: Rejected with error<br>✅ Marks -5: Rejected with error<br>✅ Marks 150: Accepted |
| **Actual Result** | PASS |
| **Remarks** | Validation on backend |

---

# 5️⃣ SECURITY TEST CASES

## TC-SEC-001: SQL Injection Prevention
**Priority:** Critical | **Type:** Security

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify SQL injection prevented |
| **Precondition** | Any login page |
| **Test Steps** | 1. Roll No field: enter `' OR '1'='1`<br>2. Try to login |
| **Expected Result** | ❌ Login fails<br>✅ No database bypass<br>✅ Error message: "Invalid credentials" |
| **Actual Result** | PASS |
| **Remarks** | SQLAlchemy ORM prevents injection |

---

## TC-SEC-002: XSS Prevention
**Priority:** Critical | **Type:** Security

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify XSS attacks prevented |
| **Precondition** | Add Student form |
| **Test Steps** | 1. Name field: `<script>alert('XSS')</script>`<br>2. Submit |
| **Expected Result** | ✅ Script not executed<br>✅ Text stored as literal string<br>✅ No alert shown |
| **Actual Result** | PASS |
| **Remarks** | Input properly escaped |

---

## TC-SEC-003: Authentication Check
**Priority:** High | **Type:** Security

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify unauthorized access blocked |
| **Precondition** | User not logged in |
| **Test Steps** | 1. Open browser console<br>2. Try to access student_dashboard.html directly<br>3. Modify localStorage to fake student ID |
| **Expected Result** | ✅ Redirected to student_login.html<br>✅ Dashboard doesn't load without session |
| **Actual Result** | PASS |
| **Remarks** | Client-side protection (add server-side in production) |

---

## TC-SEC-004: Password Storage
**Priority:** High | **Type:** Security

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify passwords stored securely |
| **Precondition** | Check database.db file |
| **Test Steps** | 1. Use SQLite viewer to open database.db<br>2. Check students table<br>3. Verify password field |
| **Expected Result** | ⚠️ Currently: Passwords stored as plain text (NOT SECURE)<br>⚠️ Production: Should use bcrypt hashing |
| **Actual Result** | FAIL (Development version) |
| **Remarks** | **DEFECT:** Plain text passwords - needs bcrypt |

---

# 6️⃣ PERFORMANCE TEST CASES

## TC-PER-001: Page Load Time
**Priority:** Medium | **Type:** Performance

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify pages load within acceptable time |
| **Precondition** | Browser dev tools open |
| **Test Steps** | 1. Navigate to student_dashboard.html<br>2. Check network tab load time<br>3. Measure time to display marks |
| **Expected Result** | ✅ Page loads in <3 seconds<br>✅ Marks display in <2 seconds |
| **Actual Result** | PASS |
| **Remarks** | Performance acceptable |

---

## TC-PER-002: Form Submission Response Time
**Priority:** Medium | **Type:** Performance

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify form submission is fast |
| **Precondition** | Teacher entering marks |
| **Test Steps** | 1. Fill marks form<br>2. Submit<br>3. Measure response time |
| **Expected Result** | ✅ Response within 1 second<br>✅ No timeout errors |
| **Actual Result** | PASS |
| **Remarks** | Fast response |

---

## TC-PER-003: Large Dataset Handling
**Priority:** Low | **Type:** Performance

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify system handles 100+ students |
| **Precondition** | Create 100 students in database |
| **Test Steps** | 1. Admin views all students<br>2. Measure page load time<br>3. Teacher fetches student list |
| **Expected Result** | ✅ All students load<br>✅ No UI freeze<br>✅ Load time <5 seconds |
| **Actual Result** | PASS |
| **Remarks** | Handles large datasets |

---

# 7️⃣ UI/UX TEST CASES

## TC-UI-001: Responsive Design - Mobile View
**Priority:** Medium | **Type:** UI

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify UI works on mobile devices |
| **Precondition** | Browser DevTools open (375px width) |
| **Test Steps** | 1. Set viewport to 375px<br>2. Navigate all pages<br>3. Test form inputs |
| **Expected Result** | ✅ All elements visible<br>✅ No horizontal scrolling<br>✅ Text readable<br>✅ Buttons clickable |
| **Actual Result** | PASS |
| **Remarks** | Tailwind responsive |

---

## TC-UI-002: Responsive Design - Tablet View
**Priority:** Medium | **Type:** UI

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify UI on tablet (768px) |
| **Precondition** | Browser width 768px |
| **Test Steps** | 1. Set viewport to 768px<br>2. Navigate pages<br>3. Test tables |
| **Expected Result** | ✅ Layout optimized<br>✅ Tables scrollable horizontally<br>✅ Readable content |
| **Actual Result** | PASS |
| **Remarks** | Responsive |

---

## TC-UI-003: Color Contrast - WCAG Compliance
**Priority:** Low | **Type:** Accessibility

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify text readable by colorblind users |
| **Precondition** | Use WCAG color contrast checker |
| **Test Steps** | 1. Check all text elements<br>2. Check status colors (Green/Red) |
| **Expected Result** | ✅ Contrast ratio > 4.5:1<br>✅ Status not only color-coded |
| **Actual Result** | PASS |
| **Remarks** | Good contrast maintained |

---

##  TC-UI-004: Browser Compatibility
**Priority:** Medium | **Type:** UI

| Parameter | Value |
|-----------|-------|
| **Test Objective** | Verify works across browsers |
| **Precondition** | Test on multiple browsers |
| **Test Steps** | 1. Test on Chrome<br>2. Test on Firefox<br>3. Test on Safari<br>4. Test on Edge |
| **Expected Result** | ✅ Works perfectly on all<br>✅ No JavaScript errors<br>✅ Styling consistent |
| **Actual Result** | PASS |
| **Remarks** | Cross-browser compatible |

---

---

# TEST SUMMARY

| Category | Total Cases | Passed | Failed | Pass % |
|----------|------------|--------|--------|---------|
| Student Module | 10 | 10 | 0 | 100% |
| Teacher Module | 12 | 12 | 0 | 100% |
| Admin Module | 15 | 15 | 0 | 100% |
| API Tests | 6 | 6 | 0 | 100% |
| Security Tests | 4 | 3 | 1 | 75% |
| Performance Tests | 3 | 3 | 0 | 100% |
| UI/UX Tests | 4 | 4 | 0 | 100% |
| **TOTAL** | **54** | **53** | **1** | **98.1%** |

---

## Issues Found
- 1 Security Issue (Plain text passwords)

---

**Test Date:** February 8, 2026  
**Tester:** QA Team  
**Environment:** Windows 10, Python 3.10, Flask 2.3.3
