import microbit
import radio

#set a device ID
this_device = "A"
#this_device = "B"
#this_device = "C"

radio.on() #start radio comms

#create fade in and out frames
frames = [] #array of frames
for brightness in range(10): #iterate over 10 brightness levels
    frame = "" #create a blank frame variable
    for row in range(5): #iterate over each row of LEDs
        frame += str(brightness) * 5 + ":" #set all 5 LEDs to the same brightness
    frames.append(frame[0:-1]) #append frame to frame array, taking off the last colon
frames += frames[::-1] #put a reversed set of frames on the end of that array
frames = [microbit.Image(frame) for frame in frames] #convert frames to micro:bit images

while True:
    if microbit.button_a.is_pressed():
        microbit.display.show(this_device) #display this device's ID if button A is pressed
    else:
        microbit.display.clear()
    received_messages = radio.receive() #check for messages over radio
    if received_messages:
        received_messages = str(received_messages).split(',') #split message into ID and message
        if received_messages[0].strip() == this_device: #first array element will be the ID
            microbit.display.show(frames, delay=20) #display the animation if ID matches
        received_messages = None
    else:
        microbit.display.clear()
