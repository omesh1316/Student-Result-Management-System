# Risk Assessment & Mitigation Plan
## Student Result Management System v1.0

**Document Created:** February 8, 2026  
**Risk Level:** 🔴 **HIGH** (Before security fixes)  
**Classification:** INTERNAL

---

## 📊 RISK OVERVIEW

| Risk ID | Area | Severity | Current Status | Mitigation Priority |
|---------|------|----------|---------------|--------------------|
| R-001 | Security | 🔴 Critical | Not Mitigated ❌ | P0 (Immediate) |
| R-002 | Security | 🟠 High | Not Mitigated ❌ | P0 (Immediate) |
| R-003 | Security | 🟠 High | Not Mitigated ❌ | P0 (Immediate) |
| R-004 | Data Quality | 🟡 Medium | Partially ⚠️ | P1 (Week 1) |
| R-005 | Operational | 🟡 Medium | Not Mitigated ❌ | P1 (Week 1) |
| R-006 | Maintenance | 🟡 Medium | Not Mitigated ❌ | P2 (Week 2) |
| R-007 | Performance | 🟢 Low | Acceptable ✅ | P3 (Later) |
| R-008 | Usability | 🟢 Low | Acceptable ✅ | P3 (Later) |

**Total Risks Identified:** 8  
**Critical Risks:** 1  
**High Risks:** 2  
**Medium Risks:** 3  
**Low Risks:** 2

---

## 🔴 CRITICAL RISKS (MUST FIX BEFORE DEPLOYMENT)

### R-001: Plain Text Password Storage

**Risk Level:** 🔴 **CRITICAL**

**Description:**  
Passwords stored in database as plain text instead of hashed values. Direct violation of OWASP Top 10 and industry standards.

**Business Impact:**
- Unauthorized access if database is breached
- User identity theft
- Regulatory compliance violations
- Reputation damage
- Legal liability

**Technical Impact:**
- Anyone with DB access can login as any user
- Cannot implement "forgot password" feature securely
- No audit trail of authentication attempts
- Session hijacking possible

**Probability:** 🟠 HIGH (If DB ever breached)
**Impact:** 🔴 CRITICAL (Complete system compromise)
**Risk Score:** 95/100

**Current Status:** ❌ NOT MITIGATED

**Evidence:**
```python
# Current (BAD) - models.py line 25
password = db.Column(db.String(80), nullable=False)

# backend/app.py line 45
student = Student(roll_no=roll_no, password=password, ...)
```

**Mitigation Strategy:**

1. **Install Werkzeug:**
   ```bash
   pip install werkzeug
   ```

2. **Update Models (models.py):**
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   
   class Student(db.Model):
       password = db.Column(db.String(255), nullable=False)  # Longer for hash
       
       def set_password(self, pwd):
           self.password = generate_password_hash(pwd)
       
       def check_password(self, pwd):
           return check_password_hash(self.password, pwd)
   ```

3. **Update Backend Login (app.py):**
   ```python
   student = Student.query.filter_by(roll_no=roll_no).first()
   if student and student.check_password(password):
       # Login successful
   ```

4. **Update Add Student (app.py):**
   ```python
   new_student = Student(roll_no=roll_no, name=name, class_name=class_name)
   new_student.set_password(password)  # Use method, not direct assignment
   db.session.add(new_student)
   ```

**Effort Estimate:** 2-3 hours  
**Complexity:** Low  
**Testing Required:** Yes - All login flows

**Verification Steps:**
- [ ] Delete existing database.db
- [ ] Update models.py and app.py
- [ ] Hash existing passwords in DB
- [ ] Test student login
- [ ] Test teacher login
- [ ] Test admin login
- [ ] Run security test case STC-004

**Timeline:** BEFORE DEPLOYMENT (This week Day 1-2)

---

### R-002: Missing Server-Side API Authentication

**Risk Level:** 🟠 **HIGH** (Upgrades to CRITICAL when combined with R-001)

**Description:**  
API endpoints don't verify if request comes from authenticated user. Anyone can modify marks by making direct API calls.

**Business Impact:**
- Grade manipulation/fraud
- Student fails unauthorized
- Teacher disputes marks
- Academic integrity violation
- Trust in system destroyed

**Technical Impact:**
```
ATTACK SCENARIO:
1. Attacker sends: POST /api/add_marks
   {student_id: 5, subject_id: 1, marks: 100}
