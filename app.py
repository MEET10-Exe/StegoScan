from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Counter for scans
total_scans = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global total_scans
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            # Save uploaded file (optional)
            upload_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(upload_path)

            # Increase scan count
            total_scans += 1

            # Here you can call your StegoScan detection logic
            # Example: result = detect_hidden_data(upload_path)

            return render_template("index.html", total_scans=total_scans)
    return render_template("index.html", total_scans=total_scans)

if __name__ == "__main__":
    app.run(debug=True)
