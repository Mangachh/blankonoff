#!/usr/bin/python3
""" 
A simple script to enable/disable blanking mode & expose on xfce4 desktops, 
changes the icon on the panel launcher.
The script prevents the screensave to start.scre
"""


from dataclasses import dataclass
from genericpath import isdir
import subprocess
import os
from subprocess import CompletedProcess

@dataclass
class PathInfo:
    """Dataclass for all the path related info used in IconChanger.
    It's easy an neat to have all in the same class, this way we can
    reuse everything
    """
    
    XFCE_PATH = "/home/cobos/.config/xfce4/panel/"
    DEF_FOLDER_NAME = "launcher"
    FILE_NAME = "screen.desktop"
    
    # TODO: create fallbacks icons
    ICON_ON = "/home/cobos/code/python/Saver_plugin/on.svg"
    ICON_OFF = "/home/cobos/code/python/Saver_plugin/off.svg"
    


class Saver:    
    """Class responsible for enabling/disabling the blanking using
    subporcess.run
    All the methods are static
    """
    
    # TODO: maybe all this data in it's own class?
    XSET_OFF = "xset s off".split(" ")
    XSET_NO_BLANK = "xset s noblank".split(" ")
    XSET_NO_EXP = "xset s noexpose".split(" ")

    XSET_ON = "xset s on".split(" ")
    XSET_BLANK = "xset s blank".split(" ")
    XSET_EXPOSE = "xset s expose".split(" ")
    
    CHECK_STATUS_CMD = "xset q | grep \"prefer blanking:\""
    # oju, it has 2 spaces
    BLANKING_ON = "prefer blanking:  yes"        
        
        
    @staticmethod
    def is_enabled() -> bool:
        """
        Checks if the blanking is activated with [xset q]

        Returns:
            bool: Is the blanking activated?
        """
        res = subprocess.check_output(Saver.CHECK_STATUS_CMD, shell=True)
        
        print(f"Holaaaa {str(res)}")        
        
        if str(res).find(Saver.BLANKING_ON) != -1:
            return True
        else:
            return False      
            
    @staticmethod
    def disable_blanking() -> None:
        """Disables he blanking on screen"""
        
        (xset, blank, expose) = Saver.__change_saver_opt(Saver.XSET_OFF, Saver.XSET_NO_BLANK, Saver.XSET_NO_EXP)    
               
        print(f"Disabled Saver:\n{xset}\n{blank}\n{expose}")  
        
        
    @staticmethod
    def enable_blanking() -> None:
        """Enables the blanking on screen"""
        
        (xset, blank, expose) = Saver.__change_saver_opt(Saver.XSET_ON, Saver.XSET_BLANK, Saver.XSET_EXPOSE) 
          
        print(f"Enabled Saver:\n{xset}\n{blank}\n{expose}")   
        
     
    @staticmethod
    def opposite_saver() -> None:
        """
        If the blanking is enabled, disables it and viceversa, if the blanking is disabled, enables it.
        The method checks properly if is enabled, so it doesn't need an argument.
        """
        if Saver.is_enabled():
            Saver.disable_blanking()
        else:
            Saver.enable_blanking()
        
    @staticmethod
    def __change_saver_opt(xset: str, blank: str, expose: str) -> tuple[CompletedProcess, CompletedProcess, CompletedProcess]:
        """
        Changes the blanking options.

        Args:
            xset (str): xset s on/off CMD order 
            blank (str): xset s no/blanking CMD order
            expose (str): sxet s expose CMD order 

        Returns:
            tuple[CompletedProcess, CompletedProcess, CompletedProcess]: completed processes
        """
        xset_res = subprocess.run(xset)
        blank_res = subprocess.run(blank)
        expose_res = subprocess.run(expose)
        
        
        return (xset_res, blank_res, expose_res)
 
   
# TODO: installation of the launcher and che
class IconChanger:
    """A class that changes the icon of a launcher in a panel
    All methods are static.
    """
    
    __ICON_TXT = "Icon"
    
    @staticmethod
    def change_icon(state: bool, parent_path: str, def_name: str, file_name: str, icon_on: str, icon_off:str) -> None:
        """
        Method that changes the icon based on the passed state. 

        Args:
            state (bool): the state of the app
            parent_path (str): start searching path
            def_name (str): default name or part of the name of the folder that contains the file. 
                            As some folders are [launcher-2], [launcher-6], [launcher-n], uses a [contains]
                            to check if the folder is candidate to have the file. in this example we'll pass
                            ["launcher"] and it will check every folder which name contains ["launcher"]
                    
            file_name (str): the name of the file that we are searching
            icon_on (str): path of the icon when the state is True
            icon_off (str): path of the icon when the state is False
        """
        
        folder = IconChanger.search_path(parent_path, def_name, file_name)
        
        if folder is None or "":
            return
        
        path = f"{folder}/{file_name}"
        print(path)
        
        # read lines
        with open(path, "r") as f:
           lines = f.readlines()
            
        # write lines
        with open(path, "r+") as f:
            
            for line in lines:
                if IconChanger.__ICON_TXT in line:
                    if state is True:
                        line = f"{IconChanger.__ICON_TXT}={icon_on}\n"
                    else:
                        line = f"{IconChanger.__ICON_TXT}={icon_off}\n"
                    
                                
                f.write(line)
                
    @staticmethod
    def search_path(parent_path: str, def_name: str, file_name: str) -> str:
        """
        Returns the correct path of the launcher. First it checks on parent folder and then
        looks for any folder that contains the def_name and then looks for the file. Then
        returns the full path.
        
        If the file doesn't exists it return [""]

        Args:
            parent_path (str): start searching path
            def_name (str): default name or part of the name of the folder that contains the file. 
                            As some folders are [launcher-2], [launcher-6], [launcher-n], uses a [contains]
                            to check if the folder is candidate to have the file. in this example we'll pass
                            ["launcher"] and it will check every folder which name contains ["launcher"]
                    
            file_name (str): the name of the file that we are searching

        Returns:
            str: full path of the file if exists, [""] if not
        """
        
        print("Searching path...")
        for fn in os.listdir(parent_path):           
            if def_name in fn:                
                dir_file = os.path.join(parent_path,fn)                
                print(f"Searching in folder: {dir_file}")
                if os.path.isdir(dir_file):
                    for file in os.listdir(dir_file):
                        if file == file_name:
                            print(f"Path found at: {dir_file}")
                            return dir_file
                             
        return ""
 
    
# program run
if __name__ == "__main__":     
    # change the saver
    Saver.opposite_saver()
    
    #change the icon
    IconChanger.change_icon(Saver.is_enabled(), 
                            PathInfo.XFCE_PATH, 
                            PathInfo.DEF_FOLDER_NAME, 
                            PathInfo.FILE_NAME, 
                            PathInfo.ICON_ON, 
                            PathInfo.ICON_OFF)
    
    input("Press any key")
    
     


