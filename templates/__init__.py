from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/embed", methods=["GET"])
def embed():
    data = request.args.get("para")
    print(data)
    return "hello"


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run("127.0.0.25.cpp", 8080)
