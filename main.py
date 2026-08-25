import argparse
from core.network_info import get_network_info
from core.discovery import scan_network, generate_subnet_ips

def main():
    parser = argparse.ArgumentParser(description="Network Scanner CLI Tool")
    parser.add_argument("-i","--info",
                        action="store_true",
                        help="display local network info")

    parser.add_argument("-s", "--scan",
                        action="store_true",
                        help="scan local network for active devices")

    args = parser.parse_args()

    if args.info:
        info = get_network_info()

        print("---")
        print(f"Interface : {info['interface']}")
        print(f"IP Address: {info['ip']}")
        print(f"Mask      : {info['mask']}")
        print(f"MAC       : {info['mac']}")

    elif args.scan:
        print("Scanning local network...")
        info = get_network_info()
        hosts_to_scan = generate_subnet_ips(info["ip"], info["mask"])

        active_hosts = scan_network(hosts_to_scan)

        print("ACTIVE HOSTS:")
        for host in active_hosts:
            print(f" -> {host}")
        print(f"Detected: {len(active_hosts)} active hosts.\n")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    