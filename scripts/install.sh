#!/bin/bash

PROJECT_NAME="Lunchbox_Acid_Matrix"
INSTALL_PATH="$HOME/$PROJECT_NAME"
VENV_PATH="$HOME/lunchbox_env"
MATRIX_LIB_REPO="https://github.com/hzeller/rpi-rgb-led-matrix"

show_help() {
  echo "
  === $PROJECT_NAME Installer ===

  Sets up all dependencies, Python venv, matrix drivers, and the project CLI.

  Usage:
    bash scripts/install.sh [--with-systemd]

  Options:
    --with-systemd   Enable auto-launch via systemd at boot
    --help           Show this help message
  "
  exit 0
}

if [[ "$1" == "--help" ]]; then show_help; fi

echo "[1/7] Updating system packages..."
sudo apt update && sudo apt install -y git python3-pip python3-venv python3-smbus i2c-tools build-essential

echo "[2/7] Creating and activating Python venv..."
python3 -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

echo "[3/7] Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install Pillow sounddevice numpy RPi.GPIO smbus2

echo "[4/7] Enabling I2C..."
sudo raspi-config nonint do_i2c 0

echo "[5/7] Installing rpi-rgb-led-matrix..."
cd ~
if [ ! -d "rpi-rgb-led-matrix" ]; then
  git clone $MATRIX_LIB_REPO
else
  cd rpi-rgb-led-matrix && git pull
fi
cd ~/rpi-rgb-led-matrix
make clean
make build-python
make install-python

echo "[6/7] Setting up project directory..."
if [ ! -d "$INSTALL_PATH" ]; then
  echo "Please unzip your project into $INSTALL_PATH"
  echo "Then re-run this installer to finalize setup."
  exit 1
fi
chmod +x "$INSTALL_PATH/src/main.py"
[ -f "$INSTALL_PATH/lunchbox_acid_matrix.py" ] && chmod +x "$INSTALL_PATH/lunchbox_acid_matrix.py"

if [[ "$1" == "--with-systemd" ]]; then
  echo "Enabling systemd..."
  sudo cp "$INSTALL_PATH/service/lunchbox_acid_matrix.service" /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable lunchbox_acid_matrix
  echo "Systemd service enabled."
fi

echo "=== INSTALL COMPLETE ==="
cd "$INSTALL_PATH"
echo "Launching CLI..."
python3 src/main.py
