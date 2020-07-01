from os.path import exists, join
from shutil import rmtree

from quick_share.defaults.tree_prefs import TREEVIEW
from quick_share.defaults.icons_prefs import ICONS
from quick_share.defaults.controller_prefs import CONTROLLER
from quick_share.defaults import quick_share_prefs as prefs
from quick_share.models.combined_share_data import CombinedShareData
from quick_share.views.tree_view import TreeView, tree_root, tree_folder, tree_item
from quick_share.widgets.qs_widgets import critical_message, info_message


class TreeViewController(object):
    """Controller for tree view related operations.

    Attributes:
        view (TreeView): View associated with Controller.
        local_packet_manager (LocalPacketManager): Instance of the LocalPacketManager.
        checked_list (list): Currently checked items in the tree.
    """
    def __init__(self, local_packet_manager):
        """Initialization of the TreeViewController.

        Args:
            local_packet_manager (LocalPacketManager): Instance of the LocalPacketManager.
        """
        self.view = TreeView()
        self.local_packet_manager = local_packet_manager
        self.checked_list = []

        self.make_manage_tree()

    def delete_tree_view_row(self, clicked_item):
        """Delete a row from the tree view.

        Args:
            clicked_item (QTreeWidgetItem): Item which is a candidate for removal.

        Returns:
            None
        """
        if not clicked_item.is_item and hasattr(clicked_item, "path") and clicked_item.path:
            valid_packet = hasattr(clicked_item, "packet") and not clicked_item.packet
            children = clicked_item.childCount() != 0
            if valid_packet and children and isinstance(clicked_item.data_type, CombinedShareData):
                deletable = False
            else:
                deletable = True
            path = clicked_item.path
            if exists(path) and deletable:
                # Prompt user if they want to delete item.
                user_value = critical_message(title=CONTROLLER.delete_item,
                                              message=CONTROLLER.delete_item_msg.format(path),
                                              cancel_button=True)
                # If end user agrees, remove path from disk and clean up tree items.
                if user_value:
                    rmtree(path)
                    for item in self.view.selectedItems():
                        item.parent().removeChild(item)
            else:
                critical_message(title=CONTROLLER.can_not_delete,
                                 message=CONTROLLER.can_not_delete_msg.format(path),
                                 cancel_button=False)

    def make_manage_tree(self):
        """Create a QTreeView of all available data that users can get.

        Returns:
            None
        """
        root = None
        root_label = None
        for data in self.local_packet_manager.received:
            parent = child = None
            for idx, folder in enumerate(data.relative_folder):
                if idx == 0 and root_label != folder:
                    root = parent = tree_root(label=folder,
                                              ico1=ICONS.person,
                                              ico2=ICONS.trash,
                                              path=data.user_folder)
                    root_label = folder
                    # Put the TreeView into place.
                    self.view.addTopLevelItem(root)
                elif idx == 0:
                    parent = root
                else:
                    child_found = False
                    for child_idx in range(parent.childCount()):
                        child = parent.child(child_idx)
                        if folder in child.text(0):
                            parent = child
                            child_found = True
                    if not child_found:
                        # Only allow the last item to be selectable. Higher branches are navigation only.
                        last_idx = idx == len(data.relative_folder) - 1
                        clickable = last_idx
                        notes = data.notes if last_idx else None
                        if isinstance(data, CombinedShareData):
                            # Path data for combined share should not be split by the current folder.
                            path = data.path
                        else:
                            # To accurately track the current folder a QTreeWidgetItem represents we want to split the
                            # Currently item by the folder.
                            path = join(data.path.split(folder)[0], folder)
                        parent = tree_folder(label=folder,
                                             parent=parent,
                                             ico1=ICONS.collection,
                                             ico2=ICONS.trash,
                                             ico3=ICONS.bulb,
                                             path=path,
                                             data=data,
                                             packet=last_idx,
                                             note=notes,
                                             clickable=clickable)
                        if idx == 1:
                            root.addChild(parent)
                            child = parent
                        else:
                            child.addChild(parent)
                            child = parent

            for file_ in data.files:
                if file_.endswith(prefs.SHARE_TYPE):
                    share_item = tree_item(label=file_,
                                           ico1=ICONS.tool,
                                           item=join(data.path, file_))
                    parent.addChild(share_item)
                    parent.children_items.append(share_item.item)

    @staticmethod
    def read_tree_view_notes(clicked_item):
        """Read notes associated with shared items.

        Args:
            clicked_item (QTreeWidgetItem): Item which is a candidate for removal.

        Returns:
            None
        """
        if hasattr(clicked_item, "note") and clicked_item.note and clicked_item.allow_checking:
            notes = clicked_item.note
            if exists(notes):
                file_ = open(notes)
                text = file_.read()
                file_.close()
                info_message(title=CONTROLLER.notes, message=text)

    def refresh_manage_tree(self):
        """Refresh the manage tree.

        Returns:
            None
        """
        self.checked_list = []
        self.view.clear()
        self.local_packet_manager.reset()
        self.make_manage_tree()

    def update_clicking_tree_view_sub_folder(self, clicked_item, is_checked):
        """Update tree view after end user clicks on a tree view sub_folder.

        Args:
            clicked_item (QTreeViewWidgetItem): Widget clicked on in tree view.
            is_checked (bool): check state of current item.

        Returns:
            None
        """
        if is_checked:
            # Clear the copy list since this is a new request.
            self.local_packet_manager.remove_copy_item(item=clicked_item.text(0))
            # Uncheck everything else since it is a whole packet we are choosing.
            for item in self.checked_list:
                item.user_check_state = 0
                item.setBackground(TREEVIEW.item_index, TreeView.COL_TRANSPARENT)
            # Clear the checked list since this is a new request.
            self.checked_list = []
            self.checked_list.append(self.view.currentItem())
            clicked_item.setBackground(TREEVIEW.item_index, TreeView.COL_MIX)
            for i in range(0, clicked_item.childCount()):
                child_item = clicked_item.child(i)
                child_item.user_check_state = 0
                child_item.setBackground(TREEVIEW.item_index, TreeView.COL_MIX)
                self.checked_list.append(child_item)
            # Add data to copy into the copy list.
            self.local_packet_manager.reset_copy_list()

            for item in clicked_item.children_items:
                if item not in self.local_packet_manager.copy_list:
                    print("Adding Copy Item: {}".format(item))
                    self.local_packet_manager.add_copy_item(item=item)
        else:
            if clicked_item in self.checked_list:
                clicked_item.setBackground(TREEVIEW.item_index, TreeView.COL_TRANSPARENT)
                self.checked_list.remove(clicked_item)
            for i in range(0, clicked_item.childCount()):
                clicked_item.user_check_state = 0
                child_item = clicked_item.child(i)
                child_item.setBackground(TREEVIEW.item_index, TreeView.COL_TRANSPARENT)
                child_item.user_check_state = 0
                if child_item in self.checked_list:
                    self.checked_list.remove(child_item)
            # Remove data from the copy list since user unchecked item.
            for item in clicked_item.children_items:
                if item in self.local_packet_manager.copy_list:
                    self.local_packet_manager.remove_copy_item(item=item)
