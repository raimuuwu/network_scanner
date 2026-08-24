import socket
import psutil

def get_network_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()

    target_interface = None
    netmask = None
    mac_address = None

    for interface, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET and addr.address == my_ip:
                target_interface = interface
                netmask = addr.netmask
                break

    if target_interface:
        for addr in psutil.net_if_addrs()[target_interface]:
            if addr.family == psutil.AF_LINK:
                mac_address = addr.address
                break
    
    return{
        "interface": target_interface,
        "ip": my_ip,
        "mask": netmask,
        "mac": mac_address
    }