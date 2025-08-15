@echo off
title Client Setup
color 0A

REM ===========================
REM Step 1: Check for Python
REM ===========================
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [*] Python not found. Installing Python 3.12...
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe -OutFile python_installer.exe"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
) ELSE (
    echo [+] Python is already installed.
)

REM ===========================
REM Step 2: Install requirements
REM ===========================
echo [*] Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install pynput psutil requests

REM ===========================
REM Step 3: Check server link
REM ===========================
echo [*] Checking if server is reachable...
python - <<EOF
import requests
try:
    url = "http://YOUR_SERVER_IP:8000/server_ip.txt"
    r = requests.get(url, timeout=5)
    if r.status_code == 200:
        print("[+] Server link OK, fetched IP:", r.text.strip())
    else:
        print("[!] Server responded with status:", r.status_code)
except Exception as e:
    print("[!] Could not reach server:", e)
EOF

REM ===========================
REM Step 4: Run client
REM ===========================
echo [*] Starting client program...
python client.py

pause
