# Student Result Management System - Defect Report

**Project:** Student Result Management System  
**Version:** 1.0  
**Report Date:** February 8, 2026  
**Environment:** Windows 10, Python 3.10, Flask, SQLite

---

## 📊 DEFECT SUMMARY

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 **CRITICAL** | 1 | Open |
| 🟠 **HIGH** | 2 | Open |
| 🟡 **MEDIUM** | 3 | Open |
| 🟢 **LOW** | 2 | Open |
| **TOTAL** | **8** | - |

---

# 🔴 CRITICAL DEFECTS

## DEFECT ID: DEF-001
**Title:** Plain Text Password Storage - Security Vulnerability  
**Severity:** 🔴 CRITICAL  
**Status:** 🔴 OPEN  
**Priority:** P0 - Must Fix

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA Team |
| **Reported Date** | February 8, 2026 |
| **Found In** | Backend (models.py, database) |
| **Affected Module** | Authentication (All roles) |
| **Reproducibility** | 100% |

### Description:
Passwords are stored in database as plain text without any encryption or hashing. This is a critical security vulnerability that violates industry security standards (OWASP).

### Steps to Reproduce:
1. Open database.db using SQLite3 viewer
2. Query: `SELECT * FROM students;`
3. Password field contains plain text (e.g., "pass123")

### Expected Behavior:
Passwords should be hashed using bcrypt or similar algorithm before storage.

### Actual Behavior:
Passwords stored as plain text, visible to anyone with database access.

### Impact:
- **High Risk:** Data breach, user account compromise
- If database is compromised, all user passwords are exposed
- Users' passwords can be used on other platforms (password reuse)
- Violates security regulations (GDPR, HIPAA if applicable)

### Root Cause:
Implementation did not include password hashing mechanism:
```python
# Current (WRONG):
student = Student(password=data.get('password'))

# Should be:
from werkzeug.security import generate_password_hash
student = Student(password=generate_password_hash(data.get('password')))
```

### Recommended Fix:
1. Install werkzeug: `pip install werkzeug`
2. Update models.py - use property setter for password hashing
3. Update login validation to use check_password_hash()
4. Migrate existing passwords (or force reset)

### Code Change Required:
```python
# In models.py
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):
    _password = db.Column('password', db.String(255), nullable=False)
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self._password, password)

# In app.py - update login
student = Student.query.filter_by(roll_no=roll_no).first()
if student and student.verify_password(password):
    # Login success
```

### Effort Estimate:
- Estimated: 2-3 hours
- Complexity: Medium

### Acceptance Criteria:
- [ ] All passwords hashed in database
- [ ] Login still works with hashed passwords
- [ ] Old passwords migrated or users reset password
- [ ] Security test passes (no plain text passwords visible)

### Release Target:
- **Should be fixed before production deployment**
- Plan for next sprint

---

# 🟠 HIGH SEVERITY DEFECTS

## DEFECT ID: DEF-002
**Title:** No Input Sanitization - XSS Vulnerability  
**Severity:** 🟠 HIGH  
**Status:** 🔴 OPEN  
**Priority:** P1 - High

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA - Security Test |
| **Reported Date** | February 8, 2026 |
| **Found In** | Frontend (HTML input fields) |
| **Affected Module** | Add Student, Add Teacher forms |
| **Reproducibility** | 100% |

### Description:
User inputs are not sanitized before storage, allowing potential XSS (Cross-Site Scripting) attacks. An attacker could inject malicious JavaScript in name, email, or other fields.

### Steps to Reproduce:
1. Login as Admin
2. Go to "Add Student" form
3. In Name field, enter: `<img src=x onerror="alert('XSS')">`
4. Submit form
5. Navigate to Admin view → Students tab
6. JavaScript alert will execute

### Expected Behavior:
- Input should be escaped as plain text
- No JavaScript should execute
- Text should be: `<img src=x onerror="alert('XSS')">`

### Actual Behavior:
- Input stored and displayed as-is
- Risk of script injection

### Impact:
- Session hijacking possible
- Credential theft
- Malware injection
- User data compromise

### Root Cause:
Missing input validation/sanitization in frontend and backend.

### Recommended Fix:
1. **Frontend:** Use textContent instead of innerHTML
2. **Backend:** Validate and escape input using bleach library

```python
# Install: pip install bleach
from bleach import clean

def add_student():
    data = request.json
    student = Student(
        name=clean(data.get('name'), tags=[], strip=True),
        email=clean(data.get('email'), tags=[], strip=True),
        # ... other fields
    )
```

### Effort Estimate:
- Estimated: 1-2 hours
- Complexity: Low

### Release Target:
- Should be fixed before production

---

## DEFECT ID: DEF-003
**Title:** No Server-Side Authentication Validation  
**Severity:** 🟠 HIGH  
**Status:** 🔴 OPEN  
**Priority:** P1 - High

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA - Security Test |
| **Reported Date** | February 8, 2026 |
| **Found In** | Backend (API endpoints) |
| **Affected Module** | All protected routes |
| **Reproducibility** | 100% |

