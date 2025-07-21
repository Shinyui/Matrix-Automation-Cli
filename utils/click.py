import uiautomator2 as ui2

def click(d: ui2.Device, resource_id: str) -> bool:
    """
    Click a UI element by its resource ID, with logic to handle multiple matches.

    If multiple elements are found with the same resource ID, the function will
    click the one in the middle. This is useful for views with repeated UI elements.

    :param d:              uiautomator2.Device. The connected Android device instance.
    :param resource_id:    str. The resource ID of the target UI element.
    :raises ValueError:    If resource_id is not provided.
    :return:               bool. True if a click was attempted, False if no element is clicked.
    """
    
    if not resource_id:
        raise ValueError("resource_id must be provided")

    btn = d(resourceId=resource_id)

    if btn.count < 1:
        print(f"No {resource_id} detected")
        return False

    if btn.count != 1:
        idx = round((btn.count -1) / 2)
        btn[idx].click()
        return True

    btn.click()
    return True