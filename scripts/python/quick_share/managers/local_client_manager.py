# NATIVE
from os import getenv, makedirs
from os.path import join, exists
from sys import platform

# INTERNAL
from quick_share.widgets.qs_widgets import critical_message
from quick_share.config import SHARED_USERS_FOLDER
from quick_share.defaults.controller_prefs import CONTROLLER
from quick_share.defaults.system_prefs import SYSTEM


class LocalClientManager(object):
    """Responsible for managing the local clients of QuickShare packets.

    Attributes:
        client (str): Current user of QuickShare.
        configured (bool): Configured state of manager. Used to determine UI state for QuickShare.
        status (str): Status message associated with the configured state of the manager. Used if there is an error
                      in configuring local client.
    """
    def __init__(self):
        self.client = None
        self.configured = True
        self.status = None
        self._configure_user()

    def _configure_user(self):
        """Configure user name.

        Returns:
            None
        """
        if SYSTEM.linux in platform:
            self.client = getenv(SYSTEM.linux_user)
        else:
            self.client = getenv(SYSTEM.win_user)
        # If the user does not have a share folder add one.
        user_share_folder = join(SHARED_USERS_FOLDER, self.client)
        if not exists(user_share_folder):
            try:
                makedirs(user_share_folder)
            except Exception as e:
                self.configured = False
                self.status = CONTROLLER.error_user_folder_msg.format(path=user_share_folder)
                critical_message(title=CONTROLLER.error_user_folder, message=self.status)
        else:
            self.status = CONTROLLER.configured
