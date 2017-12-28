"""
quick_Share.py (c) 2013 Walter Behrnes
Verision 1.0
Author: Walter Behrnes
Contact: walter.behrnes@gmail.com

Description:
       This is a houdini shelf script which allows a user to share copy paste
       data between another users machine.

Documentation:
       These variables should be edited in the config.py file:
           SHARE_BASE:
                This is the base directory where shared files will be stored.
                The directories in the folder must be the userLogin name.
                !!! THIS FOLDER MUST EXIST !!!
                !!! THIS FOLDER MUST HAVE SUBDIRECTORIES OF USERS !!!
           Base_PATH:
                This is the base directory where icons will live
                !!! COPY THE SUPPLIED ICONS HERE !!!
           EXLUDE:
                List of folder names to not put into autofill in option for
                user name adding.
To-do's:
   Add notes per cpio.
   Add ability to remove cpio cache
"""

# NATIVE
import os
import sys
import re
import shutil
import time

# INTERNAL
from config import Config
from data_types.constants.constant_characters import INVALID_CHARACTERS

# EXTERNAL
from hutil.Qt import QtCore

from hutil.Qt.QtGui import QColor
from hutil.Qt.QtGui import QIcon
from hutil.Qt.QtGui import QPixmap
from hutil.Qt.QtGui import QFont
from hutil.Qt.QtGui import QPalette
from hutil.Qt.QtGui import QBrush

from hutil.Qt.QtWidgets import QPushButton
from hutil.Qt.QtWidgets import QFrame
from hutil.Qt.QtWidgets import QHBoxLayout
from hutil.Qt.QtWidgets import QVBoxLayout
from hutil.Qt.QtWidgets import QLabel
from hutil.Qt.QtWidgets import QLineEdit
from hutil.Qt.QtWidgets import QMessageBox
from hutil.Qt.QtWidgets import QTreeWidgetItem
from hutil.Qt.QtWidgets import QWidget
from hutil.Qt.QtWidgets import QTabWidget
from hutil.Qt.QtWidgets import QTreeWidget
from hutil.Qt.QtWidgets import QSizePolicy
from hutil.Qt.QtWidgets import QCompleter
from hutil.Qt.QtWidgets import QScrollArea

# IF YOUR SHARE FOLDER HAS FOLDERS YOU WANT TO EXCLUDE
# EDIT THIS VALUE IN THE config.py FILE
EXCLUDE = Config.exclude
# THIS IS THE ROOT FOLDER WHERE YOUR SHARE FOLDERS EXIST.
# EDIT THIS VALUE IN THE config.py FILE
SHARE_BASE = Config.shared_temp
# BASE PATH WHERE YOUR ICONS ARE STORED
# EDIT THIS VALUE IN THE config.py FILE
BASE_PATH = Config.icons

# DO NOT EDIT
ICON_PLUS = "Copy_Color2_16x16.png"
ICON_MINUS = "Add_Blue_16x16.png"
ICON_REMOVE = "Delete_Blue_16x16.png"
ICON_NEXT = "Right_Clear_Orange_128x128.png"
ICON_MAIL = "Send_24x24.png"
ICON_PERSON = "PersonFolder_White_16x16.png"
ICON_COLLECTION = "CollectionFolder_Gray_16x16.png"
ICON_TOOL = "Tool_Gray_16x16x.png"
ICON_GET = "Get_GreenArrow_32x32.png"
ICON_CHECK = "check_box_down_transparent_16x16.png"
ICON_UNCHECK = "check_box_up_transparent_16x16.png"
ICON_TRASH = "trashcan_orange_22x22.png"
ICON_BULB = "Info_Bulb_24x24.png"

TREEVIEW_branch_closed = "stylesheet-branch-closed.png"
TREEVIEW_branch_open = "stylesheet-branch-open.png"

SHARE_TYPE = ".cpio"


COL_0 = QColor(0, 0, 0)
COL_192 = QColor(192, 192, 192)
COL_224 = QColor(224, 224, 224)
COL_240 = QColor(240, 240, 240)
COL_MIX = QColor(153, 204, 255)


