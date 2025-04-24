import time
import math
from rgbmatrix import RGBMatrix

class HouseMode:
    def __init__(self, matrix, audio_input=None, beat_detector=None, sensitivity=1.5):
        self.matrix = matrix
        self.audio_input = audio_input
        self.beat_detector = beat_detector
        self.sensitivity = sensitivity
        self.frame = 0
        self.phase_shift = 0
        self.bpm = 120
        self.color_offset = 0

    def draw(self):
        self.matrix.Clear()
        fft = self.audio_input.latest_fft.copy() if self.audio_input else None
        freqs = self.audio_input.freqs if hasattr(self.audio_input, "freqs") else None

        beat = False
        bass = 0.0
        if self.audio_input and self.beat_detector and fft is not None and freqs is not None:
            beat, bass, self.bpm = self.beat_detector.detect(fft, freqs)

        # Smooth waveform lines that pulse gently with bass and beat
        for x in range(self.matrix.width):
            y_center = int(
                (math.sin((self.phase_shift + x * 0.2)) + 1) * (self.matrix.height / 4)
            ) + self.matrix.height // 4

            color = self.hsv_to_rgb(((x + self.color_offset) % 255) / 255.0, 1.0, 0.7 + (bass / 400 if self.audio_input else 0.3))
            self.matrix.SetPixel(x, y_center, *color)

        self.phase_shift += 0.2
        if beat:
            self.color_offset += 12  # shift palette on beat

        self.frame += 1
        time.sleep(0.03)

    def hsv_to_rgb(self, h, s, v):
        i = int(h * 6)
        f = (h * 6) - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - f * s))
        t = int(255 * v * (1 - (1 - f) * s))
        v = int(255 * v)
        i = i % 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
