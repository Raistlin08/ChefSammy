from flask import Flask, request
import json
import reader
import os
import queue
import threading

file_queue = queue.Queue()
# read = reader.Reader()

def reader_thread():
    while True:
        item = file_queue.get(block=True)
        print("New file is being read")
        # readed = read.read(item)
        # print(readed)
        file_queue.task_done()

threading.Thread(target=reader_thread, daemon=True).start()

app = Flask(__name__)
@app.route("/", methods=["GET"])
def index():
    return "<p>Hello, World!</p>"


@app.route("/read", methods=["POST"])
def read_route():
    data = request.json
    if data is None:
        return json.jsonify({"error": "Invalid or missing JSON"}), 400
    if not os.path.isfile(data["file"]):
        return json.jsonify({"error": "Not a vaild file path"}), 400
    
    file_queue.put(data["file"])



if __name__ == '__main__':
    app.run(port=80)