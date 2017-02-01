import microbit
import random

wait = random.randint(1000, 5000)
start_wait = microbit.running_time()
waiting = True
game_won = False
#create fade in and out frames
frames = [] #array of frames
for brightness in range(10): #iterate over 10 brightness levels
    frame = "" #create a blank frame variable
    for row in range(5): #iterate over each row of LEDs
        frame += str(brightness) * 5 + ":" #set all 5 LEDs to the same brightness
    frames.append(frame[0:-1]) #append frame to frame array, taking off the last colon
frames += frames[::-1] #put a reversed set of frames on the end of that array
frames = [microbit.Image(frame) for frame in frames] #convert frames to micro:bit images

def game_won_by(number):
    number = str(number)
    for i in range(5):
        microbit.display.show(number)
        microbit.sleep(75)
        microbit.display.clear()
        microbit.sleep(75)
    return True

while True:
    time_now = microbit.running_time()
    if waiting:
        if (time_now - start_wait) > wait:
            microbit.display.show("!")
            waiting = False
        else:
            microbit.display.clear()
    else:
        if microbit.pin0.is_touched():
            game_won = game_won_by(0)
        elif microbit.pin1.is_touched():
            game_won = game_won_by(1)
        elif microbit.pin2.is_touched():
            game_won = game_won_by(2)
        if game_won:
            wait = random.randint(1000, 5000)
            start_wait = microbit.running_time()
            waiting = True
            game_won = False
