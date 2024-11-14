from flask import Flask, render_template, request
import os
import shutil
from werkzeug.utils import secure_filename
from waitress import serve

app = Flask(__name__)

# Define file categories and extensions
file_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".html", ".css"],
    "Others": []
}

# Configure upload folder (relative to the app directory)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Organize files based on their type
def organize_files():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isdir(file_path):
            continue
        file_moved = False
        for category, extensions in file_categories.items():
            if any(filename.lower().endswith(ext) for ext in extensions):
                category_folder = os.path.join(UPLOAD_FOLDER, category)
                os.makedirs(category_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(category_folder, filename))
                file_moved = True
                break
        if not file_moved:
            others_folder = os.path.join(UPLOAD_FOLDER, "Others")
            os.makedirs(others_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(others_folder, filename))

# Route to render the HTML template
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        # Get the directory path from the form
        directory = request.form.get("directory")
        
        # Validate and organize files
        if os.path.isdir(directory):
            organize_files()
            message = "Files organized successfully!"
        else:
            message = "Invalid directory."
    return render_template("index.html", message=message)

# Use Waitress to run the app
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
