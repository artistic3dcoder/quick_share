from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QGridLayout

from quick_share.defaults.icons_prefs import ICONS
from quick_share.defaults.send_prefs import SENDVIEW
from quick_share.widgets.qs_widgets import create_label, create_line_edit, create_icon_button


class SendView(QFrame):
    """View which provides controls for sending shared data."""

    def __init__(self):
        super(SendView, self).__init__()
        self.layout = QGridLayout()

        self.packet_label = create_label(width=SENDVIEW.label_width,
                                         height=SENDVIEW.widget_height,
                                         text=SENDVIEW.packet_name)
        self.packet_name = create_line_edit(height=SENDVIEW.widget_height,
                                            text=SENDVIEW.packet_default_text,
                                            obj_name=SENDVIEW.packet_obj_name)
        self.note_label = create_label(width=SENDVIEW.label_width,
                                       height=SENDVIEW.widget_height,
                                       text=SENDVIEW.note)
        self.note = create_line_edit(height=SENDVIEW.widget_height,
                                     text=SENDVIEW.notes_default_text,
                                     obj_name=SENDVIEW.note_obj_name)
        self.send_share_btn = create_icon_button(parent=self,
                                                 path=ICONS.mail,
                                                 size=SENDVIEW.send_btn,
                                                 name=SENDVIEW.send_obj_name)
        self._configure()

    def _configure(self):
        """Configure view.

        Returns:
            None
        """
        self.setObjectName(SENDVIEW.name)
        self.setContentsMargins(*SENDVIEW.margins)
        self.setFixedHeight(SENDVIEW.view_height)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(*SENDVIEW.view_margins)
        # Packet Name
        self.packet_name.setTextMargins(*SENDVIEW.edit_margins)
        self.layout.addWidget(self.packet_label, 0, 0)
        self.layout.addWidget(self.packet_name, 0, 1)
        # Notes
        self.note.setTextMargins(*SENDVIEW.edit_margins)
        self.layout.addWidget(self.note_label, 1, 0)
        self.layout.addWidget(self.note, 1, 1)
        # Send
        self.send_share_btn.setDisabled(True)
        self.layout.addWidget(self.send_share_btn, 1, 2)

        self.setLayout(self.layout)
