from flask import Flask

app = Flask(__name__)

# default / base page
@app.route("/")
def hello_world():
    return "<p>Hello,world!<p>"