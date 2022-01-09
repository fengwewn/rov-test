import RPi.GPIO as GPIO
from gpiozero import Servo, AngularServo
import time

class LowController:

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)

        self.motor1_1 = GPIO.PWM(6, 500)
        self.motor1_2 = GPIO.PWM(13, 500)
        self.motor2_1 = GPIO.PWM(19, 500)
        self.motor2_2 = GPIO.PWM(26, 500)

        self.motor1_1.start(0)
        self.motor1_2.start(0)
        self.motor2_1.start(0)
        self.motor2_2.start(0)
        
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        
        self.led1 = GPIO.PWM(17, 500)
        self.led2 = GPIO.PWM(27, 500)
        self.led3 = GPIO.PWM(22, 500)
        
        self.ledId = {'R':self.led1, 'G':self.led2, 'B':self.led3}
        
        self.led1.start(0)
        self.led2.start(0)
        self.led3.start(0)
        
        self.led1.ChangeDutyCycle(10)
        self.led2.ChangeDutyCycle(10)
        self.led3.ChangeDutyCycle(10)
        
        self.lifterServo = Servo(12, min_pulse_width=0.0005, max_pulse_width=0.0025, frame_width=0.020)
        self.lifterServo.value = -1
        # Must sleep to let lifter reset
        time.sleep(1)
        
        self.led1.ChangeDutyCycle(0)
        self.led2.ChangeDutyCycle(0)
        self.led3.ChangeDutyCycle(0)

        print('gpio inited')

    def forwards(self, force):
        self.motor1_1.ChangeDutyCycle(0)
        self.motor1_2.ChangeDutyCycle(force)
        self.motor2_1.ChangeDutyCycle(0)
        self.motor2_2.ChangeDutyCycle(force)
    
    def backwards(self, force):
        self.motor1_1.ChangeDutyCycle(force)
        self.motor1_2.ChangeDutyCycle(0)
        self.motor2_1.ChangeDutyCycle(force)
        self.motor2_2.ChangeDutyCycle(0)

    def turnRightByLeftWheel(self, force):
        """turning right with left motor"""
        self.motor1_1.ChangeDutyCycle(force)
        self.motor1_2.ChangeDutyCycle(0)
        self.motor2_1.ChangeDutyCycle(0)
        self.motor2_2.ChangeDutyCycle(0)

    def turnLeftByLeftWheel(self, force):
        self.motor1_1.ChangeDutyCycle(0)
        self.motor1_2.ChangeDutyCycle(force)
        self.motor2_1.ChangeDutyCycle(0)
        self.motor2_2.ChangeDutyCycle(0)

    def turnLeftByRightWheel(self, force):
        self.motor1_1.ChangeDutyCycle(0)
        self.motor1_2.ChangeDutyCycle(0)
        self.motor2_1.ChangeDutyCycle(force)
        self.motor2_2.ChangeDutyCycle(0)

    def turnRightByRightWheel(self, force):
        self.motor1_1.ChangeDutyCycle(0)
        self.motor1_2.ChangeDutyCycle(0)
        self.motor2_1.ChangeDutyCycle(0)
        self.motor2_2.ChangeDutyCycle(force)

    def rotateClockwise(self, force):
        self.motor1_1.ChangeDutyCycle(0)
        self.motor1_2.ChangeDutyCycle(force)
        self.motor2_1.ChangeDutyCycle(force)
        self.motor2_2.ChangeDutyCycle(0)

    def rotateAntiClockwise(self, force):
        self.motor1_1.ChangeDutyCycle(force)
        self.motor1_2.ChangeDutyCycle(0)
        self.motor2_1.ChangeDutyCycle(0)
        self.motor2_2.ChangeDutyCycle(force)

    def stop(self):
        self.motor1_1.ChangeDutyCycle(0)
        self.motor1_2.ChangeDutyCycle(0)
        self.motor2_1.ChangeDutyCycle(0)
        self.motor2_2.ChangeDutyCycle(0)
        
    def moveLifter(self, position):
        """Accept from 0-100"""
        self.lifterServo.value = (position*2-100)/100
        
    def switchLed(self, color, status):
        cycle = 0
        if(status):
            cycle = 10
        else:
            cycle = 0
        
        self.ledId.get(color, None).ChangeDutyCycle(cycle)
        
