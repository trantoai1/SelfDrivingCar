import cv2
import WebcamModule as wM
import MotorModule as mM
from DistanceModule import ThreadSonic
from LightModule import LightSensor
from SignModule import ThreadImage
from SignDetect import SignDetect

from Setting import classNames, SPEEDTURN, \
    SPEEDUP, SPEEDDOWN, LINEDETECT_RIGHT, LINEDETECT_LEFT, SIGN_30, SIGN_70, SIGN_RIGHT, SIGN_STOP, SIGN_LEFT
from gpiozero import LineSensor
from signal import pause
from time import sleep,time

#######################################

if __name__ == '__main__':
    left_sensor = LineSensor(LINEDETECT_LEFT)
    right_sensor = LineSensor(LINEDETECT_RIGHT)
    motor = mM.Motor() # Pin Numbers
    speed = SPEEDDOWN
    speedturn = SPEEDTURN
    turn = False
    currentSign = -1
    light = LightSensor()
    sonic = ThreadSonic()
    sonic.start()
    light.start()
    img = wM.getImg(size=[480, 360])
    # signdetect = ThreadImage(img)
    # signdetect.start()
    signObj = SignDetect()
    time1 = time()
    time2 = time()
    left_detect = -1
    right_detect = -1
    diff = 0.001
    try:
        while True:

            img = wM.getImg(size=[480, 360])
            #signdetect.setImg(img)
            distance = sonic.join()
            if distance :
                print('{} cm'.format(distance))
            #_, sign, signFlag = signdetect.join()
            coordinate, original_image, sign, text = signObj.localization(img)
            if sign != -1 :#and sign != currentSign:
                currentSign = sign
                print('Sign={}, name={}, flag={}'.format(sign, classNames[sign], text))
            # if sign == SIGN_30 and signFlag:
            #     speed = SPEEDDOWN
            # elif sign == SIGN_70 and signFlag:
            #     speed = SPEEDUP
            # elif sign == SIGN_STOP and signFlag:
            #     motor.stop()
            #     cv2.waitKey(1)
            #     continue

            #cv2.imshow('', image)
            #cv2.waitKey(1)
            left_detect = int(left_sensor.value)
            right_detect = int(right_sensor.value)
            if left_detect == 0 and right_detect == 0:
                motor.move(speed, 0)
            elif left_detect == 1 and right_detect == 0:

                time2 = time()
                diff = time2 - time1
                time1 = time()
                # print('left:{}'.format(diff))
                if diff > speed * 1.5:
                    motor.move(-speed, 0, speed)
                elif diff > 0.1:
                    motor.move(-speed, 0, (speed + diff) / 10)
                else:
                    motor.move(-speed, 0, diff / 10)

                motor.move(speedturn, 0.2, 0.05)


            elif left_detect == 0 and right_detect == 1:
                time2 = time()
                diff = time2 - time1
                time1 = time()
                # print('right:{}'.format(diff))
                if diff > speed * 1.5:
                    motor.move(-speed, 0, speed)
                elif diff > 0.1:
                    motor.move(-speed, 0, (speed + diff) / 10)
                else:
                    motor.move(-speed, 0, diff / 10)

                motor.move(speedturn, -0.2, 0.05)
            else:
                motor.stop()

            #sleep(0.0001)
    except KeyboardInterrupt:
        print('Stop by KeyboardInterrupt')
        sonic.stop()
        light.stop()
        #signdetect.stop()