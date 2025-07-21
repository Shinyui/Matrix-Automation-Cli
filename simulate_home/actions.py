import uiautomator2 as u2
import random
import time as t

def swipe_up_once(d: u2.Device, duration_min=0.05, duration_max=0.1):
    """
    執行一次隨機滑動，模擬往上滑動內容。

    :param d: uiautomator2 裝置物件
    :param duration_min: 滑動最短持續時間（秒）
    :param duration_max: 滑動最長持續時間（秒）
    :param wait_min: 滑動後最短等待時間（秒）
    :param wait_max: 滑動後最長等待時間（秒）
    """
    x = round(random.uniform(0.2, 0.7), 2)
    start_y = round(random.uniform(0.75, 0.85), 2)
    end_y = round(random.uniform(0.35, 0.45), 2)
    duration = round(random.uniform(duration_min, duration_max), 2)
    d.swipe(x, start_y, x, end_y, duration)
    return True

def click_heart(d: u2.Device):
    like_btn = d(resourceId="com.instagram.android:id/row_feed_button_like")

    if like_btn.count != 1:
        return False
    
    like_btn.click()
    return True

def open_comment_box(d: u2.Device):
    """
    嘗試打開 Instagram 的留言輸入框。
    :param d: uiautomator2 裝置物件
    :return: bool 是否成功開啟留言輸入區
    """
    comment_btn = d(resourceId="com.instagram.android:id/row_feed_button_comment")
    input_box = d(resourceId="com.instagram.android:id/layout_comment_thread_edittext")

    if comment_btn.count != 1:
        return False

    comment_btn.click()
    if input_box.exists and input_box.info.get("enabled", False):
        d.press("back")
        return True
    else:
        return False
    
def post_comment_like_human(d: u2.Device, comments=["😂","❤️","😩"]):
    """
    從提供的留言列表中隨機選一條，模擬人類輸入並發送 IG 留言。

    :param d: uiautomator2 裝置對象
    :param comments: list[str]，留言字串清單
    """
    if not comments:
        print("留言列表為空，無操作")
        return False

    text = random.choice(comments)

    # 找到留言按鈕並點擊
    enter_btn = d(resourceId="com.instagram.android:id/layout_comment_thread_post_button_icon")
    input_box = d(resourceId="com.instagram.android:id/layout_comment_thread_edittext")

    input_box.click()

    # 一字一字模擬輸入
    for ch in text:
        d.send_keys(ch)
        t.sleep(random.uniform(0.1, 0.25))

    enter_btn.click()
    return True

def go_back(d: u2.Device, prev_state=None, delay_min=0.2, delay_max=0.5):
    """
    根據前一個狀態，按適當次數返回鍵。

    :param d: uiautomator2 裝置對象
    :param prev_state: 字串，上一個狀態（例如 '評論'）
    :param delay_min: 每次返回後最短等待秒數
    :param delay_max: 每次返回後最長等待秒數
    """

    # 根據上一個狀態決定步數
    state_to_back_steps = {
        "評論": 2,
        "查看發文者主頁": 1,
        "發文者主頁捲動": 1,
        "按愛心": 0,
        "首頁捲動": 0,
        "（回到）首頁": 0,
    }

    steps = state_to_back_steps.get(prev_state)

    if steps <= 0:
        return False

    for _ in range(steps):
        d.press("back")
        delay = random.uniform(delay_min, delay_max)
        t.sleep(delay)
    return True

def enter_author_profile(d: u2.Device):
    """
    嘗試點擊發文者名稱，若只有一人標註才會點擊進入個人主頁。

    :param d: uiautomator2 裝置對象
    :return: True 代表有成功點擊；False 代表略過
    """
    profile_header = d(resourceId="com.instagram.android:id/row_feed_photo_profile_name")

    if profile_header.count != 1:
        return False

    text = profile_header.info.get("text", "")
    if "and" in text:
        return False

    profile_header.click()
    return True

