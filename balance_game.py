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

#function to scale accelerometer values to something more useful
def scale_values(in_value, in_max, out_max):
    return float(in_value)/float(abs(in_max))*float(out_max)

while True:
    microbit.display.clear() #clear the frame
    reading_x = 1024+microbit.accelerometer.get_x() #set x accelerometer reading to a number between 0 and 2048
    pixel_x = -8 + round(scale_values(reading_x, 2048, 20)) #scale the reading to the LED matrix (plenty of overflow to make it sensitive)
    reading_y = 1024+microbit.accelerometer.get_y()
    pixel_y = -8 + round(scale_values(reading_y, 2048, 20))
    if pixel_x > 4 or pixel_x < 0 or pixel_y > 4 or pixel_y < 0: #identify onscreen range
        on_screen = False #offscreen
    else:
        on_screen = True #onscreen
    if on_screen:
        microbit.display.set_pixel(pixel_x, pixel_y, 9) #display pixel if onscreen
    elif not on_screen and last_screen_status: #if just offscreen i.e. previous status was onscreen
        microbit.display.show(frames, delay=20) #play drop animation
        radio.send("%s, %s" % (target_device_a, message_a)) #alert other devices
        radio.send("%s, %s" % (target_device_b, message_b))
        radio.send("%s, %s" % (target_device_c, message_c))
    last_screen_status = on_screen #set last onscreen status
