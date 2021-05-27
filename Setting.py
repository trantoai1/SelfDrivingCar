import RPi.GPIO as GPIO
from gpiozero import LED

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DEBUG = True
# Motor pin config
MOTOR_EnaA = 17

MOTOR_In1A = 22
MOTOR_In2A = 27

MOTOR_EnaB = 23
MOTOR_In1B = 15
MOTOR_In2B = 18

LINEDETECT_LEFT = 20
LINEDETECT_RIGHT = 21

# Light sensor pin config
LIGHTPIN = 4  # pin light sensor
LEDPIN = 26  # pin led
LIGHT_ON = 10000
# ultra sonic sensor
# set GPIO Pins
GPIO_TRIGGER = 5
GPIO_ECHO = 6

# camera config
CAMERAMODE = 0

CAMERALANE = [0, 'vid1.mp4']
CAMERASIGN = [0, 'QuestionVideo.avi']  # QuestionVideo.avi MVI_1049.mp4

# OpenCV
#

LOWERWHITE = [[0, 30, 1], [85, 0, 0]]
UPPERWHITE = [[85, 249, 89], [179, 160, 255]]
# TRACKBAR = [[198,198,172,240],[102,80,20,214]]
TRACKBAR = [[43, 75, 0, 109], [102, 80, 20, 214]]
HSVBARENABLE = False
LANEDISPLAYMODE = 2

# Socket
HOST = '10.1.1.1'
PORT = 8000
JOYSTICK = False


MOTOR_SENSITY = 1.3
MOTOR_MAXSPEED = 0.3
# SignModule
SIGNDISTANCE = 105
LISTSIGN = [1, 4, 14, 38, 39]
classNames = ['Speed limit (20km/h)',
              'Speed limit (30km/h)',
              'Speed limit (50km/h)',
              'Speed limit (60km/h)',
              'Speed limit (70km/h)',
              'Speed limit (80km/h)',
              'End of speed limit (80km/h)',
              'Speed limit (100km/h)',
              'Speed limit (120km/h)',
              'No passing',
              'No passing for vehicles over 3.5 metric tons',
              'Right-of-way at the next intersection',
              'Priority road',
              'Yield',
              'Stop',
              'No vehicles',
              'Vehicles over 3.5 metric tons prohibited',
              'No entry',
              'General caution',
              'Dangerous curve to the left',
              'Dangerous curve to the right',
              'Double curve',
              'Bumpy road',
              'Slippery road',
              'Road narrows on the right',
              'Road work',
              'Traffic signals',
              'Pedestrians',
              'Children crossing',
              'Bicycles crossing',
              'Beware of ice/snow',
              'Wild animals crossing',
              'End of all speed and passing limits',
              'Turn right ahead',
              'Turn left ahead',
              'Ahead only',
              'Go straight or right',
              'Go straight or left',
              'Keep right',
              'Keep left',
              'Roundabout mandatory',
              'End of no passing',
              'End of no passing by vehicles over 3.5 metric tons']
