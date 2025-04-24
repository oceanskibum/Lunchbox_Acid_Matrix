
import time
import random
from rgbmatrix import RGBMatrix

class ParticleStream:
    def __init__(self, matrix, spawn_rate=15, fade_speed=0.9, audio_input=None, sensitivity=1.5):
        self.matrix = matrix
        self.particles = []
        self.spawn_rate = spawn_rate
        self.fade_speed = fade_speed
        self.audio_input = audio_input
        self.sensitivity = sensitivity
        self.frame = 0

    def draw(self):
        # Fade existing particles
        new_particles = []
        for p in self.particles:
            x, y, r, g, b = p
            r, g, b = int(r * self.fade_speed), int(g * self.fade_speed), int(b * self.fade_speed)
            if r > 5 or g > 5 or b > 5:
                self.matrix.SetPixel(x, y, r, g, b)
                new_particles.append((x, y, r, g, b))
        self.particles = new_particles

        # Spawn new particles from center
        for _ in range(self.spawn_rate):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(0.5, 2.0)
            dx = int(speed * random.uniform(0.5, 1.5) * math.cos(angle))
            dy = int(speed * random.uniform(0.5, 1.5) * math.sin(angle))
            x = self.matrix.width // 2 + dx
            y = self.matrix.height // 2 + dy
            if 0 <= x < self.matrix.width and 0 <= y < self.matrix.height:

        mod = 1.0
        if self.audio_input:
            bass = self.audio_input.get_bass_energy()
            mod = min(2.0, 1.0 + bass * self.sensitivity / 1000)
                random.randint(128, int(255 * mod))
                self.particles.append((x, y, r, g, b))
                self.matrix.SetPixel(x, y, r, g, b)

        self.frame += 1
        time.sleep(0.03)

# Suggestions:
# - Increase spawn_rate for more density
# - Lower fade_speed (e.g., 0.8) for longer particle trails
