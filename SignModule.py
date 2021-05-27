import time
from threading import Thread, RLock
from SignDetect import SignDetect
from Setting import SIGNDISTANCE, LISTSIGN


class ThreadImage(Thread):
    def __init__(self, img=None):
        self.signDetect = SignDetect()
        self.img = img
        self.RUN = True
        self.exec = False
        self.sign = -1
        self.processImg = None
        self.lock = RLock()
        super(ThreadImage, self).__init__()

    def setImg(self, img):
        with self.lock:
            self.img = img

    def run(self):
        print('Sign Module starting...')
        while self.RUN:
            with self.lock:
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
        print('Sign Module stopped!')

    def join(self):
        return self.processImg, self.sign, self.exec

    def stop(self):
        print('Sign Module stopping...')
        self.RUN = False
