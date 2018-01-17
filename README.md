# quick_share
quick_Share is a Houdini copy/paste sharing application which allows user to share their current clipboard with another Houdini user.

## Icons:
These are free icons that came from http://www.iconarchive.com.
If you want to change out your icons they have a very good selection.

## Interface Images:
!["Example Image"](/images/quick_share_example.jpg)

## Usage Requirements:
This application works by storing shared data in a common directory all users hav access to. The common diretory should have a folder for each user. Each user folder should be named after their login name for the computer they are using. 

Before using the script you will need to edit the config.QuickShareConfig class to configure QuickShare to your system. Play close attention on how the pathing is built up. Ultimately you are interested in the end result of the shared_temp, exclude, and icons folder live. If these folders do not exist you will need to make them.

To copy data: 
Simply Ctrl_C in houdini, in your desired view. Open quick_share, select the cpio data you want to send, add a user, and send. 

To recieve data:
Open quick_share, go to the manage tab, select the data you want to get, and press the get button. Ctrl_V into the appropriate view.
