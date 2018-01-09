from flask import Flask, flash, url_for, render_template, request, redirect, make_response, Response, jsonify
from flask_socketio import SocketIO

from pymongo import MongoClient

import datetime

import os

mongo_url = os.environ.get('MONGO_URL')

client = MongoClient(mongo_url)
db = client['gfdb']
leaderboard = db['leaderboard']
keys = db['keys']

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/entry', methods=["POST"])
def entry():
    key_check = keys.find_one({'key':request.headers.get('X-Api-Key')})
    if key_check and key_check.get('valid'):
        name, score = request.form.get('name'), request.form.get('score')
        socketio.emit('new_score', {'name':name,'score':score})
        leaderboard.update({'name':name},{'name':name,'score':int(score)}, upsert=True)
        return jsonify(entry = {'success':True})
    else:
        return jsonify(entry = {'success':False})

@app.route('/highscores')
def highscores():
    highscores = list(leaderboard.find({},{'_id':0}).sort('score', -1).limit(3))
    return jsonify(highscores=highscores)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
