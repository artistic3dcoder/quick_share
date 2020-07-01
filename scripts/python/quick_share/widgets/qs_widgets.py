from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QPushButton, QLabel, QLineEdit, QMessageBox, QSpacerItem, QGridLayout


def critical_message(title, message, cancel_button=False):
    """Provide a critical message box.

    Args:
        title (str): Title of message box
        message (str): Message to display in message box.
        cancel_button (bool): Add a cancel button.

    Returns:
        bool: True is end user presses Ok, False if end user presses cancel.
    """
    print("Critical yo")
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setIcon(QMessageBox.Critical)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint)
    if cancel_button:
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    result = message_box.exec_()
    print("OK")
    return result == QMessageBox.Ok


def info_message(title, message):
    """Provide an informative message box.

    Args:
        title (str): Title of message box
        message (str): Message to display in message box.

    Returns:
        None
    """
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setIcon(QMessageBox.Information)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint)
    message_box.exec_()
    """
    QMessageBox msgBox;
    msgBox.setText("The deck is empty!");
    msgBox.setInformativeText("Do you want to start a new deck?");
    msgBox.setIcon(QMessageBox::Question);
    msgBox.setStandardButtons(QMessageBox::Yes | QMessageBox::No);
    msgBox.setBaseSize(QSize(600, 120));
    int r = msgBox.exec();
    if(r==QMessageBox::Yes)
    
    """


def create_icon(path):
    """Create an icon given a path to the image source.

    Args:
        path (str): Full path to the icon image.
        name (str, optional): Object name applied to icon.

    Returns:
        QIcon
    """
    icon = QIcon(QPixmap(path))

    return icon


def create_icon_button(parent, path, size, name):
    """Create a QPushbutton with an icon.

    Args:
        parent (QWidget): Parent widget.
        path (str): Full path to the icon.
        size (tuple (int, int)): Size of icon.
        name (str, optional): Object name applied to QPushButton.
    """
    widget = QPushButton(parent)
    widget.setFlat(True)
    icon = create_icon(path=path)
    widget.setIconSize(QSize(*size))
    widget.setFixedSize(*size)
    widget.setIcon(icon)
    if name:
        widget.setObjectName(name)

    return widget


def create_label(width, height, text, transparent=True):
    """"Create a QLabel with a minimum width and height and applied text.

    Args:
        width (int): Minimum width of widget.
        height (int): Minimum height of widget.
        text (str): Text applied to label.
        transparent (bool, optional): Apply a transparent background widget.
                                      Default True.

    Returns:
        QLabel
    """
    widget = QLabel(text)
    widget.setMinimumSize(width, height)
    if transparent:
        widget.setAttribute(Qt.WA_TranslucentBackground, True)
        widget.setAttribute(Qt.WA_NoSystemBackground, True)

    return widget


def create_line_edit(height, text=None, obj_name=None):
    """"Create a QLineEdit with a minimum height applied.

    Args:
        height (int): Minimum height of widget.
        text (str, optional): Text applied to widget.
        obj_name (str, optional):


    Returns:
        QLabel
    """
    widget = QLineEdit(text)
    widget.setMinimumHeight(height)
    if text:
        widget.setText(text)
    if obj_name:
        widget.setObjectName(obj_name)

    return widget


def create_spacer_item(size):
    """Create a QSpacerItem.

    Args:
        size (tuple (int, int)): size of spacer (width, height)

    Returns:
        QSpacerItem
    """
    return QSpacerItem(*size)
