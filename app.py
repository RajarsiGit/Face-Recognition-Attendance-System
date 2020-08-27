from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, send_from_directory
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_socketio import SocketIO, emit
import os
import random
from dataset_capture import DatasetCapture
from training_dataset import TrainData
from test_dataset import TestData

main = Blueprint('main', __name__)

secret_key = str(os.urandom(20))

app = Flask(__name__)
app.config['TESTING'] = False
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'deployment'
app.config['SECRET_KEY'] = secret_key
socketio = SocketIO(app)

dataset_capture = DatasetCapture()
train_data = TrainData()
test_data = None

class DataForm(FlaskForm):
    id = StringField('Your ID', validators=[DataRequired()])
    submit = SubmitField('Send ID')

id = None

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/sendid', methods=['GET', 'POST'])
def send_id():
    global id
    form = DataForm()
    if form.validate_on_submit():
        id = form.id.data
        return redirect(url_for('.capture'))
    elif request.method == 'POST':
        form.id.data = id
    return render_template('send_id.html', form=form)

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    return render_template('capture.html')

@socketio.on('capture', namespace='/capture')
def record_capture(input):
    global id
    if dataset_capture.capture(id, input) == False:
        emit('message', {'msg' : 'Done'}, room=request.sid)

@app.route('/success_b', methods=['GET', 'POST'])
def success_b():
    return render_template("success.html", msg="Data captured!")

@app.route('/train', methods=['GET', 'POST'])
def train():
    return render_template("train.html")

@app.route('/trained', methods=['GET', 'POST'])
def trained():
    if train_data.train():
        return render_template("success.html", msg="Training Complete!")
    else:
        return redirect(url_for('.index'))

@app.route('/test', methods=['GET', 'POST'])
def test():
    global test_data
    test_data = TestData()
    return render_template("recognise.html")

@app.route('/success_a', methods=['GET', 'POST'])
def success_a():
    return render_template("success.html", msg="Testing Complete!")

@socketio.on('input', namespace='/video')
def recognise(input):
    global test_data, id
    (frame, check) = test_data.test(input.split(",")[1])
    if check:
        id = None
        emit('message', {'msg' : 'Done'}, room=request.sid)
    emit('message', {'msg' : frame}, room=request.sid)

@socketio.on('connect', namespace='/video')
def connect():
    app.logger.info("Socket connected")

if __name__ == "__main__":
    socketio.run(app, debug=True)