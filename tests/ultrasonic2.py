from gpiozero import DistanceSensor
a = DistanceSensor(trigger=9, echo=10, max_distance=10000)


while True:
    print(a.value)