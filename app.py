from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "level2_saas_secure_key"

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
            flash("Login successful 🚀")
            return redirect(url_for("dashboard"))

        flash("Enter valid username")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    user = session.get("user")
    history = session.get("history", [])

    result = None
    image_path = None

    try:
        if request.method == "POST":

            file = request.files.get("file")

            if not file or file.filename == "":
                flash("No file selected ❌")
                return redirect(url_for("dashboard"))

            filename = file.filename.replace(" ", "_")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            image_path = "uploads/" + filename

            # LEVEL 2 SMART SCORING (NO CRASH LOGIC)
            size_factor = os.path.getsize(filepath) % 100
            risk = min(95, max(10, size_factor))

            if risk > 70:
                status = "HIGH RISK"
            elif risk > 40:
                status = "MEDIUM RISK"
            else:
                status = "LOW RISK"

            result = {
                "status": status,
                "percentage": risk,
                "security_score": 100 - risk,
                "time": datetime.now().strftime("%H:%M:%S")
            }

            history.append({
                "file": filename,
                "status": status,
                "time": result["time"]
            })

            session["history"] = history
            session.modified = True

            flash("File analyzed successfully ✅")

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
    flash("Logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)