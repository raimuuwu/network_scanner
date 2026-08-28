import socket
import subprocess
import psutil

import platform

def get_active_interface():
    system = platform.system()
    if system == "Linux":
        try:
            cmd = ["ip", "route", "get", "8.8.8.8"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                words = result.stdout.split()
                if "dev" in words:
                    return words[words.index("dev") + 1]
        except Exception:
            pass

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        my_ip = s.getsockname()[0]
        s.close()

        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == my_ip:
                    return iface
    except Exception:
        pass
    return "N/A"

def get_wifi_signal(interface):
    system = platform.system()
    if system == "Windows":
        try:
            cmd = ["netsh", "wlan", "show", "interfaces"]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "Signal" in line or "Sygnał" in line:
                        return line.split(":")[1].strip()
        except Exception:
            pass
        return "N/A"

    else:
        if not interface or not interface.startswith("w"):
            return "Wired (Ethernet)"
        try:
            cmd = ["nmcli", "-t", "-f", "IN-USE,SIGNAL", "dev", "wifi"]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.startswith("*"):
                        return f"{line.split(':')[1]}%"
        except Exception:
            pass
        return "N/A"

def get_latency(target="8.8.8.8"):
    system = platform.system()
    if system == "Windows":
        cmd = ["ping", "-n", "3", "-w", "1000", target]
    else:
        cmd = ["ping", "-c", "3", "-W", "1", target]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "rtt" in line or "round-trip" in line:
                    return f"{line.split('=')[1].strip().split('/')[1]} ms"
                elif "Average" in line or "Średni" in line:
                    avg = line.split("=")[-1].strip().replace("ms", "")
                    return f"{avg} ms"
    except Exception:
        pass
    return "N/A"

def get_network_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()

    interface = get_active_interface()
    netmask = None
    mac_address = None

    if interface in psutil.net_if_addrs():
        for addr in psutil.net_if_addrs()[interface]:
            if addr.family == socket.AF_INET:
                netmask = addr.netmask
            elif addr.family == psutil.AF_LINK:
                mac_address = addr.address

    wifi_signal = get_wifi_signal(interface)
    latency = get_latency()

    return {
        "interface": interface,
        "ip": my_ip,
        "mask": netmask,
        "mac": mac_address,
        "wifi_signal": wifi_signal,
        "latency": latency,
    }