from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import json
import reader
import os, shutil
import queue
import threading

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}


def deleteFiles(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        os.remove(file_path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
deleteFiles(UPLOAD_FOLDER)
file_queue = queue.Queue()
# read = reader.Reader()

def reader_thread():
    while True:
        item = file_queue.get(block=True)
        print("New file is being read")
        # readed = read.read(item)
        # if os.path.exists(readed):
        #   os.remove(readed)
        # print(readed)
        file_queue.task_done()

threading.Thread(target=reader_thread, daemon=True).start()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return send_file("static/index.html")
    elif request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "Missing file"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"file saved to {path}")
            file.save(path)
            file_queue.put(path)
            return jsonify({"success": "File saved"}), 400

if __name__ == '__main__':
    app.run(port=80)