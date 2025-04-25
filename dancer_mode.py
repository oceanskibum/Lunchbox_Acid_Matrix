from rgbmatrix import RGBMatrix
import time
import random

# 💃 Dancer Mode Visualizer
# Description:
#   Reacts to motion magnitude from IMU sensor.
#   High magnitude creates a matrix-wide sparkle burst.
#   Light motion produces gentle waves or pulses.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    intensity = 0

    try:
        t = 0
        while True:
            matrix.Clear()

            # Simulated motion magnitude
            magnitude = 10000 + 15000 * abs(random.sin(t * 0.2))

            if magnitude > 25000:
                # High motion = full burst
                for _ in range(300):
                    x = random.randint(0, width - 1)
                    y = random.randint(0, height - 1)
                    matrix.SetPixel(x, y, 255, random.randint(50, 150), 255)
            elif magnitude > 15000:
                # Medium motion = waves
                for x in range(width):
                    y = int(32 + 10 * random.sin((x + t) * 0.3))
                    matrix.SetPixel(x, y, 128, 0, 255)

            time.sleep(0.04)
            t += 1

            if preview and t > 150:
                break

    except KeyboardInterrupt:
        matrix.Clear()
