from flask import Flask, flash, url_for, render_template, request, redirect, Response, jsonify

from pymongo import MongoClient

import datetime, requests

from collections import Counter

import smtplib

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import html2text

core_email_template = 'core_email_template.html'
stand_email_template = 'stand_email_template.html'
sending_address = "noreply@takeawaytv.co.uk"
smtp_cred = {"server":"smtp.gmail.com", "port":587, "user":"takeawaytvel@gmail.com", "psk":"Th31@nd!ng606290yeah"}

ads_url = "http://beta.activds.com:3000/TellMe?boxCode="

my_ip = "127.0.0.1"

#client = MongoClient('mongodb://127.0.0.1:27017')
client = MongoClient('mongodb://takeawaytv:0f1319a6a694aab0d735885f6caf8749@dokku-mongo-takeawaytv:27017/takeawaytv')
#client = MongoClient('mongodb://takeawaytv:0f1319a6a694aab0d735885f6caf8749@35.177.248.99:27600/takeawaytv')

db = client['takeawaytv']
touches = db['touches']
tenants = db['tenants']
files = db['files']
locations = db['locations']
keys = db['keys']

app = Flask(__name__)
app.secret_key = "829c63b4c6fe351bc517a048a529638660185e32a83aba5e"

@app.route('/')
def index():
    today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0)
    tomorrow = today + datetime.timedelta(days = 1)
    today_metrics = touch_metrics(today, tomorrow)
    return render_template('index.html', metrics=today_metrics)

@app.route('/touches_today')
def touches_today():
    today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0)
    tomorrow = today + datetime.timedelta(days = 1)
    today_metrics = touch_metrics(today, tomorrow)
    return jsonify(data=today_metrics)

@app.route('/touch/<box_code>/<card_id>')
def touch(box_code, card_id):
    if not auth(request.headers.get('X-Api-Key')):
        return jsonify(touch={'success':False,'reason':'Invalid API key'})
    today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0)
    tomorrow = today + datetime.timedelta(days = 1)
    try:
        ads_tell_me = requests.get("%s%s" % (ads_url, box_code))
    except:
        ads_tell_me = None
    if not ads_tell_me:
        return jsonify(touch = {'success':False,'reason':'activDS API error'})
    current_video = ads_tell_me.json()
    current_video_filename = current_video.get('data').get('onScreenAssets').get('onScreenVideos')[0].get('filename')
    card_holder  = tenants.find_one({'card_id':card_id}, {'_id':0})
    if card_holder == None:
        return jsonify(touch = {'success':False,'reason':'No such card holder'})
    entered_today = touches.find_one({'card_id':card_id, 'filename': current_video_filename,'timestamp':{'$gte':today, '$lt':tomorrow}})
    if (entered_today != None):
        return jsonify(touch = {'success':False,'reason':'Already touched this video'})
    video_title = files.find_one({'filename':current_video_filename}).get('video_title')
    if video_title == None:
        return jsonify(touch = {'success':False,'reason':'No such video'})
    card_holder.update({'timestamp':datetime.datetime.now()})
    card_holder.update({'video_title': video_title})
    card_holder.update({'filename': current_video_filename})
    card_holder.update({'location': locations.find_one({'code':box_code}).get('name')})
    send_message(current_video_filename, card_holder.get('email_address'), sending_address, "video")
    touches.insert_one(card_holder)
    return jsonify(touch = {'success':True})

@app.route('/stand/<stand_code>/<card_id>')
def stand(stand_code, card_id):
    if not auth(request.headers.get('X-Api-Key')):
        return jsonify(touch={'success':False,'reason':'Invalid API key'})
    today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0)
    tomorrow = today + datetime.timedelta(days = 1)
    stand_touched = locations.find_one({'code':stand_code})
    if stand_touched == None:
        return jsonify(touch={'success':False,'reason':'No such stand'})
    stand_filename = stand_touched.get('filename')
    if stand_filename == None:
        return jsonify(touch={'success':False,'reason':'No such file'})
    card_holder  = tenants.find_one({'card_id':card_id}, {'_id':0})
    if card_holder == None:
        return jsonify(touch = {'success':False,'reason':'No such card holder'})
    entered_today = touches.find_one({'card_id':card_id, 'filename': stand_filename,'timestamp':{'$gte':today, '$lt':tomorrow}})
    if (entered_today != None):
        return jsonify(touch = {'success':False,'reason':'Already touched this video'})
    video_title = files.find_one({'filename':stand_filename}).get('video_title')
    card_holder.update({'timestamp':datetime.datetime.now()})
    card_holder.update({'video_title': video_title})
    card_holder.update({'filename': stand_filename})
    card_holder.update({'location': locations.find_one({'code':stand_code}).get('name')})
    send_message(stand_filename, card_holder.get('email_address'), sending_address, "stand")
    touches.insert_one(card_holder)
    return jsonify(touch = {'success':True})

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == "POST":
        new_name = request.form.get("name").title()
        new_email = request.form.get("email").lower()
        new_id = request.form.get("card").upper()
        tenants.update({"card_id": new_id}, {"card_holder":new_name, "email_address":new_email, "card_id": new_id},upsert=True)
        flash("Added user")
    return render_template('add_user.html')

def auth(key):
    api_auth = keys.find_one({'hash':key})
    if api_auth != None:
        if datetime.datetime.now() < api_auth.get('valid_until'):
            return True
    return False

def send_message(video, send_to, send_from, msg_type):
    video_info = files.find_one({'filename': video})
    if msg_type == "video":
        video_template = render_template(core_email_template, video_contents=video_info)
    elif msg_type == "stand":
        video_template = render_template(stand_email_template, video_contents=video_info)
    subject = Header('TakeawayTV Information', 'utf-8')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = send_to
    msg['From'] = send_from
    plain_text = html2text.html2text(video_template).encode('utf-8')
    plain_text = MIMEText(plain_text,'plain','utf-8')
    html_text = MIMEText(video_template.encode('utf-8'), 'html','utf-8')
    msg.attach(plain_text)
    msg.attach(html_text)
    smtpserver = smtplib.SMTP(smtp_cred.get('server'), smtp_cred.get('port'), timeout=30)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(smtp_cred.get('user'), smtp_cred.get('psk'))
    smtpserver.sendmail(send_from, send_to, msg.as_string())

def touch_metrics(earliest_date, latest_date):
    touches_today = list(touches.find({'timestamp':{'$gte':earliest_date, '$lt':latest_date}},{'_id':0,'video_title':1,'location':1, 'timestamp':1}))
    touch_counts = dict(Counter((touch.get('video_title'), touch.get('location')) for touch in touches_today))
    traces = list(locations.find({},{'name':1,'_id':0}))
    for trace in traces:
        trace.update({"type":"bar","x":[video_title[0] for video_title in touch_counts.keys() if video_title[1] == trace.get('name')], "y":[touch_counts.get(video_title) for video_title in touch_counts.keys() if video_title[1] == trace.get('name')]})
    return traces

if __name__ == '__main__':
	app.run(debug=True)
