from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from detector import analyze_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs("static/uploads", exist_ok=True)

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

    try:
        if request.method == "POST":

            file = request.files.get("file")

            # SAFE CHECK 1
            if not file or file.filename == "":
                result = {"status": "ERROR", "message": "No file selected"}

            elif not allowed_file(file.filename):
                result = {"status": "ERROR", "message": "Only PNG, JPG, JPEG allowed"}

            else:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                file.save(filepath)

                image_path = os.path.join("static/uploads", filename)

                total_scans += 1

                # 🔥 SAFE DETECTOR CALL (IMPORTANT)
                try:
                    result = analyze_image(filepath)
                except Exception:
                    result = {
                        "status": "ERROR",
                        "percentage": 0,
                        "security_score": 0,
                        "format": filename.split(".")[-1].upper(),
                        "message": "Analysis failed safely"
                    }

                result["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception:
        # NEVER CRASH PAGE
        result = {
            "status": "SAFE MODE",
            "message": "System handled unexpected error safely"
        }

    return render_template(
        "index.html",
        result=result,
        image_path=image_path,
        total_scans=total_scans
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)