from flask import Blueprint, render_template, redirect, url_for, session, request, flash
import bcrypt
from models import Admin, Student, Class, Unit, Trainer, Department, ClassUnit

admin_bp = Blueprint("admin", __name__, template_folder="templates")


def admin_required():
    if "admin_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("admin.login"))


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admins = Admin().get_all()
        authenticated_admin = None
        for adm in admins:
            stored_pw = adm["password"]
            try:
                pw_match = bcrypt.checkpw(password.encode(), stored_pw.encode())
            except Exception:
                pw_match = (password == stored_pw)
            if adm["username"] == username and pw_match:
                authenticated_admin = adm
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
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))


# ── Students ──────────────────────────────────────────────────────────────────

@admin_bp.route("/students")
def manage_students():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    students = Student().get_all()
    classes = Class().get_all()
    class_map = {c["id"]: c["name"] for c in classes}
    for s in students:
        s["class_name"] = class_map.get(s["class_id"], "N/A")
    return render_template("admin/students.html", students=students, classes=classes)


@admin_bp.route("/students/add", methods=["POST"])
def add_student():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Student().create({
        "name": request.form["name"],
        "reg_no": request.form["reg_no"],
        "class_id": request.form["class_id"]
    })
    flash("Student added.", "success")
    return redirect(url_for("admin.manage_students"))


@admin_bp.route("/students/edit/<id>", methods=["POST"])
def edit_student(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Student().update(id, {
        "name": request.form["name"],
        "reg_no": request.form["reg_no"],
        "class_id": request.form["class_id"]
    })
    flash("Student updated.", "success")
    return redirect(url_for("admin.manage_students"))


@admin_bp.route("/students/delete/<id>", methods=["POST"])
def delete_student(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Student().delete(id)
    flash("Student deleted.", "info")
    return redirect(url_for("admin.manage_students"))


# ── Classes ───────────────────────────────────────────────────────────────────

@admin_bp.route("/classes")
def manage_classes():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    classes = Class().get_all()
    departments = Department().get_all()
    dept_map = {d["id"]: d["name"] for d in departments}
    for c in classes:
        c["department_name"] = dept_map.get(c["department_id"], "N/A")
    return render_template("admin/classes.html", classes=classes, departments=departments)


@admin_bp.route("/classes/add", methods=["POST"])
def add_class():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Class().create({
        "name": request.form["name"],
        "department_id": request.form["department_id"]
    })
    flash("Class added.", "success")
    return redirect(url_for("admin.manage_classes"))


@admin_bp.route("/classes/edit/<id>", methods=["POST"])
def edit_class(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Class().update(id, {
        "name": request.form["name"],
        "department_id": request.form["department_id"]
    })
    flash("Class updated.", "success")
    return redirect(url_for("admin.manage_classes"))


@admin_bp.route("/classes/delete/<id>", methods=["POST"])
def delete_class(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Class().delete(id)
    flash("Class deleted.", "info")
    return redirect(url_for("admin.manage_classes"))


# ── Units ─────────────────────────────────────────────────────────────────────

@admin_bp.route("/units")
def manage_units():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    units = Unit().get_all()
    classes = Class().get_all()
    trainers = Trainer().get_all()
    class_units = ClassUnit().get_all()
    unit_map = {u["id"]: u for u in units}
    class_map = {c["id"]: c["name"] for c in classes}
    trainer_map = {t["id"]: t["name"] for t in trainers}
    for cu in class_units:
        cu["class_name"] = class_map.get(cu["class_id"], "N/A")
        cu["unit_title"] = unit_map.get(cu["unit_id"], {}).get("title", "N/A")
        cu["trainer_name"] = trainer_map.get(cu["trainer_id"], "N/A")
    return render_template("admin/units.html", units=units, classes=classes,
                           trainers=trainers, class_units=class_units)


@admin_bp.route("/units/add", methods=["POST"])
def add_unit():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Unit().create({"code": request.form["code"], "title": request.form["title"]})
    flash("Unit added.", "success")
    return redirect(url_for("admin.manage_units"))


@admin_bp.route("/units/edit/<id>", methods=["POST"])
def edit_unit(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Unit().update(id, {"code": request.form["code"], "title": request.form["title"]})
    flash("Unit updated.", "success")
    return redirect(url_for("admin.manage_units"))


@admin_bp.route("/units/delete/<id>", methods=["POST"])
def delete_unit(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Unit().delete(id)
    flash("Unit deleted.", "info")
    return redirect(url_for("admin.manage_units"))


@admin_bp.route("/class_units/add", methods=["POST"])
def add_class_unit():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    ClassUnit().create({
        "class_id": request.form["class_id"],
        "unit_id": request.form["unit_id"],
        "trainer_id": request.form["trainer_id"]
    })
    flash("Unit assigned to class.", "success")
    return redirect(url_for("admin.manage_units"))


@admin_bp.route("/class_units/delete/<id>", methods=["POST"])
def delete_class_unit(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    ClassUnit().delete(id)
    flash("Assignment removed.", "info")
    return redirect(url_for("admin.manage_units"))


# ── Trainers ──────────────────────────────────────────────────────────────────

@admin_bp.route("/trainers")
def manage_trainers():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    trainers = Trainer().get_all()
    departments = Department().get_all()
    dept_map = {d["id"]: d["name"] for d in departments}
    for t in trainers:
        t["department_name"] = dept_map.get(t["department_id"], "N/A")
    return render_template("admin/trainers.html", trainers=trainers, departments=departments)


@admin_bp.route("/trainers/add", methods=["POST"])
def add_trainer():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    hashed_pw = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt()).decode()
    Trainer().create({
        "name": request.form["name"],
        "username": request.form["username"],
        "password": hashed_pw,
        "department_id": request.form["department_id"]
    })
    flash("Trainer added.", "success")
    return redirect(url_for("admin.manage_trainers"))


@admin_bp.route("/trainers/edit/<id>", methods=["POST"])
def edit_trainer(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    data = {
        "name": request.form["name"],
        "username": request.form["username"],
        "department_id": request.form["department_id"]
    }
    if request.form.get("password"):
        data["password"] = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt()).decode()
    Trainer().update(id, data)
    flash("Trainer updated.", "success")
    return redirect(url_for("admin.manage_trainers"))


@admin_bp.route("/trainers/delete/<id>", methods=["POST"])
def delete_trainer(id):
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    Trainer().delete(id)
    flash("Trainer deleted.", "info")
    return redirect(url_for("admin.manage_trainers"))