### Description:
API endpoints don't verify authentication. A user can directly call `/api/teacher/enter-marks` using curl/Postman without proper authentication check.

### Steps to Reproduce:
1. Open terminal/Postman
2. Run: 
```bash
curl -X POST http://localhost:5000/api/teacher/enter-marks \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"teacher_id":99,"subject_id":1,"marks_obtained":100}'
```
3. Request succeeds even with fake teacher_id

### Expected Behavior:
- API should verify valid authentication token/session
- Reject requests from unauthenticated users
- Return 401 Unauthorized for invalid sessions

### Actual Behavior:
- Any caller can submit marks
- No authentication required

### Impact:
- Anyone can add/modify marks
- Data integrity violated
- Teachers from wrong subjects can enter marks
- Students can potentially view other student's data

### Root Cause:
API endpoints missing authentication middleware/decorator.

### Recommended Fix:
Implement token-based authentication (JWT) or session validation:

```python
from functools import wraps
from flask import session

def require_teacher_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'teacher_id' not in session:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/teacher/enter-marks', methods=['POST'])
@require_teacher_login
def enter_marks():
    # ... rest of code
```

### Effort Estimate:
- Estimated: 3-4 hours
- Complexity: Medium

### Release Target:
- Critical for production

---

# 🟡 MEDIUM SEVERITY DEFECTS

## DEFECT ID: DEF-004
**Title:** Marks Validation Allows Floating Point Precision Loss  
**Severity:** 🟡 MEDIUM  
**Status:** 🔴 OPEN  
**Priority:** P2

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA - Data Validation Test |
| **Reported Date** | February 8, 2026 |
| **Found In** | Backend (Marks model) |
| **Affected Module** | Marks entry and calculation |
| **Reproducibility** | 100% |

### Description:
Marks are stored as Float which can cause floating-point precision issues. Percentage calculations may be inaccurate.

### Steps to Reproduce:
1. Enter marks: 33.33333
2. Calculate percentage: (33.33333 / 100) * 100
3. Result: 33.333330000000004 (floating point error)

### Example:
```
Marks Entered: 33.33333
Percentage Shown: 33.33333000000004% (incorrect display)
```

### Expected Behavior:
- Marks shown with 2 decimal places max
- Percentage rounded to 2 decimals
- No floating point artifacts

### Actual Behavior:
- Long decimal values possible
- Percentage shows all decimals

### Impact:
- Minor: Cosmetic issue in UI
- Could confuse users with long decimal displays
- Grade boundaries might be affected

### Root Cause:
Database field uses Float instead of Numeric/Decimal type.

### Recommended Fix:
```python
# In models.py - Change from Float to Numeric
marks_obtained = db.Column(db.Numeric(5, 2), nullable=False)  # Max 999.99

# In app.py - Round percentage display
percentage = round(percentage, 2)

# In frontend - Display with limited decimals
percentage.toFixed(2)  // Shows max 2 decimals
```

### Effort Estimate:
- Estimated: 1 hour
- Complexity: Low

### Release Target:
- Can be fixed in next patch

---

## DEFECT ID: DEF-005
**Title:** No Error Logs - Difficult to Debug Production Issues  
**Severity:** 🟡 MEDIUM  
**Status:** 🔴 OPEN  
**Priority:** P2

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA |
| **Reported Date** | February 8, 2026 |
| **Found In** | Backend (app.py) |
| **Affected Module** | All API endpoints |
| **Reproducibility** | N/A |

### Description:
API doesn't log errors or important events. Hard to debug issues in production. No audit trail for data changes.

### Expected Behavior:
- Error logs with timestamps
- User action audit trail
- Debug information for failed API calls

### Actual Behavior:
- No logging configured
- Errors only shown in console
- No record of who made changes

### Impact:
- Difficult production support
- No audit trail for compliance
- Hard to trace data modifications
- Security issues go undetected

### Recommended Fix:
```python
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# In API endpoints:
@app.route('/api/student/login', methods=['POST'])
def student_login():
    roll_no = data.get('roll_no')
    logging.info(f"Login attempt: {roll_no}")
    
    student = Student.query.filter_by(roll_no=roll_no).first()
    if student and student.verify_password(password):
        logging.info(f"Login successful: {roll_no}")
    else:
        logging.warning(f"Failed login attempt: {roll_no}")
```

### Effort Estimate:
- Estimated: 2 hours
- Complexity: Low

### Release Target:
- Before production

---

## DEFECT ID: DEF-006
**Title:** No Data Validation for Email Format  
**Severity:** 🟡 MEDIUM  
**Status:** 🔴 OPEN  
**Priority:** P3

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA |
| **Reported Date** | February 8, 2026 |
| **Found In** | Add Student, Add Teacher forms |
| **Affected Module** | Admin module |
| **Reproducibility** | 100% |

### Description:
Email field accepts invalid email formats. No validation on email format.

### Steps to Reproduce:
1. Login as Admin
2. Add Student
3. Email field: Enter `notanemail` (no @)
4. Submit
5. Form accepts it without error

### Expected Behavior:
- Email validation should enforce format: name@domain.com
- Show validation error: "Please enter valid email"

