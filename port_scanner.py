import requests
import socket
import os
from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor

# Scan for open ports with clean, minimal output
def scan_ports(host, port_range):
    open_ports = []
    print(f"\n--- Scanning ports on {host} ---")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda port: check_port(host, port), port_range)
        for port, is_open in zip(port_range, results):
            if is_open:
                open_ports.append(port)
                print(f"Port {port} is open")
    return open_ports

# Helper function to check a single port
def check_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            s.connect((host, port))
            return True
    except:
        return False

# Determines the type of request to send based on open ports
def suggest_request_type(open_ports):
    if 80 in open_ports or 443 in open_ports:
        return "HTTP"
    elif 21 in open_ports:
        return "FTP"
    elif open_ports:
        return "TCP"
    else:
        return "Ping"

# HTTP Request function
def http_request(host):
    url = f"http://{host}"
    print(f"\n--- Sending HTTP request to {url} ---")
    try:
        response = requests.get(url, timeout=2)
        print(f"HTTP Response Code: {response.status_code}")
        print("Response Content:", response.text[:100] + "...")
    except Exception as e:
        print(f"HTTP Request failed: {e}")

# TCP Connection function
def tcp_connection(host, port):
    print(f"\n--- Establishing TCP connection to {host}:{port} ---")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"TCP connection to {host}:{port} successful")
            s.sendall(b"Hello!")  # Example message
            data = s.recv(1024)
            print("Received:", data.decode())
    except Exception as e:
        print(f"TCP Connection failed: {e}")

# Ping function
def ping_host(host):
    print(f"\n--- Pinging {host} ---")
    ping_command = "ping -c 1" if os.name != "nt" else "ping -n 1"
    response = os.system(f"{ping_command} {host}")
    if response == 0:
        print(f"{host} is reachable.")
    else:
        print(f"{host} is unreachable.")

# FTP Connection function
def ftp_connect(host):
    print(f"\n--- Attempting FTP connection to {host} ---")
    try:
        with FTP(host, timeout=2) as ftp:
            ftp.login()
            print("FTP connection successful. Available files and directories:")
            ftp.retrlines("LIST")
    except Exception as e:
        print(f"FTP Connection failed: {e}")


