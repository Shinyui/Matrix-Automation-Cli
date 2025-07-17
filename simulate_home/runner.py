import concurrent.futures
from simulate_home.states import states, transition_matrix
from simulate_home.devices import connect_devices_from_csv
from simulate_home.walk import random_walk

def run_on_device(serial: str, d, steps):
    print(f"開始模擬裝置：{serial}")
    random_walk(
        d=d,
        states=states,
        transition_matrix=transition_matrix,
        steps=steps,
        verbose=True,
        serial=serial
    )
    print(f"完成模擬裝置：{serial}")

def run_all_devices(step=100, device_csv_path="devices.csv"):
    connected_devices = connect_devices_from_csv(device_csv_path)

    if not connected_devices:
        print("沒有可用裝置，請確認 devices.csv 是否正確")
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(run_on_device, serial, d, step)
            for serial, d in connected_devices.items()
        ]
        concurrent.futures.wait(futures)
