import smbus2
import time
import math

class IMUMotion:
    def __init__(self, bus_num=1, address=0x68):
        self.address = address
        self.bus = smbus2.SMBus(bus_num)
        self.motion_enabled = True
        self.last_motion = None

        # Wake up the MPU6050
        self.bus.write_byte_data(self.address, 0x6B, 0)

    def read_accel(self):
        def read_word(reg):
            high = self.bus.read_byte_data(self.address, reg)
            low = self.bus.read_byte_data(self.address, reg + 1)
            val = (high << 8) + low
            return val if val < 32768 else val - 65536

        ax = read_word(0x3B) / 16384.0
        ay = read_word(0x3D) / 16384.0
        az = read_word(0x3F) / 16384.0
        return ax, ay, az

    def detect_motion_state(self):
        if not self.motion_enabled:
            return "off"

        ax, ay, az = self.read_accel()
        magnitude = math.sqrt(ax*ax + ay*ay + az*az)

        if magnitude > 2.0:
            return "jump"
        elif abs(ax) > 1.2 or abs(ay) > 1.2:
            return "bounce"
        elif abs(ax) > 0.5 or abs(ay) > 0.5:
            return "walk"
        else:
            return "still"
