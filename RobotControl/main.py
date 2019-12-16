#!/usr/bin/env python3

from LineFollower import EV3Controller 
from ev3dev2.sound import Sound

commands = "lllluuxddllurrrrrrxdruuuxruulldrrrxdldllullxuulldrrxurdddxullddxrrxdrrrrxdruuuxruurrdllxulddxulldrrxddlllluurddxldrrrrxdruuuxdlllldllurrrrrrxdruu"
Push = False


orientation = 'u'   # -> orientation == commands[i]
n = len(commands)
i = 0
command = commands[i]

FLAG_RE = False     # Flag: Junction detect
FLAG_PUSH = False   # Flag: Robot just pushed a can

SHIFT_REG = 0b0000
PREV_SHIFT_REG = 0b0000

sound = Sound()
sound.beep()

def GetNewOrientation(TurnChar, orientation):
    RotationChars = "urdl"
    if ( TurnChar == 'r' ):
        orientation = RotationChars[(RotationChars.find(orientation) + 1) % len(RotationChars)]
    elif ( TurnChar == 'l'  ):
        orientation = RotationChars[(RotationChars.find(orientation) + len(RotationChars) - 1) % len(RotationChars)]
    return orientation

def TurnDirection(command, orientation): # return shortest turn direction
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


def Turn90(command, orientation, ev3):
    TurnChar = TurnDirection(command, orientation)   
    if ( TurnChar == 'o' ):
        print("ERROR: invalid turn char")

    ev3.TurnOnSpotSensor(TurnChar)

    return GetNewOrientation(TurnChar, orientation)

def Turn180(orientation, ev3):
    Robot.DrivePos(pos=140, speed = -30)                                                                            # Prev -30
    Robot.TurnOnSpotSensor('l')  # Turn 180 degree
    orientation = GetNewOrientation('l', orientation )  # Correct orientation
    orientation = GetNewOrientation('l', orientation )
    return orientation

Robot = EV3Controller()

#Robot.DrivePos(pos= 90, speed = 60)
while i < n:
        # Read value of junction detect sensor
    SHIFT_REG = Robot.DetectJunctionDouble()

        # Detect if there is a rising edge on "black" signal
    if SHIFT_REG == 1 and PREV_SHIFT_REG == 0:
        FLAG_RE = True
    else:
        FLAG_RE = False

    # Stop motors and move to next command if a junction has been detected
    if FLAG_RE:
        i = i + 1
        FLAG_PUSH = False   # The robot is done pushing the can
        if ( i >= len(commands) ):
            Robot.StopMotors()
            while True:
                sound.beep()
        elif ( i + 2 < len(commands) ):
            if ( commands[i+1] == 'x' ):
                Push = False # True: if faster
            else:
                Push = False

        if (command != commands[i] and command != commands[i].lower()): # previous != current (command)
            Robot.StopMotors
            if ( commands[i] != 'x' ):
                Robot.DrivePos(pos= 95, speed = 30) # Move the wheels to the junction

        # Read next commmand
    command = commands[i]

    if ( ((command == orientation and ord(command) > 90) or FLAG_PUSH ) and not Push):        # Kør lige ud
        Robot.BounceFollow( max_speed=70, speed_reduction = 40)                                                             #  Prev: (70)90, 40

    elif( command == 'x' ): # Drive back to previous intersection 
        orientation = Turn180(orientation, Robot)
        FLAG_PUSH = True    # Drive straight.

    elif ( command == orientation and Push ):
        Robot.BounceFollow( max_speed=70, speed_reduction = 70)                                                             # Prev: 70, 70

    else:   # Drej indtil den vender i korrekt retning
        orientation = Turn90(command, orientation, Robot)

    PREV_SHIFT_REG = SHIFT_REG
