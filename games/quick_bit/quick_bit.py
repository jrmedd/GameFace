import random
import microbit
import radio

radio.on()

ARROWS = ["<", ">"] #ARROWS to indicate whether button A or B needs pressing

CHANGE_WAIT = 250 #wait between prompting a press
QUICK_WAIT = 500 #wait between requiring a press (or else failure!)

START_WAIT = microbit.running_time() #start of the WAITING time
WAITING = True #are we WAITING to prompt a press
ROUND_OVER = False #has the round ended (by success or failure)
FAILED = False #have we FAILED
SCORE = 0 #SCORE accumulator

MY_NAME = "JAMES"

#create fade in and out FRAMES
FRAMES = [] #array of FRAMES
for brightness in range(10): #iterate over 10 brightness levels
    frame = "" #create a blank frame variable
    for row in range(5): #iterate over each row of LEDs
        frame += str(brightness) * 5 + ":" #set all 5 LEDs to the same brightness
    FRAMES.append(frame[0:-1]) #append frame to frame array, taking off the last colon
FRAMES += FRAMES[::-1] #put a reversed set of FRAMES on the end of that array
FRAMES = [microbit.Image(frame) for frame in FRAMES] #convert FRAMES to micro:bit images

def display_score(number):
    number = str(number)
    for i in range(3):
        microbit.display.scroll(number,delay=80)
        radio.send("SCORE,%s,%s" % (MY_NAME,number)) #leaderboard output (repeated for radio redundancy)
        microbit.sleep(75)
        microbit.display.clear()
        microbit.sleep(75)
    return True

while True:
    TIME_NOW = microbit.running_time() #get current time for comparison
    if WAITING: #if we're WAITING to prompt the player
        if (TIME_NOW - START_WAIT) > CHANGE_WAIT: #if we've waited long enough
            A_OR_B = ARROWS[random.randint(0, 1)] #choose a random button (A or B)
            microbit.display.show(A_OR_B) #show the user
            WAITING = False #say we're no longer WAITING for a prompt
            PRESS_WAIT = TIME_NOW #start the timer for the player to press
        else:
            microbit.display.clear() #keep display clear if we've not waited long enough
    else:
        if (microbit.button_a.is_pressed() and A_OR_B == "<") or (microbit.button_b.is_pressed() and A_OR_B == ">"):
            SCORE += 1 #increase SCORE by 1
            ROUND_OVER = True #round's done
        elif (microbit.button_a.is_pressed() and A_OR_B == ">") or (microbit.button_b.is_pressed() and A_OR_B == "<"):
            FAILED = True #player FAILED
        elif ((TIME_NOW - PRESS_WAIT) > QUICK_WAIT) and SCORE != 0: #waited too long
            FAILED = True #player FAILED
        if FAILED:
            microbit.display.show(FRAMES, delay=20) #display failure animation
            display_score(SCORE) #display the SCORE
            SCORE = 0 #reset SCORE
            FAILED = False #reset failure state
            ROUND_OVER = True #round's over
        if ROUND_OVER:
            microbit.display.clear() #clear display
            WAITING = True #start WAITING again
            START_WAIT = microbit.running_time() #start WAITING
            ROUND_OVER = False #round restarting
