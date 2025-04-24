
# Motion Sensor + LED Button Wiring Guide

This guide shows how to wire the MPU6050 IMU and DFROBOT Gravity LED Buttons (SKU: DFR0785) to a **Raspberry Pi 4** with the **Adafruit RGB Matrix Bonnet** installed. [Timeout function TBD]

---

## Overview

- The **Adafruit Bonnet** uses most GPIO pins for the LED matrix, but **GPIO 17 and 27** are available and safe.
- The **MPU6050** connects via **I2C (SDA/SCL)** which is supported natively and safely on Pi 4.
- The **DFROBOT LED buttons** are 3-wire (VCC, GND, SIGNAL). We use internal pull-up on the Pi so no external resistors are needed.

---

## Wiring Summary

### DFROBOT LED Buttons (x2)

| Pin | Use  | Wire Color | Pi GPIO | Pi Pin |
|-----|------|------------|---------|--------|
| 1   | VCC  | Red        | 3.3V    | Pin 1  |
| 2   | GND  | Black      | GND     | Pin 6  |
| 3   | SIG  | Blue/White | GPIO 17 | Pin 11 |
|     |      |            | GPIO 27 | Pin 13 |

Configure in `config/button_config.json` like this:
```json
{
  "next": 17,
  "prev": 27,
  ...
}
```

---

### MPU6050 IMU Sensor (I2C)

| Sensor | Pi GPIO | Pi Pin |
|--------|---------|--------|
| VCC    | 3.3V    | Pin 1  |
| GND    | GND     | Pin 9  |
| SDA    | GPIO 2  | Pin 3  |
| SCL    | GPIO 3  | Pin 5  |

Enable I2C:
```bash
sudo raspi-config
# Interface Options → I2C → Enable
```

Verify sensor is detected:
```bash
sudo i2cdetect -y 1
# You should see a device at address 0x68
```

---

## GPIO Layout (for reference)

```
        Pi 4 (40-pin Header) - Top View
  -----------------------------------------
  3.3V (1) (2) 5V       SDA (3) (4) 5V
  SCL (5) (6) GND      GPIO 4 (7) (8) TXD
   GND (9) (10) RXD   GPIO 17 (11) (12) GPIO 18
GPIO 27 (13) (14) GND GPIO 22 (15) (16) GPIO 23
```

---

## Button Test Snippet
Once booted, try:
```bash
python3 lunchbox_acid_matrix.py
```
Tap buttons to test:
- Tap BOTH → Brightness toggle
- Hold BOTH → Shutdown
- Double-tap BOTH → Sensitivity adjust

---

