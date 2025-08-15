import socket
import os
from datetime import datetime

# Read server IP from file created by setup_server.sh
try:
    with open("server_ip.txt", "r") as f:
        SERVER_IP = f.read().strip()
except FileNotFoundError:
    SERVER_IP = "0.0.0.0"  # Fallback if file missing

SERVER_PORT = 5000
SAVE_DIR = "received_logs"

os.makedirs(SAVE_DIR, exist_ok=True)

def start_server():
    """Start the TCP server to receive logs."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)

    print(f"[+] Server listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"[+] Connection from {client_addr}")

        try:
            data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk

            if data:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(SAVE_DIR, f"log_{client_addr[0]}_{timestamp}.log")
                with open(filename, "wb") as f:
                    f.write(data)
                print(f"[+] Saved logs to {filename}")

        except Exception as e:
            print(f"[!] Error receiving data: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()
