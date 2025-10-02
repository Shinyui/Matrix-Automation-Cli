import subprocess
import csv
import uiautomator2 as u2
import os
from typing import Optional, List, Dict

class ADBDeviceManager:
    """
    A utility class for managing Android devices connected via ADB.
    """

    def __init__(self, adb_path: str):
        """
        Initialize the device manager with a given ADB binary path.

        :param adb_path: Path to the adb executable.
        """
        self.adb_path = adb_path

    def _get_adb_device_list(self) -> List[str]:
        """
        Retrieve a list of connected ADB devices.

        :return: A list of device serial lines.
        :raises FileNotFoundError: If the ADB binary is not found.
        :raises subprocess.CalledProcessError: If the ADB command fails.
        """
        try:
            result = subprocess.check_output(
                [self.adb_path, "devices"], text=True
            )
            lines = result.strip().splitlines()
            devices = [
                line for line in lines[1:]
                if "device" in line and not line.startswith("*")
            ]
            return devices
        except FileNotFoundError:
            print(f"ADB not found at: {self.adb_path}", flush=True)
            raise
        except subprocess.CalledProcessError as e:
            print(f"ADB command failed: {e}", flush=True)
            raise

    def _get_device_ip(self, serial: str) -> Optional[str]:
        """
        Retrieve the IP address of a device by serial number.

        :param serial: The serial number of the device.
        :return: The IP address as a string, or None if not found.
        """
        try:
            result = subprocess.check_output(
                [self.adb_path, "-s", serial, "shell", "ip", "-f", "inet", "addr", "show", "wlan0"],
                text=True
            )
            for line in result.splitlines():
                line = line.strip()
                if line.startswith("inet "):
                    return line.split()[1].split("/")[0]
            return None
        except subprocess.CalledProcessError:
            return None

    def get_device_info_list(self) -> List[Dict[str, str]]:
        """
        Get a list of connected devices with their serial numbers and IP addresses.

        :return: A list of dictionaries with 'serial' and 'ip' keys.
        """
        devices = self._get_adb_device_list()
        serials = [line.split('\t')[0] for line in devices]

        info_list = []
        for serial in serials:
            ip = self._get_device_ip(serial)
            info_list.append({
                "serial": serial,
                "ip": ip or "N/A"
            })

        return info_list

    def export_to_csv(self, filename: str = "scanned_devices.csv") -> None:
        """
        Export the device information to a CSV file.

        :param device_info_list: A list of device info dictionaries.
        :param filename: The name of the output CSV file.
        """

        device_info_list = self.get_device_info_list()

        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["serial", "ip"])
            writer.writeheader()
            writer.writerows(device_info_list)
        print(f"Device info exported to: {filename}", flush=True)

    def create_device_folders(self, root_path: str) -> None:
        """
        Create a root folder and subfolders for each device based on their IP addresses.

        :param root_path: The root directory path where device folders will be created.
        """
        # 1. 掃描所有連接的裝置
        device_info_list = self.get_device_info_list()
        
        if not device_info_list:
            print("沒有找到連接的 ADB 裝置", flush=True)
            return
        
        print(f"\n找到 {len(device_info_list)} 個裝置:", flush=True)
        for info in device_info_list:
            print(f"  - Serial: {info['serial']}, IP: {info['ip']}", flush=True)
        
        # 3. 創建 root 資料夾
        if not os.path.exists(root_path):
            os.makedirs(root_path)
            print(f"\n已創建 root 資料夾: {root_path}", flush=True)
        else:
            print(f"\nroot 資料夾已存在: {root_path}", flush=True)
        
        # 4. 為每個裝置創建以 IP 命名的資料夾
        print("\n開始為每個裝置創建資料夾:", flush=True)
        for info in device_info_list:
            ip = info['ip']
            serial = info['serial']
            
            # 處理 N/A 的情況，使用 serial 作為資料夾名稱
            folder_name = ip if ip != "N/A" else f"unknown_{serial}"
            device_folder = os.path.join(root_path, folder_name)
            
            if not os.path.exists(device_folder):
                os.makedirs(device_folder)
                print(f"  ✓ 已創建資料夾: {device_folder}", flush=True)
            else:
                print(f"  - 資料夾已存在: {device_folder}", flush=True)
        
        print("\n完成！", flush=True)

def connect_devices_from_csv(file_path: str) -> Dict[str, u2.Device]:
    """
    Connect to devices listed in a CSV file using their serial numbers.

    :param file_path: Path to the CSV file containing device serial numbers.
    :return: A dictionary mapping serial numbers to connected uiautomator2.Device objects.
    """
    connected: Dict[str, u2.Device] = {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            serials = [row["serial"].strip() for row in reader if row.get("serial")]
    except FileNotFoundError:
        print(f"File not found: {file_path}", flush=True)
        return {}
    except KeyError:
        print(f"Invalid file format. Missing 'serial' column.", flush=True)
        return {}

    for serial in serials:
        try:
            d = u2.connect_usb(serial)
            connected[serial] = d
            product = d.info.get("productName", "Unknown")
            print(f"Connected to {serial}, Product: {product}", flush=True)
        except Exception as e:
            print(f"Failed to connect to {serial}: {e}", flush=True)

    return connected
