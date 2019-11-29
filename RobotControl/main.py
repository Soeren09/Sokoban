#!/usr/bin/env python3

import time
import LineFollower


from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, LightSensor#, GyroSensor

def Turn(TurnChar, orientation):    # Fixed turn
    if ( TurnChar == 'l' ):
        TurnDegree = -90
    elif ( TurnChar == 'r' ):
        TurnDegree = 90
    LineFollower.TurnOnSpot(TurnDegree)   

    RotationChars = "urdl"
    if ( TurnChar == 'r' ):
        orientation = RotationChars[(RotationChars.find(orientation) + 1) % len(RotationChars)]
    elif ( TurnChar == 'l'  ):
        orientation = RotationChars[(RotationChars.find(orientation) + len(RotationChars) - 1) % len(RotationChars)]
    return orientation

def Turn2(TurnChar, orientation):   # Line detect turn
    LineFollower.TurnOnSpotSensor(TurnChar)   

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


TurnState = False

FRONT = 0
RIGHT = 1
LEFT = 2
#solution = "lllluuxddllurrrrrrxdruuuxruulldrrrxdldllullxuulldrrxurdddxullddxrrxdrrrrxdruuuxruurrdllxulddxulldrrxddlllluurddxldrrrrxdruuuxdlllldllurrrrrrxdruu"  # Læs fra Planner   
#solution_pre_def = "lllluUxddllurRRRRRxdruUUxruulldrRRxdldllulLxuulldrRxurdDDxulldDxrRxdrRRRxdruUUxruurrdlLxuldDxulldrRxddlllluurdDxldrRRRxdruUUxdlllldllurRRRRRxdruU"
#commands = "uUxlurRxurdDxrdlLxdl"
#commands = "ulurrddlu"
#commands = "uuxuuxuux"
commands = "udududududududududududududududu"
orientation = 'u'   # -> orientation == commands[i]
n = len(commands)
i = 0



while i < n:
        # Read value of junction detect sensor
    SHIFT_REG = LineFollower.DetectJunctionDouble(LeftColorSensor, RightColorSensor)

        # Read next commmand
    command = commands[i]

        # Detect if there is a rising edge on "black" signal
    if SHIFT_REG == 1 and PREV_SHIFT_REG == 0:
        FLAG_RE = True
    else:
        FLAG_RE = False

    # Stop motors and move to next command if a junction has been detected
    if FLAG_RE and not(ignoreShift):
        i = i + 1
        if ( i >= len(commands) ):
            LineFollower.StopMotors()
            while True:
                sound.beep()

        if (command != commands[i] and command != commands[i].lower()): # previous != current (command)
            LineFollower.StopMotors()
            if ( commands[i] != 'x' ):
                LineFollower.DriveRotations(rot=0.25) # kør en lille smule -> robotten står på junction
            substate = 0
        #sound.beep()



    if ( ord(command) >= 65 and ord(command) <= 90 ):
        if ( command.lower() == orientation ):
            LineFollower.DriveRotations(rot=1.2)
            i = i + 1 # It will not see a junction -> increment
        else:
            TurnChar = TurnDirection(orientation, command.lower())
            if ( TurnChar == 'o' ):
                print("ERROR: invalid turn char")
            orientation = Turn(TurnChar, orientation)
    elif ( command == orientation and ord(command) > 90 ):
        # Kør lige ud
        LineFollower.BounceFollow(BINARY_CONTROL=False, max_speed=60, speed_reduction = 30) # max_speed = 50
    elif( command == 'x' ): # Go backwards
        LineFollower.GoBackwards()
    else:
        # Drej indtil den vender i korrekt retning
        TurnChar = TurnDirection(orientation, command)
        if ( TurnChar == 'o' ):
            print("ERROR: invalid turn char")
        #orientation = Turn(TurnChar, orientation)
        orientation = Turn2(TurnChar, orientation)

    PREV_SHIFT_REG = SHIFT_REG


####################################################################33


# while i < n:
#    # print("JunctionColorSensor: "+str(JunctionColorSensor.reflected_light_intensity))
#     # Read value of junction detect sensor
#     SHIFT_REG = LineFollower.DetectJunctionDouble(LeftColorSensor, RightColorSensor)
#     #SHIFT_REG = LineFollower.DetectJunctionSingle(JunctionColorSensor, threshold=50)

#         # Read next commmand
#     command = commands[i]

#     # Detect if there is a rising edge on "black" signal
#     if SHIFT_REG == 1 and PREV_SHIFT_REG == 0:
#         FLAG_RE = True
#     else:
#         FLAG_RE = False

#     # Stop motors and move to next command if a junction has been detected
#     if FLAG_RE and not(ignoreShift):
#         i = i + 1
#         if ( i >= len(commands) ):
#             LineFollower.StopMotors()
#             while True:
#                 sound.beep()

#         if (command != commands[i] and command != commands[i].lower()): # previous != current (command)
#             LineFollower.StopMotors()
#             if ( commands[i] != 'x' ):
#                 LineFollower.DriveRotations(rot=0.25) # kør en lille smule -> robotten står på junction
#             substate = 0
#         sound.beep()



#     if ( ord(command) >= 65 and ord(command) <= 90 ):
#         if ( command.lower() == orientation ):
#             LineFollower.DriveRotations(rot=1.2)
#             i = i + 1 # It will not see a junction -> increment
#         else:
#             TurnChar = TurnDirection(orientation, command.lower())
#             if ( TurnChar == 'o' ):
#                 print("ERROR: invalid turn char")
#             orientation = Turn(TurnChar, orientation)
#     elif ( command == orientation and ord(command) > 90 ):
#         # Kør lige ud
#         LineFollower.BounceFollow(BINARY_CONTROL=False, max_speed=60, speed_reduction = 30) # max_speed = 50
#     elif( command == 'x' ): # Go backwards
#         LineFollower.GoBackwards()
#     else:
#         # Drej indtil den vender i korrekt retning
#         TurnChar = TurnDirection(orientation, command)
#         if ( TurnChar == 'o' ):
#             print("ERROR: invalid turn char")
#         #orientation = Turn(TurnChar, orientation)
#         orientation = Turn2(TurnChar, orientation)

#     PREV_SHIFT_REG = SHIFT_REG