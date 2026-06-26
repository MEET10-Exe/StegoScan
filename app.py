from flask import Flask, render_template, request, session, send_file
import os
from datetime import datetime

from detector import analyze_image
from report import generate_pdf

app = Flask(__name__)
app.secret_key = "stegoscan_safe_mode"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def dashboard():

    # SAFE INIT
    if "user" not in session:
        session["user"] = "guest"

    if "history" not in session:
        session["history"] = []

    result = {}
    image_path = None

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if file and file.filename != "":
                filename = file.filename.replace(" ", "_")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                # SAFE IMAGE PATH FOR HTML
                image_path = "uploads/" + filename

                # ANALYZE IMAGE
                result = analyze_image(filepath)

                # SAFE HISTORY UPDATE
                history = session["history"]
                history.append({
                    "file": filename,
                    "status": result.get("status", "UNKNOWN"),
                    "score": result.get("security_score", 0),
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                session["history"] = history
                session.modified = True

    except Exception as e:
        result = {
            "status": "SAFE MODE ACTIVE",
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

    if "history" not in session:
        session["history"] = []

    file_path = generate_pdf(
        session.get("user", "guest"),
        session.get("history", [])
    )

    return send_file(file_path, as_attachment=True)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)