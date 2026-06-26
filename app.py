from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from detector import analyze_image

app = Flask(__name__)
app.secret_key = "stegoscan_secret_key"

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

total_scans = 0


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    global total_scans

    result = None
    image_path = None

    if "history" not in session:
        session["history"] = []

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                image_path = filepath
                total_scans += 1

                result = analyze_image(filepath)
                result["time"] = datetime.now().strftime("%H:%M:%S")

                session["history"].append({
                    "file": filename,
                    "status": result["status"],
                    "time": result["time"]
                })

                session.modified = True

            else:
                result = {"status": "ERROR", "message": "Invalid file"}

    except Exception as e:
        result = {"status": "SAFE MODE", "message": str(e)}

    return render_template(
        "index.html",
        result=result,
        image_path=image_path,
        total_scans=total_scans,
        history=session.get("history", [])
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)