from rgbmatrix import RGBMatrix
import time
import random

# 🚫 Idle Mode Visualizer
# Description:
#   A fun "404 - Vibes Not Found" display for when nothing is active.
#   Glitchy background flickers with subtle text scrolling and pixel noise.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    message = "404 - Vibes Not Found"

    try:
        scroll_pos = width

        while True:
            matrix.Clear()

            # Glitch flicker background
            for _ in range(100):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                r = random.randint(100, 255)
                g = 0
                b = random.randint(100, 255)
                matrix.SetPixel(x, y, r, g, b)

            # Simulated scrolling text with blocky chunks
            for i, char in enumerate(message):
                char_x = scroll_pos + i * 5
                if 0 <= char_x < width:
                    for y in range(3):
                        matrix.SetPixel(char_x, y + 30, 255, 0, 255)  # Fake text pixel band

            scroll_pos -= 1
            if scroll_pos < -len(message) * 5:
                scroll_pos = width

            time.sleep(0.05)

            if preview and scroll_pos < 10:
                break

    except KeyboardInterrupt:
        matrix.Clear()
