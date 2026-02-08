# Production Deployment Checklist & Guide
## Student Result Management System v1.0

**Document Date:** February 8, 2026  
**Deployment Type:** Initial Release to Production  
**Environment:** Linux Server / Windows Server

---

## 🚨 PRE-DEPLOYMENT STATUS

```
CURRENT STATE: ❌ NOT READY FOR PRODUCTION
BLOCKING ISSUES: 3 Critical/High Security Risks
ESTIMATED FIX TIME: 3-4 Days
```

---

## ⚠️ MANDATORY FIXES BEFORE DEPLOYMENT

### BLOCKER 1: Password Hashing
**Status:** ❌ NOT IMPLEMENTED  
**Fix Time:** 2-3 hours  
**Priority:** 🔴 CRITICAL

```bash
# Step 1: Install werkzeug
pip install werkzeug

# Step 2: Update models.py
# Add imports at top:
from werkzeug.security import generate_password_hash, check_password_hash

# Step 3: Modify Student/Teacher/Admin classes
# Add these methods to each class:
def set_password(self, pwd):
    self.password = generate_password_hash(pwd)

def check_password(self, pwd):
    return check_password_hash(self.password, pwd)

# Step 4: Update add_student endpoint
new_student = Student(...)
new_student.set_password(password)  # Use method

# Step 5: Update login endpoints  
student = Student.query.filter_by(roll_no=roll_no).first()
if student and student.check_password(password):
    # Login successful

# Step 6: Delete old database
rm database.db
# Restart app.py to create fresh DB
```

**Verification:** 
```bash
# Login should work with S001/pass123
# Check database - passwords should be hashed (start with pbkdf2:sha256)
SELECT password FROM student LIMIT 1;
# Should NOT show "pass123"
```

---

### BLOCKER 2: Server-Side API Authentication
**Status:** ❌ NOT IMPLEMENTED  
**Fix Time:** 3-4 hours  
**Priority:** 🔴 CRITICAL

```bash
# Option A: Session-Based (Simpler)
# Update every protected endpoint:

@app.route('/api/add_marks', methods=['POST'])
def add_marks():
    # Add this check:
    if 'teacher_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    # Rest of code
    teacher_id = session['teacher_id']

# Option B: JWT-Based (Better for APIs)
pip install PyJWT

# Create decorator:
from functools import wraps
from flask import request
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

# Apply to protected routes:
@app.route('/api/add_marks', methods=['POST'])
@token_required
def add_marks(current_user_id):  # Now gets user_id
    # Code here
```

**Endpoints to Protect:**
```
POST /api/add_marks
POST /api/update_marks
POST /api/add_student
POST /api/delete_student
POST /api/add_teacher
POST /api/delete_teacher
GET  /api/teacher_marks
GET  /api/student_marks
GET  /api/all_students
GET  /api/all_teachers
GET  /api/all_results
```

**Verification:**
```bash
# Test endpoint without auth:
curl -X POST http://localhost:5000/api/add_marks
# Should return: 401 Unauthorized

# Test with auth:
curl -X POST http://localhost:5000/api/add_marks \
  -H "Authorization: Bearer TOKEN"
# Should work if token valid
```

---

### BLOCKER 3: Input Validation & Sanitization
**Status:** ❌ NOT IMPLEMENTED  
**Fix Time:** 1-2 hours  
**Priority:** 🟠 HIGH

```bash
# Step 1: Install bleach
pip install bleach

# Step 2: Add sanitization function
from bleach import clean

def sanitize_input(text):
    """Remove any HTML/scripts from input"""
    allowed_tags = []  # No HTML tags allowed
    return clean(text, tags=allowed_tags, strip=True)

# Step 3: Apply to all form inputs
@app.route('/api/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Sanitize all text inputs
    name = sanitize_input(data['name'])
    email = sanitize_input(data['email'])
    
    # Use sanitized values
    new_student = Student(
        roll_no=data['roll_no'],
        name=name,
        email=email,
        password=data['password']
    )
    
    db.session.add(new_student)
    db.session.commit()

# Do this for:
# - add_student
# - add_teacher  
# - update marks
# - any text input
```

