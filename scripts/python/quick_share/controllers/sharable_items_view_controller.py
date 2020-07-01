from quick_share.views.sharable_items_view import SharableItemsView


class SharableItemsViewController(object):
    """Controls interactions with the SharableItemsView.

    Attributes:
        view (SharableItemsView): View associated with controller.
    """
    def __init__(self):
        self.view = SharableItemsView()

    @property
    def parent(self):
        return self.view.parent()

    def add_widget(self, widget):
        """Add a ShareItemView widget to the view.

        Args:
            widget (ShareItemView): Widget to add.

        Returns:
            None
        """
        self.view.layout.addWidget(widget)

    def add_spacer(self, spacer):
        """Add a QSpacerItem to the view.

        Args:
            spacer (QSpacerItem): Spacer to add to view.

        Returns:
            None
        """
        self.view.layout.addSpacerItem(spacer)
