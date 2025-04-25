#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

PROJECT_NAME="Lunchbox_Acid_Matrix"
INSTALL_PATH="$HOME/$PROJECT_NAME"
VENV_PATH="$HOME/lunchbox_env"
MATRIX_REPO="https://github.com/hzeller/rpi-rgb-led-matrix"
MATRIX_DIR="$HOME/rpi-rgb-led-matrix"
LOGFILE="/tmp/${PROJECT_NAME}_install.log"

exec > >(tee "$LOGFILE") 2>&1

echo "[DEBUG] Starting installation at $(date)"
echo "[DEBUG] Logging to $LOGFILE"

trap 'echo "[ERROR] An error occurred at line $LINENO. See $LOGFILE for details."' ERR

show_help() {
  echo "\n=== $PROJECT_NAME Installer ===\n"
  echo "This script sets up all dependencies, compiles matrix drivers, and installs the CLI."
  echo "\nUsage: bash install.sh [--with-systemd]"
  echo "\nOptions:\n  --with-systemd     Enable auto-launch at boot via systemd\n  --help             Show this help message\n"
  exit 0
}

[[ "${1:-}" == "--help" ]] && show_help

echo "[1/8] Checking system versions..."
echo "→ Python Version: $(python3 --version)"
echo "→ Pip Version: $(pip3 --version)"
echo "→ OS: $(lsb_release -ds || cat /etc/os-release)"

echo "[2/8] Installing system packages..."
sudo apt update
sudo apt install -y git python3-pip python3-venv python3-smbus i2c-tools build-essential lsb-release cython3

echo "[3/8] Creating and activating virtual environment..."
python3 -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

echo "[4/8] Installing Python packages into venv..."
pip install --upgrade pip setuptools wheel
pip install Pillow sounddevice numpy RPi.GPIO smbus2

echo "[5/8] Enabling I2C on Raspberry Pi..."
sudo raspi-config nonint do_i2c 0

echo "[6/8] Installing or updating rpi-rgb-led-matrix..."
if [[ ! -d "$MATRIX_DIR/.git" ]]; then
  echo "[DEBUG] Cloning fresh copy of rpi-rgb-led-matrix..."
  sudo rm -rf "$MATRIX_DIR"
  git clone "$MATRIX_REPO" "$MATRIX_DIR"\else
  echo "[DEBUG] Updating existing rpi-rgb-led-matrix repo..."
  cd "$MATRIX_DIR"
  git reset --hard HEAD
  git pull
fi

cd "$MATRIX_DIR"
echo "[DEBUG] Cleaning and rebuilding rpi-rgb-led-matrix..."
make clean || true
make build-python
sudo make install-python || {
  echo "[WARNING] Install failed due to permission error. Attempting manual cleanup..."
  sudo rm -rf "$VENV_PATH/lib/python3.11/site-packages/rgbmatrix-*.egg"
  sudo make install-python
}

cd ~
echo "[7/8] Verifying project directory..."
if [[ ! -d "$INSTALL_PATH" ]]; then
  echo "[ERROR] Project directory $INSTALL_PATH not found. Please unzip your project and retry."
  exit 1
fi

chmod +x "$INSTALL_PATH/src/main.py"
chmod +x "$INSTALL_PATH/lunchbox_acid_matrix.py"

if [[ "${1:-}" == "--with-systemd" ]]; then
  echo "[8/8] Setting up systemd service..."
  sudo cp "$INSTALL_PATH/service/lunchbox_acid_matrix.service" /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable lunchbox_acid_matrix
  echo "[INFO] Systemd service enabled."
fi

echo "[INFO] Installation complete at $(date)"
echo "[INFO] Log saved to $LOGFILE"
echo "[INFO] Launching CLI..."
cd "$INSTALL_PATH"
python3 src/main.py
