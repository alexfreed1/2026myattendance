# Attendance System - Thika Technical Training Institute

## Setup

1. Install dependencies:
   ```
   pip install -r attendance_system_flask/requirements.txt
   ```

2. Copy .env.example to .env and fill your Supabase details:
   ```
   copy .env.example .env  # Windows cmd
   cp .env.example .env    # Linux/Mac
   ```

3. Create tables and seed data in your Supabase project SQL Editor:
   - Paste content of `attendance_system_flask/init_db.sql`

4. Run the app:
   ```
   cd attendance_system_flask
   python app.py
   ```

5. Open http://127.0.0.1:5000

## Security Setup (Required for production)
1. Run:
   ```
   cd attendance_system_flask
   python hash_pws.py
   ```
   Copy hashed passwords.

2. In Supabase SQL Editor, update `admins`, `trainers` password fields with hashed values OR re-run modified init_db.sql.

## Test Logins (passwords: admin123, john123, mary123)
- Admin: username `admin`
- Lecturer: `john` (Electrical), `mary` (Mechanical)

## Deployment
Render/Heroku: Add env vars from .env to platform dashboard.
