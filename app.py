from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from datetime import datetime 

app = Flask(__name__)
app.secret_key = "level2_saas_secure_key"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        if username:
            session["user"] = username
            session["history"] = []
            return redirect(url_for("dashboard"))

        flash("Enter username")

    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    user = session.get("user")
    history = session.get("history", [])

    result = result or {}
image_path = image_path or ""
history = session.get("history", [])

    try:
        if request.method == "POST":

            file = request.files.get("file")

            if file and file.filename:

                filename = file.filename.replace(" ", "_")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                # SAFE STATIC PATH (IMPORTANT FIX)
                image_path = url_for('static', filename=f'uploads/{filename}')

                size = os.path.getsize(filepath)
                risk = min(95, max(5, size % 100))

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
    "score": result.get("security_score", 0),
    "time": result["time"]
})
                session["history"] = history
                session.modified = True

    except Exception as e:
        result = {
            "status": "SAFE MODE",
            "percentage": 0,
            "security_score": 0,
            "message": str(e)
        } return render_template(
        "dashboard.html",
        user=user,
        result=result,
        image_path=image_path,
        history=history
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)