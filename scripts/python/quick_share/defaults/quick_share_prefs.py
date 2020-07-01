# NATIVE
from re import compile


# File type to share.
SHARE_TYPE = ".cpio"
# Support format from v1.0.0
LEGACY_EXP = compile("^[a-zA-Z]*_[a-zA-Z]*_[0-9]*_")
# Search for Copy/Past files.
MEMORY_EXP = compile("[a-zA-Z_]*{0}$".format(SHARE_TYPE))
# Invalid naming search parameters.
INVALID_EXP = compile("[^a-zA-Z0-9_ ]+")


class QUICKSHAREVIEW:
    """Preferences for the main QuickShare View."""
    title = "QuickShare"
    copy_to_mem = "Select Copy Data To Copy Into Memory:"
    manage = "MANAGE"
    refresh = "Refresh"
    refresh_obj_name = "Refresh"
    send = "SEND"
    share_info = "Select Copy Data To Send:"
    main_layout_spacing = 5
    sharable_spacing = 10
    width = 600
    height = 500


