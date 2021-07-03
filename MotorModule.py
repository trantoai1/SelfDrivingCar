
from time import sleep
from Setting import MOTOR_EnaA,MOTOR_EnaB, GPIO



class Motor():
    def __init__(self, EnaA=MOTOR_EnaA, EnaB=MOTOR_EnaB):
        self.EnaA = EnaA
        self.EnaB = EnaB
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmB.start(0);

    def move(self, speed=0.5, turn=0, t=0):
        #print('move')

        speed *= 100
        turn *= 100
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100

        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        sleep(t)


    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        sleep(t)


# def main(motor):
#     motor.move(0.6, 0, 2)
#     motor.stop(2)
#     motor.move(-0.5, 0.2, 2)
#     motor.stop(2)
#
#
# if __name__ == '__main__':
#     motor = Motor()
#     while True:
#         main(motor)