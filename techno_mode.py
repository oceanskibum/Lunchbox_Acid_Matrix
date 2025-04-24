import time, math
class TechnoMode:
    def __init__(self, matrix, audio_input=None, beat_detector=None, sensitivity=1.5):
        self.matrix = matrix
        self.audio_input = audio_input
        self.beat_detector = beat_detector
        self.sensitivity = sensitivity
        self.frame = 0
        self.rotation = 0

    def draw(self):
        self.matrix.Clear()
        fft = self.audio_input.latest_fft.copy() if self.audio_input else None
        freqs = self.audio_input.freqs if hasattr(self.audio_input, "freqs") else None

        beat = False
        if self.audio_input and self.beat_detector and fft is not None and freqs is not None:
            beat, _, _ = self.beat_detector.detect(fft, freqs)

        if beat:
            self.rotation += 1

        center_x = self.matrix.width // 2
        center_y = self.matrix.height // 2
        for i in range(8):
            angle = self.rotation * 0.3 + i * (math.pi / 4)
            for r in range(5, 30, 2):
                x = int(center_x + math.cos(angle) * r)
                y = int(center_y + math.sin(angle) * r)
                if 0 <= x < self.matrix.width and 0 <= y < self.matrix.height:
                    color = (255, 255, 255) if i % 2 == 0 else (0, 255, 100)
                    self.matrix.SetPixel(x, y, *color)

        time.sleep(0.03)
