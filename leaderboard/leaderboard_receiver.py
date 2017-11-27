import microbit
import radio

radio.config(power=7)
radio.on()

score = 0

while True:
    score = radio.receive()
    if score:
        print(score)
