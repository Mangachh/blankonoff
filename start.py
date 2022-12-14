#!/usr/bin/python3

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
            if "State" in line:
                print(f"Found state: {line}")
                
                if "on" in line:
                    Saver.enable_blanking()
                else:
                    Saver.disable_blanking()
                
                return True                
                    
    return False

if __name__ == "__main__":
    if init() is False:
        print("Error, file not found")
    input("hola")
    
    