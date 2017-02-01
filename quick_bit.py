import microbit
import random

arrows = ["<", ">"] #arrows to indicate whether button A or B needs pressing

change_wait = 250 #wait between prompting a press
quick_wait = 500 #wait between requiring a press (or else failure!)
start_wait = microbit.running_time() #start of the waiting time
waiting = True #are we waiting to prompt a press
round_over = False #has the round ended (by success or failure)
failed = False #have we failed
score = 0 #score accumulator

#create fade in and out frames
frames = [] #array of frames
for brightness in range(10): #iterate over 10 brightness levels
    frame = "" #create a blank frame variable
    for row in range(5): #iterate over each row of LEDs
        frame += str(brightness) * 5 + ":" #set all 5 LEDs to the same brightness
    frames.append(frame[0:-1]) #append frame to frame array, taking off the last colon
frames += frames[::-1] #put a reversed set of frames on the end of that array
frames = [microbit.Image(frame) for frame in frames] #convert frames to micro:bit images

def display_score(number):
    number = str(number)
    for i in range(5):
        microbit.display.show(number)
        microbit.sleep(75)
        microbit.display.clear()
        microbit.sleep(75)
    return True

while True:
    time_now = microbit.running_time() #get current time for comparison
    if waiting: #if we're waiting to prompt the player
        if (time_now - start_wait) > change_wait: #if we've waited long enough
            a_or_b = arrows[random.randint(0,1)] #choose a random button (A or B)
            microbit.display.show(a_or_b) #show the user
            waiting = False #say we're no longer waiting for a prompt
            press_wait = time_now #start the timer for the player to press
        else:
            microbit.display.clear() #keep display clear if we've not waited long enough
    else:
        if (microbit.button_a.is_pressed() and a_or_b == "<") or (microbit.button_b.is_pressed() and a_or_b == ">"): #winning combo
            score += 1 #increase score
            round_over = True #round's done
        elif (microbit.button_a.is_pressed() and a_or_b == ">") or (microbit.button_b.is_pressed() and a_or_b == "<"): #losing combo
            failed = True #player failed
        elif (time_now - press_wait) > quick_wait: #waited too long
            failed = True #player failed
        if failed:
            microbit.display.show(frames, delay=20) #failure animation
            display_score(score) #display the score
            score = 0 #reset score
            failed = False #reset failure state
            round_over = True #round's over
        if round_over:
            microbit.display.clear() #clear display
            waiting = True #start waiting again
            start_wait = microbit.running_time() #start waiting
            round_over = False #round restarting
