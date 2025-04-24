#!/bin/bash

# Lunchbox_Acid_Viz Auto-Installer
# For Raspberry Pi 4 + Adafruit RGB Matrix Bonnet

PROJECT_NAME="Lunchbox_Acid_Viz"
INSTALL_PATH="$HOME/$PROJECT_NAME"
MATRIX_LIB_REPO="https://github.com/hzeller/rpi-rgb-led-matrix"

show_help() {
  echo "
  === $PROJECT_NAME Installer ===

  Installs all dependencies, libraries, and Python packages.
  Clones project repo (if applicable), configures I2C and LED matrix drivers,
  and launches CLI tool when finished.

  Usage:
    bash install.sh [--with-systemd]

  Options:
    --with-systemd   Enable auto-launch via systemd at boot
    --help           Show this help message

  "
  exit 0
}

if [[ "$1" == "--help" ]]; then show_help; fi

echo "[1/7] Updating system packages..."
sudo apt update && sudo apt install -y git python3-pip python3-smbus i2c-tools build-essential python3-dev

echo "[2/7] Installing Python libraries..."
pip3 install --upgrade pip
pip3 install RPi.GPIO sounddevice numpy smbus2

echo "[3/7] Enabling I2C..."
sudo raspi-config nonint do_i2c 0

echo "[4/7] Cloning and building LED matrix library..."
cd ~
if [ ! -d "rpi-rgb-led-matrix" ]; then
  git clone $MATRIX_LIB_REPO
fi
cd rpi-rgb-led-matrix
make build-python
sudo make install

echo "[5/7] Setting up project directory..."
cd ~
if [ ! -d "$INSTALL_PATH" ]; then
  echo "Please manually unzip your project into $INSTALL_PATH"
  echo "Then re-run this installer to finalize setup."
  exit 1
fi

echo "[6/7] Making CLI tool executable..."
chmod +x "$INSTALL_PATH/src/main.py"
chmod +x "$INSTALL_PATH/launch.py"

if [[ "$1" == "--with-systemd" ]]; then
  echo "[7/7] Enabling systemd service..."
  sudo cp "$INSTALL_PATH/service/lunchbox_acid_viz.service" /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable lunchbox_acid_viz
  echo "Systemd auto-launch ENABLED."
else
  echo "[7/7] Skipping systemd setup."
fi

echo "=== INSTALL COMPLETE ==="
cd "$INSTALL_PATH"
echo "Launching CLI..."
python3 src/main.py
