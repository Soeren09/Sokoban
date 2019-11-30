#!/usr/bin/env python3
from ev3dev2.motor import Motor, LargeMotor, MoveSteering, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.wheel import EV3Tire 
from ev3dev2.sound import Sound
import math


class EV3Controller:
  def __init__(self, ):
    self.name = name
    self.age = age

    self.LeftMotor = LargeMotor(OUTPUT_B)
    self.RightMotor = LargeMotor(OUTPUT_C)
    
    self.LeftSensor = ColorSensor(INPUT_1)
    self.RightSensor = ColorSensor(INPUT_4)


#LEFT_MOTOR = OUTPUT_B
#RIGHT_MOTOR = OUTPUT_C

#LeftSensor = ColorSensor(INPUT_1)
#RightSensor = ColorSensor(INPUT_4)

#LeftMotor = LargeMotor(LEFT_MOTOR)
#RightMotor = LargeMotor(RIGHT_MOTOR)

tankControl = MoveTank(LEFT_MOTOR, RIGHT_MOTOR)



def SetDutycycle(DutycycleLeft, DutycycleRight):
    LeftMotor.duty_cycle_sp = DutycycleLeft
    RightMotor.duty_cycle_sp = DutycycleRight

    # Control motor speed
    LeftMotor.command = Motor.COMMAND_RUN_DIRECT
    RightMotor.command = Motor.COMMAND_RUN_DIRECT

def StopMotors():
    LeftMotor.stop_action = Motor.STOP_ACTION_HOLD     # HOLD
    RightMotor.stop_action = Motor.STOP_ACTION_HOLD    # HOLD
    LeftMotor.command = Motor.COMMAND_STOP
    RightMotor.command = Motor.COMMAND_STOP


def TurnOnSpot(degree):
    WHEEL_DISTANCE = 85 # 115
    DiffControl = MoveDifferential(LEFT_MOTOR, RIGHT_MOTOR, EV3Tire, WHEEL_DISTANCE)
    if ( degree > 0 ):
        DiffControl.turn_right(SpeedPercent(15),int(degree))
    else:
        DiffControl.turn_left(SpeedPercent(15),int(degree))
    #DiffControl.on_arc_right(SpeedPercent(15), 150, 70000)


def TurnOnSpotSensor(TurnChar, TurnSpeed = 50):
        # WHITE = 100   # BLACK = 0
    LeftIntensity = LeftSensor.reflected_light_intensity
    RightIntensity = RightSensor.reflected_light_intensity

    if TurnChar == 'r': # Turn right
        SetDutycycle(TurnSpeed, -TurnSpeed)

        while ( LeftIntensity > 20  ):  
            LeftIntensity = LeftSensor.reflected_light_intensity

        while ( RightIntensity > 20  ):  
            RightIntensity = RightSensor.reflected_light_intensity
            
        while ( LeftIntensity > 30  ):  
            LeftIntensity = LeftSensor.reflected_light_intensity

    if TurnChar == 'l': # Turn left
        SetDutycycle(-TurnSpeed, TurnSpeed)

        while ( RightIntensity > 20  ):  
            RightIntensity = RightSensor.reflected_light_intensity

        while ( LeftIntensity > 20  ):  
            LeftIntensity = LeftSensor.reflected_light_intensity
            
        while ( RightIntensity > 30  ):  
            RightIntensity = RightSensor.reflected_light_intensity


def DriveRotations(rot=1):  # Speed value cannot exceed 30! This will Make the robot shaky and make it faulty!
    tankControl.on_for_rotations(SpeedPercent(30), SpeedPercent(30), rot)


def DetectJunctionDouble(ColorSensorLeft = LeftSensor, ColorSensorRight = RightSensor, threshold=30):
    # Both sensors see black?
    if (ColorSensorLeft.reflected_light_intensity < threshold and ColorSensorRight.reflected_light_intensity < threshold): # 30 is "ok"
        return True
    return False

def BounceFollow(max_speed=50, speed_reduction = 25):
        # WHITE = 100
        # BLACK = 0
    LeftIntensity = LeftSensor.reflected_light_intensity
    RightIntensity = RightSensor.reflected_light_intensity

    # QUICK FIX - LAV OM
    if ( LeftIntensity > 60 and RightIntensity > 60 ):
        LeftIntensity = 60
        RightIntensity = 60

    leftDutycycle = max_speed - (1 - LeftIntensity/(LeftIntensity + RightIntensity)) * speed_reduction
    rightDutycycle =  max_speed - (1 - RightIntensity/(LeftIntensity + RightIntensity)) * speed_reduction

    SetDutycycle(leftDutycycle, rightDutycycle)





## Not used 


# def DetectJunctionSingle(JunctionColorSensor, threshold = 20):
#     if ( JunctionColorSensor.reflected_light_intensity < threshold ):
#         return True
#     return False

# def TurnRight(speed=20, difference=5):
#     LeftMotor = Motor(LEFT_MOTOR)
#     RightMotor = Motor(RIGHT_MOTOR)
#     LeftMotor.duty_cycle_sp = speed
#     RightMotor.duty_cycle_sp = -(speed - difference)
#     LeftMotor.command = "run-direct"
#     RightMotor.command = "run-direct"

# def SimpleFollower(SAFE_MODE=True):    # Kører på venstre side af stregen: én sensor i midten.
#     BASE_SPEED = 40 + 20*int(not(SAFE_MODE)) # 60  40       40 (kan tage blødt sving)
#     DIFFERENCE = 5  + 3 *int(not(SAFE_MODE)) # 8   5       35
#     cs = ColorSensor(INPUT_1)
#     LeftMotor = Motor(LEFT_MOTOR)
#     RightMotor = Motor(RIGHT_MOTOR)
#     if (cs.color == ColorSensor.COLOR_BLACK):
#         LeftMotor.duty_cycle_sp = BASE_SPEED - DIFFERENCE
#         RightMotor.duty_cycle_sp = BASE_SPEED
#     else:
#         LeftMotor.duty_cycle_sp = BASE_SPEED
#         RightMotor.duty_cycle_sp = BASE_SPEED - DIFFERENCE
#     LeftMotor.command = Motor.COMMAND_RUN_DIRECT
#     RightMotor.command = Motor.COMMAND_RUN_DIRECT








