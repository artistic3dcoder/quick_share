
from quick_share.views.receive_view import ReceiveView


class ReceiveViewController(object):
    """Controller for Receive View.

    Attributes:
        view (ReceiveView): View associated with controller.
    """
    def __init__(self):
        self.view = ReceiveView()

    def disable(self):
        """Disable the button on the view.

        Returns:
            None
        """
        self.view.get_share.setDisabled(True)

    def enable(self):
        """Enable the button on the view.

        Returns:
            None
        """
        self.view.get_share.setDisabled(False)
