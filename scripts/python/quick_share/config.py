"""
Name: config.py
Version: 2.0
Author: Walter Behrnes
Contact: walter.behrnes@gmail.com
Last Modified: 06/30/2020
Description:
   config.py is a module used to configure quick_share. Configuring QuickShare is pretty straight forward to set up
   and requires that you only set a few variables. They are documented below. Make sure to read the full description
   so you fully how each entry is used.

   ** Currently quick share is configured to only share between common operating systems. If you have a need to share
   cross platform, shoot me an email and I can update the code to handle this.
"""

# EXCLUDED_USERS is a comma separated list of folder names QuickShare will ignore when showing auto complete entries for
# sharable users.  It is important to understand how QuickShare determines who you can share information with.
# When transferring files, QuickShare accesses a common network folder which all users have access to.
# The folder QuickShare accesses should contain sub-folders named after the login name of the of individuals you want to
# share with. Don't worry we will talk about that folder when we get to SHARED_USERS_FOLDER. Now that we understand the
# basic idea behind how QuickShare determines who you can share with lets discuss how to ignore users or random folders
# that might be in the share folder.

# Here are some examples of how to exclude users and folders.
# To Exclude nothing: *Make sure to add a trailing comma
#    EXCLUDED_USERS = None,
# To Exclude a user add the users login name in quotes followed by a comma:
#    EXCLUDED_USERS = "Bob",
# To Exclude Several users or random folders add the items in quotes separated by commas:
#    EXCLUDED_USERS = "bob", "june, "tom", "junk_folder"
EXCLUDED_USERS = None,

# SHARED_USERS_FOLDER is the common shared directory all users can access. If this folder does not exist, you will need
# to create it. Once a user starts QuickShare a folder with their user name will automatically be created in this
# common share folder it it does not exist.
# ** To insure the paths is interpreted correctly the path should wrapped in quotes with a 'r' before the path.
# For example:
#    SHARED_USERS_FOLDER = r"C:\Users\waldo\Dropbox\users"
SHARED_USERS_FOLDER = r"c:\Users\waldo\Dropbox\users"
