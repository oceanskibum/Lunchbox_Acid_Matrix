import time, math, random
class BassHouseMode:
    def __init__(self, matrix, audio_input=None, beat_detector=None, sensitivity=1.5):
        self.matrix = matrix
        self.audio_input = audio_input
        self.beat_detector = beat_detector
        self.sensitivity = sensitivity
        self.color_offset = 0
        self.frame = 0

    def draw(self):
        self.matrix.Clear()
        fft = self.audio_input.latest_fft.copy() if self.audio_input else None
        freqs = self.audio_input.freqs if hasattr(self.audio_input, "freqs") else None

        beat = False
        if self.audio_input and self.beat_detector and fft is not None and freqs is not None:
            beat, _, _ = self.beat_detector.detect(fft, freqs)

        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                hue = ((x + y + self.color_offset) % 255) / 255.0
                brightness = 0.5 + 0.5 * math.sin((x + y + self.frame) * 0.1)
                if beat and random.random() > 0.95:
                    brightness = 1.0
                r, g, b = self.hsv_to_rgb(hue, 1.0, brightness)
                self.matrix.SetPixel(x, y, r, g, b)

        if beat:
            self.color_offset += 20
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
