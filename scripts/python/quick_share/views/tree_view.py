from PySide2.QtCore import Qt
from PySide2.QtCore import QRect
from PySide2.QtGui import QBrush, QColor, QIcon, QPixmap
from PySide2.QtWidgets import QTreeWidget, QSizePolicy, QHeaderView, QTreeWidgetItem

from quick_share.models.combined_share_data import CombinedShareData
from quick_share.models.share_data import ShareData
from quick_share.defaults.tree_prefs import TREEVIEW


class TreeView(QTreeWidget):
    """View which represents file that have been shared with user."""
    COL_TRANSPARENT = QBrush(QColor(0, 0, 0, 0))
    COL_MIX = QBrush(QColor(129, 190, 240))

    def __init__(self):
        super(TreeView, self).__init__()
        self.size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._configure()

    def _configure(self):
        """Configure QuickShareTreeView.

        Returns:
            None
        """
        self.setHeaderHidden(True)
        self.setAllColumnsShowFocus(True)
        self.size_policy.setVerticalStretch(TREEVIEW.tree_stretch)
        self.size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.size_policy)
        self.setColumnCount(3)

        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.setGeometry(QRect(*TREEVIEW.tree_rect))
        self.setMaximumHeight(TREEVIEW.tree_height)


def tree_root(label, ico1, ico2, path):
    """Create and configure a top level QTreeWidgetItem.

    Args:
        label (str): label applied to widget.
        ico1 (str): Full path to icon image applied to first column of tree widget.
        ico2 (str): Full path to icon image applied to second column of tree widget.
        path (str): Full path to directory this QTreeWidget represents.

    Returns:
        QTreeWidgetItem
    """

    widget = QTreeWidgetItem()
    widget.setBackgroundColor(0, QColor(0, 0, 0, 0))
    widget.setBackgroundColor(1, QColor(0, 0, 0, 0))
    # Apply icons
    person_icon = QIcon(QPixmap(ico1))
    trash_icon = QIcon(QPixmap(ico2))
    widget.setIcon(0, person_icon)
    widget.setIcon(1, trash_icon)
    # Configure tree widget.
    widget.extra_data = False
    widget.setFirstColumnSpanned(True)
    widget.setText(0, label)
    widget.is_sub_folder = False
    widget.is_item = False
    widget.allow_checking = False
    widget.user_check_state = 0
    widget.path = path

    return widget


def tree_folder(label, parent, ico1, ico2, ico3, path, data, packet=False,  note=None, clickable=True):
    """Create and configure a QTreeWidgetItem which represents a folder.

    Args:
        label (str): label applied to widget.
        parent (QTreeWidgetItem): Parent widget QTreeWidgetItem will attach to.
        ico1 (str): Full path to icon image applied to first column of tree widget.
        ico2 (str): Full path to icon image applied to second column of tree widget.
        ico3 (str): Full path to icon image applied to third column of tree widget.
        path (str): Full path to directory this QTreeWidget represents.
        data (qs_model): Data type tree folder represents. This is used to determine if we can delete a given item.
        packet (bool): Does this item represent the sharable packet?
        note (str, Optional): Full path to notes, if applicable. This would only be applied to the tree_folder which
                              contains the share files.
        clickable (bool, Optional): Can the user check this item?

    Returns:
        QTreeWidgetItem
    """
    widget = QTreeWidgetItem(parent, 0)
    widget.setBackgroundColor(0, QColor(0, 0, 0, 0))
    widget.setBackgroundColor(1, QColor(0, 0, 0, 0))
    widget.setBackgroundColor(2, QColor(0, 0, 0, 0))
    widget.allow_checking = clickable
    widget.data_type = data
    widget.user_check_state = 0
    widget.setText(0, label)
    widget.setIcon(0, QIcon(QPixmap(ico1)))
    if isinstance(data, ShareData) or (isinstance(data, CombinedShareData) and packet):
        widget.setIcon(1, QIcon(QPixmap(ico2)))
    if note:
        widget.setIcon(2, QIcon(QPixmap(ico3)))
    widget.is_sub_folder = True
    widget.is_item = False
    widget.packet = packet
    widget.note = note
    widget.path = path
    widget.pointer = widget
    widget.children_items = []

    return widget


def tree_item(label, ico1, item):
    """Create and configure a QTreeWidgetItem which represents a folder.

    Args:
        label (str): label applied to widget.
        ico1 (str): Full path to icon image applied to first column of tree widget.
        item (str): Path to item on disk this widget represents.

    Returns:
        QTreeWidgetItem
    """
    widget = QTreeWidgetItem(0)
    widget.setBackgroundColor(0, QColor(0, 0, 0, 0))
    widget.setText(0, label)
    widget.allow_checking = True
    widget.user_check_state = 0
    icon = QIcon(QPixmap(ico1))
    widget.setIcon(0, icon)
    widget.is_sub_folder = False
    widget.is_item = True
    widget.item = item
    widget.pointer = widget
    # Do not assign flags to items. Essentially the user can not do anything other than see the items.
    widget.setFlags(Qt.NoItemFlags)

    return widget
