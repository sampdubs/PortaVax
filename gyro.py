import threading
import os

import board
import busio

import adafruit_lsm9ds0

class MovingAverage():
    def __init__(self, readings=100, needsZero=False):
        self.data = []
        self.readings = readings
        self.ready = False
        self.offset = 0
        self.zeroed = not needsZero
    
    def update(self, datum):
        if len(self.data) < self.readings:
            self.data.append(datum)
        else:
            self.data.pop(0)
            self.data.append(datum)
            self.ready = True
    
    def zero(self):
        self.offset = self._average()
        self.zeroed = True
    
    def _average(self):
        return sum(self.data) / len(self.data) - self.offset

    def __str__(self):
        if self.ready and self.zeroed:
            return str(self._average())
        return "..."
    
    def __format__(self, spec):
        if self.ready and self.zeroed:
            return "{:0.3f}".format(self._average())
        return "..."

class MovingAverage3D():
    def __init__(self, readings=100, needsZero=False):
        self.data = [MovingAverage(readings, needsZero) for _ in range(3)]

    def update(self, datum):
        datum = list(datum)
        for i in range(3):
            self.data[i].update(datum[i])
    
    def zero(self):
        for ma in self.data:
            ma.zero()

    def is_ready(self):
        return all([ma.ready and ma.zeroed for ma in self.data])
    
    def _average(self):
        return [ma._average() for ma in self.data]

    def __str__(self):
        return "({}, {}, {})".format(*self.data)
    
    def __format__(self, spec):
        return str(self)

class Gyro():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)

        self.value = MovingAverage3D(needsZero=True)

        threading.Timer(0.1, self.update).start()
    
    def zero(self):
        self.value.zero()
    
    def update(self):
        self.value.update(self.sensor.gyro)
    
    def is_ready(self):
        return self.value.is_ready()
    
    def get(self):
        return self.value._average()

if __name__ == "__main__":
    gyro = Gyro()
    while True:
        if gyro.is_ready():
            print(gyro.get())