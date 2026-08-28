import socket
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

import platform

def generate_subnet_ips(ip,mask):
    addresses = ipaddress.ip_network(f"{ip}/{mask}",strict=False)
    ip_list = [str(host) for host in addresses.hosts()]

    return ip_list

def ping_icmp(ip):
    if platform.system() == "Windows":
        cmd = ["ping", "-n", "3", "-w", "1000", ip]
    else:
        cmd = ["ping", "-c", "3", "-W", "1", ip]

    result = subprocess.run(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return ip, (result.returncode == 0)

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, TimeoutError):
        return "Unknown"

def scan_network(ip_list):
    active_hosts = []

    print(f"Scanning {len(ip_list)} addresses...")

    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(ping_icmp, ip) for ip in ip_list]

        for future in as_completed(futures):
            ip, is_alive = future.result()
            if is_alive:
                hostname = get_hostname(ip)
                print(f"[+] Active host: {ip} ({hostname})")

                active_hosts.append({"ip": ip, "hostname": hostname})

    return active_hosts

