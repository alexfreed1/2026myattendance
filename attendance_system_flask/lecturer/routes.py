from flask import Blueprint, render_template, redirect, url_for, session, request, flash
import bcrypt
from datetime import datetime
from models import Trainer, Department, Class, Unit, Student, Attendance, ClassUnit

lecturer_bp = Blueprint("lecturer", __name__, template_folder="templates")

@lecturer_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        trainers = Trainer().get_all()
        authenticated_trainer = None
        for trainer in trainers:
            stored_pw = trainer["password"]
            try:
                pw_match = bcrypt.checkpw(password.encode(), stored_pw.encode())
            except Exception:
                pw_match = (password == stored_pw)
            if trainer["username"] == username and pw_match:
                authenticated_trainer = trainer
                break

        if authenticated_trainer:
            session["trainer_id"] = authenticated_trainer["id"]
            session["trainer_username"] = authenticated_trainer["username"]
            session["trainer_department_id"] = authenticated_trainer["department_id"]
            flash("Logged in successfully!", "success")
            return redirect(url_for("lecturer.dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("lecturer/login.html")


@lecturer_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "trainer_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("lecturer.login"))

    trainer_id = session["trainer_id"]
    trainer_department_id = session["trainer_department_id"]

    # Classes in trainer's department
    all_classes = Class().get_all()
    classes = [c for c in all_classes if c["department_id"] == trainer_department_id]

    selected_class_id = request.args.get("class_id")
    selected_unit_id = request.args.get("unit_id")
    selected_week = request.args.get("week")
    selected_lesson = request.args.get("lesson")

    students = []
    units_for_class = []

    if selected_class_id:
        db = Student().supabase
        students = db.from_("students").select("*").eq("class_id", selected_class_id).execute().data

        # Units assigned to this trainer for the selected class
        class_units = db.from_("class_units").select("unit_id")\
            .eq("class_id", selected_class_id)\
            .eq("trainer_id", trainer_id).execute().data
        unit_ids = [cu["unit_id"] for cu in class_units]

        if unit_ids:
            units_for_class = db.from_("units").select("*").in_("id", unit_ids).execute().data

        if selected_unit_id and selected_week and selected_lesson:
            attendance_records = db.from_("attendance").select("*")\
                .eq("unit_id", selected_unit_id)\
                .eq("trainer_id", trainer_id)\
                .eq("lesson", selected_lesson)\
                .eq("week", selected_week).execute().data

            attendance_dict = {rec["student_id"]: rec["status"] for rec in attendance_records}
            for student in students:
                student["attendance_status"] = attendance_dict.get(student["id"], "Absent")

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
    if "trainer_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("lecturer.login"))

    trainer_id = session["trainer_id"]
    unit_id = request.form["unit_id"]
    class_id = request.form["class_id"]
    lesson = request.form["lesson"]
    week = request.form["week"]
    attendance_data = request.form.getlist("attendance")  # list of "student_id-Status"

    db = Attendance().supabase

    # Get student IDs for this class
    student_ids = [s["id"] for s in db.from_("students").select("id").eq("class_id", class_id).execute().data]

    if student_ids:
        db.from_("attendance").delete()\
            .eq("unit_id", unit_id)\
            .eq("trainer_id", trainer_id)\
            .eq("lesson", lesson)\
            .eq("week", week)\
            .in_("student_id", student_ids).execute()

    records_to_insert = []
    for item in attendance_data:
        student_id, status = item.rsplit("-", 1)
        records_to_insert.append({
            "student_id": student_id,
            "unit_id": unit_id,
            "trainer_id": trainer_id,
            "lesson": lesson,
            "week": int(week),
            "status": status,
            "date": datetime.now().strftime('%Y-%m-%d')
        })

    if records_to_insert:
        db.from_("attendance").insert(records_to_insert).execute()

    flash("Attendance submitted successfully!", "success")
    return redirect(url_for("lecturer.dashboard",
                            class_id=class_id, unit_id=unit_id,
                            week=week, lesson=lesson))


@lecturer_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("lecturer.login"))
