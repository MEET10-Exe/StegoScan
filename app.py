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

    result = None
    image_path = None

    # SAFE SESSION HANDLING
    if "user" not in session:
        session["user"] = "guest"

    if "history" not in session:
        session["history"] = []

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if file and file.filename != "":
                filepath = os.path.join("static/uploads", file.filename)
                file.save(filepath)

                image_path = filepath

                result = analyze_image(filepath)

                session["history"].append({
                    "file": file.filename,
                    "status": result.get("status", "UNKNOWN"),
                    "score": result.get("security_score", 0),
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                session.modified = True

    except Exception as e:
        result = {
            "status": "SAFE ERROR MODE",
            "message": str(e)
        }

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result,
        image_path=image_path,
        history=session["history"]
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