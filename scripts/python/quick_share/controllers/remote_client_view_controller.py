from quick_share.views.remote_client_picker_view import RemoteClientPickerView


class RemoteClientViewController(object):
    """Remove client view controller.

    Responsible for interactions in the RemoteClientView.

    Attributes:
        view (RemoteClientPickerView): View associated with controller.
        remote_client_manager (RemoteClientManager): Remote client manager instance.
    """
    def __init__(self, remote_client_manager):
        """Initialization of RemoteClientViewController.

        Args:
            remote_client_manager (RemoteClientManager): Remote client manager instance.
        """
        self.view = RemoteClientPickerView()
        self.remote_client_manager = remote_client_manager

        self._configure_completer()

    def add_client(self, name, release_callback):
        """Add a user name to the Person Picker View.

        Note:
            These are the individuals who will receive share data.

        Args:
            name (str): Users name who will have data shared with them.
            release_callback (Method): Method to call when a user is removed from the share list.

        Returns:
            None
        """
        self.view.add_user_name(name=name, release_callback=release_callback)

    def clear_finder(self):
        """Clear the remote client picker.

        Returns:
            None
        """
        self.view.person_finder.setText("")

    def get_target_user(self):
        """QWidget: remote client finder"""
        return str(self.view.person_finder.item.text()).strip()

    def _configure_completer(self):
        """Configure completer associated with QuickSharePersonPickerView.

        Note:
            This allows auto-completion of valid uses while sharing.

        Returns:
            None
        """
        self.view.add_completer(users=self.remote_client_manager.clients)

    def remove_client_widget(self, widget):
        """Remove a client from the view.

        Args:
            widget (ShareViewItem): Widget to remove.

        Returns:
            None
        """
        self.view.users_box.removeWidget(widget.parent())
