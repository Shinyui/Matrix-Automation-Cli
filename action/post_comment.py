import random
import time as t
import uiautomator2 as u2

def post_comment(d: u2.Device, input_box_id: str = "", post_btn_id: str = "", comments: list[str] = [], min_wait: float = 0.1, max_wait : float = 0.25) -> bool:
    """
    Simulate human-like typing to post a random comment on an Android app.

    Selects a random comment from the provided list, clicks the input field,
    types each character with a random delay between keystrokes, and submits it.

    :param d: uiautomator2.Device. The connected Android device instance.
    :param input_box_id: str. Resource ID of the comment input text box.
    :param post_btn_id: str. Resource ID of the comment submit button.
    :param comments: list[str]. A list of possible comment strings to choose from.
    :param min_wait: float. Minimum delay (in seconds) between each character input.
    :param max_wait: float. Maximum delay (in seconds) between each character input.
    :raises ValueError: If input_box_id, post_btn_id, or comments are missing or invalid.
    :return: bool. True if the comment was successfully typed and posted.
    """

    if not input_box_id:
        raise ValueError("input_box_id must be provided")
    
    if not post_btn_id:
        raise ValueError("post_btn_id must be provided")

    if not comments or not isinstance(comments, list):
        raise ValueError("comments must be a non-empty list of strings")

    text = random.choice(comments)

    # Find and click the input box
    input_box = d(resourceId=input_box_id)
    post_btn = d(resourceId=post_btn_id)
    input_box.click()

    # Simulate typing character by character
    for ch in text:
        d.send_keys(ch)
        t.sleep(random.uniform(min_wait, max_wait))

    post_btn.click()
    return True