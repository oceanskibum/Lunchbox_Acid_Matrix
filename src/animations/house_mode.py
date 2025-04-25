from rgbmatrix import RGBMatrix

def run_animation(matrix: RGBMatrix, preview=False):
    import time
    matrix.Clear()
    for i in range(0, 64, 4):
        for j in range(0, 64, 4):
            matrix.SetPixel(i, j, 0, 255, 128)
    if preview:
        time.sleep(10)
    else:
        while True:
            time.sleep(1)
