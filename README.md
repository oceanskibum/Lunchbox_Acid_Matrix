
```
 _                      _     ____                           _     _ 
| |                    | |   |  _ \                /\       (_)   | |
| |    _   _ _ __   ___| |__ | |_) | _____  __    /  \   ___ _  __| |
| |   | | | | '_ \ / __| '_ \|  _ < / _ \ \/ /   / /\ \ / __| |/ _` |
| |___| |_| | | | | (__| | | | |_) | (_) >  <   / ____ \ (__| | (_| |
|______\__,_|_| |_|\___|_| |_|____/ \___/_/\_\ /_/    \_\___|_|\__,_|

>>> SYSTEM ONLINE — WELCOME TO LUNCHBOX_ACID_MATRIX V1.12                  
```

> **Modular LED Matrix Visualizer** built for Raspberry Pi 4 with the Adafruit RGB Matrix Bonnet.  
> Features real-time audio-reactive visuals, motion controls, and genre-driven animation modes.

---

## 🚫 Compatibility Warning

> This project **will not work on Raspberry Pi 5**.  
> The `rpi-rgb-led-matrix` library by hzeller is not currently compatible with Pi 5 hardware due to DMA/interrupt architecture changes.  
> Please use a **Raspberry Pi 4** for stable operation.

---

## 🔥 Features

- Genre-reactive modes: `House`, `Bass`, `Techno`, `BassHouse`
- USB microphone support with beat/BPM detection
- IMU motion-reactive control (`Jump`, `Bounce`, `Walk`)
- Configurable buttons with layered combo logic
- Idle playlist auto-cycling visuals
- CLI tool and full install script
- Fade transitions between modes

---

## 🧪 Setup

```bash
sudo apt update && sudo apt install -y \
  python3-pip python3-smbus python3-venv i2c-tools build-essential git
```

Enable I2C:
```bash
sudo raspi-config  # Interface Options → I2C → Enable
```

---

## 🧰 Install (One Liner)

```bash
curl -sSL https://raw.githubusercontent.com/oceanskibum/Lunchbox_Acid_Matrix/main/scripts/install.sh | bash
```

For systemd auto-start:
```bash
curl -sSL https://raw.githubusercontent.com/oceanskibum/Lunchbox_Acid_Matrix/main/scripts/install.sh | bash -s -- --with-systemd
```

---

## 🧠 Folder Structure

```
Lunchbox_Acid_Matrix/
├── config/
│   └── button_config.json
├── src/
│   ├── animations/
│   ├── audio/
│   ├── input/
│   ├── utils/
│   │   └── button_handler.py
├── scripts/
│   └── install.sh
├── lunchbox_acid_matrix.py
├── README.md
├── LICENSE
```

---

## 🎛️ Button System

```json
// config/button_config.json
{
  "next": 17,
  "prev": 27,
  "modes": {
    "brightness_toggle": { "combo": ["next", "prev"], "type": "tap" },
    "shutdown":         { "combo": ["next", "prev"], "type": "hold", "duration": 2 },
    "sensitivity_menu": { "combo": ["next", "prev"], "type": "double_tap", "within": 1.5 }
  },
  "menu_actions": {
    "sensitivity_adjust": {
      "mode": "sensitivity_menu",
      "increase": "next",
      "decrease": "prev",
      "timeout": 5
    }
  }
}
```

---

## 📜 License

MIT — Remix and flash responsibly.

