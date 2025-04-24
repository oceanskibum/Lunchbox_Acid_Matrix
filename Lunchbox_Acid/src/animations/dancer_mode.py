import time, math, random

class DancerMode:
    def __init__(self, matrix, imu_input=None):
        self.matrix = matrix
        self.imu_input = imu_input
        self.frame = 0
        self.mode = "still"

    def draw(self):
        self.matrix.Clear()

        if self.imu_input:
            self.mode = self.imu_input.detect_motion_state()

        if self.mode == "jump":
            self.flash_color()
        elif self.mode == "bounce":
            self.wave_lines(speed=0.3)
        elif self.mode == "walk":
            self.flicker_grid()
        else:
            self.smooth_gradient()

        self.frame += 1
        time.sleep(0.04)

    def flash_color(self):
        r, g, b = random.randint(150, 255), random.randint(0, 150), random.randint(100, 255)
        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                self.matrix.SetPixel(x, y, r, g, b)

    def wave_lines(self, speed):
        for x in range(self.matrix.width):
            y = int((math.sin((self.frame * speed + x) * 0.3) + 1) * (self.matrix.height / 3)) + 10
            color = (int((math.sin(x * 0.1) + 1) * 127), 255 - x*3 % 255, x*5 % 255)
            if 0 <= y < self.matrix.height:
                self.matrix.SetPixel(x, y, *color)

    def flicker_grid(self):
        for x in range(0, self.matrix.width, 4):
            for y in range(0, self.matrix.height, 4):
                if random.random() > 0.8:
                    self.matrix.SetPixel(x, y, 255, 255, 255)

    def smooth_gradient(self):
        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                val = int((math.sin(x * 0.1 + self.frame * 0.05) + math.cos(y * 0.1)) * 127) & 255
                self.matrix.SetPixel(x, y, val, val // 2, 255 - val)
