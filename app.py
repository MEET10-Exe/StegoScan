from flask import Flask, render_template, request, session, send_file
import os
import traceback
from datetime import datetime

from detector import analyze_image
from report import generate_pdf

app = Flask(__name__)
app.secret_key = "debug_mode_key"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "history" not in session:
        session["history"] = []

    if "user" not in session:
        session["user"] = "guest"

    result = {}
    image_path = None

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if not file:
                raise Exception("No file received")

            if file.filename == "":
                raise Exception("Empty filename")

            filename = file.filename.replace(" ", "_")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            image_path = "uploads/" + filename

            result = analyze_image(filepath)

            session["history"].append({
                "file": filename,
                "status": result.get("status", "UNKNOWN"),
                "score": result.get("security_score", 0),
                "time": datetime.now().strftime("%H:%M:%S")
            })

            session.modified = True

    except Exception as e:
        # 🔥 IMPORTANT: SHOW REAL ERROR
        error_msg = traceback.format_exc()

        return f"""
        <h2>❌ SERVER ERROR (DEBUG MODE)</h2>
        <pre>{error_msg}</pre>
        """

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result,
        image_path=image_path,
        history=session["history"]
    )


@app.route("/download")
def download():
    try:
        file_path = generate_pdf(
            session.get("user", "guest"),
            session.get("history", [])
        )
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"PDF ERROR: {str(e)}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)