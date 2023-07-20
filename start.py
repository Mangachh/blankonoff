#!/usr/bin/python3

"""
Autostart script. This scripts launches everytime the os 
starts. I got some issues with the app not savind the 
state, so based on the launcher icon, it will update the 
screensaver and the blinking of the os.

Author: Mangachh
Version: 1.5
"""

from finalSaver import Saver
from finalSaver import IconChanger
from finalSaver import PathInfo

# check the status of the icon

# if icon is off, then turn everything off
# if icon is onn, then turn everything on

def init() -> bool:
    info = PathInfo()
    path = IconChanger.search_path_info(info)
    
    
    with open(f"{path}/{info.FILE_NAME}", "r") as f:
        for line in f:
            if PathInfo.ICON_ON in line:
                Saver.enable_blanking()
                return True 
            elif PathInfo.ICON_OFF in line:
                Saver.disable_blanking()
                return True                        
                    
    return False

if __name__ == "__main__":
    if init() is False:
        print("Error, file not found")
    # input("hola")
    
    