from math import sin
from gpiozero import Motor

m = Motor(20, 21)
n = Motor(6, 5)
def drive(speed):
    if speed > 0:
        m.forward(speed)
        n.forward(speed)
    else:
        m.backward(-speed)
        n.backward(-speed)

t = 0
while True:
    #drive(sin(t))
    drive(1)
    t += 0.00005
