from gyro import Gyro
from gpiozero import Robot, DistanceSensor
from geographiclib.geodesic import Geodesic
from time import time
import threading

class PortaVax():
    def __init__(self,
        left_motor_pins,
        right_motor_pins,
        GPSD,
        target_lat_lon,
        forward_distance_pins,
        left_distance_pins,
        right_distance_pins,
    ):
        self.robot = Robot(left=left_motor_pins, right=right_motor_pins)
        self.gpsd = GPSD
        self.target_lat_lon = target_lat_lon
        if forward_distance_pins:
            self.forward_distance_sensor = DistanceSensor(*forward_distance_pins)
            self.left_distance_sensor = DistanceSensor(*left_distance_pins)
            self.right_distance_sensor = DistanceSensor(*right_distance_pins)
        self.gyro = Gyro()

    def drive(self, speed, turn):
        self.differential_drive(max(-1, min(1, speed + turn)), max(-1, min(1, speed - turn)))

    def differential_drive(self, left, right):
        self.robot.value = (left, right)

    def stop(self):
        self.robot.stop()
    
    def get_position(self):
        return (0, 0) # TODO: replace with actual gps
    
    def get_bearing(self):
        return 0 # TODO: replace with actual gps
    
    def turn_degrees(self, degrees):
        gyro_start = self.gyro.get()
        gyro_target = gyro_start + degrees
        while abs(self.gyro.get() - gyro_target) < 5:
            if self.gyro.get() > gyro_target:
                self.differential_drive(0.1, -0.1)
            else:
                self.differential_drive(-0.1, 0.1)
        self.stop()
    
    def turn_to_target(self):
        target_bearing = Geodesic.WGS84.Inverse(*self.get_position(), *self.target_lat_lon)['azi1']
        current_bearing = self.get_bearing()
        print("Current bearing: {}".format(self.get_bearing()))
        turn = target_bearing - current_bearing
        self.turn_degrees(turn)
        print("Target bearing: {}".format(target_bearing))
        print("Final bearing: {}".format(self.get_bearing()))
    
    def drive_straight_gyro_pid(self, gyro_target, finish_time):
        error = gyro_target - self.gyro.get()
        Kp = 0.02
        self.differential_drive(0.8 + Kp * error, 0.8 - Kp * error)
        if time() < finish_time:
            threading.Timer(0.1, self.drive_straight_gyro_pid, [gyro_target, finish_time]).start()

    def drive_straight(self, seconds=5):
        gyro_target = self.gyro.get()
        self.drive_straight_gyro_pid(gyro_target, time() + seconds)

        