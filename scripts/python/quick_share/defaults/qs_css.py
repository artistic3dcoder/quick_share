CSS = """
QWidget {
    background-color: #b5c0c9;
    font-weight: normal;
    font-size: 7pt;
    font-weight: 500;
    color: #000000; 
}

QFrame#SharableItem {
    background-color: #b5c0c9;
    border: 2px solid #81888f;
    border-radius: 6px;
}

QFrame#SendFrame {
    background-color: #b5c0c9;
    border: 2px solid #81888f;
    border-radius: 6px;
}

QFrame#ReceiveView {
    background-color: #81bef0;
    border-radius: 3;
}

QFrame#SelectedUsers {
    border: 2px solid #81888f;
    border-radius: 6px;
}

QFrame#SendToUser {
    background-color: #81bef0;
    border-radius: 3;
}

QWidget#Users {
    background-color: #81bef0;
    border-radius: 20;
}

QPushButton#Send {
    background-color: #b5c0c9;
}

QPushButton#Refresh {
    background-color: #b5c0c9;
    border: 1px solid #81888f;
    border-radius: 3px;
}
QPushButton:hover#Refresh {
    background-color: #81bef0;
    border: 1px solid #81888f;
    border-radius: 3px;
}

QPushButton#UserIcon{
    background-color: #b5c0c9;
}

QPushButton#GetShare{
    background-color: #81bef0;
}

QLineEdit#Finder {
    background-color: #81bef0;
    border: 2px solid #81888f;
    border-radius: 6px;
    color: #000000; 
}

QLineEdit#Packet {
    background-color: #81bef0;
    border: 2px solid #81888f;
    border-radius: 6px;
    color: #000000; 
}

QLineEdit#PacketNote {
    background-color: #81bef0;
    border: 2px solid #81888f;
    border-radius: 6px;
    color: #000000; 
}

QLineEdit#UpdateShare {
    background-color: #b5c0c9;
    border-radius: 3;
    color: #000000; 
}

QLineEdit#SharableNote {
    background-color: #81bef0;
    border: 2px solid #81888f;
    border-radius: 6px;
    color: #000000; 
}

QTreeWidget::item:pressed,QTreeWidget::item:selected{
    background-color:#81bef0;
    color: #000000;
}

QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(icons/vline.png) 0;
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(icons/branch-more.png) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(icons/branch-end.png) 0;
}

QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {
        border-image: none;
        image: url(icons/branch-closed.png);
}

QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings  {
        border-image: none;
        image: url(icons/branch-open.png);
}

QLabel {
    color: #000000;   
}

QTabWidget::pane { /* The tab widget frame */
    border: 2px solid #81888f;
}

QTabWidget::tab-bar {
    left: 5px; /* move to the right by 5px */
}

QTabBar::tab {
    background: #b5c0c9;
    border: 2px solid #81888f;
    border-bottom-color: #b5c0c9; /* same as the pane color */
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 8ex;
    padding: 2px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: #81bef0;
}

QTabBar::tab:selected {
    border-color: #81888f;
    border-bottom-color: #81bef0; /* same as pane color */
}

QTabBar::tab:!selected {
    border-color: #81888f;
    border-bottom-color: #b5c0c9; /* same as pane color */
    margin-top: 2px; /* make non-selected tabs look smaller */
}
"""
