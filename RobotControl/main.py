#!/usr/bin/env python3
import time
import LineFollower
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, LightSensor#, GyroSensor


def Turn(TurnChar, orientation):
    if ( TurnChar == 'l' ):
        TurnDegree = -90
    elif ( TurnChar == 'r' ):
        TurnDegree = 90
    LineFollower.TurnOnSpot(TurnDegree)
    # wait for TurnOnSpot
    #time.sleep(2)    # indstil denne eller lav noget der kan se hvornår LineFollower.TurnOnSpot er færdig med at dreje.    

    RotationChars = "urdl"
    if ( TurnChar == 'r' ):
        orientation = RotationChars[(RotationChars.find(orientation) + 1) % len(RotationChars)]
    elif ( TurnChar == 'l'  ):
        orientation = RotationChars[(RotationChars.find(orientation) + len(RotationChars) - 1) % len(RotationChars)]
    return orientation


def TurnDirection(orientation, command):
    # return 'r' or 'l' to represent a left turn or right turn    'o' represents no turn needed
    if ( orientation == command ):
        return 'o'

    if ( orientation == 'u' ):
        if ( command == 'l' ):
            return 'l'
        return 'r'

    if ( orientation == 'r' ):
        if ( command == 'u' ):
            return 'l'
        return 'r'

    if ( orientation == 'd' ):
        if ( command == 'r' ):
            return 'l'
        return 'r'

    if ( orientation == 'l' ):
        if ( command == 'd' ):
            return 'l'
        return 'r'


FLAG_RE = False

SHIFT_REG = 0b0000
PREV_SHIFT_REG = 0b0000


substate = 0
ignoreShift = False

sound = Sound()
sound.beep()

RightColorSensor = ColorSensor(INPUT_4)
LeftColorSensor = ColorSensor(INPUT_1)
#JunctionColorSensor = LightSensor(INPUT_2)

#gyr = GyroSensor(INPUT_2)

TurnState = False

FRONT = 0
RIGHT = 1
LEFT = 2
commands = "uuuurrrrddddlllluuuurdrurrdddd"  # Læs fra Planner   
orientation = 'u'   # -> orientation == commands[i]
n = len(commands)
i = 0



while i < n:
   # print("JunctionColorSensor: "+str(JunctionColorSensor.reflected_light_intensity))
    # Read value of junction detect sensor
    SHIFT_REG = LineFollower.DetectJunctionDouble(LeftColorSensor, RightColorSensor)
    #SHIFT_REG = LineFollower.DetectJunctionSingle(JunctionColorSensor, threshold=50)

    # Detect if there is a rising edge on "black" signal
    if SHIFT_REG == 1 and PREV_SHIFT_REG == 0:
        FLAG_RE = True
    else:
        FLAG_RE = False

    # Stop motors and move to next command if a junction has been detected
    if FLAG_RE and not(ignoreShift):
        i = i + 1
        if (command != commands[i]): # previos != current (command)
            LineFollower.StopMotors()
            LineFollower.DriveRotations(rot=0.25) # kør en lille smule -> robotten står på junction
            substate = 0
        sound.beep()

    
    # Read next commmand
    command = commands[i]
    if ( command == orientation ):
        # Kør lige ud
        LineFollower.BounceFollow(BINARY_CONTROL=False, max_speed=80, speed_reduction = 30) # max_speed = 50
    else:
        # Drej indtil den vender i korrekt retning
        TurnChar = TurnDirection(orientation, command)
        if ( TurnChar == 'o' ):
            print("ERROR: invalid turn char")
        orientation = Turn(TurnChar, orientation)

    PREV_SHIFT_REG = SHIFT_REG

    




    # If command is equal to FRONT move forward
    #if ( command == 'u' ):
        #LineFollower.SimpleFollower(SAFE_MODE=True)
        #LineFollower.BounceFollow()

    # If command is equal to RIGHT turn right
    #if ( command == 'r' ):
        #if ( substate == 0 ):
            #ignoreShift = True
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



# Lav funktion som tager string: "uuUdLrr" -> "uuuuddllrrr"
def MapBigPushChars(commands):
    # do something with commands to remove big chars.
    return commands
