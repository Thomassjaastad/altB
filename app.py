import string
from flask import Flask
from flask import render_template


def create_board(numbRows, numbColumns):
    rows = range(1, numbRows + 1)
    columns = string.ascii_lowercase[:numbColumns]
    board = [[0]*numbRows for i in range(numbColumns)]
    for i in range(numbRows):
        for j in range(numbColumns):
            board[i][j] = f'{rows[i]}{columns[j]}'
    return board


app = Flask(__name__)


@app.route("/")
def hello_world():

    return f"<p>{create_board(4,4)}</p>"


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
