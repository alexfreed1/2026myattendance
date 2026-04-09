from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from models import Trainer, Department, Class, Unit, Student, Attendance, ClassUnit

lecturer_bp = Blueprint("lecturer", __name__)

@lecturer_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        trainer_model = Trainer()
        trainers = trainer_model.get_all()
        authenticated_trainer = None
        for trainer in trainers:
            if trainer["username"] == username and trainer["password"] == password:
                authenticated_trainer = trainer
                break

        if authenticated_trainer:
            session["trainer_id"] = authenticated_trainer["id"]
            session["trainer_username"] = authenticated_trainer["username"]
            session["trainer_department_id"] = authenticated_trainer["department_id"]
            flash("Logged in successfully!", "success")
            return redirect(url_for("lecturer.select_department"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("lecturer/login.html")

@lecturer_bp.route("/select_department", methods=["GET", "POST"])
def select_department():
    if "trainer_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("lecturer.login"))
    
    departments = Department().get_all()
    
    if request.method == "POST":
        department_id = request.form["department_id"]
        session["selected_department_id"] = department_id
        return redirect(url_for("lecturer.dashboard"))
        
    return render_template("lecturer/select_department.html", departments=departments)

@lecturer_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "trainer_id" not in session or "selected_department_id" not in session:
        flash("Please select a department first.", "warning")
        return redirect(url_for("lecturer.select_department"))
    
    trainer_id = session["trainer_id"]
    selected_department_id = session["selected_department_id"]
    
    class_model = Class()
    classes = [c for c in class_model.get_all() if c["department_id"] == int(selected_department_id)]
    
    unit_model = Unit()
    class_unit_model = ClassUnit()
    
    selected_class_id = request.args.get("class_id")
    selected_unit_id = request.args.get("unit_id")
    selected_week = request.args.get("week")
    selected_lesson = request.args.get("lesson")

    students = []
    units_for_class = []
    attendance_records = []

    if selected_class_id:
        students = Student().supabase.from_("students").select("*").eq("class_id", selected_class_id).execute().data
        
        # Get units assigned to this trainer for the selected class
        class_units = class_unit_model.supabase.from_("class_units").select("unit_id").eq("class_id", selected_class_id).eq("trainer_id", trainer_id).execute().data
        unit_ids = [cu["unit_id"] for cu in class_units]
        units_for_class = unit_model.supabase.from_("units").select("*").in_("id", unit_ids).execute().data

        if selected_unit_id and selected_week and selected_lesson:
            attendance_records = Attendance().supabase.from_("attendance").select("*")\
                                .eq("unit_id", selected_unit_id)\
                                .eq("trainer_id", trainer_id)\
                                .eq("lesson", selected_lesson)\
                                .eq("week", selected_week).execute().data
            
            # Create a dictionary for quick lookup of existing attendance
            attendance_dict = {(rec["student_id"]): rec["status"] for rec in attendance_records}
            
            # Merge attendance status into student data
            for student in students:
                student["attendance_status"] = attendance_dict.get(student["id"], "Absent") # Default to Absent

    return render_template("lecturer/dashboard.html", 
                           classes=classes, 
                           students=students, 
                           units_for_class=units_for_class,
                           selected_class_id=selected_class_id,
                           selected_unit_id=selected_unit_id,
                           selected_week=selected_week,
                           selected_lesson=selected_lesson,
                           lessons=["L1", "L2", "L3", "L4"],
                           weeks=range(1, 53))

@lecturer_bp.route("/submit_attendance", methods=["POST"])
def submit_attendance():
    if "trainer_id" not in session or "selected_department_id" not in session:
        flash("Please log in and select a department first.", "warning")
        return redirect(url_for("lecturer.select_department"))

    trainer_id = session["trainer_id"]
    unit_id = request.form["unit_id"]
    class_id = request.form["class_id"]
    lesson = request.form["lesson"]
    week = request.form["week"]
    attendance_data = request.form.getlist("attendance") # List of student_id-status

    attendance_model = Attendance()
    
    # First, delete existing attendance for this unit, trainer, lesson, week, and class
    # This simplifies updates: delete all then insert new ones
    # Note: Supabase doesn't support deleting based on related table columns directly
    # So we need to get student_ids for the class first
    student_ids_in_class = [s["id"] for s in Student().supabase.from_("students").select("id").eq("class_id", class_id).execute().data]

    if student_ids_in_class:
        attendance_model.supabase.from_("attendance").delete()\
            .eq("unit_id", unit_id)\
            .eq("trainer_id", trainer_id)\
            .eq("lesson", lesson)\
            .eq("week", week)\
            .in_("student_id", student_ids_in_class).execute()

    records_to_insert = []
    for item in attendance_data:
        student_id, status = item.split("-")
        records_to_insert.append({
            "student_id": int(student_id),
            "unit_id": int(unit_id),
            "trainer_id": trainer_id,
            "lesson": lesson,
            "week": int(week),
            "status": status,
            "date": "2025-01-01" # Placeholder, ideally this would be dynamically set
        })
    
    if records_to_insert:
        attendance_model.supabase.from_("attendance").insert(records_to_insert).execute()

    flash("Attendance submitted successfully!", "success")
    return redirect(url_for("lecturer.dashboard", class_id=class_id, unit_id=unit_id, week=week, lesson=lesson))

@lecturer_bp.route("/logout")
def logout():
    session.pop("trainer_id", None)
    session.pop("trainer_username", None)
    session.pop("trainer_department_id", None)
    session.pop("selected_department_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("lecturer.login"))
