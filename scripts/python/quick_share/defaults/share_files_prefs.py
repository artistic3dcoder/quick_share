from re import compile

from quick_share.defaults.quick_share_prefs import SHARE_TYPE


class SHARE_FILES:
    """Regular expressions associated with QuickShare."""
    # Identifies legacy share files associated with v1.0.0 of tool.
    legacy = compile("^[a-zA-Z]*_[a-zA-Z]*_[0-9]*_")
    # Identifies Houdini CPIO files stored in the temp drive of the users machine.
    memory = compile("[a-zA-Z_]*{0}$".format(SHARE_TYPE))
    # Identifies core notes associated with share packet.
    notes = "Notes.txt"
    # Folder name QuickShare shares are stored under.
    quick_share_folder = "quickshare_data"
    # Folder name where Houdini saves it's temp files.
    houdini_temp_folder = "houdini_temp"
