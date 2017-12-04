from flask import Flask, flash, url_for, render_template, request, redirect, make_response, Response, jsonify
from flask_socketio import SocketIO

from pymongo import MongoClient

import datetime

#client = MongoClient('mongodb://127.0.0.1:27017')
client = MongoClient(' mongodb://gfdb:cf0261e516ebaebcb91f8be770e41d3f@dokku-mongo-gfdb:27017/gfdb')
db = client['gfdb']
leaderboard = db['leaderboard']

app = Flask(__name__)

app.secret_key = 'G@m3F@c3!'

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
