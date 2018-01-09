import serial
import requests
import os

MB = serial.Serial('/dev/tty.usbmodem1412', baudrate=115200)
ENTRY_URL = "https://api.gameface.xyz/entry"
API_KEY = {"X-Api-Key":os.environ.get('GF_API')}

last_score = 0
last_name = None

while True:
    score = MB.readline()
    score = score.split(",")
    if score[0] == "SCORE":
        this_name = score[1].strip()
        this_score = score[2].strip()
        submission_data = {'name':this_name, 'score':this_score}
        if  this_score != last_score or this_name != last_name:
            last_name = this_name
            last_score = this_score
            entry = requests.post(ENTRY_URL, data=submission_data, headers=API_KEY)
