from gpiozero import LineSensor
from signal import pause
from time import sleep,time
from Setting import GPIO, LINEDETECT_RIGHT, LINEDETECT_LEFT
from MotorModule import Motor


left_sensor = LineSensor(LINEDETECT_LEFT)
right_sensor = LineSensor(LINEDETECT_RIGHT)
speed = 0.35
speedturn = 0.2
motor = Motor()

time1 = time()
time2 = time()

diff = 0.001
while True:

    left_detect = int(left_sensor.value)
    right_detect = int(right_sensor.value)
    '''if left_detect == 0 and right_detect == 0:
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
    '''
    if left_detect == 0 and right_detect == 0:
        motor.move(speed,0)
    elif left_detect == 1 and right_detect == 0:

        time2 = time()
        diff = time2 - time1
        time1 = time()
        #print('left:{}'.format(diff))
        if diff > speed*1.5:
            motor.move(-speed, 0, speed)
        elif diff > 0.1:
            motor.move(-speed, 0, (speed+diff)/10)
        else:
            motor.move(-speed, 0, diff/10)

        motor.move(speedturn,0.2,0.05)


    elif left_detect == 0 and right_detect == 1:
        time2 = time()
        diff = time2 - time1
        time1 = time()
        #print('right:{}'.format(diff))
        if diff > speed * 1.5:
            motor.move(-speed, 0, speed)
        elif diff > 0.1:
            motor.move(-speed, 0, (speed + diff) / 10)
        else:
            motor.move(-speed, 0, diff / 10)

        motor.move(speedturn,-0.2,0.05)


    else:
        motor.stop()
    #print('left:{}, right: {}'.format(left_detect,right_detect))
    sleep(0.0001)