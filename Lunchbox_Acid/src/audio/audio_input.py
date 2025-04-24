import numpy as np
import sounddevice as sd
import threading

class AudioInput:
    def __init__(self, samplerate=44100, blocksize=1024, channels=1, bass_range=(20, 150)):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.bass_range = bass_range
        self.stream = None
        self.latest_fft = np.zeros(blocksize // 2)
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        if self.running:
            return
        self.running = True
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            channels=self.channels,
            dtype='float32',
            callback=self.audio_callback
        )
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.running = False

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print("Audio input status:", status)
        data = indata[:, 0]
        fft = np.abs(np.fft.rfft(data))
        with self.lock:
            self.latest_fft = fft

    def get_bass_energy(self):
        with self.lock:
            fft = self.latest_fft.copy()
        freqs = np.fft.rfftfreq(self.blocksize, d=1.0 / self.samplerate)
        bass_mask = (freqs >= self.bass_range[0]) & (freqs <= self.bass_range[1])
        return np.mean(fft[bass_mask]) if np.any(bass_mask) else 0.0
