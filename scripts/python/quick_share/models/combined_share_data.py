"""Models associated with QuickShare."""


class CombinedShareData(object):
    """Shared data object.

    Used to link share data with Manage tree widgets.

    Attributes:
        top_level (QWidget): Widget associating data to UI tree.
        files (list): Items represented by ShareData.
        path (str): Full path to items represented in ShareData.
        folder (str): Full path to folder holding ShareData.
        relative_folder (list (str)): Relative folder path in parts starting at user folder of person who shared data.
        notes (str): Full path to notes file associated with share files.
        user_folder (str): Full path to the user folder under shared directory.
        split (bool, Optional): Used to signify if folder which holds shared data is split when looking the last two
                                items in the relative folders list. Combining these two folders is the actual folder
                                name.
    """
    def __init__(self, top_level=None, files=None, path=None, folder=None, split=True):
        self.top_level = top_level
        self.files = files if files else []
        self.path = path
        self.folder = folder
        self.relative_folder = None
        self.split_folder = False
        self.notes = None
        self.user_folder = None
        self.split = split
