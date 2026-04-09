# Unit Attendance Register System (Flask + Supabase)

This project implements a Unit Attendance Register System for Thika Technical Training Institute, featuring Admin and Lecturer portals. The backend is built with Flask and uses Supabase for the database, with deployment targeting Render.

## Project Structure

```
attendance_system_flask/
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── database.py
├── models.py
├── admin/
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       └── admin_dashboard.html
├── lecturer/
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       └── lecturer_dashboard.html
└── templates/
    ├── base.html
    ├── index.html
    └── login.html
```

## Setup and Installation

### 1. Supabase Database Setup
1. Create a new project on [Supabase](https://supabase.com/).
2. Go to the **SQL Editor** in your Supabase dashboard.
3. Copy the contents of `init_db.sql` and run it to set up the tables and seed data.
   - **Supabase URL**: `https://zdtxdpbmksaznbhjepjp.supabase.co`
   - **Supabase Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpkdHhkcGJta3Nhem5iaGplcGpwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTY2NjI5MiwiZXhwIjoyMDkxMjQyMjkyfQ.TA-d5_iv-EmVr9OlMXm9m5Vyirf2IzwckTYNwfL_kxY` (service_role key)

### 2. Local Development
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure `config.py` contains your Supabase credentials and a `SECRET_KEY`.
4. Run the application:
   ```bash
   python app.py
   ```

### 3. Deployment on Render
1. Connect your GitHub repository to [Render](https://render.com/).
2. Create a new **Web Service**.
3. Use the following settings:
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add Environment Variables in the Render dashboard:
   - `SECRET_KEY` (generate a strong, random key)
   - The `SUPABASE_URL` and `SUPABASE_KEY` are already configured in `render.yaml`.

## Login Credentials (Demo)

### Admin Portal
- **Username**: admin
- **Password**: admin123

### Lecturer Portal
- **Trainer 1**: john / john123
- **Trainer 2**: mary / mary123

