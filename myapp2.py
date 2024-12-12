from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('start.html')

@app.route("/reversed")
def reversed():
    rev = request.args['rev'][::-1]
    return render_template('reversed.html', rev=rev)

