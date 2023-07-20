#!/usr/bin/python3

""" 
A simple script to enable/disable blanking mode & expose on xfce4 desktops, 
changes the icon on the panel launcher.
The script prevents the screensave to start.

Author: Mangachh
Version: 1.0
"""


from dataclasses import dataclass
from faulthandler import is_enabled
import subprocess
import os
from subprocess import CompletedProcess

from cairo import SubpixelOrder

@dataclass
class PathInfo:
    """Dataclass for all the path related info used in IconChanger.
    It's easy an neat to have all in the same class, this way we can
    reuse everything
    """
    HOME = os.path.expanduser('~')
    PARENT_FOLDER = HOME + "/.config/xfce4/panel/"
    DEF_FOLDER_NAME = "launcher"
    FILE_NAME = "blankonoff.desktop"
    
    # TODO: create fallbacks icons    
    ICON_ON = f"{HOME}/.local/share/blankonoff/on.svg"
    ICON_OFF = f"{HOME}/.local/share/blankonoff/off.svg"
    
    


class Saver:    
    """Class responsible for enabling/disabling the blanking using
    subporcess.run
    All the methods are static
    """
    
    # TODO: maybe all this data in it's own class?
    XSET_OFF = "xset s off"
    XSET_NO_BLANK = "xset s noblank"
    XSET_NO_EXP = "xset s noexpose"
    XSET_NO_DPMS = "xset -dpms"
    XPOWER_NO_PRES = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/presentation-mode -s false"

    XSET_ON = "xset s on"
    XSET_BLANK = "xset s blank"
    XSET_EXPOSE = "xset s expose"
    XSET_DPMS = "xset +dpms"
    XPOWER_PRES = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/presentation-mode -s true"
    
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
        
        return str(res).find(Saver.BLANKING_ON) != -1
        
        # if str(res).find(Saver.BLANKING_ON) != -1:
        #     return True
        # else:
        #     return False      
            
    @staticmethod
    def disable_blanking() -> None:
        """Disables he blanking on screen"""
        
        Saver.__change_saver_opt(Saver.XSET_OFF, Saver.XSET_NO_BLANK, Saver.XSET_NO_EXP, Saver.XSET_NO_DPMS, Saver.XPOWER_PRES)                  
         
        
        
    @staticmethod
    def enable_blanking() -> None:
        """Enables the blanking on screen"""
        
        Saver.__change_saver_opt(Saver.XSET_ON, Saver.XSET_BLANK, Saver.XSET_EXPOSE, Saver.XSET_DPMS, Saver.XPOWER_NO_PRES) 
          
        
        
     
    @staticmethod
    def opposite_saver() -> bool:
        """
        If the blanking is enabled, disables it and viceversa, if the blanking is disabled, enables it.
        The method checks properly if is enabled, so it doesn't need an argument.
        """
        if Saver.is_enabled():
            Saver.disable_blanking()
            return False
        else:
            Saver.enable_blanking()
            return True
        
    @staticmethod
    def __change_saver_opt(xset: str, blank: str, expose: str, dpms: str, pres_mode: str) -> None:
        """
        Changes the blanking options.

        Args:
            xset (str): xset s on/off CMD order 
            blank (str): xset s no/blanking CMD order
            expose (str): sxet s expose CMD order 

        Returns:
            None
        """
        dpms_res = subprocess.run(dpms, shell=True)
        pres_res = subprocess.run(pres_mode, shell=True)
        
        xset_res = subprocess.run(xset, shell=True)
        blank_res = subprocess.run(blank, shell=True)
        expose_res = subprocess.run(expose, shell=True)       
        
        print("Printing responses...")
        print(f"{dpms_res}\n{pres_res}\n{xset_res}\n{blank_res}\n{expose_res}")
    
 
   
# TODO: installation of the launcher and che
class IconChanger:
    """A class that changes the icon of a launcher in a panel
    All methods are static.
    """
    
    __ICON_TXT = "Icon"
    
    def change_icon_w_info(state: bool, data: PathInfo) -> None:
        """Changes the icon using the class PathInfo to get all the data needed

        Args:
            state (bool): state of the app
            data (PathInfo): info of the paths
        """
        
        IconChanger.change_icon(state, 
                                PathInfo.PARENT_FOLDER, 
                                PathInfo.DEF_FOLDER_NAME, 
                                PathInfo.FILE_NAME, 
                                PathInfo.ICON_ON, 
                                PathInfo.ICON_OFF)
        
        
        
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
        
        # read lines
        with open(path, "r") as f:
           lines = f.readlines()
            
        # write lines
        print("Reading file...")
        icon_p : str
        with open(path, "r+") as f:
            
            # Rewrites the launcher file, change the icon
            for line in lines:              
                if IconChanger.__ICON_TXT in line:
                    if state is True:   
                        icon_p = f"{IconChanger.__ICON_TXT}={icon_on}\n"                         
                    else:
                        icon_p = f"{IconChanger.__ICON_TXT}={icon_off}\n"    
                        
                    line = icon_p
                    print(f"Icon line found. Writing: {icon_p}")
                                
                f.write(line)
        
        print("File writed...")        
    
    
        
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
        
        # ugly
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
 
 
    @staticmethod 
    def search_path_info(info: PathInfo) -> str:
        return IconChanger.search_path(info.PARENT_FOLDER, info.DEF_FOLDER_NAME, info.FILE_NAME)
    
# program run
if __name__ == "__main__":     
    
    is_enabled = Saver.opposite_saver()
    
    #change the icon
    IconChanger.change_icon_w_info(is_enabled, PathInfo)
    input("Press any key")
    
     


