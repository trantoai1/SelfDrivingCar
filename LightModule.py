#!/usr/local/bin/python
import time
from Setting import LED, GPIO, LIGHTPIN, LIGHT_ON, LEDPIN
from threading import Thread,RLock

class LightSensor(Thread):
    def __init__(self):
        self.PINSENSOR = LIGHTPIN
        self.RUN = True
        self.lock = RLock()
        self.led = LED(LEDPIN)
        super(LightSensor, self).__init__()

    def run(self):
        print('Light Module starting...')
        while self.RUN:
            with self.lock:
                value = self.rc_time()
                if (value < LIGHT_ON):
                    #print("Lights are ON")
                    self.led.on()
                else:
                    #print("Lights are OFF")
                    self.led.off()

            time.sleep(0.5)  # let it breathe
        print('Light Module stopped!')


    def rc_time(self):
        count = 0
        # Output on the pin for
        GPIO.setup(self.PINSENSOR, GPIO.OUT)
        GPIO.output(self.PINSENSOR, GPIO.LOW)
        time.sleep(0.1)
        # Change the pin back to input
        GPIO.setup(self.PINSENSOR, GPIO.IN)

        # Count until the pin goes high
        while (GPIO.input(self.PINSENSOR) == GPIO.LOW):
            count += 1
            if count > LIGHT_ON:
                return count

        return count

    def stop(self):
        print('Light Module stopping...')
        self.RUN = False
#define the pin that goes to the circuit

#
# pin_to_circuit= 4
# led = LED(26)
# def rc_time (pin_to_circuit):
#     count = 0
#
#     #Output on the pin for
#     GPIO.setup(pin_to_circuit, GPIO.OUT)
#     GPIO.output(pin_to_circuit, GPIO.LOW)
#     time.sleep(0.1)
#
#     #Change the pin back to input
#     GPIO.setup(pin_to_circuit, GPIO.IN)
#
#     #Count until the pin goes high
#     while (GPIO.input(pin_to_circuit) == GPIO.LOW):
#         count += 1
#         if count > Setting.LIGHT_ON:
#             return count
#
#     return count
#
# #Catch when script is interupted, cleanup correctly
# def lightsensor():
#     try:
#         # Main loop
#
#         while True:
#
#             value = rc_time(pin_to_circuit)
#             #debug('Ldr Value:'.format(value))
#             print(value)
#             if ( value < Setting.LIGHT_ON):
#                     print("Lights are ON")
#
#                     led.on()
#             else :
#                     print("Lights are OFF")
#                     led.off()
#             time.sleep(1)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         GPIO.cleanup()
#
# if __name__ == '__main__':
#     lightsensor()