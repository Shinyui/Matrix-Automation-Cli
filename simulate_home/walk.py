import sys
import random
import time as t
from simulate_home.actions import swipe_up_once, click_heart, open_comment_box, post_comment_like_human, enter_author_profile, go_back
from utils import load_comments_from_txt

def random_walk(d, states, transition_matrix, start_state="（回到）首頁", steps=20, verbose=True, serial="UNKNOWN"):
    current_state = start_state
    walk_sequence = [current_state]
    prev_state = None
    current_action_result = None

    for i in range(steps):
        if verbose:
            print(f"[{serial}] Step {i+1}: {current_state}", flush=True)

        try:
            match current_state:
                case "首頁捲動":
                    current_action_result = swipe_up_once(d)

                case "按愛心":
                    current_action_result = click_heart(d)

                case "評論":
                    current_action_result = open_comment_box(d)
                    if current_action_result:
                        comments = load_comments_from_txt("comments.txt")
                        current_action_result = post_comment_like_human(d, comments)

                case "查看發文者主頁":
                    current_action_result = enter_author_profile(d)
                    
                case "發文者主頁捲動":
                    current_action_result = swipe_up_once(d)

                case "（回到）首頁":
                    if prev_state:
                        go_back(d, prev_state)

                case _:
                    print(f"[{serial}] 未知狀態：{current_state}", flush=True)

        except Exception as e:
            print(f"[{serial}] 執行 {current_state} 發生錯誤：{e}", flush=True)

        if current_action_result is False:
            print(f"[{serial}] 動作「{current_state}」執行失敗，重新抽選狀態", flush=True)

            current_state = random.choice(states)
            t.sleep(1)
            continue

        weights = transition_matrix.get(current_state)
        if not weights:
            raise ValueError(f"[{serial}] transition_matrix 缺少：{current_state}")

        next_state = random.choices(states, weights=weights, k=1)[0]
        walk_sequence.append(next_state)
        prev_state = current_state
        current_state = next_state

        t.sleep(1)

    print(f"[{serial}] 模擬完成", flush=True)
    return walk_sequence