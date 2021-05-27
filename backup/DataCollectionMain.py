import WebcamModule as wM
from JoyStickModule import getJS
import MotorModule as mM
import cv2
from time import sleep
import pickle
import socket
from Setting import HOST,PORT,JOYSTICK
if JOYSTICK:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)
    client, addr = s.accept()
curveList = []
avgVal = 10
maxThrottle = 0.3
motor = mM.Motor()

record = 0
# trackbar = [118, 157, 0, 240]
# #dcM = DataCollectionModule()
#dcR = DataCollectionModule(folder='DataCollectedRaw')
# def valTrackbars(wT=480, hT=240):
#     widthTop = trackbar[0]
#     heightTop = trackbar[1]
#     widthBottom = trackbar[2]
#     heightBottom = trackbar[3]
#     points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop),
#                          (widthBottom, heightBottom), (wT - widthBottom, heightBottom)])
#     return points
#
#
# def warpImg(img, points, w, h, inv=False):
#     pts1 = np.float32(points)
#     pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
#
#     if inv:
#         matrix = cv2.getPerspectiveTransform(pts2, pts1)
#     else:
#         matrix = cv2.getPerspectiveTransform(pts1, pts2)
#
#     imgWarp = cv2.warpPerspective(img, matrix, (w, h))
#     return imgWarp
#
#
# def getLaneCurve(img):
#     imgThres = utlis.thresholding(img)
#     hT, wT, c = img.shape
#     points = valTrackbars()
#     imgWarp = warpImg(imgThres, points, wT, hT)
#
#     imgInvWarp = warpImg(imgWarp, points, wT, hT, inv=True)
#
#     imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
#     imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
#     imgLaneColor = np.zeros_like(img)
#     imgLaneColor[:] = 0, 255, 0
#     imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
#
#     # cv2.imshow('ImageStack', imgLaneColor)
#     return imgLaneColor


while True:
    # sleep(1)
    if JOYSTICK:
        data = client.recv(1024)

        joyVal = pickle.loads(data)
    else:
        joyVal = getJS()
    #print(type(joyVal))
    steering = joyVal['axis1'] * 0.1
    throttle = joyVal['o'] * maxThrottle
    if int(joyVal['share']) == 1:
        if record == 0: print('Recording Started ...')
        record += 1
        sleep(0.300)
    if record == 1:

        img = wM.getImg(False, size=[240, 120])
        #cv2.imshow(img)
        # if steering!=0 and throttle!=0:
        #dcR.saveData(img, steering, throttle)
        #img = getLaneCurve(img)
        #dcM.saveData(img, steering, throttle)
        dataprint = {}
        dataprint['throttle'] = throttle;
        dataprint['steering'] = steering;

        print('dataprint:{}'.format(dataprint))
        if JOYSTICK:
            msg = 'save Image'
            client.sendall(bytes(msg, "utf8"))
        # cv2.imshow('current IMG', img)
    elif record == 2:
        #dcM.saveLog()
        #dcR.saveLog()
        if JOYSTICK:
            msg = 'save Log'
            client.sendall(bytes(msg, "utf8"))
        record = 0

    motor.move(throttle, steering)
    cv2.waitKey(1)
