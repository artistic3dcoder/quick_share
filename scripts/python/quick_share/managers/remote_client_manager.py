from os import listdir
from os.path import join, isdir

from quick_share.config import SHARED_USERS_FOLDER, EXCLUDED_USERS


class RemoteClientManager(object):
    """Responsible for managing remote clients, recipients, of QuickShare packets.

    Attributes:
        clients (list (str)): All users who are eligible to receive packet data.
    """

    def __init__(self):
        self.clients = []
        self._share_clients = []
        self.collect_sharable_clients()

    @property
    def share_clients(self):
        """list (str): Clients who ave been selected to share packet data with."""
        return self._share_clients

    @property
    def share_clients_count(self):
        """Int: Number of clients to share with."""
        return len(self.share_clients)

    def collect_sharable_clients(self):
        """Collect a list of valid users who can have share data sent to them.

        Returns:
            None
        """
        self.clients = []
        if isdir(SHARED_USERS_FOLDER):
            for i, item in enumerate(listdir(SHARED_USERS_FOLDER)):
                path = join(SHARED_USERS_FOLDER, item)
                if isdir(path):
                    pass_check = True
                    if EXCLUDED_USERS is not None and isinstance(EXCLUDED_USERS, tuple):
                        for exclude_item in (item for item in EXCLUDED_USERS if item is not None):
                            if exclude_item in item:
                                pass_check = False
                    if pass_check:
                        self.clients.append(item)

    def add_share_client(self, client):
        """Add a client to the share client list.

        Note:
            Clients in this list will have packets shared with them.

        Args:
            client (str): Client name who will receive packet data.

        Raises:
            ValueError: If client already in internal self.share_clients.
            IndexError: If client is not a valid member of internal self.clients.

        Returns:
            None
        """
        if client in self.clients:
            if client not in self.share_clients:
                self.share_clients.append(client)
            else:
                raise ValueError("Client: {} already added.")
        else:
            raise IndexError("Client: {} not found. Valid clients include: {}.".format(client, self.clients))

    def remove_share_client(self, client):
        """Remove a client from the share client list.

        Note:
            Clients in this list will have packets shared with them.

        Args:
            client (str): Client name who will be removed from the share list.

        Returns:
            None
        """
        if client in self.share_clients:
            self.share_clients.remove(client)
