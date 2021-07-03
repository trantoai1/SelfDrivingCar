import time
from threading import Thread, RLock
from SignDetect import SignDetect
from Setting import SIGNDISTANCE, LISTSIGN
import WebcamModule as wM

class ThreadImage(Thread):
    def __init__(self):
        self.signDetect = SignDetect()
        self.img = wM.getImg(size=[480, 360])
        self.RUN = True
        self.exec = False
        self.sign = -1
        self.processImg = self.img
        self.lock = RLock()
        super(ThreadImage, self).__init__()

    def setImg(self, img):
        with self.lock:
            self.img = img

    def run(self):
        print('Sign Module is starting...')
        while self.RUN:
            with self.lock:
                self.img = wM.getImg(size=[480, 360])
                coordinate, self.processImg, sign_type, text = self.signDetect.localization(self.img)
                if coordinate is not None:
                    top = int(coordinate[0][1] * 1.05)
                    #left = int(coordinate[0][0] * 1.05)
                    bottom = int(coordinate[1][1] * 0.95)
                    #right = int(coordinate[1][0] * 0.95)
                    if abs(bottom - top) > SIGNDISTANCE:
                        print(abs(bottom - top))
                        self.exec = True
                else:
                    self.exec = False
                if sign_type in LISTSIGN:
                    self.sign = sign_type
                else:
                    self.sign = -1
            time.sleep(0.001)  # let it breathe
        print('Sign Module was stopped!')

    def join(self):
        return self.processImg, self.sign, self.exec

    def stop(self):
        print('Sign Module is stopping...')
        self.RUN = False
