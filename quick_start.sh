#!/bin/bash

echo "[*] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "[+] Python $PYTHON_VERSION found"
echo ""

if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv .venv
    echo "[+] Virtual environment created"
else
    echo "[+] Virtual environment already exists"
fi
echo ""

echo "[*] Activating virtual environment..."
source .venv/bin/activate
echo ""

echo "[*] Installing required packages..."
pip install -r requirements.txt
echo "[+] Packages installed"
echo ""

if [ ! -f ".env" ]; then
    echo "[!] .env file not found"
    echo "Get The env key- Please read the README.md"

fi

echo "[*] Testing installation..."
if python3 osint.py --list > /dev/null 2>&1; then
    echo "[+] Installation successful!"
else
    echo "[!] Installation test failed. Check your configuration."
    exit 1
fi

echo "     Setup Complete!    "

echo "Happy hunting!"
