import time, random
class BassMode:
    def __init__(self, matrix, audio_input=None, beat_detector=None, sensitivity=1.5):
        self.matrix = matrix
        self.audio_input = audio_input
        self.beat_detector = beat_detector
        self.sensitivity = sensitivity
        self.frame = 0
        self.flash = False

    def draw(self):
        fft = self.audio_input.latest_fft.copy() if self.audio_input else None
        freqs = self.audio_input.freqs if hasattr(self.audio_input, "freqs") else None

        beat = False
        if self.audio_input and self.beat_detector and fft is not None and freqs is not None:
            beat, _, _ = self.beat_detector.detect(fft, freqs)

        if beat:
            self.flash = True
            self.color = [random.randint(200, 255), random.randint(0, 100), random.randint(0, 255)]

        if self.flash:
            for x in range(self.matrix.width):
                for y in range(self.matrix.height):
                    self.matrix.SetPixel(x, y, *self.color)
            self.flash = False
        else:
            self.matrix.Clear()

        time.sleep(0.05)
