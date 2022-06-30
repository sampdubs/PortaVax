import smbus
import time

address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)

input_voltage = 5

while True:
    bus.write_byte(address, A0)
    value = bus.read_byte(address)
    print("Measured voltage: {:0.3f}".format(value / 255 * input_voltage))
    time.sleep(0.1)
