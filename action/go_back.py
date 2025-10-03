import uiautomator2 as u2
import time as t
import random
from typing import Dict


def go_back(
    d: u2.Device,
    prev_state: str,
    state_to_back_steps: Dict[str, int],
    delay_min: float = 0.2,
    delay_max: float = 0.5
) -> bool:
    """
    Navigate backward based on the previous UI state.

    This function presses the back button multiple times based on the
    given mapping of states to back press counts. It simulates human-like
    delay between each press.

    :param d: uiautomator2.Device instance representing the connected device.
    :param prev_state: The previous logical state name (e.g., '評論').
    :param state_to_back_steps: A dict mapping state names to number of back presses.
    :param delay_min: Minimum delay (in seconds) between back presses.
    :param delay_max: Maximum delay (in seconds) between back presses.
    :return: True if back presses were made, False if no action was needed.
    :raises KeyError: If prev_state is not in state_to_back_steps.
    """

    if prev_state not in state_to_back_steps:
        raise KeyError(f"State '{prev_state}' not defined in state_to_back_steps")

    steps = state_to_back_steps[prev_state]

    if steps <= 0:
        return False

    for _ in range(steps):
        d.press("back")
        delay = random.uniform(delay_min, delay_max)
        t.sleep(delay)

    return True
