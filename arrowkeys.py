import keyboard
from gps import *
from drive import PortaVax

if __name__ == "__main__":
    pv = PortaVax(
        (20, 21),
        (6, 5),
        gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0))

    while True:
        speed = 0
        angle = 0
        if keyboard.is_pressed("right arrow"):
            angle += 1
        if keyboard.is_pressed("left arrow"):
            angle -= 1
        if keyboard.is_pressed("up arrow"):
            speed += 1
        if keyboard.is_pressed("down arrow"):
            angle -= 1
        pv.drive(speed, angle)
