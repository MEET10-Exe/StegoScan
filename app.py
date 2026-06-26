from flask import Flask, render_template, request, session, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import traceback

from detector import analyze_image
from report import generate_pdf

# -----------------------------
# Flask App Configuration
# -----------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "stegoscan_secure_key")

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}

app.config.update(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH=10 * 1024 * 1024  # 10 MB limit
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Utility Functions
# -----------------------------
def allowed_file(filename: str) -> bool:
    """Check if uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# Error Handlers
# -----------------------------
@app.errorhandler(500)
def internal_error(error):
    """Custom error page for server errors."""
    return render_template(
        "dashboard.html",
        error="⚠️ Internal server error occurred. Please try again.",
        history=session.get("history", []),
        result={},
        image_path=None
    ), 500


# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def dashboard():
    """Main dashboard route for file upload and analysis."""

    session.setdefault("history", [])
    session.setdefault("user", "guest")

    result, image_path, error = {}, None, None

    try:
        if request.method == "POST":
            file = request.files.get("file")

            # --- Validation checks ---
            if not file:
                error = "❌ No file uploaded"
            elif file.filename.strip() == "":
                error = "❌ Please select a file"
            elif not allowed_file(file.filename):
                error = "❌ Only PNG, JPG, JPEG, BMP formats are allowed"
            else:
                # --- Secure unique filename ---
                filename = secure_filename(file.filename)
                unique_name = datetime.now().strftime("%Y%m%d%H%M%S_") + filename
                filepath = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], unique_name)

                file.save(filepath)
                image_path = f"uploads/{unique_name}"

                # --- Run analysis ---
                try:
                    result = analyze_image(filepath)
                    if not isinstance(result, dict):
                        result = {}
                except Exception:
                    print(traceback.format_exc())
                    result = {
                        "status": "ERROR",
                        "message": "Image analysis failed",
                        "percentage": 0,
                        "security_score": 0
                    }

                # --- Save history ---
                history_item = {
                    "file": unique_name,
                    "status": result.get("status", "UNKNOWN"),
                    "score": result.get("security_score", 0),
                    "time": datetime.now().strftime("%H:%M:%S")
                }
                session["history"].insert(0, history_item)
                session["history"] = session["history"][:20]  # keep last 20
                session.modified = True

    except Exception:
        print(traceback.format_exc())
        error = "⚠️ Unexpected error occurred"

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result,
        image_path=image_path,
        history=session["history"],
        error=error
    )


@app.route("/download")
def download():
    """Generate and download PDF report."""
    try:
        file_path = generate_pdf(session.get("user", "guest"), session.get("history", []))
        return send_file(file_path, as_attachment=True)
    except Exception:
        print(traceback.format_exc())
        return "❌ PDF generation failed"


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