class QShare(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setProperty("houdiniStyle", True)

        self.qShareObject = self
        self.counter = 0
        # CREATE A FONTS THAT WE WILL USE THROUGH OUT CLASS
        self.font = QFont("Helvetica", 9, QFont.Bold, True)
        self.font.setPixelSize(9)
        self.font_title = QFont("Helvetica", 10, QFont.Bold, True)
        self.font_title.setPixelSize(10)
        self.palette_black = QPalette()
        self.palette_black.setColor(QPalette.Foreground, QtCore.Qt.black)

        # CLASS VARS
        self.sendList = []              # USERS WE WILL SEND TO
        self.cpioList = []              # ITEMS WE WILL SEND
        self.received_cpio_list = []    # ITEMS SENT TO USER
        self.baseFolders = []           # BASE FOLDERS OF RECEIVED DATA
        self.copyList = []              # ITEMS WE WILL COPY
        self.checkedList = []           # ITEMS THAT ARE CURRENTLY CHECKED
        self.dirs = []

        # GET TEMP DIR AND USER NAME
        if 'linux' in sys.platform:
            self.cpioSender = os.environ.get("USER")
            self.cpio_temp_dir = "/tmp"
        else:
            self.cpioSender = os.environ.get("USERNAME")
            self.cpio_temp_dir = os.environ.get("TMP")

        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab1, "Send")
        self.tab_widget.addTab(self.tab2, "Manage")

        self.tree = QTreeWidget()
        self.hbox2_controls_frame = QFrame()
        self.get_cpio = QPushButton("", self)
        self.scrollArea_Frame = QFrame()
        self.scrollArea_Users = QScrollArea()
        self.userBox = QVBoxLayout()
        self.hbox_controls_frame = QFrame()
        self.packet_note = QLineEdit("PACKET NOTES", self)
        self.name_edit = QLineEdit("IDENTIFYING NAME", self)
        self.send_cpio = QPushButton("", self)

        # layout manager page 1
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(5)
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.vbox.addWidget(self.tab_widget)

        # layout for each page
        self.tab1_vbox = QVBoxLayout(self.tab1)

        # POPULATE SEND TAB page 1
        self.make_cpio_table()
        self.get_people()
        self.make_people_table()
        self.make_send_button()

        # layout for page 2
        self.tab2_vbox = QVBoxLayout(self.tab2)
        self.tab2_vbox.setAlignment(QtCore.Qt.AlignTop)

        # POPULATE Manage TAB page 2
        self.get_available_packets()
        self.make_manage_tree()
        self.tab2_vbox.addStretch(1)
        self.make_recieve_button()

        self.setLayout(self.vbox)

    def add_user_name(self):
        """
        ADD TYPED USER NAME TO SEND LIST
        """
        # GET TEXT
        text = self.sender().selfItem.text()

        if text != "":
            if text not in self.sendList:
                self.sendList.append(text)
                if text in self.dirs:
                    # FRAME TO HOLD CONTROLS HBOX
                    hbox_controls_frame = QFrame()
                    hbox_controls_frame.setFixedHeight(34)
                    # HBOX TO HOLD CONTROLS
                    hbox_controls = QHBoxLayout()

                    # ADD UPDATE BUTTON W/ ICON
                    user_update = QPushButton("", self)
                    user_update.setFlat(True)
                    user_update.setStyleSheet("QPushButton { border:none};")
                    icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_REMOVE)))
                    user_update.setIcon(icon)
                    user_update.setIconSize(QtCore.QSize(16, 16))
                    user_update.pressState = 0
                    user_update.container = hbox_controls_frame
                    user_update.selfItem = user_update
                    user_update.parent = hbox_controls_frame
                    user_update.control = hbox_controls
                    user_update.released.connect(self.qShareObject.remove_user)
                    hbox_controls.addWidget(user_update)

                    # CPIO TEXT
                    user_text = QLabel(text)
                    user_text.setStyleSheet("QWidget { color: rgb(25, 25, 25) }")
                    user_text.setFont(self.font)
                    hbox_controls.addWidget(user_text)

                    # ADD STRETCH TO PUSH UPDATE BUTTON TO RIGHT
                    hbox_controls.addStretch(1)
                    user_update.label = user_text
                    user_update.text = text

                    hbox_controls_frame.setLayout(hbox_controls)
                    self.userBox.addWidget(hbox_controls_frame)
                    self.sender().setText("")
                else:
                    title = "INVALID ENTRY"
                    message = "USE NAME DOES NOT APPEAR TO BE VALID"
                    QMessageBox.critical(None, title, message, QMessageBox.Ok)
            else:
                self.sender().setText("")

    def add_cpio_data(self):
        """
        THIS SETS THE STYLE SHEET ON THE QTGUI INSTANCE TO VISUALLY DISPLAY
        IF WE WANT TO SEND AN ITEM, IT ALSO ADDS OR REMOVES THE ITEM FROM THE SEND LIST
        """

        state = 1 - self.sender().pressState
        if state == 1:
            self.sender().info.setHidden(False)
            self.sender().line.setHidden(False)

            icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_PLUS)))
            self.sender().selfItem.setIcon(icon)
            self.sender().selfItem.setStyleSheet("QPushButton { border:none};")
            self.sender().selfItem.pressState = 1
            # ADD ITEM TO SEND LIST
            if self.sender().itemToSend not in self.cpioList:
                self.cpioList.append(self.sender())
            if len(self.cpioList) == 1:
                self.send_cpio.setDisabled(False)
        else:
            self.sender().info.setHidden(True)
            self.sender().line.setHidden(True)

            icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_MINUS)))
            self.sender().selfItem.setIcon(icon)
            self.sender().selfItem.setStyleSheet("QPushButton { border:none};")
            self.sender().selfItem.pressState = 0
            # REMOVE ITEM FROM SEND LIST
            if self.sender().itemToSend in self.cpioList:
                self.cpioList.remove(self.sender())
            if len(self.cpioList) == 0:
                self.send_cpio.setDisabled(True)

    def get_packet_data(self):
        """ 
        HANDLE PULLING CPIO DATA FROM PEOPLE FOLDER AND PLACING IN /TMP FOLDER 
        """
        for curItem in self.copyList[0]:
            exp = re.compile('[a-zA-Z_]*.cpio$')
            m = re.search(exp, curItem)
            dest = "{1}{0}{2}".format(os.sep, self.cpio_temp_dir, m.group())
            shutil.copyfile(curItem, dest)
        message = "Copy Data ready!\n\nCTRL + V in the appropriate network to past your data."
        QMessageBox.information(None, "DATA FETCHED", message, QMessageBox.Ok)

    def get_available_packets(self):
        """ 
        GET A LIST AVAILABLE PACKETS THAT USER CAN PULL 
        """

        # GET CPIO FILES
        root_dir = os.path.join(SHARE_BASE, self.cpioSender, "houdiniCpioData")
        if os.path.isdir(root_dir):
            for item in os.listdir(root_dir):
                cur_path = os.path.join(root_dir, item)
                if os.path.isdir(cur_path):
                    self.baseFolders.append(item)
                    for cpioRecieveFolder in os.listdir(cur_path):
                        current_item = os.path.join(cur_path, cpioRecieveFolder)
                        if os.path.isdir(current_item):
                            data = {'topLevel': item, 'files': [], 'path': current_item, 'folder': cpioRecieveFolder}
                            cur_item = os.path.join(cur_path, cpioRecieveFolder)
                            if os.path.isdir(cur_item):
                                for cpioFile in os.listdir(cur_item):
                                    if os.path.isfile(os.path.join(cur_item, cpioFile)):
                                        if SHARE_TYPE in cpioFile:
                                            data['files'].append(cpioFile)
                            self.received_cpio_list.append(data)

    def get_people(self):
        """
        GET A LIST OF /PEOPLE/, ADD TO WINDOW SO ARTIST CAN CHOOSE WHAT TO SEND
        """

        people_dir_content = os.listdir(SHARE_BASE)
        self.dirs = []
        for i, item in enumerate(people_dir_content):
            path = os.path.join(SHARE_BASE, item)
            if os.path.isdir(path):
                pass_check = True
                for text in EXCLUDE:
                    if text in item:
                        pass_check = False
                if pass_check:
                    self.dirs.append(item)

    def handle_clicked(self, item, column):
        """
        HANDLE CLICKED ITEMS IN SELF.TREE
        """
        clicked_item = self.tree.currentItem()
        if clicked_item.allowChecking:
            is_checked = 1 - clicked_item.userCheckState
            clicked_item.userCheckState = is_checked

            folder = None
            person = None
            the_file = None

            # GET ELEMENTS OF NOTE AND DELETE PATH
            if clicked_item.isSubFolder:
                folder = str(clicked_item.text(0))
                person = str(clicked_item.parent().text(0))
            if clicked_item.isItem:
                the_file = str(clicked_item.text(0))
                folder = str(clicked_item.parent().text(0))
                person = str(clicked_item.parent().parent().text(0))
            if not clicked_item.isItem and not clicked_item.isSubFolder:
                person = str(clicked_item.text(0))
            # READ IF CLICKED COLUMN 2
            if self.tree.currentColumn() == 2:
                user_folder = "{1}{0}{2}{0}houdiniCpioData".format(os.sep, SHARE_BASE, self.cpioSender)
                if not clicked_item.isItem and clicked_item.isSubFolder:
                    if clicked_item.isSubFolder:
                        path = "{1}{0}{2}{0}{3}".format(os.sep, user_folder, person, folder)
                        note_file = "{1}{0}Notes.txt".format(os.sep, path)
                        text = open(note_file).read()
                        QMessageBox.information(None, "Notes", text, QMessageBox.Ok)
            # DELETE IF CLICKED COLUMN 1
            if self.tree.currentColumn() == 1:
                if not clicked_item.isItem:
                    path = None
                    user_folder = "{1}{0}{2}{0}houdiniCpioData".format(os.sep, SHARE_BASE, self.cpioSender)
                    if not clicked_item.isItem and not clicked_item.isSubFolder:
                        path = "{1}{0}{2}".format(os.sep, user_folder, person)
                    if clicked_item.isSubFolder:
                        path = "{1}{0}{2}{0}{3}".format(os.sep, user_folder, person, folder)
                    if clicked_item.isItem:
                        path = "{1}{0}{2}{0}{3}{0}{4}".format(os.sep, user_folder, person, folder, the_file)
                    # PROMPT USER IF THEY WANT TO DELETE THIS ITEM
                    message = "ARE YOU SURE YOU WANT TO DELETE:\n{0}".format(path)
                    user_value = QMessageBox.critical(None, "DELETE ITEM?", message, QMessageBox.Ok, QMessageBox.Cancel)

                    if user_value == QMessageBox.Ok:
                        print("REMOVING: {0}".format(path))
                        shutil.rmtree(path)
                        for item in self.tree.selectedItems():
                            item.parent().removeChild(item)
            # UPDATE IF CHECKED COLUMN 0
            if self.tree.currentColumn() == 0:
                if self.tree.currentItem().isSubFolder:

                    if is_checked:
                        self.copyList = []  # CLEAR COPY LIST
                        # UNCHECK EVERYTHING ELSE SINCE IT IS A WHOLE PACKET WE ARE CHOOSING
                        for item in self.checkedList:
                            item.userCheckState = 0
                            if item.isSubFolder:
                                brush = QBrush(QColor(230, 230, 230))
                                item.setBackground(0, brush)
                            else:
                                brush = QBrush(QColor(240, 240, 240))
                                item.setBackground(0, brush)

                        # CLEAR CHECKED LIST
                        self.checkedList = []
                        self.checkedList.append(self.tree.currentItem())
                        for i in range(0, self.tree.currentItem().childCount()):
                            self.tree.currentItem().child(i).userCheckState = 0
                            brush = QBrush(QColor(153, 204, 255))
                            self.tree.currentItem().child(i).setBackground(0, brush)
                            self.checkedList.append(self.tree.currentItem().child(i))

                        # ADD DATA TO COPY INTO COPY LIST
                        if self.tree.currentItem().childrenItems not in self.copyList:
                            self.copyList.append(self.tree.currentItem().childrenItems)
                    else:
                        if self.tree.currentItem() in self.checkedList:
                            self.checkedList.remove(self.tree.currentItem())
                        for i in range(0, self.tree.currentItem().childCount()):
                            self.tree.currentItem().userCheckState = 0
                            self.tree.currentItem().child(i).userCheckState = 0
                            if self.tree.currentItem().child(i) in self.checkedList:
                                self.checkedList.remove(self.tree.currentItem().child(i))

                        # REMOVE DATA FROM COPY LIST
                        if self.tree.currentItem().childrenItems in self.copyList:
                            self.copyList.remove(self.tree.currentItem().childrenItems)

                if self.tree.currentItem().isItem:
                    temp_array = [self.tree.currentItem().item]
                    if is_checked:
                        if temp_array not in self.copyList:
                            self.copyList.append(temp_array)
                        if self.tree.currentItem().item not in self.checkedList:
                            self.checkedList.append(self.tree.currentItem().item)
                    else:
                        if temp_array in self.copyList:
                            self.copyList.remove(temp_array)
                        if self.tree.currentItem().item in self.checkedList:
                            self.checkedList.remove(self.tree.currentItem().item)

                # ENABLE GET CPIO IF USER HAS SOMETHING TO COPY
                if len(self.copyList) != 0:
                    self.get_cpio.setDisabled(False)
                else:
                    self.get_cpio.setDisabled(True)

    def make_manage_tree(self):
        """ 
        MAKE A TREE VIEW OF ALL A AVAILABLE COPY DATA THAT USER CAN GET
        """
        refresh = QPushButton("Refresh", self)
        refresh.pressed.connect(self.refresh_manage_tree)
        self.tab2_vbox.addWidget(refresh)
        info = QLabel("Select Copy Data To Copy Into Memory:")
        info.setFont(self.font)
        info.setPalette(self.palette_black)
        self.tab2_vbox.addWidget(info)

        # MAKE TREE
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setAllColumnsShowFocus(True)

        self.set_tree()

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setVerticalStretch(100)
        size_policy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(size_policy)

        self.tree.setColumnCount(3)
        self.tree.setColumnWidth(0, 390)
        self.tree.setColumnWidth(1, 25)
        self.tree.setColumnWidth(2, 25)
        self.tree.setGeometry(QtCore.QRect(0, 0, 400, 450))
        self.tree.setMaximumHeight(650)
        self.tab2_vbox.addWidget(self.tree)
        self.tree.itemClicked.connect(self.qShareObject.handle_clicked)

    def make_people_table(self):
        """
        ALLOW USE TO TYPE A NAME TO ADD TO THE USER LIST
        """

        info = QLabel("Type User Names To Add.[Press Enter To Add]")
        info.setFont(self.font)
        info.setPalette(self.palette_black)
        self.tab1_vbox.addWidget(info)

        line = QLineEdit("ENTER USER NAME HERE", self)
        line.mousePressEvent = lambda _: line.selectAll()
        line.setMinimumHeight(20)
        line.selfItem = line
        line.returnPressed.connect(self.add_user_name)
        completer = QCompleter(self.dirs, line)
        line.setCompleter(completer)
        self.tab1_vbox.addWidget(line)
        self.tab1_vbox.addStretch(1)

        # MAKE USER AREA SCROLLABLE
        self.scrollArea_Frame.setMinimumWidth(450)
        self.scrollArea_Users.setWidget(self.scrollArea_Frame)
        self.scrollArea_Frame.setProperty("houdiniStyle", True)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(100)

        size_policy.setHeightForWidth(self.scrollArea_Users.sizePolicy().hasHeightForWidth())
        self.scrollArea_Users.setSizePolicy(size_policy)
        self.userBox.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea_Frame.setLayout(self.userBox)
        self.scrollArea_Frame.setFrameShape(QFrame.StyledPanel)
        self.scrollArea_Users.setWidgetResizable(True)

        self.tab1_vbox.addWidget(self.scrollArea_Users)

    def make_recieve_button(self):
        """
        BOX WHICH LISTS THE ITEMS YOU WANT TO RECIEVE
        """

        # FRAME TO HOLD CONTROLS HBOX
        self.hbox2_controls_frame.setFixedHeight(50)

        # HBOX TO HOLD CONTROLS
        hbox_controls = QHBoxLayout()
        # GET YOUR DATA TEXT
        info = QLabel("GET YOUR DATA:")
        info.setFont(self.font)
        info.setPalette(self.palette_black)
        hbox_controls.addWidget(info)

        # ADD UPDATE BUTTON W/ ICON
        self.get_cpio.setStyleSheet("QPushButton { border:none};")
        self.get_cpio.setIcon(QIcon(QPixmap(os.path.join(BASE_PATH, ICON_GET))))
        self.get_cpio.setIconSize(QtCore.QSize(24, 24))
        self.get_cpio.setDisabled(True)
        self.get_cpio.released.connect(self.qShareObject.get_packet_data)
        hbox_controls.addStretch(1)
        hbox_controls.addWidget(self.get_cpio)

        self.hbox2_controls_frame.setLayout(hbox_controls)
        self.tab2_vbox.addWidget(self.hbox2_controls_frame)

    def make_send_button(self):
        """
        MAKE A BUTTON THAT SENDS THE DATA
        """

        # FRAME TO HOLD CONTROLS HBOX

        self.hbox_controls_frame.setFixedHeight(60)

        # HBOX TO HOLD CONTROLS
        hbox_controls = QHBoxLayout()

        vbox2 = QVBoxLayout()
        vbox2.setSpacing(10)
        vbox2.setAlignment(QtCore.Qt.AlignTop)

        hbox_controls.addLayout(vbox2)

        # HBOX FOR PACKET NAME
        hbox2 = QHBoxLayout()
        info = QLabel("PACKET NAME:")
        info.setFont(self.font)
        info.setPalette(self.palette_black)
        hbox2.addWidget(info)

        # EDIT
        self.name_edit.setFixedWidth(300)
        self.name_edit.setMinimumHeight(20)
        hbox2.addWidget(self.name_edit)
        vbox2.addLayout(hbox2)

        # HBOX FOR NOTE
        hbox3 = QHBoxLayout()
        # LABEL
        info = QLabel("NOTE:")
        info.setFont(self.font)
        info.setPalette(self.palette_black)
        hbox3.addWidget(info)

        # EDIT
        self.packet_note.setMinimumHeight(20)
        hbox3.addWidget(self.packet_note)
        vbox2.addLayout(hbox3)

        # ADD UPDATE BUTTON W/ ICON
        self.send_cpio.setStyleSheet("QPushButton { border:none};")
        icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_MAIL)))
        self.send_cpio.setIcon(icon)
        self.send_cpio.setIconSize(QtCore.QSize(24, 24))
        self.send_cpio.setDisabled(True)
        self.send_cpio.released.connect(self.qShareObject.send_cpio_data)
        hbox_controls.addStretch(1)
        hbox_controls.addWidget(self.send_cpio)

        self.hbox_controls_frame.setLayout(hbox_controls)
        self.tab1_vbox.addWidget(self.hbox_controls_frame)

    def make_cpio_table(self):
        """ GET A LIST OF /TMP/ CPIO FILES, ADD TO
        WINDOW SO ARTIST CAN CHOOSE WHAT TO SEND """
        cpio_info = QLabel("Select Copy Data To Send:")
        cpio_info.setFont(self.font)
        cpio_info.setPalette(self.palette_black)
        self.tab1_vbox.addWidget(cpio_info)
        # GET CPIO FILES
        files = os.listdir(self.cpio_temp_dir)
        copy_data = []
        for the_file in files:
            if ".cpio" in the_file:
                copy_data.append(the_file.strip(".cpio"))

        for i, info in enumerate(copy_data):
            # FRAME TO HOLD CONTROLS HBOX
            hbox_controls_frame = QFrame()
            hbox_controls_frame.setFixedHeight(34)

            # HBOX TO HOLD CONTROLS
            hbox_controls = QHBoxLayout()

            # ADD UPDATE BUTTON W/ ICON
            cpio_update = QPushButton("", self)
            cpio_update.setStyleSheet("QPushButton { border:none};")
            icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_MINUS)))
            cpio_update.setIcon(icon)
            cpio_update.setIconSize(QtCore.QSize(16, 16))
            cpio_update.pressState = 0
            cpio_update.container = hbox_controls_frame
            cpio_update.selfItem = cpio_update
            cpio_update.released.connect(self.qShareObject.add_cpio_data)
            hbox_controls.addWidget(cpio_update)

            # CPIO TEXT
            cpio_text = QLabel(info)
            cpio_text.setStyleSheet("QWidget { color: rgb(25, 25, 25) }")
            cpio_text.setFont(self.font)
            cpio_update.itemToSend = info
            hbox_controls.addWidget(cpio_text)

            # ADD STRETCH TO PUSH UPDATE BUTTON TO RIGHT
            hbox_controls.addStretch(1)

            info = QLabel("NOTE:")
            info.setFont(self.font)
            info.setPalette(self.palette_black)
            info.setHidden(True)
            hbox_controls.addWidget(info)

            line = QLineEdit("", self)
            line.selfItem = line
            line.setMinimumWidth(325)
            line.setHidden(True)
            cpio_update.info = info
            cpio_update.line = line
            hbox_controls.addWidget(line)

            hbox_controls_frame.setLayout(hbox_controls)
            self.tab1_vbox.addWidget(hbox_controls_frame)
        self.tab1_vbox.addSpacing(10)

    def refresh_manage_tree(self):
        """
        refresh the manage tree
        """
        self.tree.clear()
        self.received_cpio_list = []
        self.baseFolders = []
        self.get_available_packets()
        self.set_tree()

    def remove_user(self):
        """ 
        REMOVE USERS FROM SEND LIST 
        """
        self.sendList.remove(self.sender().text)
        self.sender().label.close()
        self.sender().close()
        self.userBox.removeWidget(self.sender().parent)
        self.sender().parent.setParent(None)

    def send_cpio_data(self):
        """ 
        Send cpio Data to users in list 
        """
        # CHECK  TO SEE IF USER CHANGED THE NAME OR PUT A PACKET NAME
        if self.name_edit.text() == "IDENTIFYING NAME" or not self.name_edit.text():
            title = "INVALID NAME ENTRY"
            message = "PACKET NAME DOES NOT APPEAR TO BE VALID"
            QMessageBox.critical(None, title, message, QMessageBox.Ok)
            return False

        # CHECK  TO SEE IF USER ADDED A NOTE
        if self.packet_note.text() == "PACKET NOTES" or not self.packet_note.text():
            title = "INVALID NOTE ENTRY"
            message = "PACKET NOTE DOES NOT APPEAR TO BE VALID"
            QMessageBox.critical(None, title, message, QMessageBox.Ok)
            return False

        # MAKE SURE USER IS NOT TRYING TO SEND AN INVALID CHARACTER
        for item in INVALID_CHARACTERS:
            if item in self.name_edit.text():
                title = "INVALID NAME ENTRY"
                message = "PACKET NAME APPEARS TO HAVE AN INVALID CHARACTER IN IT'S NAME"
                QMessageBox.critical(None, title, message, QMessageBox.Ok)
                return False

        localtime = time.asctime(time.localtime(time.time()))
        localtime = localtime.replace("  ", " ").replace(" ", "_")
        parts = localtime.split("_")
        send_time = "{0}_{1}_{2}".format(parts[0], parts[1], parts[2])
        packet_name = str(self.name_edit.text().replace(".", "_").replace(" ", "_"))
        # SEND THE CPIO DATA TO THE CURRENT USER(S)
        if self.sendList and self.cpioList:
            if len(self.sendList) > 0:
                for user in self.sendList:
                    if os.path.isdir(os.path.join(SHARE_BASE, str(user))):

                        path = "{0}{1}{2}_{3}".format(os.path.join(SHARE_BASE, str(user), 'houdiniCpioData',
                                                                   self.cpioSender), os.sep, send_time, packet_name)
                        file_path = "{0}{1}Notes.txt".format(path, os.sep)

                        if not os.path.isdir(path):
                            os.makedirs(path)

                        f = open(file_path, 'w')
                        packet_note = "Packet:\n{0}\n\n".format(str(self.packet_note.text()))
                        f.write(packet_note)

                        for cpio in self.cpioList:
                            if cpio.line.text():
                                note = "{0}cpio:\n{1}\n\n".format(cpio.itemToSend, str(cpio.line.text()))
                                f.write(note)

                            source = "{1}{0}{2}.cpio".format(os.sep, self.cpio_temp_dir, str(cpio.itemToSend))
                            destination = "{1}{0}{2}.cpio".format(os.sep, path, str(cpio.itemToSend))
                            print("\nCOPIED: {0} to: \n\t{1}".format(source, destination))

                            shutil.copyfile(source, destination)
                        f.close()
                title = "DATA SENT"
                message = "Copy Data Sent To User(s)!"
                QMessageBox.information(None, title, message, QMessageBox.Ok)
        else:
            title = "MISSING USERS"
            message = "PLEASE ADD A USER BEFORE TRYING TO SEND DATA!"
            QMessageBox.critical(None, title, message, QMessageBox.Ok)

    def set_tree(self):
        """
        set the contents of the receive tree
        """
        for topLevelFolder in self.baseFolders:
            # MAKE A TOP LEVEL ITEM FOR EACH USER THAT HAS SENT DATA
            top_level = QTreeWidgetItem()
            icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_PERSON)))
            top_level.setIcon(0, icon)
            icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_TRASH)))
            top_level.setIcon(1, icon)
            top_level.extra_data = False
            top_level.setFirstColumnSpanned(True)
            top_level.setText(0, topLevelFolder)
            top_level.isSubFolder = False
            top_level.isItem = False
            top_level.setFont(0, self.font)
            top_level.allowChecking = False
            top_level.userCheckState = 0
            # WE FILL IN THE TREE HERE
            for folder in self.received_cpio_list:
                if topLevelFolder in folder['topLevel']:
                    sub_folder = QTreeWidgetItem(top_level, 0)
                    sub_folder.allowChecking = True
                    sub_folder.userCheckState = 0
                    sub_folder.setText(0, folder['folder'])
                    icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_COLLECTION)))
                    sub_folder.setIcon(0, icon)
                    icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_TRASH)))
                    sub_folder.setIcon(1, icon)
                    icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_BULB)))
                    sub_folder.setIcon(2, icon)
                    sub_folder.isSubFolder = True
                    sub_folder.isItem = False
                    sub_folder.pointer = sub_folder
                    sub_folder.childrenItems = []
                    sub_folder.setFont(0, self.font)
                    for cur_file in folder['files']:
                        if ".cpio" in cur_file:
                            sub_folder_item = QTreeWidgetItem(0)
                            sub_folder_item.setText(0, cur_file)
                            sub_folder_item.allowChecking = True
                            sub_folder_item.userCheckState = 0
                            icon = QIcon(QPixmap(os.path.join(BASE_PATH, ICON_TOOL)))
                            sub_folder_item.setIcon(0, icon)
                            sub_folder_item.isSubFolder = False
                            sub_folder_item.isItem = True
                            cur_item = "{1}{0}{2}".format(os.sep, folder['path'], cur_file)
                            sub_folder_item.item = cur_item
                            sub_folder_item.pointer = sub_folder_item
                            sub_folder.addChild(sub_folder_item)
                            sub_folder.childrenItems.append(sub_folder_item.item)
                            sub_folder.addChild(sub_folder_item)
                            sub_folder_item.setFont(0, self.font)
                    top_level.addChild(sub_folder)
            # PUT THE TREE VIEW INTO PLACE
            self.tree.addTopLevelItem(top_level)
