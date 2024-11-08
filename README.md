# ddos
import requests
import socket
import os
from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor

def scan_ports(host, port_range):
    open_ports = []
    print(f"\nScanning ports on {host}...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda port: check_port(host, port), port_range)
        for port, is_open in zip(port_range, results):
            if is_open:
                open_ports.append(port)
                print(f"Port {port} is open.")
    return open_ports

def check_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            s.connect((host, port))
            return True
    except:
        return False

def suggest_request_type(open_ports):
    if 80 in open_ports or 443 in open_ports:
        return "HTTP"
    elif 21 in open_ports:
        return "FTP"
    elif open_ports:
        return "TCP"
    else:
        return "Ping"

def http_request(host):
    url = f"http://{host}"
    print(f"\nTrying HTTP request to {url}...")
    try:
        response = requests.get(url, timeout=2)
        print(f"HTTP Response: {response.status_code}")
        print("Preview:", response.text[:100] + "...")
    except Exception as e:
        print(f"HTTP request failed: {e}")

def tcp_connection(host, port):
    print(f"\nAttempting TCP connection to {host}:{port}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"TCP connection to {host}:{port} was successful.")
            s.sendall(b"Hello!")
            data = s.recv(1024)
            print("Received:", data.decode())
    except Exception as e:
        print(f"TCP connection failed: {e}")

def ping_host(host):
    print(f"\nPinging {host}...")
    ping_command = "ping -c 1" if os.name != "nt" else "ping -n 1"
    response = os.system(f"{ping_command} {host}")
    if response == 0:
        print(f"{host} is reachable.")
    else:
        print(f"{host} is unreachable.")

def ftp_connect(host):
    print(f"\nAttempting FTP connection to {host}...")
    try:
        with FTP(host, timeout=2) as ftp:
            ftp.login()
            print("FTP connection successful. Here are some files and directories:")
            ftp.retrlines("LIST")
    except Exception as e:
        print(f"FTP connection failed: {e}")

def main():
    host = input("Please enter the IP address or hostname you want to scan: ")
    port_range = range(1, 1024)
    open_ports = scan_ports(host, port_range)

    if not open_ports:
        print("\nNo open ports were found. Trying to ping the host...")
        ping_host(host)
        return

    request_type = suggest_request_type(open_ports)
    print(f"\nBased on open ports, the best type of request to send is: {request_type}")

    if request_type == "HTTP":
        http_request(host)
    elif request_type == "FTP":
        ftp_connect(host)
    elif request_type == "TCP":
        tcp_connection(host, open_ports[0])
    else:
        ping_host(host)

main()
