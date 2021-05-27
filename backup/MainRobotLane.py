import Setting
from MotorModule import Motor
from LaneModule import getLaneCurve
import WebcamModule
import cv2
from SignDetect import preprocess_image, findContour, findLargestSign, removeSmallComponents, remove_other_color


##################################################
motor = Motor()
##################################################

def main():

    img = WebcamModule.getImg()
    #test contours





    ##########################
    curveVal= getLaneCurve(img,2,timer = cv2.getTickCount())
    #cv2.imshow('view',img)
    sen = Setting.MOTOR_SENSITY  # SENSITIVITY
    maxVAl= Setting.MOTOR_MAXSPEED # MAX SPEED
    if curveVal>maxVAl:curveVal = maxVAl
    if curveVal<-maxVAl: curveVal =-maxVAl
    #print(curveVal)
    if curveVal>0:
        sen =1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    print(curveVal)
    motor.move(0.20,-curveVal*sen,0.01)
    motor.stop(1)
    #cv2.waitKey(1)


if __name__ == '__main__':
    while True:
        main()