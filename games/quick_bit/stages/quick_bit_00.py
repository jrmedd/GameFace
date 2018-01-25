import random
import microbit

ARROWS = ["<", ">"] #ARROWS to indicate whether button A or B needs pressing


SCORE = 0 #SCORE accumulator

random_number = random.randint(0,1)
selected_arrow = ARROWS[random_number]
microbit.display.show(selected_arrow)