### Actual Behavior:
- Any string accepted as valid email

### Impact:
- Invalid contact information stored
- Notifications won't work if email feature added
- Data quality issues

### Root Cause:
No email format validation in frontend or backend.

### Recommended Fix:
```python
# Backend validation
import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

if not re.match(EMAIL_REGEX, email):
    return jsonify({'success': False, 'message': 'Invalid email format'})

# Frontend validation - add type="email" to HTML input
<input type="email" required>
```

### Effort Estimate:
- Estimated: 30 minutes
- Complexity: Low

---

# 🟢 LOW SEVERITY DEFECTS

## DEFECT ID: DEF-007
**Title:** Missing "No Data" Message in Some Views  
**Severity:** 🟢 LOW  
**Status:** 🔴 OPEN  
**Priority:** P3

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA - UI Test |
| **Reported Date** | February 8, 2026 |
| **Found In** | Frontend (admin_dashboard, teacher_dashboard) |
| **Affected Module** | View tables |
| **Reproducibility** | 100% |

### Description:
When there's no data, some tables still show "Loading..." message indefinitely instead of "No data found".

### Steps to Reproduce:
1. New teacher with no marks entered
2. Go to "View Marks" tab
3. See loading spinner stays visible

### Expected Behavior:
- After 2 seconds, show: "No marks found"
- Hide loading spinner

### Actual Behavior:
- Loading spinner visible indefinitely
- User doesn't know if page is broken

### Impact:
- Poor UX
- User confusion
- No critical impact

### Recommended Fix:
```javascript
if (data.success && data.marks.length > 0) {
    // Show table
} else {
    document.getElementById('marksTableContainer').innerHTML = 
        '<p class="text-center text-gray-500 py-8">No marks found</p>';
}
```

### Effort Estimate:
- Estimated: 30 minutes
- Complexity: Low

---

## DEFECT ID: DEF-008
**Title:** Grade Calculation Boundary Condition Issue  
**Severity:** 🟢 LOW  
**Status:** 🔴 OPEN  
**Priority:** P4

| Attribute | Value |
|-----------|-------|
| **Reported By** | QA - Calculation Test |
| **Reported Date** | February 8, 2026 |
| **Found In** | Backend (app.py - get_student_results) |
| **Affected Module** | Result calculation |
| **Reproducibility** | Specific percentage values |

### Description:
Student with exactly 70.00% shows grade "B" but should show "B+" as per logic (70-79 = B+).

### Steps to Reproduce:
1. Create student with total: 140 marks out of 200
2. Percentage = 70%
3. Check grade assignment

### Current Grade Logic:
```python
if percentage >= 90:  grade = 'A+'
elif percentage >= 80: grade = 'A'
elif percentage >= 70: grade = 'B+'   # Should trigger at 70
elif percentage >= 60: grade = 'B'
```

### Expected Behavior:
- 70% should get "B+" (because >= 70)

### Actual Behavior:
- Logic is correct, but might fail due to floating point

### Impact:
- Rare edge case
- Low severity

### Recommended Fix:
Use Decimal instead of Float for precise comparison:
```python
from decimal import Decimal
percentage = Decimal(str(percentage)).quantize(Decimal('0.01'))
```

### Effort Estimate:
- Estimated: 30 minutes
- Complexity: Low

---

# DEFECT RESOLUTION TRACKING

## Critical Issues Action Items

### Issue #1: Password Hashing - MUST FIX
- [ ] Update models.py with bcrypt hashing
- [ ] Update login validation
- [ ] Migrate existing passwords
- [ ] Test all login flows
- [ ] Security review
- **Target Date:** Within 1 week

### Issue #2: Input Sanitization - MUST FIX
- [ ] Install bleach library
- [ ] Sanitize all user inputs
- [ ] Test XSS prevention
- [ ] Security review
- **Target Date:** Within 1 week

### Issue #3: API Authentication - MUST FIX  
- [ ] Implement JWT or session validation
- [ ] Add decorators to protected endpoints
- [ ] Test unauthorized access is blocked
- [ ] Security audit
- **Target Date:** Before production

---

# RECOMMENDATIONS FOR FUTURE RELEASES

1. **Testing:**
   - Implement automated unit tests
   - Add integration tests for API endpoints
   - Set up continuous integration (CI/CD)

2. **Code Quality:**
   - Add code linting (flake8)
   - Implement type hints
   - Code review process

3. **Monitoring:**
   - Add error tracking (Sentry)
   - Set up performance monitoring
   - User analytics

4. **Documentation:**
   - API documentation (Swagger/OpenAPI)
   - User manual for each role
   - Developer documentation

5. **Database:**
   - Implement database migrations (Alembic)
   - Add data backup strategy
   - Performance optimization

---

# Defect Report Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| QA Lead | QA Team | 8-Feb-2026 | ✓ |
| Development Lead | Dev Team | - | - |
| Project Manager | PM | - | - |

---

**Document Version:** 1.0  
**Last Updated:** February 8, 2026  
**Next Review Date:** February 15, 2026
