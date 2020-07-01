from os.path import join,  abspath, dirname


class ICONS:
    """Icons associated with QuickShare."""
    _root = join(dirname(dirname(abspath(__file__))), "icons")

    plus = join(_root, "Copy_Color2_16x16.png")
    minus = join(_root, "Add_Blue_16x16.png")
    remove = join(_root, "Delete_Blue_16x16.png")
    next = join(_root, "Right_Clear_Orange_128x128.png")
    mail = join(_root, "Send_24x24.png")
    person = join(_root, "PersonFolder_White_16x16.png")
    collection = join(_root, "CollectionFolder_Gray_16x16.png")
    tool = join(_root, "Tool_Gray_16x16x.png")
    get = join(_root, "Get_GreenArrow_32x32.png")
    check = join(_root, "check_box_down_transparent_16x16.png")
    uncheck = join(_root, "check_box_up_transparent_16x16.png")
    trash = join(_root, "trashcan_orange_22x22.png")
    bulb = join(_root, "Info_Bulb_24x24.png")
