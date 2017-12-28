# quick_share
quick_Share is a Houdini copy/paste sharing application which allows user to share their current clipboard with another Houdini user.

## Icons:
These are free icons that came from http://www.iconarchive.com.
If you want to change out your icons they have a very good selection.

## Interface Images:
[logo]: https://github.com/walterbehrnes/quick_share/quick_share_example.jpg "Example Image"

## Usage Requirements:
This application works by storing shared data in a common directory all users hav access to. The common diretory should have a folder for each user. Each user folder should be named after their login name for the computer they are using. 

Before using the script you will need to edit the top part of the script. It has a few variable that need to be set. After the variables have been set, make a shelf button and past the code in, or link to the code through the shelf button. 

- SHARE_BASE:Directory where share files will be stored. A folder for each user should exist in the share base.
- BASE_PATH:Directory where icons will live
- EXLUDE:List of folder names to ignore when listing users to share data with. 

To copy data: 
Simply Ctrl_C in houdini, in your desired view. Open quick_share, select the cpio data you want to send, add a user, and send. 

To recieve data:
Open quick_share, go to the manage tab, select the data you want to get, and press the get button. Ctrl_V into the appropriate view.
