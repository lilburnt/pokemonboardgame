from flask import Flask, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from process import process_excel_file

UPLOAD_FOLDER = "/path/to/upload"
ALLOWED_EXTENSIONS = {"xlsx"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            process_excel_file(file_path)
            return redirect(url_for("upload_file", filename=filename))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
