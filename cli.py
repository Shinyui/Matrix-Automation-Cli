import argparse
from utils.device import ADBDeviceManager
from instagram.simulate_home_activity.concurrent_runner import run_all_devices as instagram_simulate_home
from threads.simulate_home_activity.concurrent_runner import run_all_devices as threads_simulate_home

def main():
    parser = argparse.ArgumentParser(
        description="Matrix Automation Cli",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    scan_parser = subparsers.add_parser("device", help="Scan devices")
    scan_parser.add_argument("--mode", type=str, help="Scan mode")
    scan_parser.add_argument("--path", type=str, help="ADB path")
    scan_parser.add_argument("--file", type=str, help="Output file name")

    insta_parser = subparsers.add_parser("instagram", help="Run Instagram simulation")
    insta_parser.add_argument("--mode", type=str, help="Automation mode")
    insta_parser.add_argument("--device", type=str, help="Device list")
    insta_parser.add_argument("--step", type=int, default=100, help="Simulation steps")

    threads = subparsers.add_parser("threads", help="Run Threads simulation")
    threads.add_argument("--mode", type=str, help="Automation mode")
    threads.add_argument("--device", type=str, help="Device list")    
    threads.add_argument("--step", type=int, default=100, help="Simulation steps")

    args = parser.parse_args()

    if args.command == "device":
        if args.mode == "scan":
            print("scanning devices", flush=True)
            device = ADBDeviceManager(args.path)
            device_info = device.get_device_info_list()
            device.export_to_csv(device_info_list=device_info,filename=args.file)
    
    elif args.command == "instagram":
        if args.mode == "home":
            instagram_simulate_home(device_csv_path=args.device, step=args.step)
        elif args.mode == "reels":
            print("simulate instagram reels")

    elif args.command == "threads":
        if args.mode == "home":
            threads_simulate_home(device_csv_path=args.device, step=args.step)
        elif args.mode == "reels":
            print("simulate threads reels")

if __name__ == "__main__":
    main()
