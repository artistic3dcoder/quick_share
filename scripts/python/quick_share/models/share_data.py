class ShareData(object):
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
    """
    def __init__(self, top_level=None, files=None, path=None, folder=None):
        self.top_level = top_level
        self.files = files if files else []
        self.path = path
        self.folder = folder
        self.relative_folder = None
        self.split_folder = False
        self.notes = None
        self.user_folder = None
