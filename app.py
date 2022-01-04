import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template
import string
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


### UPLOAD FILE ###
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are: txt, pdf, png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)


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
