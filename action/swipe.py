import random
import uiautomator2 as u2

def swipe(d: u2.Device, direction: str = "up", min_wait: float = 0.05, max_wait: float = 0.1) -> bool:
    """
    Perform a single randomized swipe to simulate upward or downward scrolling.

    This function randomly generates swipe start and end points along the Y-axis
    to mimic natural user behavior when scrolling content vertically.

    :param d: uiautomator2.Device. The connected Android device instance.
    :param direction: str. The swipe direction: "up" or "down".
    :param duration_min: float. Minimum duration (in seconds) for the swipe.
    :param duration_max: float. Maximum duration (in seconds) for the swipe.
    :raises ValueError: If an invalid direction is provided.
    :return: bool. True if swipe was performed.
    """
    x = round(random.uniform(0.2, 0.7), 2)

    if direction == "up":
        start_y = round(random.uniform(0.75, 0.85), 2)
        end_y = round(random.uniform(0.35, 0.45), 2)
    elif direction == "down":
        start_y = round(random.uniform(0.35, 0.45), 2)
        end_y = round(random.uniform(0.75, 0.85), 2)
    else:
        raise ValueError('direction must be "up" or "down"')

    duration = round(random.uniform(min_wait, max_wait), 2)
    d.swipe(x, start_y, x, end_y, duration)
    return True
