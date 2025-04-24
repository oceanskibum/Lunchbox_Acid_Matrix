
# IMU Setup for Motion-Reactive LED Display

This guide explains how to connect an MPU6050 or MPU9250 sensor to the Raspberry Pi running Lunchbox_Acid_Viz using I2C (safe with Adafruit RGB Matrix Bonnet).

## Hardware

- MPU6050/9250
- 4 female-female jumper wires
- Raspberry Pi with Adafruit Bonnet

## Wiring

| MPU Pin | Pi GPIO Pin | Label   |
|---------|-------------|---------|
| VCC     | Pin 1       | 3.3V    |
| GND     | Pin 9       | GND     |
| SDA     | Pin 3       | GPIO2 (SDA) |
| SCL     | Pin 5       | GPIO3 (SCL) |

These I2C pins are **safe to use** with the bonnet.

## Software Setup

```bash
sudo apt install -y python3-smbus i2c-tools
sudo raspi-config  # Enable I2C under Interfaces
```

Then reboot the Pi. Test with:
```bash
i2cdetect -y 1  # Should show "68" for MPU6050
```

## Controls

- Hold the PREV button for 2 seconds = Toggle motion mode ON/OFF
- A short flash/scroll will confirm the toggle
- Current state is saved to `state.json`

