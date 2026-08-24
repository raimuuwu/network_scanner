import argparse
from core.network_info import get_network_info

def main():
    parser = argparse.ArgumentParser(description="Network Scanner CLI Tool")
    parser.add_argument("-i","--info",
                        action="store_true",
                        help="display local network info")

    args = parser.parse_args()

    if args.info:
        info = get_network_info()

        print("---")
        print(f"Interface : {info['interface']}")
        print(f"IP Address: {info['ip']}")
        print(f"Mask      : {info['mask']}")
        print(f"MAC       : {info['mac']}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    