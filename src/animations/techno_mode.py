from rgbmatrix import RGBMatrix
import time
import math

# 🛠 Techno Mode Visualizer
# Description:
#   Generates rotating circular patterns and grid sweeps,
#   simulating industrial techno beats with a mechanized feel.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    center_x = width // 2
    center_y = height // 2
    radius = min(center_x, center_y) - 4
    t = 0

    try:
        while True:
            matrix.Clear()

            # Draw radial arms like clock hands
            for arm in range(8):  # 8 radial lines
                angle = (t * 0.1 + arm * (math.pi / 4)) % (2 * math.pi)
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        px = x + i
                        py = y + j
                        if 0 <= px < width and 0 <= py < height:
                            matrix.SetPixel(px, py, 0, 255, 255)

            # Add a sweeping grid of bars
            for i in range(0, width, 8):
                col_intensity = int((math.sin(t * 0.1 + i) + 1) * 127)
                for y in range(height):
                    matrix.SetPixel(i, y, col_intensity, 0, 255 - col_intensity)

            time.sleep(0.04)
            t += 1

            if preview and t > 300:
                break

    except KeyboardInterrupt:
        matrix.Clear()
