from os import listdir

import cv2
import numpy as np
# from MotorModule import Motor
from backup.HSVTrackBar import HSVTrackBar
#from SignDetect import preprocess_image, removeSmallComponents, findContour, remove_other_color
from backup.utlis import debug
from backup import utlis
import Setting
curveList = []
avgVal = 10

def empty(a):
    pass
if Setting.HSVBARENABLE:
    hsv_ = HSVTrackBar()

def getLaneCurve(img, display=2, timer=0, hsvbar = Setting.HSVBARENABLE):
    ###
    imgCopy2 = img.copy()
    imgThres = utlis.thresholding(img)

    # cv2.imshow('thresh1',imgThres)
    # binary_image = preprocess_image(img)
    # # cv2.imshow('preprocess_image',binary_image)
    # binary_image = removeSmallComponents(binary_image, 300)
    # # print(binary_image)
    # # cv2.imshow('removeSmallComponents', binary_image)
    # binary_image = cv2.bitwise_and(binary_image, binary_image, mask=remove_other_color(img))
    # cv2.imshow('bitwise_and', binary_image)
    # # binary_image = remove_line(binary_image)
    #
    # # cv2.imshow('BINARY IMAGE', binary_image)
    # contours = findContour(binary_image)
    if hsvbar:
        hsv = cv2.cvtColor(imgCopy2, cv2.COLOR_BGR2HSV)
        lower, upper = hsv_.getHSV()
        imgThres = cv2.inRange(hsv, lower, upper)
        cv2.imshow('thresh2', imgThres)

    imgCopy  = img.copy()
    imgResult = img.copy()

    ###
    hT, wT, c = img.shape
    points = utlis.valTrackbars(240, 120)
    imgWarp = utlis.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utlis.drawPoints(imgCopy, points)
    ###
    middlePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint-middlePoint



    ###
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    #####
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        #cv2.imshow('imgThres', imgInvWarp)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)

        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        timer = cv2.getTickFrequency()
        cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgWarp)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)


    #
    #
    #
    # cv2.imshow('Thres', imgThres)
    # cv2.imshow('Warp', imgWarp)
    # cv2.imshow('Warp Points', imgWarpPoints)
    #


    # cv2.imshow('Histogram', imgHist)

    #### NORMALIZATION
    curve = curve / 100
    if curve > 1: curve == 1
    if curve < -1: curve == -1
    return curve


if __name__ == '__main__':
    #cap = cv2.VideoCapture(Setting.CAMERALANE[Setting.CAMERAMODE])
    initializeTrackbars = Setting.TRACKBAR[Setting.CAMERAMODE]
    utlis.initializeTrackbars(initializeTrackbars)
    frameCounter = 0
    # motor = Motor()
    sen = Setting.MOTOR_SENSITY
    sign_list = listdir("/Users/trantoai/Desktop/IMG14")

    while True:
        for sign_file in sign_list:
            # img = cv2.imread('/Users/trantoai/Desktop/IMG13/Image_162156007699707.jpg')
            img = cv2.imread("/Users/trantoai/Desktop/IMG14/"+sign_file)

            cv2.imshow('origin', img)
            #img = cv2.resize(img,(480,240)) # RESIZE
            curve = getLaneCurve(img, display=Setting.LANEDISPLAYMODE, timer = cv2.getTickCount())
            debug(curve)
            #motor.move(0.20,-curve*sen,1)
            #motor.stop(1)
            #cv2.imshow('Vid', img)
            #time.sleep(1)
            cv2.waitKey(1200)
            #print(sign_file)
        # frameCounter += 1
        # if Setting.CAMERAMODE == 1:
        #     if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        #         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #         frameCounter = 0
        # success, img = cap.read() # GET THE IMAGE
        # cv2.imshow('origin',img)
        # img = cv2.resize(img,(480,240)) # RESIZE
        # curve = getLaneCurve(img, display=Setting.LANEDISPLAYMODE, timer = cv2.getTickCount())
        # debug(curve)
        # motor.move(0.20,-curve*sen,1)
        # #motor.stop(1)
        # #cv2.imshow('Vid', img)
        # cv2.waitKey(1)