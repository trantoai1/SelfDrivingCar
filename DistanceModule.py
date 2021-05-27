# Libraries

import time
from Setting import GPIO, GPIO_TRIGGER, GPIO_ECHO
from threading import Thread, RLock


class ThreadSonic(Thread):
    def __init__(self):
        self.GPIO_TRIGGER = GPIO_TRIGGER
        self.GPIO_ECHO = GPIO_ECHO
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        self.RUN = True
        self.currentDis = False
        self.lock = RLock()
        super(ThreadSonic, self).__init__()

    def run(self):
        print('Distance Module starting...')
        while self.RUN:
            with self.lock:
                ds = self.distance()
                if ds < 10:
                    self.currentDis = True
                else:
                    self.currentDis = False
            time.sleep(1)  # let it breathe
        print('Distance Module stopped!')
    def join(self):
        return self.currentDis

    # set GPIO direction (IN / OUT)

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.01)
        GPIO.output(self.GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distan = (TimeElapsed * 34300) / 2
        return distan

    def stop(self):
        print('Distance Module stopping...')
        self.RUN = False