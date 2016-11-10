import microbit
import radio

#device IDs to communicate with – set arbitrarily
target_device_a = "A"
target_device_b = "B"
target_device_c = "C"

#messages to send by default
message_a = "apple"
message_b = "banana"
message_c = "cantaloupe"

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
    if microbit.button_a.was_pressed():
        radio.send("%s, %s" % (target_device_a, message_a))
        microbit.display.show(frames, delay=20)
    if microbit.button_b.was_pressed():
        radio.send("%s, %s" % (target_device_b, message_b))
        microbit.display.show(frames, delay=20)
    microbit.accelerometer.current_gesture()
    if microbit.accelerometer.was_gesture("face up"):
        radio.send("%s, %s" % (target_device_c, message_c))
        microbit.display.show(frames, delay=20)
