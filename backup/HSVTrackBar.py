import cv2
import numpy as np

import Setting


def empty(a):
    pass
class HSVTrackBar():
    def __init__(self):
        self.HSVTrackBarName = 'HSVTrackBar'
        cv2.namedWindow(self.HSVTrackBarName)
        cv2.resizeWindow(self.HSVTrackBarName, 640, 240)
        cv2.createTrackbar("HUE Min", self.HSVTrackBarName, 0, 179, empty)
        cv2.createTrackbar("HUE Max", self.HSVTrackBarName, 179, 179, empty)
        cv2.createTrackbar("SAT Min", self.HSVTrackBarName, 0, 255, empty)
        cv2.createTrackbar("SAT Max", self.HSVTrackBarName, 255, 255, empty)
        cv2.createTrackbar("VALUE Min", self.HSVTrackBarName, 0, 255, empty)
        cv2.createTrackbar("VALUE Max", self.HSVTrackBarName, 255, 255, empty)
        cv2.setTrackbarPos("HUE Min", self.HSVTrackBarName, pos=Setting.LOWERWHITE[Setting.CAMERAMODE][0])
        cv2.setTrackbarPos("HUE Max", self.HSVTrackBarName, pos=Setting.UPPERWHITE[Setting.CAMERAMODE][0])
        cv2.setTrackbarPos("SAT Min", self.HSVTrackBarName, pos=Setting.LOWERWHITE[Setting.CAMERAMODE][1])
        cv2.setTrackbarPos("SAT Max", self.HSVTrackBarName, pos=Setting.UPPERWHITE[Setting.CAMERAMODE][1])
        cv2.setTrackbarPos("VALUE Min", self.HSVTrackBarName, pos=Setting.LOWERWHITE[Setting.CAMERAMODE][2])
        cv2.setTrackbarPos("VALUE Max", self.HSVTrackBarName, pos=Setting.UPPERWHITE[Setting.CAMERAMODE][2])


    def getHSV(self):
        h_min = cv2.getTrackbarPos("HUE Min", self.HSVTrackBarName)
        h_max = cv2.getTrackbarPos("HUE Max", self.HSVTrackBarName)
        s_min = cv2.getTrackbarPos("SAT Min", self.HSVTrackBarName)
        s_max = cv2.getTrackbarPos("SAT Max", self.HSVTrackBarName)
        v_min = cv2.getTrackbarPos("VALUE Min", self.HSVTrackBarName)
        v_max = cv2.getTrackbarPos("VALUE Max", self.HSVTrackBarName)
        print('HSV:min:{}, max:{}'.format([h_min, s_min, v_min],[h_max, s_max, v_max]))
        return np.array([h_min, s_min, v_min]),np.array([h_max, s_max, v_max])