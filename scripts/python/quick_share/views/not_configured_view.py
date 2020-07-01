from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout


class NotConfiguredView(QWidget):
    """View which is displayed if there is an issue configuring QuickShare."""
    def __init__(self, message):
        """Initialization of NotConfiguredView.

        Args:
            message (str): Message to display in view.
        """
        super(NotConfiguredView, self).__init__()
        label = QLabel(message)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
