import string
from flask import Flask, render_template
from db import db


def create_board(numbRows, numbColumns):
    rows = range(1, numbRows + 1)
    columns = string.ascii_lowercase[:numbColumns]
    board = [[0]*numbRows for i in range(numbColumns)]
    for i in range(numbRows):
        for j in range(numbColumns):
            board[i][j] = f'{rows[i]}{columns[j]}'
    return board


def get_route(route_id):
    return db.get(route_id)


def get_hold_positions(route_id):
    positions = []
    for holds in db[f'{route_id}']["holds"]:
        positions.append(holds["position"])
    return positions


def get_hold_types(route_id):
    hold_types = []
    for holds in db[f'{route_id}']["holds"]:
        hold_types.append(holds["hold_type"])
    return hold_types


app = Flask(__name__)


@ app.route('/board')
@ app.route('/board/<route_id>')
def board(route_id=None):
    numb_rows = 5
    numb_columns = 5
    board = create_board(numb_rows, numb_columns)
    route = get_route(route_id) if route_id else None
    positions = get_hold_positions(route_id)
    hold_types = get_hold_types(route_id)
    return render_template('board.html', board=board, route=route, positions=positions, hold_types=hold_types)


@ app.route('/create')
def create(route_id=None):
    numb_rows = 5
    numb_columns = 5
    board = create_board(numb_rows, numb_columns)
    return render_template('create_route.html', board=board)
