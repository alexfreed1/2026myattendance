# TODO.md - Making Attendance System Work Perfectly

## Approved Plan Steps (Progress: 2/6)

### 1. Create TODO.md [COMPLETED]
   - [x] Created this file to track progress.

### 2. Environment Setup [COMPLETED]
   - [x] Created .env.example and .env (with creds)
   - [x] Updated requirements.txt (+bcrypt duplicate ignored)
   - [x] Updated app.py (dotenv + Config)
   - [x] Updated database.py/config.py (env-only)
   - [x] Updated README.md (setup instructions)

### 3. Security Improvements [COMPLETED]
   - [x] Installed bcrypt
   - [x] Updated admin/lecturer routes.py (bcrypt.checkpw)
   - [x] Created hash_pws.py script
   - [x] Updated README.md (security instructions)

### 4. Fix Templates & Error Handling [COMPLETED]
   - [x] Verified all templates exist (base/index + admin/lecturer dashboards, lists, logins)
   - [x] Added try/except to model.get_all() (safe DB fetch)
   - [x] Dynamic date in attendance

### 5. Testing & Local Run [READY]
   - [x] Instructions in updated README.md
   - Test full flow: index → login → CRUD/attendance

### 4. Fix Templates & Error Handling
   - Verify/create missing templates (admin/dashboard.html etc.)
   - Add try/except to Supabase calls

### 5. Testing & Local Run
   - Instructions in updated README.md
   - Test full flow: index → login → CRUD/attendance

### 6. Deployment Polish
   - Update Procfile/render.yaml for env vars
   - Final tests

**Next: Step 3 - Security Improvements**

**Status:** Env setup done. Run `pip install -r attendance_system_flask/requirements.txt` then `cd attendance_system_flask && python app.py` to test base functionality before security.

