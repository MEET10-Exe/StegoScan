from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    send_file
)

from werkzeug.utils import secure_filename
from detector import analyze_image
from pdf_report import generate_pdf

import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "stegoscan_v3_secret"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )
total_scans = 0

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        if username:
            session["user"] = username
            session["history"] = []
            return redirect(url_for("dashboard"))
        else:
            flash("Please enter your username.")

    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    history = session.get("history", [])

    result = {}
    image_path = None

    if request.method == "POST":

        file = request.files.get("file")
        if not file or file.filename == "":
            flash("Please select an image.")
            return redirect(url_for("dashboard"))

        if not allowed_file(file.filename):
            flash("Only PNG, JPG and JPEG files are allowed.")
            return redirect(url_for("dashboard"))

        if file and file.filename != "" and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(filepath)
            
            analysis = analyze_image(filepath)

            image_path = url_for("static", filename=f"uploads/{filename}")

            size = os.path.getsize(filepath)
            risk = size % 100

            if risk > 70:
                status = "HIGH RISK"
            elif risk > 40:
                status = "MEDIUM RISK"
            else:
                status = "LOW RISK"

            result = {
              "status": analysis["status"],
              "percentage": analysis["percentage"],
              "security_score": analysis["security_score"],
              "width": analysis["width"],
              "height": analysis["height"],
              "format": analysis["format"],
              "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S") 
            } 
             
            session["last_result"] = result

            history.append({
                "file": filename,
                "status": status,
                "score": result["security_score"],
                "risk": result["percentage"],
                "time": result["time"]
            })

            session["history"] = history
            session.modified = True

        else:
            flash("Please select an image.")

    return render_template(
        "dashboard.html",
        user=user,
        result=result,
        image_path=image_path,
        history=history
    )


@app.route("/download_report")
def download_report():

    if "last_result" not in session:
        flash("No report available.")
        return redirect(url_for("dashboard"))

    pdf_file = generate_pdf(session["last_result"])

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="StegoScan_Report.pdf"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)