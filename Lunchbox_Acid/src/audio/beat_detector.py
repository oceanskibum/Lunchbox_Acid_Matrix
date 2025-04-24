import numpy as np
import time

class BeatDetector:
    def __init__(self, buffer_size=43, bass_range=(60, 130), decay=0.95):
        self.energy_buffer = []
        self.time_buffer = []
        self.buffer_size = buffer_size
        self.bass_range = bass_range
        self.last_beat_time = 0
        self.decay = decay
        self.beat_threshold = 1.5
        self.bpm = 0

    def detect(self, fft, freqs, timestamp=None):
        # Get bass band energy
        bass_mask = (freqs >= self.bass_range[0]) & (freqs <= self.bass_range[1])
        bass_energy = np.mean(fft[bass_mask]) if np.any(bass_mask) else 0.0

        # Update energy buffer
        self.energy_buffer.append(bass_energy)
        if len(self.energy_buffer) > self.buffer_size:
            self.energy_buffer.pop(0)

        avg_energy = np.mean(self.energy_buffer) if self.energy_buffer else 1e-6
        threshold = avg_energy * self.beat_threshold
        timestamp = timestamp or time.time()

        # Beat detected
        if bass_energy > threshold:
            time_since_last = timestamp - self.last_beat_time
            self.last_beat_time = timestamp
            self.time_buffer.append(time_since_last)
            if len(self.time_buffer) > 10:
                self.time_buffer.pop(0)

            if len(self.time_buffer) > 1:
                avg_interval = np.mean(self.time_buffer)
                self.bpm = int(60.0 / avg_interval)

            return True, bass_energy, self.bpm
        return False, bass_energy, self.bpm

    def get_bpm(self):
        return self.bpm
