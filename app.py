import string
import pprint
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


def get_route(route_id):

    db = {
        '111':
        {
            "name": "kat in the hat",
            "holds": ["1a", "3a", "3c", "5c", "3e", "5e"]
        }
    }

    return db.get(route_id)


app = Flask(__name__)


@ app.route("/")
def hello_world():
    return f"<pre>{create_board(4,4)}</pre>"


@ app.route('/hello')
@ app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@ app.route('/board')
@ app.route('/board/<route_id>')
def board(route_id=None):
    numb_rows = 5
    numb_columns = 5
    board = create_board(numb_rows, numb_columns)
    route = get_route(route_id) if route_id else None
    return render_template('board.html', board=board, route=route)
