#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, 
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor 
from ev3dev2.led import Leds

# TODO: Add code here

# init
tank = MoveTank(OUTPUT_A, OUTPUT_B)
tank.cs = ColorSensor()

try:
    # Follow the line for 4500ms
    tank.follow_line(
        kp=11.3, ki=0.05, kd=3.2,
        speed=SpeedPercent(30),
        follow_for=follow_for_ms,
        ms=4500
    )
except Exception:
    tank.stop()
    raise