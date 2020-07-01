from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QFrame, QGridLayout, QLayout

from quick_share.defaults.icons_prefs import ICONS
from quick_share.defaults.sharable_prefs import SHARABLE
from quick_share.widgets.qs_widgets import create_icon_button, create_label, create_line_edit


class ShareItemView(QFrame):
    """View which represents a single sharable item in the SharableItemsView."""
    def __init__(self, data, callback):
        """Instantiation of ShareItemView.

        Args:
            data (str): Full path to the sharable item.
            callback (method): Method to call when user clicks button.

        Returns:
            None
        """
        super(ShareItemView, self).__init__()
        self.callback = callback
        self.layout = QGridLayout()
        self.update_btn = create_icon_button(parent=self,
                                             path=ICONS.minus,
                                             size=SHARABLE.icon,
                                             name=SHARABLE.update_obj_name)
        self.share_text = create_label(width=SHARABLE.min_widget_width,
                                       height=SHARABLE.widget_height,
                                       text=data)
        self.note_label = create_label(width=SHARABLE.min_widget_width,
                                       height=SHARABLE.widget_height,
                                       text=SHARABLE.note)
        self.note = create_line_edit(height=SHARABLE.widget_height,
                                     text="",
                                     obj_name=SHARABLE.note_obj_name)

        self._configure()

    def _configure(self):
        """Configure the ShareItemView.

        Returns:
            None
        """
        self.setObjectName(SHARABLE.sharable_item_obj_name)
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.layout.setContentsMargins(*SHARABLE.default_margins)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        self.share_text.setParent(self)
        self.note_label.setParent(self)
        self.note_label.setHidden(True)
        self.note.setParent(self)
        self.note.setHidden(True)

        self.layout.addWidget(self.update_btn, 0, 0)
        self.layout.addWidget(self.share_text, 0, 1)
        self.layout.addWidget(self.note_label, 0, 2)
        self.layout.addWidget(self.note, 0, 3)

        self.update_btn.pressState = 0
        self.update_btn.container = self
        self.update_btn.selfItem = self.update_btn
        self.update_btn.itemToSend = self.share_text
        self.update_btn.info = self.note_label
        self.update_btn.line = self.note
        self.setLayout(self.layout)
        self.update_btn.released.connect(lambda: self.callback(source_widget=self.update_btn))
        self.setMinimumHeight(SHARABLE.min_widget_height)
        self.update()
