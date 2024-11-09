import requests
import socket
import os
from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

# Scan for open ports with clean, minimal output
def scan_ports(host, port_range):
    open_ports = []
    print(colored(f"\n--- Scanning ports on {host} ---", "blue"))
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda port: check_port(host, port), port_range)
        for port, is_open in zip(port_range, results):
            if is_open:
                open_ports.append(port)
                print(colored(f"Port {port} is open", "blue"))
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
    print(colored(f"\n--- Sending HTTP request to {url} ---", "blue"))
    try:
        response = requests.get(url, timeout=2)
        print(colored(f"HTTP Response Code: {response.status_code}","blue"))
        print("Response Content:", response.text[:100] + "...")
    except Exception as e:
        print(colored(f"HTTP Request failed: {e}", "red"))

# TCP Connection function
def tcp_connection(host, port):
    print(colored(f"\n--- Establishing TCP connection to {host}:{port} ---", "blue"))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"TCP connection to {host}:{port} successful")
            s.sendall(b"Hello!")  # Example message
            data = s.recv(1024)
            print("Received:", data.decode())
    except Exception as e:
        print(colored(f"TCP Connection failed: {e}", "red"))

# Ping function
def ping_host(host):
    print(colored(f"\n--- Pinging {host} ---", "blue"))
    ping_command = "ping -c 1" if os.name != "nt" else "ping -n 1"
    response = os.system(f"{ping_command} {host}")
    if response == 0:
        print(colored(f"{host} is reachable.", "green"))
    else:
        print(colored(f"{host} is unreachable.", "red"))

# FTP Connection function
def ftp_connect(host):
    print(colored(f"\n--- Attempting FTP connection to {host} ---", "blue"))
    try:
        with FTP(host, timeout=2) as ftp:
            ftp.login()
            print(colored("FTP connection successful. Available files and directories:", "green"))
            ftp.retrlines("LIST")
    except Exception as e:
        print(colored(f"FTP Connection failed: {e}", "red"))


