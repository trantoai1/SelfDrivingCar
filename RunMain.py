import cv2
import WebcamModule as wM
import MotorModule as mM
from DistanceModule import ThreadSonic
from LightModule import LightSensor
from SignModule import ThreadImage


from Setting import classNames,GPIO, LINEDETECT_RIGHT, LINEDETECT_LEFT
from gpiozero import LineSensor
from signal import pause
from time import sleep

#######################################

if __name__ == '__main__':
    left_sensor = LineSensor(LINEDETECT_LEFT)
    right_sensor = LineSensor(LINEDETECT_RIGHT)
    motor = mM.Motor() # Pin Numbers
    speed = 0.2
    speedturn = 0.2
    turn = False
    light = LightSensor()
    sonic = ThreadSonic()
    sonic.start()
    light.start()
    img = wM.getImg(size=[480, 360])
    signdetect = ThreadImage(img)
    signdetect.start()
    try:
        while True:

            img = wM.getImg(size=[480, 360])
            signdetect.setImg(img)
            distance = sonic.join()
            if distance :
                print('{} cm'.format(distance))
            image, sign, signFlag = signdetect.join()
            if sign != -1:
                print('Sign={}, name={}, flag={}'.format(sign, classNames[sign], signFlag))
            cv2.imshow('', image)
            cv2.waitKey(1)
            """left_detect = int(left_sensor.value)
            right_detect = int(right_sensor.value)
            if left_detect == 0 and right_detect == 0:
                motor.move(speed, 0)
            elif left_detect == 1 and right_detect == 0:
                if not turn:
                    motor.move(-speed, 0, 0.1)
                    turn = True
                else:
                    motor.move(speedturn, 0.2, 0.1)

                    turn = False
            elif left_detect == 0 and right_detect == 1:
                if not turn:
                    motor.move(-speed, 0, 0.1)
                    turn = True
                else:
                    motor.move(speedturn, -0.2, 0.1)
                    turn = False
            else:
                motor.stop()
            """
            # print('left:{}, right: {}'.format(left_detect,right_detect))
            #sleep(0.001)
    except KeyboardInterrupt:
        #print('Stop by KeyboardInterrupt')
        sonic.stop()
        light.stop()
        signdetect.stop()