from flask import Flask, render_template, request, session, send_file
import os
from datetime import datetime

from detector import analyze_image
from report import generate_pdf

app = Flask(__name__)
app.secret_key = "stegoscan_final_key_2026"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME ----------------
@app.route("/", methods=["GET", "POST"])
def dashboard():

    # SAFE SESSION INIT (NO CRASH)
    history = session.get("history", [])
    user = session.get("user", "guest")

    result = {"status": "READY"}
    image_path = None

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if file and file.filename:

                filename = file.filename.replace(" ", "_")
                filepath = os.path.join(UPLOAD_FOLDER, filename)

                file.save(filepath)

                # IMPORTANT: static-safe path
                image_path = "uploads/" + filename

                # AI ANALYSIS
                result = analyze_image(filepath)

                # SAFE HISTORY UPDATE (NO SESSION CRASH)
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
        result=result,
        image_path=image_path,
        history=history,
        user=user
    )


# ---------------- PDF DOWNLOAD ----------------
@app.route("/download")
def download():

    history = session.get("history", [])
    user = session.get("user", "guest")

    file_path = generate_pdf(user, history)

    return send_file(file_path, as_attachment=True)


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)