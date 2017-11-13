# Ideas so far

## Balance game (super-tentative title)

This is a multi-player, multi-component game, incorporating programming, electronics, design, and fabrication.

### Components involved

The balance game uses 8 BBC micro:bits:

* 2 x handheld controllers (to be handled by two players simultaneously)
* 4 x checkpoints (one at the end of each room for each team)
* 2 x indicators (connected to each team, utilising buzzers and LEDs!)

The following hardware is utilised:

* Accelerometer
* Buttons
* LED matrix
* Piezo buzzers (via GPIO)
* **Radio communication** is used by all micro:bits to co-ordinate the game

All of the enclosures will be designed by the teams, so long as they meet prescribed design criteria and core functionality is maintained.

### Objectives

* Players must get their micro:bit from one side of the room to the other, hitting the checkpoint at each end.
* To make things more complex, two people have to carry the micro:bit. Their grip will be ensured using the GPIO pins, and they will be penalised if either player releases their grip.
* But it's worse than that: players have to keep their micro:bits evenly balanced, and avoid jerking them around. An LED on the matrix indicates how imbalanced their micro:bits are.
* It's also **A RACE**!
