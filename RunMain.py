import cv2
#import WebcamModule as wM
import MotorModule as mM
#from DistanceModule import ThreadSonic
from LightModule import LightSensor
#from SignModule import ThreadImage
#from SignDetect import SignDetect

from Setting import classNames, SPEEDTURN, \
    SPEEDUP, SPEEDDOWN, SIGN_30, SIGN_70, SIGN_RIGHT, SIGN_STOP, SIGN_LEFT, GPIO_ECHO, GPIO
from signal import pause
from time import sleep,time

#######################################

if __name__ == '__main__':
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    motor = mM.Motor() # Pin Numbers
    speed = SPEEDDOWN
    speedturn = SPEEDTURN

    currentSign = -1
    light = LightSensor()
    #sonic = ThreadSonic()
    #sonic.start()
    light.start()

    #signdetect = ThreadImage()
    #signdetect.start()
    #signObj = SignDetect()


    try:
        while True:

            #img = wM.getImg(size=[480, 360])
            #signdetect.setImg(img)
            distance = (GPIO.input(GPIO_ECHO)==GPIO.HIGH)
            if distance :
                print('speed up {} '.format(distance))
                speed = 1
                motor.move(speed,t= 3)
                speed = SPEEDDOWN
            #image, sign, signFlag = signdetect.join()
            #coordinate, original_image, sign, text = signObj.localization(img)
            #if sign != -1 :#and sign != currentSign:
                #currentSign = sign
                #print('Sign={}, name={}, flag={}'.format(sign, classNames[sign], signFlag))
            #if sign == SIGN_30 and signFlag:
               # speed = SPEEDDOWN
            # elif sign == SIGN_70 and signFlag:
            #     speed = SPEEDUP
            #elif sign == SIGN_STOP:
             #   pass
                #speed = 0


            #cv2.imshow('sl', image)
            #cv2.waitKey(1)
            motor.move(speed, 0)

            #sleep(0.0001)
    except KeyboardInterrupt:
        print('Stop by KeyboardInterrupt')
        #sonic.stop()
        light.stop()
        #signdetect.stop()