#!/usr/bin/env python3
from ev3dev2.motor import Motor, LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_D, MoveTank, SpeedPercent, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.wheel import EV3Tire 
from ev3dev2.sound import Sound
import math

def TurnRight(speed=20, difference=5):
    LeftMotor = Motor(OUTPUT_B)
    RightMotor = Motor(OUTPUT_C)
    LeftMotor.duty_cycle_sp = speed
    RightMotor.duty_cycle_sp = -(speed - difference)
    LeftMotor.command = "run-direct"
    RightMotor.command = "run-direct"

def StopMotors():
    LeftMotor = Motor(OUTPUT_A)
    RightMotor = Motor(OUTPUT_D)
    LeftMotor.stop_action = Motor.STOP_ACTION_HOLD
    RightMotor.stop_action = Motor.STOP_ACTION_HOLD
    LeftMotor.command = Motor.COMMAND_STOP
    RightMotor.command = Motor.COMMAND_STOP
    

def TurnOnSpot(degree):
    WHEEL_DISTANCE = 91 # 115
    DiffControl = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, WHEEL_DISTANCE)
    DiffControl.turn_right(SpeedPercent(15),int(degree))
    #DiffControl.on_arc_right(SpeedPercent(15), 150, 70000)


def DriveRotations(rot=1):
    tankControl = MoveTank(OUTPUT_B, OUTPUT_C)
    tankControl.on_for_rotations(SpeedPercent(20), SpeedPercent(20), rot)

def SimpleFollower(SAFE_MODE=True):    # Kører på venstre side af stregen: én sensor i midten.
    BASE_SPEED = 40 + 20*int(not(SAFE_MODE)) # 60  40       40 (kan tage blødt sving)
    DIFFERENCE = 5  + 3 *int(not(SAFE_MODE)) # 8   5       35
    cs = ColorSensor(INPUT_1)
    LeftMotor = Motor(OUTPUT_B)
    RightMotor = Motor(OUTPUT_C)
    if (cs.color == ColorSensor.COLOR_BLACK):
        LeftMotor.duty_cycle_sp = BASE_SPEED - DIFFERENCE
        RightMotor.duty_cycle_sp = BASE_SPEED
    else:
        LeftMotor.duty_cycle_sp = BASE_SPEED
        RightMotor.duty_cycle_sp = BASE_SPEED - DIFFERENCE
    LeftMotor.command = Motor.COMMAND_RUN_DIRECT
    RightMotor.command = Motor.COMMAND_RUN_DIRECT

def CalibrateSensors():
    pass

def DetectJunction(cs_left, cs_right, TWO_SENSORS = True, threshold=40):
    if TWO_SENSORS:
        # Both sensors see black?
        if (cs_left.reflected_light_intensity < threshold and cs_right.reflected_light_intensity < threshold): # 30 is "ok"
            return True
        else:
            return False
    else:
        if (cs.reflected_light_intensity < 20):
            return True
        else:
            return False
         #SHIFT_REG = int(cs.color == ColorSensor.COLOR_BLACK) # Based on .color

def BounceFollow(BINARY_CONTROL=False, max_speed=40, speed_reduction = 30):
    # Define motors and sensors
    LeftSensor = ColorSensor(INPUT_1)
    RightSensor = ColorSensor(INPUT_4)

    LeftMotor = LargeMotor(OUTPUT_A)
    RightMotor = LargeMotor(OUTPUT_D)
    sound = Sound()
    

    # Check if color sensors see black      --- Rewrite into refected light intensity
    if ( BINARY_CONTROL ):
        LeftBlack =  (LeftSensor.color == ColorSensor.COLOR_BLACK)
        RightBlack = (RightSensor.color == ColorSensor.COLOR_BLACK)
        
        BASE_SPEED = 35
        SPEED_REDUCTION = 20
        LeftMotor.duty_cycle_sp = BASE_SPEED - int(LeftBlack)*SPEED_REDUCTION
        RightMotor.duty_cycle_sp = BASE_SPEED - int(RightBlack)*SPEED_REDUCTION
    else:
            # WHITE = 100
            # BLACK = 0
        LeftIntensity = LeftSensor.reflected_light_intensity
        RightIntensity = RightSensor.reflected_light_intensity

        # QUICK FIX - LAV OM
        if ( LeftIntensity > 60 and RightIntensity > 60 ):
            LeftIntensity = 60
            RightIntensity = 60

        #if (LeftIntensity < 40 and RightIntensity < 40): # 30 is "ok"
        #    sound.beep()
        #else:
        LeftMotor.duty_cycle_sp = max_speed - (1 - LeftIntensity/(LeftIntensity + RightIntensity)) * speed_reduction
        RightMotor.duty_cycle_sp = max_speed - (1 - RightIntensity/(LeftIntensity + RightIntensity)) * speed_reduction

    # Control motor speed
    LeftMotor.command = Motor.COMMAND_RUN_DIRECT
    RightMotor.command = Motor.COMMAND_RUN_DIRECT
    
