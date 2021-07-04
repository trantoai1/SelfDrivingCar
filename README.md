Yêu cầu
Xây dựng xe tự hành theo line với những yêu cầu
−	Đi theo line đen có sẵn
−	Tự động bật sáng dưới hầm tối
−	Tự tăng tốc khi gặp chướng ngại vật (cầu)
−	Nhận diện biển báo theo mô hình học sâu (Optional)
PHẦN CỨNG
−	Raspberry Pi model 3B +
−	Camera Raspberry Pi V1 OV5647 5MP
−	Arduino UNO
−	L298N Motor Driver
−	SN-LIGHT-MOD (Light sensor module)
−	IR sensor x2 (Line sensor)
−	Ultrasonic sensor HC-SR04
−	Power
−	LED x2
MÔ HÌNH MẠCH
 
NGUYÊN LÝ HOẠT ĐỘNG
Motor Module
•	L298N nhận tín hiệu motor từ Arduino qua pin 4-7 để điều khiển bánh xe tiến hoặc lùi
•	L298N nhận tín hiệu ENABLE từ Raspberry Pi để tăng tốc, giảm tốc, dừng lại dựa vào biển báo, chướng ngại vật.
Code
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
Line Module
•	IR sensor nhận tín hiệu cảm biến hồng ngoại vào pin 2, 3 của Arduino
•	Arduino xử lý code gửi tín hiệu điều khiển motor L298N qua pin 4, 5, 6, 7
Code
#define LS 2 // left sensor
#define RS 3 // right sensor
#define LM1 5 // left motor M1a
#define LM2 4 // left motor M2a
#define RM1 6 // right motor M2a
#define RM2 7 // right motor M2b
#define echoPin 8 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 9 //attach pin D3 Arduino to pin Trig of HC-SR04
#define outSonic 10
void setup()
{
  pinMode(outSonic, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT);
  pinMode(LS, INPUT);
  pinMode(RS, INPUT);
  pinMode(LM1, OUTPUT);
  pinMode(LM2, OUTPUT);
  pinMode(RM1, OUTPUT);
  pinMode(RM2, OUTPUT);
  //Serial.begin(9600);
}
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement

void loop()
{
  dist();
  if (distance <=10)
  {
    digitalWrite(outSonic, HIGH);
  }
  else
  {
    digitalWrite(outSonic, LOW);
  }
  if (digitalRead(LS) && digitalRead(RS)) 
  {
    digitalWrite(LM1, LOW);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, LOW);
    digitalWrite(RM2, LOW); 
  }
  if (!digitalRead(LS) && (digitalRead(RS))
  {
    digitalWrite(LM1, HIGH);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, LOW);
    digitalWrite(RM2, HIGH);
  }
  if ((digitalRead(LS)) && !digitalRead(RS)) 
  {
    digitalWrite(LM1, LOW);
    digitalWrite(LM2, HIGH);
    digitalWrite(RM1, HIGH);
    digitalWrite(RM2, LOW);
    //Serial.println("RIGHT");
  }

  if (!(digitalRead(LS)) && !(digitalRead(RS))) 
  {
    digitalWrite(LM1, HIGH);
    digitalWrite(LM2, LOW);
    digitalWrite(RM1, HIGH);
    digitalWrite(RM2, LOW);
    \
  }
}

Ultra sonic sensor
•	Ultra sonic sensor nhận dữ liệu gửi vào pin 8 (echo) và pin 9 (trig)
Code
void dist()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH); 
  distance = duration * 0.034 / 2; 
}

•	Arduino sẽ tính toán tốc độ âm thanh và khoảng cách nhỏ hơn 10 cm sẽ gửi out qua pin 10 tới Raspberry Pi
•	Khi Raspberry Pi nhận tín hiệu HIGH từ Arduino sẽ tăng tốc vòng quay bánh xe
Code
distance = (GPIO.input(GPIO_ECHO)==GPIO.HIGH)
if distance :
    print('speed up {} '.format(distance))
    speed = 1
    motor.move(speed,t= 3)
    speed = SPEEDDOWN

Light sensor
•	Hoạt động multi thread trong raspberry pi
•	Tín hiệu từ SN-LIGHT-MODE sẽ được raspberry pi xử lý và bật đèn led
Code
class LightSensor(Thread):
    def __init__(self):
        self.PINSENSOR = LIGHTPIN
        self.RUN = True
        self.lock = RLock()
        self.led = LED(LEDPIN)
        super(LightSensor, self).__init__()

    def run(self):
        print('Light Module is starting...')
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
        print('Light Module was stopped!')


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
        print('Light Module is stopping...')
        self.RUN = False

Sign Detect Module
•	Tensorflow 2.0.0
•	Google colab
•	CNN
model = Sequential()
model.add(Conv2D(64, (3 , 3), padding='same'))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Conv2D(64, (3 , 3), padding='same'))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(classes))
 

KẾT QUẢ
Nhận diện biển báo:
Stop
 
Keep left
 
Keep right
 
Speed limit 70KM/h
 
 
Speed limit 30KM/h
 
Di chuyển theo lane
 

Vượt chướng ngại
 

Bật đèn
 


VIDEO DEMO
Di chuyển theo line, vượt ngại vật và đèn
https://www.youtube.com/watch?v=zeyhuXUoed0
Di chuyển và nhận diện biển báo
https://www.youtube.com/watch?v=_xUih76J3ds
