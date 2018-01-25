import random
import microbit

ARROWS = ["<", ">"] #ARROWS to indicate whether button A or B needs pressing


SCORE = 0 #SCORE accumulator

WAITING_FOR_PRESS = False

START_TIME = microbit.running_time() #return time in millseconds

while True:
    TIME_NOW = microbit.running_time()
    if not WAITING_FOR_PRESS:
        if (TIME_NOW - START_TIME > 250):
            random_number = random.randint(0,1)
            selected_arrow = ARROWS[random_number]
            microbit.display.show(selected_arrow)
            WAITING_FOR_PRESS = True
        else:
            microbit.display.clear()
    elif WAITING_FOR_PRESS:
        if (microbit.button_a.is_pressed() and selected_arrow == "<") or (microbit.button_b.is_pressed() and selected_arrow == ">"):
            SCORE += 1
            WAITING_FOR_PRESS = False

        elif (microbit.button_a.is_pressed() and selected_arrow == ">") or (microbit.button_b.is_pressed() and selected_arrow == "<"):
            microbit.display.scroll(str(SCORE))
            SCORE = 0
            WAITING_FOR_PRESS = False
        START_TIME = TIME_NOW
