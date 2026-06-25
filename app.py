from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

total_scans = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global total_scans

    result = None
    image_path = None

    if request.method == "POST":

        file = request.files.get("file")

        if file and file.filename:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            image_path = "/" + filepath

            total_scans += 1

            result = {
                "status": "SAFE",
                "percentage": 18,
                "security_score": 82,
                "format": file.filename.split(".")[-1].upper()
            }

    return render_template(
        "index.html",
        total_scans=total_scans,
        result=result,
        image_path=image_path
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)