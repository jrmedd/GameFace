from flask import Flask, flash, url_for, render_template, request, redirect, make_response, Response, jsonify
from flask_socketio import SocketIO

from pymongo import MongoClient

import datetime

import os

mongo_url = os.environ.get('MONGO_URL')

#client = MongoClient('mongodb://127.0.0.1:27017')

client = MongoClient(mongo_url)
db = client['gfdb']
leaderboard = db['leaderboard']

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/entry/<name>/<score>')
def entry(name, score):
    socketio.emit('new_score', {'name':name,'score':score})
    leaderboard.update({'name':name},{'name':name,'score':int(score)}, upsert=True)
    return jsonify(entry = {'success':True})

@app.route('/highscores')
def highscores():
    highscores = list(leaderboard.find({},{'_id':0}).sort('score', -1).limit(3))
    return jsonify(highscores=highscores)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
