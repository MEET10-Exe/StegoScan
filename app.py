@app.route("/", methods=["GET", "POST"])
def dashboard():

    result = {}
    image_path = None

    # SAFE SESSION INIT
    if "user" not in session:
        session["user"] = "guest"

    if "history" not in session:
        session["history"] = []

    try:
        if request.method == "POST":
            file = request.files.get("file")

            if file and file.filename != "":
                filepath = os.path.join("static/uploads", file.filename)
                file.save(filepath)

                image_path = filepath

                result = analyze_image(filepath)

                if not result:
                    result = {}

                session["history"].append({
                    "file": file.filename,
                    "status": result.get("status", "UNKNOWN"),
                    "score": result.get("security_score", 0),
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                session.modified = True

    except Exception as e:
        result = {
            "status": "SAFE MODE ACTIVE",
            "message": str(e)
        }

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result,
        image_path=image_path,
        history=session["history"]
    )