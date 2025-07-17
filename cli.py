import sys
import argparse
from simulate_home.devices import get_device_info_list, export_to_csv
from simulate_home.runner import run_all_devices

def main():
    parser = argparse.ArgumentParser(
        description="📱 Instagram 自動化控制工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="可用指令")

    scan_parser = subparsers.add_parser("scan", help="🔍 掃描目前已連接的 ADB 裝置並匯出 CSV")
    scan_parser.add_argument("--path", type=str, help="ADB path")
    scan_parser.add_argument("--output", type=str, default="scanned_devices.csv", help="輸出檔案名稱")

    simulate_parser = subparsers.add_parser("simhome", help="🤖 開始模擬所有 devices.csv 裡的裝置操作")
    simulate_parser.add_argument("--device", type=str, default="devices.csv", help="欲載入的裝置清單 CSV")
    scan_parser.add_argument("--step", type=int, default=100, help="執行步驟")


    args = parser.parse_args()

    if args.command == "scan":
        print("🔍 正在掃描裝置...")
        sys.stdout.flush()
        device_info = get_device_info_list(adb_path=args.path)
        export_to_csv(device_info, filename=args.output)
    elif args.command == "simulate":
        print("🤖 開始模擬操作...")
        sys.stdout.flush()

        run_all_devices(device_csv_path=args.csv)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
