import socket
import threading
import ipaddress
import netifaces as ni

discoveredDevices = []

def get_device_name(ip):
    try:
        hostname = socket.gethostbyaddr(ip)
        return hostname[0]
    except socket.herror:
        return ip

def scanPort(ip, port=3000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port)) 
        if result == 0: 
            device_name = get_device_name(ip)
            discoveredDevices.append({'ip': ip, 'name': device_name})
        sock.close()
    except Exception as e:
        print(f"Error scanning {ip}: {e}")

def scanNetwork(network, port=3000):
    network = ipaddress.IPv4Network(network)
    for ip in network.hosts():
        threading.Thread(target=scanPort, args=(str(ip), port)).start()
