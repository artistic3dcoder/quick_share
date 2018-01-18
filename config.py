"""
Name: config.py
Version: 1.0
Author: Walter Behrnes
Contact: walter.behrnes@gmail.com
Last Modified: 01/16/2018
Description:
   config.py is a module used to configure quick_share
Example:
    import config
Requires:

"""

# NATIVE
import os
import getpass
from os.path import expanduser


class QuickShareConfig(object):
    """
    Config is essentially a repository for Global values used through out coding
    """

    # DERIVED CONSTANTS: DO NOT EDIT THIS SECTION
    user_name = getpass.getuser()
    user_home = expanduser("~")
    os_name = os.name
    system_temp = os.environ.get("TMP")

    # configure root pathing.
    # edit this as needed.
    win_root = "C:"
    linux_root = "/"
    # SET ROOT BASED ON OS
    if os.name == 'nt':
        root = win_root
    else:
        root = linux_root

    # THIS SEEMS TO BE A BUG BETWEEN 2.7 AND 3
    if "Documents" in user_home:
        user_home = user_home.replace("Documents", "")
    if "\\" in user_home:
        user_home = user_home.replace("\\", "/")

    # specify the root folder where your code lives
    # this was setup to work on a network folder.
    # the initial configuration is setup to use dropbox located in the users home folder.
    network = '{0}/Dropbox'.format(user_home)

    # code is a common code directory  where code and icon data for code lives
    # the initial configuration was setup to work from the network folder.
    # change this as needed.
    code = '{0}/coding'.format(network)

    # temp is where time files wll be stored.
    # This will be used by applications which need to store temporary files
    # edit / create this folder if needed.
    temp = "{0}/tmp".format(root)

    # this is the common shared directory all users can access.
    # this was initially setup to use the network folder, change as needed.
    shared_temp = "{0}/shared".format(network)

    # location where icon files live. 
    # this folder will need to be created and icons will need to be placed here.
    icons = "{0}/icons/tools/quick_share".format(code)

    # these are folders you do not want quick_share to see.
    # edit as needed.
    exclude = ["character"]

    # HERE WE ARE CONFIGURING THE ICONS USED BY THE GUI
    icon_plus = os.path.join(icons, "Copy_Color2_16x16.png")
    icon_minus = os.path.join(icons, "Add_Blue_16x16.png")
    icon_remove = os.path.join(icons, "Delete_Blue_16x16.png")
    icon_next = os.path.join(icons, "Right_Clear_Orange_128x128.png")
    icon_mail = os.path.join(icons, "Send_24x24.png")
    icon_person = os.path.join(icons, "PersonFolder_White_16x16.png")
    icon_collection = os.path.join(icons, "CollectionFolder_Gray_16x16.png")
    icon_tool = os.path.join(icons, "Tool_Gray_16x16x.png")
    icon_get = os.path.join(icons, "Get_GreenArrow_32x32.png")
    icon_check = os.path.join(icons, "check_box_down_transparent_16x16.png")
    icon_uncheck = os.path.join(icons, "check_box_up_transparent_16x16.png")
    icon_trash = os.path.join(icons, "trashcan_orange_22x22.png")
    icon_bulb = os.path.join(icons, "Info_Bulb_24x24.png")

    # CONFIGURE THE SHARE DATA TYPE. FOR HOUDINI WE ARE SETTING THIS TO .cpio
    # QuickShare COULD EASILY BE MODIFIED TO WORK WITH OTHER 3D APPS THAT
    # STORE THEIR COPY PASTE MEMORY TO DISK. (like Maya, or Nuke)
    share_type = ".cpio"

    # CONFIGURE CHARACTERS WE WILL CONSIDER INVALID FOR USE
    invalid_characters = ["*", "#", "!", "%", "&", "^", "(", ")", "@", "$", "~", ",", ".", ";", "/", "{", "}", "[", "]",
                          "|", "\\", ":", "\\t", "\\n", "?", "<", ">"]