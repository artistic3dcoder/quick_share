from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QFrame, QScrollArea, QSizePolicy, QCompleter

from quick_share.defaults.icons_prefs import ICONS
from quick_share.defaults.remove_clients_prefs import SENDTOVIEW
from quick_share.widgets.qs_widgets import create_label, create_line_edit, create_icon_button


class RemoteClientPickerView(QWidget):
    """View which provides controls for selecting individuals to share data with."""
    def __init__(self):
        super(RemoteClientPickerView, self).__init__()
        self.layout = QVBoxLayout()

        self.label = create_label(width=SENDTOVIEW.label_width,
                                  height=SENDTOVIEW.widget_height,
                                  text=SENDTOVIEW.help)
        self.person_finder = create_line_edit(height=SENDTOVIEW.widget_height,
                                              text=SENDTOVIEW.default,
                                              obj_name=SENDTOVIEW.finder_obj_name)
        self.users_box = QVBoxLayout()
        self.scroll_area_frame = QFrame()
        self.scroll_area_users = QScrollArea()

        self._configure()

    def _configure(self):
        """Configure QuickSharePersonPickerView.

        Returns:
            None
        """
        self.setObjectName(SENDTOVIEW.widget_obj_name)
        self.label.setParent(self)
        # Configure person finder.
        self.person_finder.mousePressEvent = lambda _: self.person_finder.selectAll()
        self.person_finder.setMinimumHeight(SENDTOVIEW.view_finder_height)
        self.person_finder.item = self.person_finder
        self.person_finder.setTextMargins(*SENDTOVIEW.finder_margins)
        self.person_finder.setParent(self)
        # Configure users box
        self.scroll_area_frame.setFrameStyle(QFrame.NoFrame)
        self.scroll_area_frame.setObjectName(SENDTOVIEW.selected_users)
        self.scroll_area_frame.setMinimumWidth(SENDTOVIEW.frame_width)
        self.scroll_area_frame.setMinimumHeight(SENDTOVIEW.min_frame_height)
        self.scroll_area_users.setWidget(self.scroll_area_frame)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(SENDTOVIEW.stretch)
        size_policy.setHeightForWidth(self.scroll_area_users.sizePolicy().hasHeightForWidth())
        self.scroll_area_users.setSizePolicy(size_policy)
        self.scroll_area_users.setFrameStyle(QFrame.NoFrame)
        self.users_box.setAlignment(Qt.AlignTop)
        self.scroll_area_frame.setLayout(self.users_box)

        self.scroll_area_users.setWidgetResizable(True)
        self.scroll_area_users.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Add Widgets to view
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.person_finder)
        self.layout.addStretch(1)
        self.layout.addWidget(self.scroll_area_users)
        self.setLayout(self.layout)

    def add_completer(self, users):
        """Add a completer to the view which facilitates finding valid individuals to share with.

        Args:
            users (list(str)): Users that can receive share data.

        Returns:
            None
        """
        completer = QCompleter(users, self.person_finder)
        self.person_finder.setCompleter(completer)

    def add_user_name(self, name, release_callback):
        """Add a user name to the Person Picker View.

        Note:
            These are the individuals who will receive share data.

        Args:
            name (str): Users name who will have data shared with them.
            release_callback (Method): Method to call when a user is removed from the share list.

        Returns:
            None
        """
        # Add a frame and layout to hold copy item.
        frame = QFrame()
        frame.setObjectName(SENDTOVIEW.add_user_frame_obj_name)
        frame.setFixedHeight(SENDTOVIEW.copy_item_height)
        layout = QHBoxLayout()
        layout.setContentsMargins(*SENDTOVIEW.send_to_user_margins)

        # Add an update button with an icon.This will allow end user to delete the user from the send list.
        user_update = create_icon_button(parent=self,
                                         path=ICONS.remove,
                                         size=SENDTOVIEW.copy_icon,
                                         name=SENDTOVIEW.user_icon_obj_name)
        user_text = create_label(width=SENDTOVIEW.label_width,
                                 height=SENDTOVIEW.widget_height,
                                 text=name)
        user_update.released.connect(lambda: release_callback(source_widget=user_update))

        user_update.pressState = 0
        user_update.container = frame
        user_update.selfItem = user_update
        user_update.parent = frame
        user_update.control = layout
        user_update.label = user_text
        user_update.text = name

        layout.addWidget(user_update)
        layout.addWidget(user_text)

        frame.setLayout(layout)
        self.users_box.addWidget(frame)
        self.person_finder.setText("")
