import sys
import uiautomator2 as u2
import subprocess
import csv

def get_adb_device_list(adb_path):
    try:
        result = subprocess.check_output([adb_path, "devices"]).decode("utf-8")
        lines = result.strip().splitlines()
        devices = [
            line for line in lines[1:]
            if "device" in line and not line.startswith("*")
        ]
        return devices
    except FileNotFoundError:
        print(f"找不到 adb，可確認路徑是否正確：{adb_path}")
        sys.stdout.flush()
        return []
    except subprocess.CalledProcessError as e:
        print(f"adb 執行錯誤：{e}")
        sys.stdout.flush()
        return []

def get_device_ip(serial, adb_path):
    try:
        result = subprocess.check_output(
            [adb_path, "-s", serial, "shell", "ip", "-f", "inet", "addr", "show", "wlan0"]
        ).decode("utf-8")
        for line in result.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                return line.split()[1].split("/")[0]
        return None
    except subprocess.CalledProcessError:
        return None

def get_device_info_list(adb_path):
    devices = get_adb_device_list(adb_path)
    device_serials = [line.split('\t')[0] for line in devices]

    device_info_list = []
    for serial in device_serials:
        ip = get_device_ip(serial, adb_path)
        device_info_list.append({
            "serial": serial,
            "ip": ip or "N/A"
        })
    return device_info_list

def export_to_csv(device_info_list, filename="scanned_devices.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["serial", "ip"])
        writer.writeheader()
        writer.writerows(device_info_list)
    print(f"裝置資訊已匯出至：{filename}")
    sys.stdout.flush()

def connect_devices_from_csv(file_path: str):
    connected_devices = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            serial_list = [row["serial"].strip() for row in reader if row.get("serial")]
    except FileNotFoundError:
        print(f"找不到檔案：{file_path}")
        sys.stdout.flush()

        return {}
    except KeyError:
        print(f"檔案格式錯誤，請確認包含 'serial' 欄位")
        return {}

    for serial in serial_list:
        try:
            d = u2.connect_usb(serial)
            connected_devices[serial] = d
            product = d.info.get('productName', '未知')
            print(f"已連接 {serial}，裝置資訊：{product}")
        except Exception as e:
            print(f"連接 {serial} 失敗：{e}")

    return connected_devices