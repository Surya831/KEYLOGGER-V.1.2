#!/bin/bash

echo -e "\e[32m[+] Server Setup for Kali Linux\e[0m"
echo "-------------------------------------"

# ===========================
# Step 1: Get local IP
# ===========================
IP=$(hostname -I | awk '{print $1}')
echo "[+] Server IP Address: $IP"
echo "[+] Give this IP to your client so they can connect."

# Save IP for server.py and client use
echo "$IP" > server_ip.txt

# ===========================
# Step 2: Check for Python
# ===========================
if ! command -v python3 &>/dev/null; then
    echo "[*] Python not found. Installing Python 3..."
    sudo apt update && sudo apt install -y python3 python3-pip
else
    echo "[+] Python is already installed."
fi

# ===========================
# Step 3: Install requirements
# ===========================
echo "[*] Installing required Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install psutil

# ===========================
# Step 4: Start server (TCP) in background
# ===========================
echo "[*] Starting TCP log server..."
nohup python3 server.py > server.log 2>&1 &

# ===========================
# Step 5: Start HTTP server to share IP
# ===========================
echo "[*] Starting HTTP server on port 8000 to share IP..."
nohup python3 -m http.server 8000 > http_server.log 2>&1 &

echo "[+] HTTP server running. Clients can get IP from: http://$IP:8000/server_ip.txt"
