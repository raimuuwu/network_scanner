import socket
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_subnet_ips(ip,mask):
    addresses = ipaddress.ip_network(f"{ip}/{mask}",strict=False)
    ip_list = [str(host) for host in addresses.hosts()]

    return ip_list

# currently unused
def ping_host(ip):
    ports_to_check = [80, 443, 22, 445, 5353, 8080, 62078]
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(0.3)
        result = s.connect_ex((ip,port))
        s.close()
        if result == 0:
            return True
    return False

def ping_icmp(ip):
    cmd = ["ping", "-c", "3", "-W", "1", ip]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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