**Test Injection:**
```
Try entering as name: <script>alert('XSS')</script>
Should either:
- Remove script tag, or
- Show error: "Invalid characters"
```

---

## ✅ DEPLOYMENT CHECKLIST

### Phase 1: Pre-Deployment (Day 1)

#### Security Fixes
- [ ] Password hashing implemented
- [ ] Server-side authentication added
- [ ] Input sanitization applied
- [ ] All 3 critical fixes tested
- [ ] Security audit passed
- [ ] OWASP Top 10 review completed

#### Code Quality
- [ ] Code review completed
- [ ] All test cases passing (53/54)
- [ ] No console errors
- [ ] No Python warnings
- [ ] Clean code without debug statements
- [ ] Comments added for complex logic

#### Documentation
- [ ] README.md complete
- [ ] API documentation done
- [ ] User manual written
- [ ] Admin guide created
- [ ] Deployment guide ready
- [ ] Troubleshooting doc prepared

#### Testing
- [ ] Functional testing: 100%
- [ ] Security testing: 100%
- [ ] Performance testing: 100%
- [ ] Compatibility testing: 100%
- [ ] UAT with actual users
- [ ] Load testing (100+ records)

---

### Phase 2: Environment Preparation (Day 2)

#### Server Setup (Linux/Windows)
- [ ] OS updated to latest patch
- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] Firewall configured
- [ ] Ports opened (5000, 443)

#### Database Setup
- [ ] SQLite database located on persistent storage
- [ ] Backup strategy defined
- [ ] Database permissions secured (600)
- [ ] Initial data loaded
- [ ] Backup tested to restore

#### Application Configuration
- [ ] Flask SECRET_KEY set (strong, random)
- [ ] CORS configured for production domain
- [ ] Database path correct
- [ ] Log directory created and permissions set
- [ ] Environment variables configured

```bash
# Sample environment setup
export FLASK_ENV=production
export FLASK_SECRET_KEY=your-secret-key-here
export DATABASE_URL=sqlite:////var/lib/app/database.db
export LOG_LEVEL=INFO
```

#### SSL/HTTPS Configuration
- [ ] SSL certificate acquired
- [ ] Certificate installed on server
- [ ] HTTPS configured in web server (Nginx/Apache)
- [ ] HTTP redirects to HTTPS
- [ ] Certificate renewal plan set

---

### Phase 3: Application Deployment (Day 3)

#### Backend Deployment
- [ ] Code transferred to production server
- [ ] Repository cloned or files uploaded
- [ ] Virtual environment created from requirements.txt
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Admin account created
- [ ] Default subjects loaded
- [ ] Application started

#### Frontend Deployment
- [ ] Static files served by web server
- [ ] API endpoints updated for production URL
- [ ] CORS headers configured
- [ ] Caching headers set
- [ ] Compression enabled
- [ ] CDN configured (if needed)

#### Web Server Configuration
- [ ] Nginx or Apache installed
- [ ] Reverse proxy configured for Flask app
- [ ] Static file serving configured
- [ ] SSL certificates installed
- [ ] Performance optimizations applied
- [ ] Security headers added

```nginx
# Example Nginx config
server {
    listen 443 ssl;
    server_name results.example.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /var/www/app/frontend;
    }
}
```

#### Application Service
- [ ] Systemd service created (Linux)
- [ ] Service configured to auto-start
- [ ] Service logs configured
- [ ] Service status monitored
- [ ] Restart policy set (always)

