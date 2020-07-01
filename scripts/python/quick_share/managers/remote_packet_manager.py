from datetime import datetime
from os import makedirs
from os.path import join, isdir
from shutil import copyfile

from quick_share.config import SHARED_USERS_FOLDER
from quick_share.defaults.quick_share_prefs import SHARE_TYPE
from quick_share.defaults.controller_prefs import CONTROLLER
from quick_share.defaults.share_files_prefs import SHARE_FILES


class RemotePacketManager(object):
    """Responsible for handing collecting of packets that will be sent to a host machine.

    Attributes:
        remote_client_manager (RemoteClientManager): Responsible for managing Remote clients.
        local_client_manager (LocalClientManager): Responsible for managing local clients.
        local_packet_manager (LocalPacketManager): Responsible for managing local packets.
    """
    def __init__(self, remote_client_manager, local_client_manager, local_packet_manager):
        self.remote_client_manager = remote_client_manager
        self.local_client_manager = local_client_manager
        self.local_packet_manager = local_packet_manager

    def create_user_shared_item_folder(self, packet_name, user):
        """Create folder in user folder which represents the current shared packet.

        Args:
            packet_name (str): Name associated with packet.
            user (str): Name of user to send to.

        Returns:
            str: path of folder where share will be copied to.
        """
        cur_date = datetime.now().date()
        path = join(SHARED_USERS_FOLDER,
                    str(user),
                    SHARE_FILES.quick_share_folder,
                    self.local_client_manager.client,
                    str(cur_date.year),
                    str(cur_date.month).zfill(2),
                    str(cur_date.day).zfill(2),
                    packet_name)
        if not isdir(path):
            makedirs(path)
        return path

    def send_share_data(self, items, packet_name, notes):
        """ Send share data to all users in the list.

        Args:
            items (list (QWidget)): Items which should be sent to remote clients.
            packet_name (str): Name associated with shared packet.
            notes (str): Notes to share with packet.

        Returns:
            None
        """
        for user in (x for x in self.remote_client_manager.share_clients if isdir(join(SHARED_USERS_FOLDER, str(x)))):
            path = self.create_user_shared_item_folder(packet_name, user)
            file_ = open(join(path, SHARE_FILES.notes), 'w')
            file_.write(CONTROLLER.packet_note.format(note=notes))
            self.transfer_share_data(items=items, f=file_, path=path)
            file_.close()

    def transfer_share_data(self, items, f, path):
        """Iterate all share items, write associated notes to file and Copy shared data to a given path.

        Args:
            items (list (QWidget)): Items which should be sent to remote clients.
            f (File Object): Open file object.
            path (str): Full path to directory where share data is written to.

        Returns:
            None
        """
        for share_item in items:
            if share_item.line.text().strip():
                f.write("{0}{2}:\n{1}\n\n".format(share_item.itemToSend.text(),
                                                  str(share_item.line.text()),
                                                  SHARE_TYPE.replace(".", "")))
            item = "{}{}".format(str(share_item.itemToSend.text()), SHARE_TYPE)
            source = join(self.local_packet_manager.source_dir, item)
            dest = join(path, item)
            print("\nCOPIED: {0} to: \n\t{1}".format(source, dest))
            copyfile(source, dest)
