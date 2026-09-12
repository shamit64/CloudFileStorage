from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    files = []

    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            modified = os.path.getmtime(filepath)

            files.append({
                "name": filename,
                "size": round(size / 1024, 2),
                "date": datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M:%S")
            })

    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return "No file selected"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    file.save(os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    ))

    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


@app.route("/delete/<filename>")
def delete_file(filename):

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)