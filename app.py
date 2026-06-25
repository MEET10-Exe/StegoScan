from flask import Flask, render_template, request
from detector import analyze_image
from datetime import datetime
import os

app = Flask(__name__)
scan_count = 0

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html", result={"security_score": 0})


@app.route("/scan", methods=["POST"])
def scan():

    file = request.files["image"]

    if file:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)
        global scan_count
        scan_count += 1

        result = analyze_image(filepath)

        image_path = "/" + filepath.replace("\\", "/")

        scan_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        filename = file.filename

        return render_template(
    
    "index.html",
    result=result,
    image_path=image_path,
    scan_time=scan_time,
    filename=filename,
    scan_count=scan_count,
)
            
        

    return render_template("index.html")

if __name__ == "__main__":
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
