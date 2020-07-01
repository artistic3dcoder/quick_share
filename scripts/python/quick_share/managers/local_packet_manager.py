# NATIVE
from os import getenv, listdir, sep
from os.path import isdir, isfile, join
from sys import platform
from re import search, match
from shutil import copyfile

# INTERNAL
from quick_share.models.combined_share_data import CombinedShareData
from quick_share.models.share_data import ShareData
from quick_share.config import SHARED_USERS_FOLDER
from quick_share.defaults.quick_share_prefs import SHARE_TYPE
from quick_share.defaults.share_files_prefs import SHARE_FILES
from quick_share.defaults.system_prefs import SYSTEM


class LocalPacketManager(object):
    """Responsible for handing collecting of packets that have been shared with the current user.

    Attributes:
        local_client_manager (SendManager): Informs PacketManager who the current user is.
    """
    def __init__(self, local_client_manager):
        self.local_client_manager = local_client_manager
        self._copy_list = []
        self._received = []
        self._sharable_source_dir = None
        self._sharable_source_dir_items = None
        self._configure_temp_drive()
        self.get_available_packets()

    @property
    def copy_list(self):
        """list (str): Full path to  sharable items to copy."""
        return self._copy_list

    @property
    def received(self):
        """list (str): Packets that have been shared with local client."""
        return self._received

    @property
    def source_dir(self):
        """str: Full path to where sharable source data is found."""
        return self._sharable_source_dir

    @property
    def source_dir_items(self):
        """list (str): Items which a valid for sharing."""
        return self._sharable_source_dir_items

    def reset_copy_list(self):
        """Remove all items from copy list.

        Returns:
            None
        """
        self._copy_list = []

    def copy_list_count(self):
        """Returns number of items in copy list.

        Returns:
            Int
        """
        return len(self._copy_list)

    def add_copy_item(self, item):
        """Register an item to be shared.

        Args:
            item (list (str)): Full path to item to share.

        Returns:
            None
        """
        self._copy_list.append(item)

    def remove_copy_item(self, item):
        """Remove a sharable item from the copy_list.

        Args:
            item (list (str)): Full path to item to remove from copy_list.

        Returns:
            None
        """
        valid_items = []
        for copy_path in self._copy_list:
            if item in copy_path:
                valid_items.append(item)
        for vi in valid_items:
            self._copy_list.remove(vi)

    def _configure_temp_drive(self):
        """Configure the temp drive and store in self.sharable_source_dir.

        Note:
            The self.sharable_source_dir is where QuickShare looks for the users temp files to share.

        Returns:
            None
        """
        if SYSTEM.linux in platform:
            temp = SYSTEM.linux_temp
        else:
            temp = getenv(SYSTEM.win_temp)
        self._sharable_source_dir = join(temp, SHARE_FILES.houdini_temp_folder)
        self._sharable_source_dir_items = listdir(self.source_dir)

    def reset(self):
        """Reset PacketManager and re-evaluate what packets are available.

        Returns:
            None
        """
        self._received = []
        self.get_available_packets()

    def get_available_packets(self):
        """Iterate share temp and collect available packets the user can pull.

        Returns:
            None
        """
        root_dir = join(SHARED_USERS_FOLDER, self.local_client_manager.client, SHARE_FILES.quick_share_folder)
        if isdir(root_dir):
            # The quicker share folder should hold a list of uses that have sent files. Let's find those user folders.
            for root_item in (item for item in listdir(root_dir) if isdir(join(root_dir, item))):
                cur_path = join(root_dir, root_item)
                # Find all folder under assumed user folder.
                for user_item in (item for item in listdir(cur_path) if isdir(join(cur_path, item))):
                    legacy = match(SHARE_FILES.legacy, str(user_item))
                    if hasattr(legacy, "group"):
                        # Collect v1.0.0 legacy packets for backward compatibility.
                        legacy_path = join(cur_path, user_item)
                        self.get_packets(cur_path=legacy_path,
                                         cur_folder=user_item,
                                         root_item=root_item,
                                         root_dir=root_dir,
                                         user_dir=cur_path,
                                         split_folder_name=[legacy.group()[:-1], user_item.replace(legacy.group(), "")])
                    else:
                        # Check if we have a new style folder.
                        self.get_sorted_packets(user_path=cur_path,
                                                root_item=root_item,
                                                root_dir=root_dir,
                                                user_dir=cur_path)

    def get_sorted_packets(self, user_path, root_item, root_dir, user_dir):
        """Find packets sorted by four digit year, two digit month, two digit day, and shared packet.

        Args:
            user_path (str): Full path to start of search. This is assumed to be the name of the user.
            root_item (str): root folder name associated with this search.
            root_dir (str): Full path to root folder.
            user_dir (str): Full path to the user dir associated with Sharable item. This is the user sharing the data,
                            not the current users collecting data.
        Returns:
            None
        """
        # Check if we have a year folder.
        for year_folder in self.get_packet_generator(path=user_path, digits=4, start=2015, end=2100):
            year_path = join(user_path, year_folder)
            # Check if we have a month folder.
            for month_folder in self.get_packet_generator(path=year_path, digits=2, start=0, end=13):
                month_path = join(year_path, month_folder)
                # Check if we have a day folder.
                for day_folder in self.get_packet_generator(path=month_path, digits=2, start=0, end=32):
                    day_path = join(month_path, day_folder)
                    # Check if we have a receive folder. This is the folder that represents the data the user sent.
                    for receive_folder in (item for item in listdir(day_path) if isdir(join(day_path, item))):
                        receive_path = join(day_path, receive_folder)
                        # Check if we have a share folder. This is the name of the packet the user sent.
                        self.get_packets(cur_path=receive_path,
                                         cur_folder=receive_folder,
                                         root_item=root_item,
                                         root_dir=root_dir,
                                         user_dir=user_dir)

    def get_packet_data(self):
        """ Collect packet data that has been share with end user and place in temp directory.

        Note:
            By replacing current copy data we effectively hijack the copy-paste system allowing us to paste copy data
            from another users session.

        Returns:
            None
        """
        for current_item in self.copy_list[0]:
            m = search(SHARE_FILES.memory, current_item)
            dest = join(self.source_dir, m.group())
            copyfile(current_item, dest)

    @staticmethod
    def get_packet_generator(path, digits, start, end):
        """Create and return a generator which will iterate a folder and return sub-folders which are digits and fall
        between a given range

        Args:
            path (str): Full path to directory to search.
            digits (int): Number of digits folder must have to qualify.
            start (int): Start number folder must be larger than.
            end (int): End number folder must be smaller than.

        Returns:
            Generator
        """
        return (x for x in listdir(path) if
                isdir(join(path, x)) and x.isdigit() and len(x) == digits and start < int(x) < end)

    def get_packets(self, cur_path, cur_folder,  root_item, root_dir, user_dir, split_folder_name=None):
        """Find packet data.

        Args:
            cur_path (str): Current path to directory being parsed.
            cur_folder (str): Name of the current folder.
            root_item (str): Top level item being parsed.
            root_dir (str): Full path to the root directory
            user_dir (str): Full path to the user dir associated with Sharable item. This is the user sharing the data,
                            not the current users collecting data.
            split_folder_name (list): Split the last folder name to register as two tree branches when picking this
                                      packet item.

        Returns:
            None
        """
        if split_folder_name:
            data = CombinedShareData(top_level=root_item, path=cur_path, folder=cur_folder)
        else:
            data = ShareData(top_level=root_item, path=cur_path, folder=cur_folder)
        notes_file = None
        # Collect the shared files. Only collect files that match out share type or is a note.
        for file_ in (x for x in listdir(cur_path) if
                      isfile(join(cur_path, x)) and x.endswith(SHARE_TYPE) or x == SHARE_FILES.notes):
            if file_ == SHARE_FILES.notes:
                notes_file = join(cur_path, SHARE_FILES.notes)
            else:
                data.files.append(file_)
        # Only store data if we found shared files.
        if data.files:
            # Store root path to user who sent packet. This is needed so we can delete the branch if the end user wants
            # to clean up there store.
            if user_dir:
                data.user_folder = user_dir
            # Store notes path if we found notes.
            if notes_file:
                data.notes = notes_file
            # Store the relative folder path as a list. This will be used to build the tree.
            if split_folder_name is None:
                data.relative_folder = cur_path.replace(root_dir, "").split(sep)[1:]
            else:
                # In this case we want to split the folder name at the give str.
                data.relative_folder = cur_path.replace(root_dir, "").split(sep)[1:-1] + split_folder_name
            # save the data to the received share list. Only structures that found share data will be shown in the tree.
            self.received.append(data)
