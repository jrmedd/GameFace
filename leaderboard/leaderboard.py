import serial
import requests

mb = serial.Serial('/dev/tty.usbmodem1412', baudrate=115200)

while True:
    score = mb.readline()
    score = score.split(",")
    if score[0] == "SCORE":
        requests.get("http://127.0.0.1:5000/entry/%s" % (score[1].strip()))
