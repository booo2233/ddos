from port_scanner import *
# Main function to scan all ports and perform the best-suited request
def main():
    host = input("Enter the IP address or hostname to scan: ")
    port_range = range(1, 1024)  # Common port range
    open_ports = scan_ports(host, port_range)

    if not open_ports:
        print("\nNo open ports detected; attempting to ping the host.")
        ping_host(host)
        return

    request_type = suggest_request_type(open_ports)
    print(f"\nSuggested request type based on open ports: {request_type}")

    # Send the appropriate request based on detected open ports
    if request_type == "HTTP":
        http_request(host)
    elif request_type == "FTP":
        ftp_connect(host)
    elif request_type == "TCP":
        tcp_connection(host, open_ports[0])  # Use the first available open port
    else:
        ping_host(host)

if __name__ == "__main__":
    
     main()