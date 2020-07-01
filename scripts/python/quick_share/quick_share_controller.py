"""
quick_Share.py (c) 2020 Walter Behrnes
Verision 2.0
Author: Walter Behrnes
Contact: walter.behrnes@gmail.com

Description:
       Quick share is an application which will allow a user to share copy paste data between another users machine.
       The application can be used in a shelf, shell, or a python panel.

Documentation:
       In order for quick share to work correctly you will need to  edit the config.py file to suit your
       work configuration.
       
To-do's:
   * Add line item ability to view notes per share item. Currently you can only see the notes at each top level share.
   * Add ability to remove a caches for a full user. Currently you can remove shared items but not the shared user.
"""
from os import chdir
from os.path import dirname, abspath
import sys
from re import search

# INTERNAL
# Before moving forward change our CWD, this will allow our app to see our icons.
code_base = dirname(abspath(__file__))
chdir(code_base)
sys.path.append(code_base)

from controllers.tree_view_controller import TreeViewController
from controllers.send_view_controller import SendViewController
from controllers.sharable_items_view_controller import SharableItemsViewController
from controllers.remote_client_view_controller import RemoteClientViewController
from controllers.receive_view_controller import ReceiveViewController

from managers.local_packet_manager import LocalPacketManager
from managers.remote_packet_manager import RemotePacketManager
from managers.local_client_manager import LocalClientManager
from managers.remote_client_manager import RemoteClientManager

from defaults.quick_share_prefs import SHARE_TYPE, QUICKSHAREVIEW, INVALID_EXP
from defaults.controller_prefs import CONTROLLER
from defaults.icons_prefs import ICONS
from defaults.send_prefs import SENDVIEW
from defaults.sharable_prefs import SHARABLE
from defaults.tree_prefs import TREEVIEW

from views.quick_share_view import QuickShareView
from views.share_item_view import ShareItemView
from views.not_configured_view import NotConfiguredView
from widgets.qs_widgets import critical_message, info_message, create_icon, create_spacer_item


