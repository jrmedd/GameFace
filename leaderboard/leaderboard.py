import serial
import requests

mb = serial.Serial('/dev/ttyACM0', baudrate=115200)
last_score = 0
last_name = None

while True:
    score = mb.readline()
    score = score.split(",")
    if score[0] == "SCORE":
        this_name = score[1].strip()
        this_score = score[2].strip()
        if  this_score != last_score or this_name != last_name:
            last_name = this_name
            last_score = this_score
            requests.get("http://127.0.0.1:5000/entry/%s/%s" % (this_name, this_score))
