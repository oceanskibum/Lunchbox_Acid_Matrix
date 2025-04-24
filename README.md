
```
 _                      _     ____                           _     _ 
| |                    | |   |  _ \                /\       (_)   | |
| |    _   _ _ __   ___| |__ | |_) | _____  __    /  \   ___ _  __| |
| |   | | | | '_ \ / __| '_ \|  _ < / _ \ \/ /   / /\ \ / __| |/ _` |
| |___| |_| | | | | (__| | | | |_) | (_) >  <   / ____ \ (__| | (_| |
|______\__,_|_| |_|\___|_| |_|____/ \___/_/\_\ /_/    \_\___|_|\__,_|

>>> SYSTEM ONLINE — WELCOME TO LUNCHBOX_ACID_MATRIX 
>>> V1.13   
```

# Lunchbox Acid Matrix

A Raspberry Pi 4-powered LED matrix visualizer built for technologists who require modular visual mayhem in a small form factor that is envirormentally aware. [PLUR.TECH]

---

## Navigation
```
Lunchbox_Acid_Matrix/
├── README_IMU.md                   # IMU + DFROBOT button wiring guide
├── lunchbox_acid_matrix.py         # Main runtime launcher
├── service/
│   └── lunchbox_acid_matrix.service  # systemd startup unit
├── config/
│   ├── button_config.json          # Button mappings and layered combos
│   ├── config.json                 # Core settings (mode, brightness, etc)
│   ├── playlist.json               # Playlist mode configuration
│   └── state.json                  # Runtime persistence for last mode, brightness
├── src/
│   ├── main.py                     # CLI tool (interactive configuration)
│   ├── animations/
│   │   ├── bass_mode.py
│   │   ├── basshouse_mode.py
│   │   ├── dancer_mode.py
│   │   ├── fade_transition.py
│   │   ├── house_mode.py
│   │   ├── idle_mode.py
│   │   └── techno_mode.py
│   ├── audio/
│   │   └── audio_input.py          # USB mic support + beat detection
│   └── input/
│       └── imu_input.py            # Motion via MPU6050 (dancer mode)
```
---

## Project Highlights
- 64x64 LED Matrix (Adafruit RGB Matrix Bonnet)
- USB mic input for **beat detection and sensitivity tuning**
- IMU support for **motion-reactive dance mode**
- Button-based interaction for field operation (no screen needed)
- CLI configuration tool for setup and customization
- Visuals react to genre, playlist, motion, or ambient vibe

---

## Raspberry Pi 5 Warning
This project **will not work on a Pi 5** due to driver incompatibility with hzeller's RGB matrix library.  
Use a **Raspberry Pi 4 (recommended: 4GB or 8GB)**.

---

## Hardware Required
- Raspberry Pi 4
- Adafruit RGB Matrix Bonnet
- 64x64 RGB Matrix panel
- DFROBOT Gravity LED Push Buttons (DFR0785, x2)
- MPU6050 (motion sensor)
- USB Microphone (for audio-reactive visuals)

---

## Features
- Genre-reactive modes: `house`, `bass`, `techno`, `basshouse`
- Audio sensitivity adjustment (button or config)
- Motion-reactive “Dancer Mode”
- Visual “404 - Vibes Not Found” idle animation
- Playlist mode with automatic cycling
- Button-only operation for backpack use
- Fully editable config files
- Stylized CLI interface for setup & testing

---

## Installation
```bash
# SSH into your Pi
sudo apt update && sudo apt install -y git unzip

# Clone the repo
git clone https://github.com/oceanskibum/Lunchbox_Acid_Matrix.git
cd Lunchbox_Acid_Matrix

# Run the installer
bash scripts/install.sh
```

To enable auto-launch:
```bash
bash scripts/install.sh --with-systemd
```

---

## Running the CLI Tool
Use the CLI from terminal to configure:
```bash
python3 src/main.py
```

---

## Running the Matrix Display (Field Mode)
No screen required — just power it:
```bash
python3 lunchbox_acid_matrix.py
```

This pulls config from:
- `config/config.json`
- `config/playlist.json`
- `config/state.json`

Uses buttons to interact live.

---

## Wiring & GPIO
See `README_IMU.md` for detailed wiring instructions for:
- DFROBOT Gravity buttons (3-wire)
- MPU6050 IMU
- Compatible GPIOs with Adafruit Bonnet

---

## Customize
Edit these files:
- `config/config.json` → master settings
- `playlist.json` → cycling mode
- `state.json` → runtime memory
- `button_config.json` → combo logic

---

## License
MIT — Share, remix

---

