from datetime import datetime

from gpiozero import LineSensor
from signal import pause
from time import sleep
from Setting import GPIO, LINEDETECT_RIGHT, LINEDETECT_LEFT
from MotorModule import Motor


left_sensor = LineSensor(LINEDETECT_LEFT)
right_sensor = LineSensor(LINEDETECT_RIGHT)
speed = 0.2
speedturn = 0.2
motor = Motor()
turn = False
while True:

    left_detect = int(left_sensor.value)
    right_detect = int(right_sensor.value)
    if left_detect == 0 and right_detect == 0:
        motor.move(speed,0)
    elif left_detect == 1 and right_detect == 0:
        if not turn:
            motor.move(-speed, 0, 0.1)
            turn = True
        else:
            motor.move(speedturn,0.2,0.1)

            turn = False
    elif left_detect == 0 and right_detect == 1:
        if not turn:
            motor.move(-speed, 0, 0.1)
            turn = True
        else:
            motor.move(speedturn,-0.2,0.1)
            turn = False
    else:
        motor.stop()

    #print('left:{}, right: {}'.format(left_detect,right_detect))
    sleep(0.001)