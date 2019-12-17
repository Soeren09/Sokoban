#!/usr/bin/env python3
from ev3dev2.motor import Motor, LargeMotor, MoveSteering, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.wheel import EV3Tire 
from ev3dev2.sound import Sound
import math


class EV3Controller:
    def __init__(self):
        WHEEL_DISTANCE = 85 # 115
        

        self.LeftMotor = LargeMotor(OUTPUT_B)
        self.RightMotor = LargeMotor(OUTPUT_C)

            # Run mode
        self.LeftMotor.run_direct()
        self.RightMotor.run_direct() 

            # Stop mode
        self.LeftMotor.stop_action = LargeMotor.STOP_ACTION_HOLD     # HOLD
        self.RightMotor.stop_action = LargeMotor.STOP_ACTION_HOLD    # HOLD

        self.LeftSensor = ColorSensor(INPUT_1)
        self.RightSensor = ColorSensor(INPUT_4)

    
    def DetectJunctionDouble(self, threshold=30):
        
        # Both sensors see black?
        if (self.LeftSensor.reflected_light_intensity < threshold and self.RightSensor.reflected_light_intensity < threshold): # 30 is "ok"
            return True
        return False


    def SetDutycycle(self, DutycycleLeft, DutycycleRight):
        self.LeftMotor.duty_cycle_sp = DutycycleLeft
        self.RightMotor.duty_cycle_sp = DutycycleRight

            # Control motor speed
        self.LeftMotor.command = LargeMotor.COMMAND_RUN_DIRECT
        self.RightMotor.command = LargeMotor.COMMAND_RUN_DIRECT
    
    def DrivePos(self, pos, speed=30):
        self.LeftMotor.position = 0
        self.RightMotor.position = 0
            
        self.SetDutycycle(speed, speed)

        while ((abs(self.LeftMotor.position) < pos) & (abs(self.RightMotor.position) < pos)):
            pass

        self.SetDutycycle(0,0)
  
    def StopMotors(self):
        self.SetDutycycle(0,0)
        self.LeftMotor.command = LargeMotor.COMMAND_STOP
        self.RightMotor.command = LargeMotor.COMMAND_STOP

    def TurnOnSpotSensor(self, TurnChar, TurnSpeed = 50, twist = 0):
        if TurnChar == 'r': # Turn right
            self.SetDutycycle(TurnSpeed, -TurnSpeed)

            while ( self.LeftSensor.reflected_light_intensity > 15  ):
                pass  

            while ( self.RightSensor.reflected_light_intensity > 20  ):
                pass  

            if (twist):
                while ( self.LeftSensor.reflected_light_intensity > 40  ):
                    pass  

        if TurnChar == 'l': # Turn left
            self.SetDutycycle(-TurnSpeed, TurnSpeed)

            while ( self.RightSensor.reflected_light_intensity > 15  ):
                pass  

            while ( self.LeftSensor.reflected_light_intensity > 20  ):
                pass  

            if (twist):
                while ( self.RightSensor.reflected_light_intensity > 40  ):
                    pass  

        self.StopMotors()

    def BounceFollow(self, max_speed=50, speed_reduction = 25):
            # WHITE = 100
            # BLACK = 0
        LeftIntensity = self.LeftSensor.reflected_light_intensity
        RightIntensity = self.RightSensor.reflected_light_intensity

        # QUICK FIX - LAV OM
        if ( LeftIntensity > 60 and RightIntensity > 60 ):
            LeftIntensity = 60
            RightIntensity = 60

        leftDutycycle = max_speed - (1 - LeftIntensity/(LeftIntensity + RightIntensity)) * speed_reduction
        rightDutycycle =  max_speed - (1 - RightIntensity/(LeftIntensity + RightIntensity)) * speed_reduction

        self.SetDutycycle(leftDutycycle, rightDutycycle)