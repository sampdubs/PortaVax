from math import sin
from gpiozero import Motor

m = Motor(20, 21)
def drive(speed):
    if speed > 0:
        m.forward(speed)
    else:
        m.backward(-speed)

t = 0
while True:
    drive(sin(t))
    t += 0.00005