```ini
# /etc/systemd/system/student-results.service
[Unit]
Description=Student Result Management System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/app/backend
ExecStart=/var/www/app/.venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

### Phase 4: Testing & Validation (Day 4)

#### Smoke Testing
- [ ] Website loads (HTTPS)
- [ ] Student login works
- [ ] Teacher login works
- [ ] Admin login works
- [ ] Can add student
- [ ] Can enter marks
- [ ] Can view results
- [ ] Can logout

#### Functional Testing
- [ ] All CRUD operations working
- [ ] Calculations correct
- [ ] Grades assigned properly
- [ ] Pass/fail logic correct
- [ ] Error messages display
- [ ] Forms validate input

#### Security Testing
- [ ] Cannot access `/admin` without login
- [ ] Cannot view other student marks
- [ ] Cannot use other teacher's marks
- [ ] HTTPS enforced
- [ ] Passwords hashed in DB
- [ ] API requires authentication

#### Performance Testing
- [ ] Page load <3 seconds
- [ ] API response <1 second
- [ ] Database handles 1000+ records
- [ ] No memory leaks
- [ ] CPU usage normal

#### Browser Compatibility
- [ ] Chrome ✅
- [ ] Firefox ✅
- [ ] Safari ✅
- [ ] Edge ✅
- [ ] Mobile browsers ✅

---

### Phase 5: Go-Live (Day 5)

#### Pre-Launch
- [ ] Final backup taken
- [ ] Rollback plan documented
- [ ] Team trained
- [ ] Support lined up
- [ ] Monitoring active
- [ ] Alerts configured

#### Launch Activities
- [ ] DNS updated (if new domain)
- [ ] Load balancer configured
- [ ] Database replicated (if applicable)
- [ ] Backup automated
- [ ] Monitoring started
- [ ] Logs checked

#### Post-Launch (First 24 hours)
- [ ] Monitor error logs
- [ ] Check user feedback
- [ ] Monitor performance metrics
- [ ] Verify backups working
- [ ] Check security logs
- [ ] Ready for issues

#### Post-Launch (Week 1)
- [ ] No critical issues
- [ ] User training complete
- [ ] Documentation updated
- [ ] Performance baseline established
- [ ] Regular backups confirmed
- [ ] Support team confident

---

## 📊 DEPLOYMENT REQUIREMENTS

### Hardware Requirements
```
Minimum:
- Processor: 2 CPU cores
- RAM: 2 GB
- Storage: 10 GB
- Bandwidth: 10 Mbps

Recommended:
- Processor: 4+ CPU cores
- RAM: 8 GB
- Storage: 50 GB
- Bandwidth: 100 Mbps
```

### Software Requirements
```
- OS: Linux (Ubuntu 20.04+) or Windows Server 2019+
- Python: 3.10 or higher
- Database: SQLite (dev) or PostgreSQL (production)
- Web Server: Nginx 1.20+ or Apache 2.4+
- SSL: Let's Encrypt or paid certificate
```

### Network Requirements
```
- Port 80: HTTP (redirects to HTTPS)
- Port 443: HTTPS (main application)
- Port 22: SSH (administration only)
- Firewall: Restrict to necessary ports only
- DDoS Protection: Consider for public-facing
```

---

## 🔐 SECURITY HARDENING

### Before Deployment, Apply:

1. **Change Default Credentials:**
   ```python
   # Generate secure random password
   import secrets
   new_password = secrets.token_urlsafe(32)
   
   # Use for admin account
   ```

2. **Set Strong SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   # Use output in Flask config
   ```

3. **Enable Security Headers:**
   ```python
   @app.after_request
   def set_security_headers(response):
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'SAMEORIGIN'
       response.headers['X-XSS-Protection'] = '1; mode=block'
       response.headers['Strict-Transport-Security'] = 'max-age=31536000'
       return response
   ```

