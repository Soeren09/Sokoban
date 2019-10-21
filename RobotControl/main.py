#!/usr/bin/env python3

import LineFollower
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_4, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, GyroSensor

FLAG_RE = False

SHIFT_REG = 0b0000
PREV_SHIFT_REG = 0b0000


substate = 0
ignoreShift = False

sound = Sound()
sound.beep()

cs_right = ColorSensor(INPUT_4)
cs_left = ColorSensor(INPUT_1)

gyr = GyroSensor(INPUT_2)

TurnState = False

FRONT = 0
RIGHT = 1
LEFT = 2

commands = [FRONT, RIGHT, FRONT, RIGHT, FRONT, RIGHT, FRONT, RIGHT]  # Læs fra Planner
n = len(commands)
i = 0

#while True:
#    print("Left: "+str(cs_left.reflected_light_intensity)+", Right: "+str(cs_right.reflected_light_intensity)+", Gyro: "+str(gyr.angle))

#while True:
#    LineFollower.BounceFollow()

while i < n:

    # Read value of junction detect sensor
    SHIFT_REG = LineFollower.DetectJunction(cs_left, cs_right)

    # Detect if there is a rising edge on "black" signal
    if SHIFT_REG == 1 and PREV_SHIFT_REG == 0:
        FLAG_RE = True
    else:
        FLAG_RE = False

    # Stop motors and move to next command
    if FLAG_RE and not(ignoreShift):
        LineFollower.StopMotors()
        substate = 0
        i = i + 1
        sound.beep()
    
    # Read next commmand
    command = commands[i]

    # If command is equal to FRONT move forward
    if ( command == FRONT ):
        #LineFollower.SimpleFollower(SAFE_MODE=True)
        LineFollower.BounceFollow()

    # If command is equal to RIGHT turn right
    if ( command == RIGHT ):
        if ( substate == 0 ):
            ignoreShift = True
    #        LineFollower.DriveRotations(rot=0.2)
    #        LineFollower.TurnOnSpot(45)
    #        substate = 1
    #    if ( substate == 1 ):
    #        ignoreShift = False
    #        LineFollower.TurnRight(speed=20, difference=8)
    #        if ( cs_front.color == ColorSensor.COLOR_BLACK ):
    #            LineFollower.StopMotors()
    #            i = i + 1
    #            substate = 0

    # load shift reg val into previous shift reg val
    PREV_SHIFT_REG = SHIFT_REG