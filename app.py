from flask import Flask, render_template, request, redirect, url_for
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

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".mp3", ".wav", ".aac", ".flac", ".mp4", ".avi", ".mov", ".mkv", ".zip", ".rar", ".tar", ".gz", ".py", ".js", ".html", ".css"}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check if a file is allowed
def allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

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
        # Check if a file was uploaded
        if 'file' not in request.files:
            message = "No file part"
            return render_template("index.html", message=message)
        file = request.files['file']
        
        # If user doesn't select a file, browser also submits an empty part without a filename
        if file.filename == '':
            message = "No selected file"
            return render_template("index.html", message=message)
        
        if file and allowed_file(file.filename):
            # Save the file securely
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            message = "File uploaded successfully!"

            # Organize files after upload
            organize_files()
        else:
            message = "Invalid file type."

    return render_template("index.html", message=message)

# Use Waitress to run the app
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