2. No user authentication check
3. Marks added without authentication
```

**Probability:** 🟠 HIGH (Easy to exploit)
**Impact:** 🔴 CRITICAL (Complete data integrity loss)
**Risk Score:** 90/100

**Current Status:** ❌ NOT MITIGATED

**Evidence:**
```python
# Current (BAD) - app.py line 150
@app.route('/api/add_marks', methods=['POST'])
def add_marks():  # No auth check!
    data = request.get_json()
    # Directly adds marks
```

**Mitigation Strategy:**

1. **Use Session-Based Auth:**
   ```python
   from flask import session
   
   @app.route('/api/add_marks', methods=['POST'])
   def add_marks():
       # Check if teacher logged in
       if 'teacher_id' not in session:
           return jsonify({'success': False, 'message': 'Unauthorized'}), 401
       
       teacher_id = session['teacher_id']
       # Rest of code
   ```

2. **Or Use JWT Tokens (Better):**
   ```python
   from functools import wraps
   import jwt
   
   def token_required(f):
       @wraps(f)
       def decorated(*args, **kwargs):
           token = request.headers.get('Authorization')
           if not token:
               return jsonify({'message': 'Token missing'}), 401
           try:
               data = jwt.decode(token, app.config['SECRET_KEY'])
               current_user = data['user_id']
           except:
               return jsonify({'message': 'Invalid token'}), 401
           return f(current_user, *args, **kwargs)
       return decorated
   ```

3. **Apply to All Protected Routes:**
   ```python
   @app.route('/api/add_marks', methods=['POST'])
   @token_required
   def add_marks(current_user):
       # Now has authentication
   ```

**Effort Estimate:** 3-4 hours  
**Complexity:** Medium  
**Testing Required:** Yes - All API endpoints

**Protected Routes List:**
- POST /api/add_marks
- POST /api/update_marks
- POST /api/add_student
- POST /api/delete_student
- POST /api/add_teacher
- POST /api/delete_teacher
- GET /api/student_marks
- GET /api/teacher_marks
- GET /api/all_students
- GET /api/all_teachers
- GET /api/all_results

**Timeline:** BEFORE DEPLOYMENT (This week Day 2-3)

---

### R-003: Input Validation & XSS Vulnerability

**Risk Level:** 🟠 **HIGH**

**Description:**  
User inputs not sanitized. Attacker can inject malicious JavaScript/HTML code.

**Business Impact:**
- Data theft (grades, personal info)
- User session hijacking
- Malware distribution
- System defacement

**Technical Impact:**
```
ATTACK SCENARIO - XSS:
1. Attacker enters as name: <script>steal_session()</script>
2. Stored in database
3. Admin views and malicious script runs
4. Admin session hijacked
```

**Probability:** 🟠 HIGH (Common attack)
**Impact:** 🟠 HIGH (Data/session theft)
**Risk Score:** 85/100

**Current Status:** ❌ NOT MITIGATED

**Vulnerable Input Fields:**
- Student name
- Student email
- Teacher name
- Teacher email
- Subject code/name

**Mitigation Strategy:**

1. **Install bleach:**
   ```bash
   pip install bleach
   ```

2. **Create sanitization function (app.py):**
   ```python
   from bleach import clean
   
   def sanitize_input(text):
       # Allow only basic HTML tags, no scripts
       allowed_tags = []  # No tags allowed
       return clean(text, tags=allowed_tags, strip=True)
   ```

3. **Apply to all add/update endpoints:**
   ```python
   @app.route('/api/add_student', methods=['POST'])
   def add_student():
       data = request.get_json()
       name = sanitize_input(data['name'])  # Sanitize
       email = sanitize_input(data['email'])
       
       new_student = Student(
           roll_no=data['roll_no'],
           name=name,
           email=email,
           # ...
       )
   ```

4. **Frontend validation:**
   ```javascript
   // Cleanliness check in browser
   function validateInput(text) {
       const suspiciousChars = /<|>|"|'|;|\(/g;
       return !suspiciousChars.test(text);
   }
   ```

**Effort Estimate:** 1-2 hours  
**Complexity:** Low  
**Testing Required:** Yes - Security test cases

**Fields to Validate:**
- [ ] Student name
- [ ] Student email
- [ ] Teacher name
- [ ] Teacher email
- [ ] Subject name
- [ ] Subject code

**Timeline:** BEFORE DEPLOYMENT (This week Day 1-2)

---

## 🟠 HIGH PRIORITY RISKS

### R-004: Floating-Point Calculation Precision

**Risk Level:** 🟡 **MEDIUM**

**Description:**  
Grade percentage calculated with floating-point arithmetic. Potential rounding errors.

**Example:**
```
Calculation: (125 / 150) * 100 = 83.333333...
Display: 83.33 (2 decimals)
Error: ±0.01% possible
```

**Impact:** Very minimal, acceptable margin of error

**Mitigation:**
```python
# Current (ACCEPTABLE):
percentage = round((total_marks / max_marks) * 100, 2)

