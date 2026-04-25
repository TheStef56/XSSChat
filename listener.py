from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    print(request.args)
    return "ok"

app.run("0.0.0.0", 9000)