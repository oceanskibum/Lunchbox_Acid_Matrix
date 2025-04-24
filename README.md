
```
  _                  _               _               _    _           _             
 | |                | |             | |             | |  (_)         | |            
 | |     ___   ___  | | _____  _   _| |__   ___ _ __| | ___  ___  ___| |_ ___  _ __ 
 | |    / _ \ / _ \ | |/ / _ \| | | | '_ \ / _ \ '__| |/ / |/ _ \/ __| __/ _ \| '__|
 | |___| (_) | (_) ||   < (_) | |_| | |_) |  __/ |  |   <| |  __/\__ \ || (_) | |   
 |______\___/ \___(_)_|\_\___/ \__,_|_.__/ \___|_|  |_|\_\_|\___||___/\__\___/|_|   
                                                                                   
                    >>> SYSTEM ONLINE — WELCOME TO LUNCHBOX_ACID_VIZ
```

> **Modular LED Matrix Visualizer** for Raspberry Pi + Adafruit RGB Bonnet  
> Visuals that can be audio-reactive , motion-reactive, and mildly mind-reactive. Button mapped for easy mobile management. 

---

## `> BOOT INFO`

```plaintext
SYSTEM: Raspberry Pi 4 (8GB recommended)
DISPLAY: Adafruit 64x64 RGB Matrix + Bonnet
AUDIO: USB Mic (FFT-powered bass detection)
MOTION: MPU6050 IMU (via I2C)
```

---

## `> FEATURES`

```
[+] Audio-reactive visualizations (bass, BPM, beat)
[+] Genre-based modes: HOUSE, BASS, TECHNO, BASSHOUSE
[+] IMU-powered motion mode (walk, bounce, jump)
[+] Button controls: brightness, mode, shutdown, toggle features
[+] Playlist system for idle ambient visuals
[+] Auto-switch visuals based on detected BPM
[+] Fade transitions between modes
```

---

## `> One-Liner Install`

Run this on your Pi to set up Lunchbox_Acid_Matrix instantly:

```bash
curl -sSL https://raw.githubusercontent.com/oceanskibum/Lunchbox_Acid_Matrix/main/scripts/install.sh | bash
```
#Enable auto-start on boot with systemd:

```bash
curl -sSL https://raw.githubusercontent.com/oceanskibum/Lunchbox_Acid_Matrix/main/scripts/install.sh | bash -s -- --with-systemd
```

---

## `> SETUP`

```bash
sudo apt update && sudo apt install -y python3-pip python3-smbus i2c-tools build-essential git
pip3 install sounddevice numpy RPi.GPIO
```

Enable I2C:
```bash
sudo raspi-config  # Interface Options > I2C > Enable
```

---

## `> RUN`

```bash
python3 launch.py
```

Autostart with systemd:
```bash
sudo cp service/lunchbox_acid_viz.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lunchbox_acid_viz
sudo systemctl start lunchbox_acid_viz
```

---

## `> FILE STRUCTURE`

```
Lunchbox_Acid_Viz/
├── config/          # Visual settings, playlist, state
├── src/
│   ├── animations/  # Visual effects
│   ├── audio/       # USB mic & beat detection
│   ├── input/       # IMU sensor logic
│   ├── utils/       # Transitions and helpers
├── launch.py        # Main runner
├── README.md
├── README_IMU.md    # Motion mode setup
├── LICENSE          # MIT
├── CONTRIBUTING.md  # Pull request info
```

---

## `> CONFIGURE`

```json
// config/config.json
{
  "visualization": "house_mode",
  "audio_reactive": true,
  "audio_sensitivity": 1.5,
  "idle_message": "404 - Vibes Not Found"
}
```

```json
// config/playlist.json
{
  "default": ["house_mode", "bass_mode", "techno_mode"],
  "interval_sec": 90
}
```

---

## `> HACKABLE CONTROLS`

| Action                     | Control                          |
|----------------------------|----------------------------------|
| Switch visual              | NEXT button                      |
| Previous visual            | PREV button                      |
| Change brightness          | Tap both buttons                 |
| Toggle motion mode         | Hold PREV for 2s                 |
| Sensitivity toggle         | Double-tap both buttons quickly  |
| Safe shutdown              | Hold BOTH for 2s                 |

---

## `> LICENSE`

```plaintext
MIT License — remix, remap, re-drop.
```
