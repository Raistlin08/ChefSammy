from flask import Flask, request
import queue
import threading
import json
# import elaborator



# elab = elaborator.Elaborator()
chunks_queue = queue.Queue()

def elaborator_thread():
    while True:
        item = chunks_queue.get(block=True)
        print("New chunks is being analyzed")
        # analized = elab.analize(item)
        # print(analized)
        chunks_queue.task_done()
        
        
threading.Thread(target=elaborator_thread, daemon=True).start()


app = Flask(__name__)


@app.route('/chunk', methods=['POST'])
def add_chunck():
    data = request.json
    if data is None:
        return json.jsonify({"error": "Invalid or missing JSON"}), 400
    chunks_queue.put(data["chunk"])

if __name__ == '__main__':
    app.run()