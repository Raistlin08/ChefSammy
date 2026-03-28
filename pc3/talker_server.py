from flask import Flask, request, send_file, jsonify, send_from_directory
import talker

# talk = Talker()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return send_from_directory("static","index.html")


@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["user"]
    print(user_message)
    # ai_message = talk.question(user_message)
    # return jsonify({"ai":ai_message})
    return jsonify({"ai": "Messagio ai"})

if __name__ == '__main__':
    app.run(port=8080)