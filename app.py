from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
from datetime import datetime

from detector import analyze_image
from report import generate_pdf

app = Flask(__name__)
app.secret_key = "saas_secure_key_2026"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")

        if username:
            session["user"] = username
            session["history"] = []
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    history = session.get("history", [])

    result = {}
    image_path = None

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if file and file.filename:

                filename = file.filename.replace(" ", "_")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                image_path = "uploads/" + filename

                result = analyze_image(filepath)

                history.append({
                    "file": filename,
                    "status": result.get("status", "UNKNOWN"),
                    "score": result.get("security_score", 0),
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                session["history"] = history
                session.modified = True

    except Exception as e:
        result = {"status": "SAFE MODE", "message": str(e)}

    return render_template(
        "dashboard.html",
        user=user,
        result=result,
        image_path=image_path,
        history=history
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- PDF ----------------
@app.route("/download")
def download():
    file_path = generate_pdf(
        session.get("user", "guest"),
        session.get("history", [])
    )
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)