from PySide2.QtWidgets import QFrame, QHBoxLayout

from quick_share.defaults.icons_prefs import ICONS
from quick_share.defaults.receive_prefs import RECEIVE
from quick_share.widgets.qs_widgets import create_icon_button, create_label


class ReceiveView(QFrame):
    """View which provides functionality for accepting a share object."""
    def __init__(self):
        super(ReceiveView, self).__init__()
        self.hbox_controls = QHBoxLayout()
        self.get_share = create_icon_button(parent=self,
                                            path=ICONS.get,
                                            size=RECEIVE.icon,
                                            name=RECEIVE.get_obj_name)
        self.get_data_label = create_label(width=RECEIVE.label_width,
                                           height=RECEIVE.widget_height,
                                           text=RECEIVE.get_data)

        self._configure()

    def _configure(self):
        """Configure QuickShareReceiveView.

        Returns:
            None
        """
        self.setObjectName(RECEIVE.view_obj_name)
        self.setFixedHeight(RECEIVE.view_height)
        self.hbox_controls.setContentsMargins(*RECEIVE.margins)
        self.hbox_controls.addWidget(self.get_data_label)
        self.get_share.setDisabled(True)
        self.hbox_controls.addStretch(1)
        self.hbox_controls.addWidget(self.get_share)

        self.setLayout(self.hbox_controls)
