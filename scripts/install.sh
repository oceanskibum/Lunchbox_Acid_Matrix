#!/bin/bash

set -euo pipefail
trap 'echo "Error occurred on line $LINENO. Exiting." && exit 1' ERR

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

if [[ "${1:-}" == "--help" ]]; then show_help; fi

# Version Checks
echo "Checking system versions..."

PYTHON_VERSION=$(python3 -V 2>&1)
PIP_VERSION=$(pip3 -V 2>&1)
OS_VERSION=$(lsb_release -ds || cat /etc/os-release | grep PRETTY_NAME)

echo "Python Version: $PYTHON_VERSION"
echo "Pip Version: $PIP_VERSION"
echo "OS: $OS_VERSION"

# Step 1: System Packages
echo "[1/8] Installing system packages..."
sudo apt update && sudo apt install -y \
  git python3-pip python3-venv python3-smbus \
  i2c-tools build-essential lsb-release

# Step 2: Python Virtual Environment
echo "[2/8] Creating and activating virtual environment..."
python3 -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

# Step 3: Python Dependencies
echo "[3/8] Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install Pillow sounddevice numpy RPi.GPIO smbus2

# Step 4: Enable I2C
echo "[4/8] Enabling I2C on Pi..."
sudo raspi-config nonint do_i2c 0 || true

# Step 5: rpi-rgb-led-matrix Install
echo "[5/8] Installing or updating rpi-rgb-led-matrix..."
cd ~

if [ ! -d "rpi-rgb-led-matrix" ]; then
  echo "Cloning rpi-rgb-led-matrix..."
  git clone $MATRIX_LIB_REPO
else
  echo "Checking existing rpi-rgb-led-matrix repo..."
  if [ -d "rpi-rgb-led-matrix/.git" ]; then
    cd rpi-rgb-led-matrix
    git reset --hard HEAD
    git pull
  else
    echo "Warning: Existing rpi-rgb-led-matrix is not a valid git repo. Re-cloning..."
    echo "Removing old rpi-rgb-led-matrix directory (requires sudo)..."
    sudo rm -rf rpi-rgb-led-matrix
    git clone $MATRIX_LIB_REPO
  fi
fi

cd ~/rpi-rgb-led-matrix
make clean
make build-python
make install-python

# Step 6: Validate Project Folder
echo "[6/8] Validating project folder..."
if [ ! -d "$INSTALL_PATH" ]; then
  echo "Project folder not found at $INSTALL_PATH"
  echo "Please unzip the project into: $INSTALL_PATH"
  exit 1
fi

chmod +x "$INSTALL_PATH/src/main.py" || true
[ -f "$INSTALL_PATH/lunchbox_acid_matrix.py" ] && chmod +x "$INSTALL_PATH/lunchbox_acid_matrix.py"

# Step 7: Optional systemd Setup
if [[ "${1:-}" == "--with-systemd" ]]; then
  echo "[7/8] Configuring systemd auto-start..."
  sudo cp "$INSTALL_PATH/service/lunchbox_acid_matrix.service" /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable lunchbox_acid_matrix
  echo "Systemd service enabled."
else
  echo "[7/8] Skipping systemd setup (run with --with-systemd to enable)."
fi

# Step 8: Done
echo "[8/8] Install complete."
cd "$INSTALL_PATH"
echo "Launching CLI..."
python3 src/main.py
