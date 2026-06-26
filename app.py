from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
from datetime import datetime

from detector import analyze_image
from report import generate_pdf

app = Flask(__name__)
app.secret_key = "stegoscan_final_key"

UPLOAD_FOLDER = "static/uploads"
REPORT_FOLDER = "reports"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


# ---------------- FILE CHECK ----------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- DASHBOARD ----------------
@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        session["user"] = "guest"

    user = session["user"]

    result = None
    image_path = None

    if "history" not in session:
        session["history"] = []

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if not file or file.filename == "":
                result = {"status": "ERROR", "message": "No file selected"}

            elif not allowed_file(file.filename):
                result = {"status": "ERROR", "message": "Only PNG, JPG, JPEG allowed"}

            else:
                filename = file.filename.replace(" ", "_")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                image_path = filepath

                result = analyze_image(filepath)

                time_now = datetime.now().strftime("%H:%M:%S")
                result["time"] = time_now

                session["history"].append({
                    "file": filename,
                    "status": result["status"],
                    "score": result.get("security_score", 0),
                    "time": time_now
                })

                session.modified = True

    except Exception as e:
        result = {
            "status": "SAFE MODE ACTIVE",
            "message": "System recovered safely",
            "debug": str(e)
        }

    return render_template(
        "dashboard.html",
        user=user,
        result=result,
        image_path=image_path,
        history=session.get("history", [])
    )


# ---------------- PDF DOWNLOAD ----------------
@app.route("/download")
def download():
    file_path = generate_pdf(session["user"], session.get("history", []))

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    return "PDF not found", 404


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)