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
@app.route("/", methods=["GET", "POST"])
def index():
    return "<p>Hello, World!</p>"





if __name__ == '__main__':
    app.run(port=80)