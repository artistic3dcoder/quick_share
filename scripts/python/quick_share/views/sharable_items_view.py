from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLayout

from quick_share.defaults.sharable_prefs import SHARABLE


class SharableItemsView(QWidget):
    """View which provides a list of sharable items."""
    def __init__(self):
        super(SharableItemsView, self).__init__()
        self.layout = QVBoxLayout()
        self._configure()

    def _configure(self):
        """Configure SharableItemsView.

         Returns:
             None
         """
        self.layout.setContentsMargins(*SHARABLE.default_margins)
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setLayout(self.layout)