4. **Enable Rate Limiting:**
   ```bash
   pip install Flask-Limiter
   ```
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/api/student_login', methods=['POST'])
   @limiter.limit("5 per minute")
   def student_login():
       # Prevents brute force attacks
   ```

5. **Database Backup Automation:**
   ```bash
   # Cron job for daily backup
   0 2 * * * cp /var/lib/app/database.db /var/backups/database-$(date +%Y%m%d).db
   ```

6. **Logging & Monitoring:**
   ```python
   import logging
   logging.basicConfig(
       filename='/var/log/app/app.log',
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

---

## 🚀 DEPLOYMENT COMMANDS

### Linux Deployment

```bash
# 1. Connect to server
ssh user@production-server.com

# 2. Clone or upload code
git clone <repo> /var/www/app
# OR
scp -r Student_Result_management/ user@server:/var/www/app

# 3. Create virtual environment
cd /var/www/app
python3 -m venv .venv
source .venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Set permissions
chown -R www-data:www-data /var/www/app
chmod -R 755 /var/www/app
chmod 700 /var/www/app/backend

# 6. Create database directory
mkdir -p /var/lib/app
chmod 750 /var/lib/app

# 7. Initialize database
cd /var/www/app/backend
python app.py  # Run once to create DB, then Ctrl+C

# 8. Set up systemd service
sudo cp student-results.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable student-results
sudo systemctl start student-results
sudo systemctl status student-results

# 9. Configure web server
sudo cp nginx.conf /etc/nginx/sites-available/student-results
sudo ln -s /etc/nginx/sites-available/student-results /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 10. Check logs
tail -f /var/log/student-results/error.log
```

### Windows Server Deployment

```batch
REM 1. Open PowerShell as Administrator

REM 2. Navigate to project
cd C:\www\Student_Result_management

REM 3. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

REM 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM 5. Initialize database
cd backend
python app.py
REM Press Ctrl+C after it starts

REM 6. Create Windows Service
C:\path\to\nssm.exe install StudentResults "C:\www\Student_Result_management\.venv\Scripts\python.exe" "C:\www\Student_Result_management\backend\app.py"
nssm start StudentResults

REM 7. Configure IIS (if using IIS as reverse proxy)
REM Add URL Rewrite rule to forward to Flask on localhost:5000
```

---

## 📈 POST-DEPLOYMENT MONITORING

### Metrics to Monitor:
```
- Application uptime
- Response time (API)
- Error rate
- Database size
- Disk space
- Memory usage
- CPU usage
- Failed login attempts
- User activity
```

### Alerts to Configure:
```
- Application down (critical)
- Error rate >1% (warning)
- Response time >5s (warning)
- Disk space <10% (warning)
- Failed logins >10/minute (alert)
- Database size >1GB (warning)
```

### Daily Checks:
```
- Application running
- No errors in logs
- Database backup successful
- Performance metrics normal
- No security alerts
- User feedback collected
```

---

## 🔄 ROLLBACK PROCEDURE

If deployment fails or critical issues found:

```bash
# 1. Notify users
# 2. Stop application
systemctl stop student-results

# 3. Restore from backup
cp /var/backups/database-before-deploy.db /var/lib/app/database.db

# 4. Revert code
git revert HEAD  # or restore previous version

# 5. Restart application
systemctl start student-results

# 6. Verify
curl -I https://results.example.com
# Should see 200 OK

# 7. Monitor logs
tail -f /var/log/student-results/error.log
```

---

## 📝 DEPLOYMENT SIGN-OFF

### Must Have Approvals Before Deployment:

- [ ] **Development Manager:** _____________ Date: _______
- [ ] **Security Officer:** _____________ Date: _______
- [ ] **Database Administrator:** _____________ Date: _______
- [ ] **System Administrator:** _____________ Date: _______
- [ ] **Project Owner:** _____________ Date: _______

---

## 📞 DEPLOYMENT SUPPORT CONTACTS

During deployment, have these available:

| Role | Name | Phone | Email |
|------|------|-------|-------|
| DevOps Lead | _____________ | _____________ | _____________ |
| Database Admin | _____________ | _____________ | _____________ |
| Security Officer | _____________ | _____________ | _____________ |
| App Developer | _____________ | _____________ | _____________ |
| Support Manager | _____________ | _____________ | _____________ |

---

## ✅ FINAL CHECKLIST

Before clicking "Deploy":

- [ ] All 3 security blockers fixed and tested
- [ ] All tests passing (54/54)
- [ ] Security audit passed
- [ ] Performance tested with production load
- [ ] Backups verified to restore
- [ ] Rollback plan documented
- [ ] Team trained
- [ ] Support team ready
- [ ] On-call schedule set
- [ ] Monitoring configured
- [ ] Documentation complete

---

**Deployment Guide Version:** 1.0  
**Last Updated:** February 8, 2026  
**Ready for Deployment:** ❌ NO (Fix 3 security issues first)  
**Estimated Go-Live After Fixes:** 5-7 days
