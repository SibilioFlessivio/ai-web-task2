from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('start-template.html')



