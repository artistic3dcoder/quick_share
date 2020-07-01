from quick_share.views.send_view import SendView


class SendViewController(object):
    """Controls interactions with the SendView View.

    Attributes:
        view (SendView): View associated with controller.
    """
    def __init__(self):
        self.view = SendView()

    def enable_share_btn(self):
        """Disable the share button.

        Returns:
            None
        """
        self.view.send_share_btn.setDisabled(False)

    def get_note(self):
        """Return name associated with Packet.

        Returns:
            str
        """
        return str(self.view.note.text()).strip()

    def get_packet_name(self):
        """Return name associated with Packet.

        Returns:
            str
        """
        return str(self.view.packet_name.text())

    def get_cleaned_packet_name(self):
        """"Return a cleaned packet name ready for consumption.

        Returns:
            str
        """
        return self.get_packet_name().replace(".", "_").replace(" ", "_")

    def disable_share_btn(self):
        """Disable the share button.

        Returns:
            None
        """
        self.view.send_share_btn.setDisabled(False)
