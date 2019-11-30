#!/usr/bin/env python3
from ev3dev2.motor import Motor, LargeMotor, MoveSteering, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.wheel import EV3Tire 
from ev3dev2.sound import Sound
import math

#LEFT_MOTOR = OUTPUT_B
#RIGHT_MOTOR = OUTPUT_C

#LeftSensor = ColorSensor(INPUT_1)
#RightSensor = ColorSensor(INPUT_4)

#LeftMotor = LargeMotor(LEFT_MOTOR)
#RightMotor = LargeMotor(RIGHT_MOTOR)


# Sætter motorer op: 
# mA = ev3.LargeMotor('outA')
# mA.run_direct()
# mA.polarity = "inversed"

# Når vi ser linjen: 
# if ((not saw_line) & (lC.value() < LIGHT_THRESHOLD)):
#             saw_line = True
#             line_time = timer()
#             mA.position = 0
#             mB.position = 0 

# Vi sætter position til 0, fordi det skal man åbenbart for at det virker optimalt

# Når vi har set en linje kører vi lidt frem:
#         if (saw_line & (mA.position+mB.position > 500)):
#             saw_line = False
#             step += 1
#             integral = 0
#             last_error = lB.value() - lA.value()

#             Drej til højre: 
#         mA.duty_cycle_sp = -75
#         mB.duty_cycle_sp = 75
#         mA.duty_cycle_sp = -75
#         mB.duty_cycle_sp = 75
#         mA.position = 0
#         mB.position = 0
#         while ((mA.position > -200) & (mB.position < 200)):
#             pass

#         while lA.value() > BLACK_THRESHOLD:
#             mA.duty_cycle_sp = -30 #0
#             mB.duty_cycle_sp = 30 #45



class EV3Controller:
    def __init__(self):
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
        #self.LeftMotor.command = LargeMotor.COMMAND_RUN_DIRECT
        #self.RightMotor.command = LargeMotor.COMMAND_RUN_DIRECT
    
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

    def TurnOnSpotSensor(self, TurnChar, TurnSpeed = 30):
            # WHITE = 100   # BLACK = 0
        LeftIntensity = self.LeftSensor.reflected_light_intensity
        RightIntensity = self.RightSensor.reflected_light_intensity

        if TurnChar == 'r': # Turn right
            self.SetDutycycle(TurnSpeed, -TurnSpeed)

            while ( LeftIntensity > 15  ):  
                LeftIntensity = self.LeftSensor.reflected_light_intensity

            while ( RightIntensity > 20  ):  
                RightIntensity = self.RightSensor.reflected_light_intensity
                
            while ( LeftIntensity > 20  ):  
                LeftIntensity = self.LeftSensor.reflected_light_intensity

        if TurnChar == 'l': # Turn left
            self.SetDutycycle(-TurnSpeed, TurnSpeed)

            while ( RightIntensity > 15  ):  
                RightIntensity = self.RightSensor.reflected_light_intensity

            while ( LeftIntensity > 20  ):  
                LeftIntensity = self.LeftSensor.reflected_light_intensity
                
            while ( RightIntensity > 20  ):  
                RightIntensity = self.RightSensor.reflected_light_intensity


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




    # def TurnOnSpot(self, degree):
    #     WHEEL_DISTANCE = 85 # 115
    #     DiffControl = MoveDifferential(LEFT_MOTOR, RIGHT_MOTOR, EV3Tire, WHEEL_DISTANCE)
    #     if ( degree > 0 ):
    #         DiffControl.turn_right(SpeedPercent(15),int(degree))
    #     else:
    #         DiffControl.turn_left(SpeedPercent(15),int(degree))
    #     #DiffControl.on_arc_right(SpeedPercent(15), 150, 70000)



