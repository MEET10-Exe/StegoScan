from flask import Flask, render_template, request, session, send_file
import os
from datetime import datetime
from detector import analyze_image
from report import generate_pdf

app = Flask(__name__)
app.secret_key = "stegoscan_final_fix"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# SAFE MEMORY STORE (NO SESSION LIST CRASH)
history_store = {}


@app.route("/", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        session["user"] = "guest"

    user = session["user"]

    if user not in history_store:
        history_store[user] = []

    result = {}
    image_path = None

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if file and file.filename != "":
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)

                image_path = filepath

                result = analyze_image(filepath)

                history_store[user].append({
                    "file": file.filename,
                    "status": result.get("status", "UNKNOWN"),
                    "score": result.get("security_score", 0),
                    "time": datetime.now().strftime("%H:%M:%S")
                })

    except Exception as e:
        result = {
            "status": "SAFE MODE",
            "message": str(e)
        }

    return render_template(
        "dashboard.html",
        user=user,
        result=result,
        image_path=image_path,
        history=history_store[user]
    )


@app.route("/download")
def download():
    user = session.get("user", "guest")
    file_path = generate_pdf(user, history_store.get(user, []))
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)