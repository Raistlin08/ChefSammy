from flask import Flask

app = Flask(__name__)
@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/read", methods=["POST"])
def hello_world():
    return "<p>Hello, World!</p>"



if __name__ == '__main__':
    app.run(port=80)