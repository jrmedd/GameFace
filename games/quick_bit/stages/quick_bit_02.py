import random
import microbit

ARROWS = ["<", ">"] #ARROWS to indicate whether button A or B needs pressing


SCORE = 0 #SCORE accumulator

WAITING_FOR_PRESS = False

while True:
    if not WAITING_FOR_PRESS:
        random_number = random.randint(0,1)
        selected_arrow = ARROWS[random_number]
        microbit.display.show(selected_arrow)
        WAITING_FOR_PRESS = True
    elif WAITING_FOR_PRESS:
        if (microbit.button_a.is_pressed() and selected_arrow == "<") or (microbit.button_b.is_pressed() and selected_arrow == ">"):
            SCORE += 1
            microbit.display.scroll(str(SCORE))
            WAITING_FOR_PRESS = False
