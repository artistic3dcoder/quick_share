from sys import argv, exit
from os.path import dirname, abspath, join, isdir, exists
from os import listdir

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt


def load_modules():
    """Dynamically load modules."""
    root = dirname(__file__)
    dir = []
    for d in listdir(root):
        s = join(abspath(root), d)
        if isdir(s) and exists(join(s, "__init__.py")):
            dir.append(d)
    for d in dir:
        __import__("quick_share." + d, fromlist=["*"])


try:
    load_modules()
except Exception:
    pass

from defaults import qs_css, quick_share_prefs
from views import quick_share_view
from models import combined_share_data
from widgets import qs_widgets
import quick_share_controller

QUICK_SHARE = None


def show_python_panel():
    """Instantiate QuickShare for a Houdini python panel.

    Returns:
        QWidget
    """
    controller = quick_share_controller.QuickShareController()
    return controller.view


def show():
    """Instantiate a free standing QuickShare view.

    Returns:
        None
    """
    global QUICK_SHARE
    QUICK_SHARE = quick_share_controller.QuickShareController()
    QUICK_SHARE.view.show()


def reload_modules():
    """Reload all modules related to QuickShare.

    Returns
        None
    """
    reload(quick_share_prefs)
    reload(qs_css)
    reload(combined_share_data)
    reload(qs_widgets)
    reload(quick_share_view)
    reload(quick_share_controller)


if __name__ == "__main__":
    app = QApplication(argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_DisableHighDpiScaling)
    ex = quick_share_controller.QuickShareController()
    ex.show()
    exit(app.exec_())
