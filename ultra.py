import RPi.GPIO as GPIO
import time
from threading import Timer
 
class Ultra:
    def __init__(self, trig, echo):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        #set GPIO Pins
        self.GPIO_TRIGGER = trig
        self.GPIO_ECHO = echo
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        self.distance = -1
    
    def measure(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
            if StartTime - StopTime > 0.2:
                self.distance = -1
                return
    
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        self.distance = distance
    
    def start(self, delay):
        self.measure()
        self.timer = Timer(delay, self.start, [delay])
        self.timer.start()
    
    def stop(self):
        self.timer.cancel()