import concurrent.futures
from threads.simulate_home_activity import markov_walk
from threads.simulate_home_activity.states import states, transition_matrix
from core.device import connect_devices_from_csv


def run_on_device(serial: str, d, steps: int) -> None:
    """
    Run a Markov walk simulation on a single device.

    :param serial: Serial number of the device.
    :param d: uiautomator2.Device instance.
    :param steps: Number of steps in the simulation.
    """
    print(f"[{serial}] Simulation started.", flush=True)

    markov_walk.random_walk(
        d=d,
        states=states,
        transition_matrix=transition_matrix,
        steps=steps,
        verbose=True,
        serial=serial
    )

    print(f"[{serial}] Simulation completed.", flush=True)


def run_all_devices(step: int = 100, device_csv_path: str = "devices.csv") -> None:
    """
    Run the simulation on all devices listed in a CSV file.

    :param adb_path: Path to the adb executable.
    :param step: Number of steps for each device simulation.
    :param device_csv_path: Path to the CSV file containing device serial numbers.
    """
    connected_devices = connect_devices_from_csv(device_csv_path)

    if not connected_devices:
        print("No available devices found. Please check the CSV file.", flush=True)
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(run_on_device, serial, d, step)
            for serial, d in connected_devices.items()
        ]
        concurrent.futures.wait(futures)
