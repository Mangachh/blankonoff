#!/usr/bin/python3
'''
A simple script to create a "not disturb" mode. Instead of disabling the screen saver
it uses xset s settings. 

'''


from genericpath import isdir
import subprocess
import os
from subprocess import CompletedProcess

# TODO: all methods are static methods, maybe
class Saver:
    '''
    Class for enable or disable the screensaver. 
    It uses xset s options to assure compatibility.
    '''
    
    XSET_OFF = "xset s off".split(" ")
    XSET_NO_BLANK = "xset s noblank".split(" ")
    XSET_NO_EXP = "xset s noexpose".split(" ")

    XSET_ON = "xset s on".split(" ")
    XSET_BLANK = "xset s blank".split(" ")
    XSET_EXPOSE = "xset s expose".split(" ")
    
    CHECK_STATUS_CMD = "xset q | grep \"prefer blanking:\""
    # oju, it has 2 spaces
    BLANKING_ON = "prefer blanking:  yes"        
        
        
    @property
    def is_enabled(self) -> bool:
        '''Is the screensaver enabled? Checks using \"xset q\"'''
        res = subprocess.check_output(Saver.CHECK_STATUS_CMD, shell=True)
        
        print(f"Holaaaa {str(res)}")        
        
        if str(res).find(Saver.BLANKING_ON) != -1:
            return True
        else:
            return False      
            
        
    def disable_screen_saver(self) -> None:
        ''' Disables screensaver '''
        (xset, blank, expose) = Saver.__change_saver_opt(Saver.XSET_OFF, Saver.XSET_NO_BLANK, Saver.XSET_NO_EXP)    
               
        print(f"Disabled Saver:\n{xset}\n{blank}\n{expose}")  
        

    def enable_screen_saver(self) -> None:
        ''' Enables screensaver '''
        (xset, blank, expose) = Saver.__change_saver_opt(Saver.XSET_ON, Saver.XSET_BLANK, Saver.XSET_EXPOSE) 
          
        print(f"Enabled Saver:\n{xset}\n{blank}\n{expose}")   
        
     
    def opposite_saver(self) -> None:
        '''If the screensaver is enabled, disables it and viceversa'''
        if self.is_enabled:
            self.disable_screen_saver()
        else:
            self.enable_screen_saver()
        
    @staticmethod
    def __change_saver_opt(xset: str, blank: str, expose: str) -> tuple[CompletedProcess, CompletedProcess, CompletedProcess]:
        '''Changes the xset s options'''
        xset_res = subprocess.run(xset)
        blank_res = subprocess.run(blank)
        expose_res = subprocess.run(expose)
        
        
        return (xset_res, blank_res, expose_res)
 
   
# TODO: installation of the launcher and che
class ChangerIcon:
    '''A class that changes the icon for the launcher at panel.
    Hardcoded name at the moment'''
    # hardcoded, later we'll search
    
    __XFCE_PATH = "/home/cobos/.config/xfce4/panel/"
    
    __DEF_FOLDER_NAME = "launcher"
    __FILE = "screen.desktop"
    
    # TODO: create fallbacks icons
    __ICON_ON = "/home/cobos/code/python/Saver_plugin/on.svg"
    __ICON_OFF = "/home/cobos/code/python/Saver_plugin/off.svg"
    __ICON_TXT = "Icon"
    
    @staticmethod
    def change_icon(state: bool) -> None:
        '''Method that changes the icon based on the state'''
        folder = ChangerIcon.search_path()
        
        if folder is None or "":
            return
        
        path = f"{folder}/{ChangerIcon.__FILE}"
        print(path)
        
        # read lines
        with open(path, "r") as f:
           lines = f.readlines()
            
        # write lines
        with open(path, "r+") as f:
            
            for line in lines:
                if ChangerIcon.__ICON_TXT in line:
                    if state is True:
                        line = f"{ChangerIcon.__ICON_TXT}={ChangerIcon.__ICON_ON}\n"
                    else:
                        line = f"{ChangerIcon.__ICON_TXT}={ChangerIcon.__ICON_OFF}\n"
                    #
                #
                
                f.write(line)
                
    @staticmethod
    def search_path() -> str:
        '''Searchs for the correct path of the launcher. Returns empty if not exists'''
        print("Searching path...")
        for fn in os.listdir(ChangerIcon.__XFCE_PATH):           
            if ChangerIcon.__DEF_FOLDER_NAME in fn:                
                dir_file = os.path.join(ChangerIcon.__XFCE_PATH,fn)                
                print(f"Searching in folder: {dir_file}")
                if os.path.isdir(dir_file):
                    for file in os.listdir(dir_file):
                        if file == ChangerIcon.__FILE:
                            print(f"Path found at: {dir_file}")
                            return dir_file
                        #
                    #
                #
            #
        #
        
        return ""
 
    
# program run
if __name__ == "__main__": 
    s = Saver()
    s.opposite_saver()
    ChangerIcon.change_icon(s.is_enabled)
    
    input("Press any key")
    
     


