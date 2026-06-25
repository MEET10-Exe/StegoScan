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

        if file and file.filename != "":

            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(filepath)

            total_scans += 1

            # -------------------------
            # DEMO RESULT
            # Replace with detector.py
            # -------------------------

            security_score = 82
            risk_percentage = 18

            result = {
                "status": "SAFE",
                "percentage": risk_percentage,
                "security_score": security_score,
                "width": "Auto",
                "height": "Auto",
                "format": filename.split(".")[-1].upper(),
                "time": datetime.now().strftime("%H:%M:%S")
            }

            image_path = filepath

    return render_template(
    "index.html",
    total_scans=total_scans,
    result=result,
    image_path="/" + filepath
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)