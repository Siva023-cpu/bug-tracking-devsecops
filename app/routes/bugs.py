from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Bug, Solution
from app import db
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

bugs_bp = Blueprint("bugs", __name__)

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in \
        current_app.config["ALLOWED_EXTENSIONS"]

@bugs_bp.route("/")

@bugs_bp.route("/add-bug", methods=["GET", "POST"])
@login_required
def add_bug():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        severity = request.form.get("priority")
        file = request.files.get("bug_attachment")

        if not title or not description:
            flash("All fields are required!", "danger")
            return redirect(url_for("bugs.add_bug"))

        # Handle file attachment
        filename = None
        if file and file.filename != "":
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, "static/uploads", filename)
                file.save(upload_path)
            else:
                flash("File type not allowed!", "danger")
                return redirect(url_for("bugs.add_bug"))

        # Create new bug
        new_bug = Bug(
            title=title,
            description=description,
            severity=severity,
            status="Open",
            reported_by=current_user.username,
            user_id=current_user.id,
            attachment=filename  # save filename in DB
        )

        db.session.add(new_bug)
        db.session.commit()

        flash("Bug reported successfully!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("add_bug.html")

@bugs_bp.route("/bug/<int:bug_id>")
@login_required
def bug_detail(bug_id):
    from app.models import Bug

    bug = Bug.query.get_or_404(bug_id)
    return render_template("bug_detail.html", bug=bug)

@bugs_bp.route("/bug/<int:bug_id>/update", methods=["POST"])
@login_required
def update_status(bug_id):
    bug = Bug.query.get_or_404(bug_id)

    new_status = request.form.get("status")
    if new_status:
        bug.status = new_status
        db.session.commit()
        flash("Bug status updated successfully!", "success")

    return redirect(url_for("main.dashboard"))

@bugs_bp.route("/bug/<int:bug_id>/add-solution", methods=["POST"])
@login_required
def add_solution(bug_id):
    bug = Bug.query.get_or_404(bug_id)

    content = request.form.get("solution")
    file = request.files.get("solution_attachment")

    filename = None
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        upload_path = os.path.join("app/static/uploads", filename)
        file.save(upload_path)

    new_solution = Solution(
        content=content,
        user=current_user.username,
        bug_id=bug.id,
        attachment=filename
    )

    db.session.add(new_solution)
    db.session.commit()

    flash("Solution added successfully!", "success")
    return redirect(url_for("bugs.bug_detail", bug_id=bug.id))


@bugs_bp.route("/solution-download/<filename>")
@login_required
def download_solution(filename):
    """Serve solution attachments for download."""
    upload_folder = os.path.join(current_app.root_path, "static/uploads")
    
    # Check if file exists
    file_path = os.path.join(upload_folder, filename)
    if not os.path.exists(file_path):
        flash("File not found!", "danger")
        return redirect(url_for("main.dashboard"))
    
    return send_from_directory(upload_folder, filename, as_attachment=True)