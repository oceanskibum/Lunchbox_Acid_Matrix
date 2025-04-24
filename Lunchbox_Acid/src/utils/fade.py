import time

def fade_out(matrix, duration=0.5, steps=10):
    """Fades out the current screen over a number of steps."""
    width = matrix.width
    height = matrix.height
    for step in range(steps, 0, -1):
        fade_factor = step / steps
        for x in range(width):
            for y in range(height):
                r, g, b = matrix.GetPixel(x, y)
                matrix.SetPixel(x, y,
                                int(r * fade_factor),
                                int(g * fade_factor),
                                int(b * fade_factor))
        time.sleep(duration / steps)

def fade_in(matrix, frame_func, duration=0.5, steps=10):
    """Fades in a new frame from black using the provided frame drawing function."""
    for step in range(1, steps + 1):
        frame_func(intensity=step / steps)
        time.sleep(duration / steps)