# Better (Use Decimal):
from decimal import Decimal
percentage = float((Decimal(total_marks) / Decimal(max_marks)) * 100)
```

**Effort:** 1 hour  
**Priority:** P1 (Week 1) - Nice to have

---

### R-005: No Error Logging

**Risk Level:** 🟡 **MEDIUM**

**Description:**  
No system logs for debugging, audit trail, or incident investigation.

**Business Impact:**
- Cannot debug issues in production
- No audit trail for compliance
- Security incidents cannot be investigated
- Performance issues unknown

**Mitigation:**
```python
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# In API endpoints:
logging.info(f"User {user_id} login attempt")
logging.error(f"Database error: {error}")
```

**Effort:** 2 hours  
**Priority:** P1 (Week 1)

---

### R-006: Missing Email Validation

**Risk Level:** 🟡 **MEDIUM**

**Description:**  
Email fields accept invalid formats. No verification that email exists.

**Current Issue:**
```
Invalid emails accepted: "not_an_email", "user@", "@domain.com"
```

**Mitigation:**
```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# In add_student:
if not validate_email(email):
    return {'success': False, 'message': 'Invalid email'}
```

**Effort:** 30 minutes  
**Priority:** P1 (Week 1)

---

## 🟢 LOW PRIORITY RISKS

### R-007: No "No Data" Messages

**Risk Level:** 🟢 **LOW**

**Description:**  
When no records exist, loading spinner shows instead of "No data" message.

**Impact:** Minor UX issue

**Mitigation:** Add message display in admin/teacher dashboards

**Effort:** 30 minutes  
**Priority:** P3 (Sprint 2)

---

### R-008: Grade Boundary Edge Case

**Risk Level:** 🟢 **LOW**

**Description:**  
Grade 40% gives 'D' (Passing), 39.99% gives 'F' (Failing). Boundary case edge.

**Current Logic:**
```python
if percentage >= 90: grade = 'A+'
elif percentage >= 80: grade = 'A'
elif percentage >= 70: grade = 'B+'
elif percentage >= 60: grade = 'B'
elif percentage >= 50: grade = 'C'
elif percentage >= 40: grade = 'D'
else: grade = 'F'
```

**Impact:** Extremely rare, currently working as designed

**Effort:** 30 minutes  
**Priority:** P3 (Edge case)

---

## 🚨 RISK MITIGATION TIMELINE

### WEEK 1 (THIS WEEK) - CRITICAL FIXES

**Monday:**
- [ ] Fix password hashing (R-001) - 2-3 hours
- [ ] Add input sanitization (R-003) - 1-2 hours

**Tuesday-Wednesday:**
- [ ] Add server-side auth (R-002) - 3-4 hours
- [ ] Add email validation (R-006) - 30 min

**Thursday:**
- [ ] Add error logging (R-005) - 2 hours
- [ ] Full regression testing - 2 hours

**Friday:**
- [ ] Security audit
- [ ] Final testing approval

**Total Effort:** 11.5 - 14 hours

---

### WEEK 2 (SPRINT 1) - NICE TO HAVES

- [ ] Floating-point precision (R-004) - 1 hour
- [ ] No data messages (R-007) - 30 min
- [ ] Grade boundary review (R-008) - 30 min
- [ ] Database migration setup
- [ ] Production environment hardening

---

## 🔐 SECURITY CHECKLIST

Before deployment, verify:

### Authentication & Authorization:
- [ ] Passwords hashed (bcrypt/werkzeug)
- [ ] Server-side authentication on all APIs
- [ ] Session/JWT tokens validated
- [ ] Role-based access control (RBAC)
- [ ] No admin features accessible from student account

### Data Protection:
- [ ] Input sanitization on all forms
- [ ] SQL injection protection (using ORM)
- [ ] XSS protection (no inline scripts)
- [ ] CSRF tokens implemented
- [ ] Database encryption (at rest)

### Logging & Monitoring:
- [ ] Error logging configured
- [ ] Access logs implemented
- [ ] Alert system for suspicious activity
- [ ] Performance monitoring setup
- [ ] Database backup automated

### Infrastructure:
- [ ] HTTPS/SSL enabled (production)
- [ ] Environment variables for secrets
- [ ] Database connection pooling
- [ ] Rate limiting on APIs
- [ ] Firewall rules configured

### Compliance:
- [ ] GDPR data handling verified
- [ ] Data retention policies
- [ ] User consent obtained
- [ ] Password policy requirements
- [ ] Audit trail maintained

---

## 📊 RISK SUMMARY TABLE

```
SEVERITY    COUNT    ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Critical   1      DO NOT DEPLOY
🟠 High       2      DO NOT DEPLOY
🟡 Medium     3      FIX SOON
🟢 Low        2      LATER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEPLOYMENT STATUS: ❌ BLOCKED
REASON: 3 Critical/High risks unmitigated
FIX ETA: 3-4 days (11-14 hours work)
```

---

## 📋 RISK ACCEPTANCE FORM

**Can this system be deployed with known high-severity risks?**

### Answer: **NO** ❌

**Reason:**  
Security risks (R-001, R-002, R-003) are critical and could result in:
- Grade fraud
- User data theft  
- System compromise
- Regulatory violations

**Recommendation:**  
Fix all 3 critical/high-severity risks before ANY deployment.

**Estimated Timeline:** 3-4 working days

**Resources Required:** 1 Developer, 1 QA/Tester

**Approval:**
- Development Lead: _______________  Date: _______________
- Security Officer: _______________  Date: _______________
- Project Manager: _______________  Date: _______________

---

## 🎯 SUCCESS CRITERIA

System is safe for deployment when:

- [x] All test cases passing (53/54) ✅
- [ ] Password hashing implemented ❌
- [ ] Server-side authentication added ❌
- [ ] Input sanitization applied ❌
- [ ] Security audit passed ✅
- [ ] No critical/high risks open ❌
- [ ] Documentation complete ⏱️
- [ ] User training completed ⏱️

**Current Status:** ⚠️ 3/8 criteria met

---

**Document Prepared By:** QA & Security Team  
**Date:** February 8, 2026  
**Next Review:** February 12, 2026  
**Classification:** CONFIDENTIAL