class QuickShareController(object):
    """Controller logic for QuickShare.
    
    Attributes:

        local_client_manager (LocalClientManager): Manages local client user.
        remote_client_manager (RemoteClientManager): Manages remote client users.
        local_packet_manager (LocalPacketManager): Manages packet data for local client.
        remote_packet_manager (RemotePacketManager): Manages packet data for remote clients.
        tree_controller (TreeViewController): Controller for TreeView.
        send_controller (SendViewController): Controller for the SendView.
        sharable_items_controller (SharableItemsViewController): Controller for the SharableItemsVIew.
        remote_client_controller (RemoteClientViewController): Controller for the RemoveClientView.
        receive_view_controller (ReceiveViewController): Controller for the ReceiveView.
        view (quick_share_view.QuickShareView): Main Interface for QuickShare.
        share_list (list): Holds a reference of items to send to selected remote clients.

    """
    def __init__(self, parent=None):
        super(QuickShareController, self).__init__()
        self.local_client_manager = LocalClientManager()
        self.remote_client_manager = RemoteClientManager()
        self.local_packet_manager = LocalPacketManager(local_client_manager=self.local_client_manager)
        self.remote_packet_manager = RemotePacketManager(remote_client_manager=self.remote_client_manager,
                                                         local_client_manager=self.local_client_manager,
                                                         local_packet_manager=self.local_packet_manager)
        self.tree_controller = TreeViewController(local_packet_manager=self.local_packet_manager)
        self.send_controller = SendViewController()
        self.sharable_items_controller = SharableItemsViewController()
        self.remote_client_controller = RemoteClientViewController(remote_client_manager=self.remote_client_manager)
        self.receive_view_controller = ReceiveViewController()
        if not self.local_client_manager.configured:
            self.view = NotConfiguredView(message=self.local_client_manager.status)
        else:
            self.view = QuickShareView(sharable_items_view=self.sharable_items_controller.view,
                                       user_view=self.remote_client_controller.view,
                                       send_view=self.send_controller.view,
                                       tree_view=self.tree_controller.view,
                                       receive_view=self.receive_view_controller.view,
                                       parent=parent)

            self.share_list = []

            # Configure Send Tab
            self.populate_sharable_items_view()
            self._configure_connections()

    def show(self):
        """Show QuickShare View.

        Returns:
            None
        """
        self.view.show()

    def _configure_connections(self):
        """Configure callbacks between widgets and logic methods.

        Returns:
            None
        """
        self.view.refresh_btn.pressed.connect(self.tree_controller.refresh_manage_tree)
        self.send_controller.view.send_share_btn.released.connect(self.send_share_data)
        self.receive_view_controller.view.get_share.released.connect(self.get_packet_data)
        self.tree_controller.view.itemClicked.connect(self.handle_clicked)
        self.remote_client_controller.view.person_finder.returnPressed.connect(self.add_user_name)

    def add_user_name(self):
        """Collect target user and add them to the send list.

        Returns:
            None
        """
        target_user = self.remote_client_controller.get_target_user()
        if target_user:
            try:
                self.remote_client_manager.add_share_client(client=target_user)
            except IndexError:
                critical_message(title=CONTROLLER.invalid_entry, message=CONTROLLER.invalid_entry_msg)
                return
            except ValueError:
                return
            self.remote_client_controller.add_client(name=target_user, release_callback=self.remove_user)
        else:
            self.remote_client_controller.clear_finder()

    def add_share_data(self, source_widget):
        """Add/remove the item from the send list and set icon on sender item to display if it will be shared.

        Returns:
            None
        """
        state = bool(1 - source_widget.pressState)
        if state:
            source_widget.info.setHidden(False)
            source_widget.line.setHidden(False)
            source_widget.selfItem.setIcon(create_icon(path=ICONS.plus))
            source_widget.selfItem.pressState = 1
            # Add item to send list.
            if source_widget.itemToSend not in self.share_list:
                self.share_list.append(source_widget)
            if len(self.share_list) == 1:
                self.send_controller.enable_share_btn()
        else:
            source_widget.info.setHidden(True)
            source_widget.line.setHidden(True)
            source_widget.selfItem.setIcon(create_icon(path=ICONS.minus))
            source_widget.selfItem.pressState = 0
            # Remove item from send list.
            if source_widget.itemToSend in self.share_list:
                self.share_list.remove(source_widget)
            if len(self.share_list) == 0:
                self.send_controller.disable_share_btn()

    def get_packet_data(self):
        """ Collect packet data that has been share with end user and place in temp directory.

        Returns:
            None
        """
        self.local_packet_manager.get_packet_data()
        info_message(title=CONTROLLER.data_fetched, message=CONTROLLER.data_fetched_msg)

    def handle_clicked(self):
        """Handle clicking of tree view item.

        Returns:
            None
        """
        clicked_item = self.tree_controller.view.currentItem()

        # Read Notes.
        if self.tree_controller.view.currentColumn() == TREEVIEW.notes_index:
            self.tree_controller.read_tree_view_notes(clicked_item=clicked_item)
            self.tree_controller.view.setCurrentItem(clicked_item, TREEVIEW.item_index)
        # Delete row.
        if self.tree_controller.view.currentColumn() == TREEVIEW.delete_index:
            self.tree_controller.delete_tree_view_row(clicked_item=clicked_item)
            self.tree_controller.view.setCurrentItem(clicked_item, TREEVIEW.item_index)

        # Select | Unselect item.
        if self.tree_controller.view.currentColumn() == TREEVIEW.item_index:
            is_checked = 1 - clicked_item.user_check_state
            clicked_item.user_check_state = is_checked
            if hasattr(clicked_item, "allow_checking") and clicked_item.allow_checking:
                if clicked_item.is_sub_folder and not clicked_item.is_item:
                    self.tree_controller.update_clicking_tree_view_sub_folder(clicked_item=clicked_item,
                                                                              is_checked=is_checked)
                # Enable the get_share file button if the user has something to copy.
                if self.local_packet_manager.copy_list_count() != 0:
                    self.receive_view_controller.enable()
                else:
                    self.receive_view_controller.disable()
            if not is_checked:
                self.tree_controller.view.setItemSelected(clicked_item, False)

    def populate_sharable_items_view(self):
        """Get a list of /tmp/ share files, add to window so artist can choose what to send.
        
        Returns:
            None
        """
        # create a generator and iterate each sharable item and add it to the share_items_view.
        for data in (x.strip(SHARE_TYPE) for x in self.local_packet_manager.source_dir_items if x.endswith(SHARE_TYPE)):
            sharable = ShareItemView(data=data, callback=self.add_share_data)
            sharable.setParent(self.sharable_items_controller.parent)
            self.sharable_items_controller.add_widget(widget=sharable)
        self.sharable_items_controller.add_spacer(create_spacer_item(SHARABLE.spacer))

        self.view.tab1_vbox.addSpacing(QUICKSHAREVIEW.sharable_spacing)

    def remove_user(self, source_widget):
        """ Remove users from send list.

        Args:
            source_widget (QPushButton): Push button widget to associated with user.

        Returns:
            None
        """
        self.remote_client_manager.remove_share_client(client=source_widget.text)
        source_widget.label.close()
        source_widget.close()
        self.remote_client_controller.remove_client_widget(widget=source_widget.parent)
        source_widget.parent.setParent(None)

    def send_share_data(self):
        """ Send share data to all users in the list.

        Returns:
            None
        """
        # Check to see if the user changed the name or put a packet name.
        packet_name = self.send_controller.get_packet_name()
        if any([packet_name == SENDVIEW.packet_default_text, not packet_name]):
            critical_message(title=CONTROLLER.invalid_name,
                             message=CONTROLLER.invalid_name_msg)
            return

        # Check that the user added a note.
        if self.send_controller.get_note() == SENDVIEW.packet_notes or not self.send_controller.get_note():
            critical_message(title=CONTROLLER.invalid_note,
                             message=CONTROLLER.invalid_pkg_note)
            return

        # Check that user is not trying to send an invalid character.
        if hasattr(search(INVALID_EXP, packet_name), "group"):
            critical_message(title=CONTROLLER.invalid_note,
                             message=CONTROLLER.invalid_note_msg)
            return

        # SEND THE SHARE DATA TO THE CURRENT USER(S)
        if self.remote_client_manager.share_clients_count and self.share_list:
            self.remote_packet_manager.send_share_data(items=self.share_list,
                                                       packet_name=self.send_controller.get_cleaned_packet_name(),
                                                       notes=self.send_controller.get_note())
            info_message(title=CONTROLLER.data_sent,
                         message=CONTROLLER.data_sent_msg)
            self.tree_controller.refresh_manage_tree()
        else:
            critical_message(title=CONTROLLER.missing_users,
                             message=CONTROLLER.missing_users_msg)
