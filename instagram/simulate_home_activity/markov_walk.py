import random
import time as t
from pathlib import Path
from action import swipe, click, parse_comment, post_comment, go_back
from typing import List, Dict
from instagram.simulate_home_activity.state_to_back_steps import state_to_back_steps


def random_walk( d, states: List[str], transition_matrix: Dict[str, List[float]], start_state: str = "（回到）首頁", steps: int = 20, verbose: bool = True, serial: str = "UNKNOWN") -> List[str]:
    """
    Perform a random walk through UI states based on a transition matrix.

    This function simulates a user navigating an Android app by randomly
    transitioning between predefined UI states, executing actions accordingly.

    :param d: The uiautomator2.Device object representing the device.
    :param states: List of all possible state names.
    :param transition_matrix: A dictionary mapping current states to transition probabilities.
    :param start_state: The initial state to begin the walk.
    :param steps: Total number of steps to simulate.
    :param verbose: Whether to print logs for each step.
    :param serial: Device serial identifier (for logging).
    :return: A list recording the sequence of visited states.
    """
    current_state = start_state
    walk_sequence = [current_state]
    prev_state = None
    action_result = None

    for i in range(steps):
        if verbose:
            print(f"[{serial}] Step {i + 1}: {current_state}", flush=True)

        try:
            match current_state:
                case "（回到）首頁":
                    if prev_state:
                        go_back.go_back(d, prev_state, state_to_back_steps)

                case "首頁捲動":
                    action_result = swipe.swipe(d)

                case "按愛心":
                    action_result = click.click(d, resource_id="com.instagram.android:id/row_feed_button_like")

                case "評論":
                    action_result = click.click(d, resource_id="com.instagram.android:id/row_feed_button_comment")
                    if action_result:
                        BASE_DIR = Path(__file__).resolve().parent
                        comment_path = BASE_DIR / "comments.txt"
                        comments = parse_comment.load_comments_from_txt(comment_path)
                        action_result = post_comment.post_comment(d, comments=comments, 
                                                     input_box_id="com.instagram.android:id/layout_comment_thread_edittext", 
                                                     post_btn_id="com.instagram.android:id/layout_comment_thread_post_button_icon"
                                                    )

                case "查看發文者主頁":
                    action_result = click.click(d, resource_id="com.instagram.android:id/row_feed_photo_profile_name")

                case "發文者主頁捲動":
                    action_result = swipe.swipe(d)

                case _:
                    print(f"[{serial}] Unknown state: {current_state}", flush=True)

        except Exception as e:
            print(f"[{serial}] Error during '{current_state}': {e}", flush=True)

        if action_result is False:
            print(f"[{serial}] Action '{current_state}' failed, retrying with a random state.", flush=True)
            current_state = random.choice(states)
            t.sleep(1)
            continue

        weights = transition_matrix.get(current_state)
        if not weights:
            raise ValueError(f"[{serial}] Missing transition weights for state: {current_state}")

        next_state = random.choices(states, weights=weights, k=1)[0]
        walk_sequence.append(next_state)
        prev_state = current_state
        current_state = next_state

        t.sleep(1)

    print(f"[{serial}] Walk completed.", flush=True)
    return walk_sequence
