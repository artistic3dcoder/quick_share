"""
Name: config.py
Version: 1.0
Author: Walter Behrnes
Contact: walter.behrnes@gmail.com
Last Modified: 102/08/2017
Description:
   config.py is a module used to configure quick_share
Example:
    import config
Requires:

"""

# NATIVE
import os
import sys
import getpass
from os.path import expanduser


class Config(object):
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
    # the initial configuration was setup to use dropbox
    network = '{0}/Dropbox'.format(user_home)

    # code is a common code direcotry  where code and icon data for code lives
    # the initial configuration was setup to work from the network folder.
    # change this as needed.
    code = '{0}/coding'.format(network)

    # temp is where time files wll be stored.
    # This will be used by applications which need to store temporary files
    # edit / createt this folder if needed.
    temp = "{0}/tmp".format(root)

    # this is the common shared direcotry all users can access.
    # this was initially setup to use the network folder, change as needed.
    shared_temp = "{0}/shared".format(network)

    # location where icon files live. 
    # this folder will need to be created and icons will need to be placed here.
    icons = "{0}/icons/tools/quick_share".format(code)

    # these are folders you do not want quick_share to see.
    # edit as needed.
    exclude = ["character"]

    def __init__(self):
        pass
