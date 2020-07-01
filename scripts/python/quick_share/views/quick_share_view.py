"""View associated with QuickShare."""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QTabWidget

from quick_share.defaults.quick_share_prefs import QUICKSHAREVIEW
from quick_share.defaults.qs_css import CSS


class QuickShareView(QWidget):
    """Interface for QuickShare."""

    def __init__(self, sharable_items_view, user_view, send_view, tree_view, receive_view, parent=None):
        super(QuickShareView, self).__init__(parent)
        # Store references to Views.
        self.sharable_items_view = sharable_items_view
        self.user_view = user_view
        self.send_view = send_view
        self.tree_view = tree_view
        self.receive_view = receive_view

        self.main_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab1_vbox = QVBoxLayout()
        self.tab2_vbox = QVBoxLayout()

        # Tab1 widgets (Send).
        self.share_info_label = QLabel(QUICKSHAREVIEW.share_info)

        # Tab2 widgets (Manage).
        self.refresh_btn = QPushButton(QUICKSHAREVIEW.refresh, self)
        self.copy_info_label = QLabel(QUICKSHAREVIEW.copy_to_mem, self)

        self._configure()

    def _configure(self):
        """Configure QuickView.

        Returns:
            None
        """
        self.sharable_items_view.setParent(self)
        self.send_view.setParent(self)
        self.user_view.setParent(self)
        self.tree_view.setParent(self)
        self.receive_view.setParent(self)

        # Configure widget and layouts.
        self.refresh_btn.setObjectName(QUICKSHAREVIEW.refresh_obj_name)

        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setSpacing(QUICKSHAREVIEW.main_layout_spacing)
        self.tab2_vbox.setAlignment(Qt.AlignTop)
        # Add views to tab1 (Send Tab)
        self.tab1_vbox.addWidget(self.share_info_label)
        self.tab1_vbox.addWidget(self.sharable_items_view)
        self.tab1_vbox.addWidget(self.user_view)
        self.tab1_vbox.addWidget(self.send_view)
        # Add Items to tab2 (Manage Tab)
        self.tab2_vbox.addWidget(self.refresh_btn)
        self.tab2_vbox.addWidget(self.copy_info_label)
        self.tab2_vbox.addWidget(self.tree_view)
        self.tab2_vbox.addStretch(1)
        self.tab2_vbox.addWidget(self.receive_view)
        self.setLayout(self.main_layout)
        # Add tabs
        self.tab1.setLayout(self.tab1_vbox)
        self.tab2.setLayout(self.tab2_vbox)
        self.tab_widget.addTab(self.tab1, QUICKSHAREVIEW.send)
        self.tab_widget.addTab(self.tab2, QUICKSHAREVIEW.manage)
        self.main_layout.addWidget(self.tab_widget)
        self.setStyleSheet(CSS)
        self.setMinimumSize(QUICKSHAREVIEW.width, QUICKSHAREVIEW.height)
        self.setWindowTitle(QUICKSHAREVIEW.title)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
