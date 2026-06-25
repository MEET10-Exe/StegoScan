from flask import Flask, render_template, request
from detector import analyze_image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

scan_count = 0


@app.route("/")
@app.route("/")
def home():
    return render_template(
        "index.html",
        result={
            "status": "READY",
            "percentage": 0,
            "security_score": 100,
            "format": "-",
            "width": "-",
            "height": "-"
        },
        scan_count=scan_count,
        image_path=None
    )


@app.route("/scan", methods=["POST"])
def scan():
    global scan_count

    file = request.files.get("image")

    if not file:
        return render_template(
            "index.html",
            result={"status": "No file uploaded", "percentage": 0, "security_score": 0},
            scan_count=scan_count
        )

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    scan_count += 1

    result = analyze_image(filepath)

    return render_template(
        "index.html",
        result=result,
        image_path="/" + filepath.replace("\\", "/"),
        scan_count=scan_count
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)