# Motion Detection via MPU6050 using smbus2

import smbus2
import time

class IMUInput:
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self.address = 0x68
        self.bus.write_byte_data(self.address, 0x6B, 0)  # Wake up MPU6050

    def read_movement(self):
        accel_x = self.read_word_2c(0x3B)
        accel_y = self.read_word_2c(0x3D)
        accel_z = self.read_word_2c(0x3F)
        magnitude = (accel_x**2 + accel_y**2 + accel_z**2)**0.5
        return magnitude

    def read_word_2c(self, reg):
        high = self.bus.read_byte_data(self.address, reg)
        low = self.bus.read_byte_data(self.address, reg+1)
        val = (high << 8) + low
        return val - 65536 if val >= 0x8000 else val
