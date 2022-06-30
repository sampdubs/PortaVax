# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the LSM9DS0 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import time
import os

import board
import busio

import adafruit_lsm9ds0

class MovingAverage():
    def __init__(self, readings=100):
        self.data = []
        self.readings = readings
        self.ready = False
    
    def update(self, datum):
        if len(self.data) < self.readings:
            self.data.append(datum)
        else:
            self.data.pop(0)
            self.data.append(datum)
            self.ready = True
    
    def _average(self):
        return sum(self.data) / len(self.data)

    def __str__(self):
        if self.ready:
            return str(self._average())
        return "..."
    
    def __format__(self, spec):
        if self.ready:
            return "{:0.3f}".format(self._average())
        return "..."

class MovingAverage3D():
    def __init__(self, readings=100):
        self.data = [MovingAverage(readings) for _ in range(3)]

    def update(self, datum):
        datum = list(datum)
        for i in range(3):
            self.data[i].update(datum[i])
    
    def _average(self):
        return [ma._average() for ma in self.data]

    def __str__(self):
        return "({0:0.3f},{1:0.3f},{2:0.3f})".format(*self.data)
    
    def __format__(self, spec):
        return str(self)
    

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)

temp = MovingAverage()
accel = MovingAverage3D()
mag = MovingAverage3D()
gyro = MovingAverage3D()


# Main loop will read the acceleration, magnetometer, gyroscope, Temperature
# values every second and print them out.
while True:
    # Read acceleration, magnetometer, gyroscope, temperature.
    accel.update(sensor.acceleration)
    mag.update(sensor.magnetic)
    gyro.update(sensor.gyro)
    temp.update(sensor.temperature)
    os.system("clear")
    # Print values.
    print("Acceleration (m/s^2):\t\t{}".format(accel))
    print("Magnetometer (gauss):\t\t{}".format(mag))
    print("Gyroscope (degrees/sec):\t{}".format(gyro))
    print("Temperature:\t\t\t{}C".format(temp))
    # Delay for a second.
    # time.sleep(0.2)
