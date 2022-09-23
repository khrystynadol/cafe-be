from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return 'Home'


@app.route("/api/v1/hello-world-<value>")
def hello_world(value):
    return "Hello world " + value, 200


if __name__ == "__main__":
    app.run()
