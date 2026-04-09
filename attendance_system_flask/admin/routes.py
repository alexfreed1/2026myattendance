from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from models import Admin, Student, Class, Unit, Trainer, Department, ClassUnit

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        admin_model = Admin()
        # In a real application, you would hash the password and compare securely
        # For this demo, we'll do a direct comparison based on the provided credentials
        admins = admin_model.get_all()
        authenticated_admin = None
        for admin in admins:
            if admin["username"] == username and admin["password"] == password:
                authenticated_admin = admin
                break

        if authenticated_admin:
            session["admin_id"] = authenticated_admin["id"]
            session["admin_username"] = authenticated_admin["username"]
            flash("Logged in successfully!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("admin/login.html")

@admin_bp.route("/dashboard")
def dashboard():
    if "admin_id" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("admin.login"))
    return render_template("admin/dashboard.html")

@admin_bp.route("/logout")
def logout():
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))

# Placeholder routes for other admin functionalities
@admin_bp.route("/students")
def manage_students():
    if "admin_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("admin.login"))
    students = Student().get_all()
    return render_template("admin/students.html", students=students)

@admin_bp.route("/classes")
def manage_classes():
    if "admin_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("admin.login"))
    classes = Class().get_all()
    departments = Department().get_all()
    return render_template("admin/classes.html", classes=classes, departments=departments)

@admin_bp.route("/units")
def manage_units():
    if "admin_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("admin.login"))
    units = Unit().get_all()
    classes = Class().get_all()
    trainers = Trainer().get_all()
    return render_template("admin/units.html", units=units, classes=classes, trainers=trainers)

@admin_bp.route("/trainers")
def manage_trainers():
    if "admin_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("admin.login"))
    trainers = Trainer().get_all()
    departments = Department().get_all()
    return render_template("admin/trainers.html", trainers=trainers, departments=departments)
