from curses import panel
from curses.ascii import isdigit
import subprocess
import os
import shutil

# check the route of this files
# if files are NOT in the folder, move them
# when files are in folder create the launcher
# use copy, not mv.

PATH = "/.local/share/blankonoff/"
HOME = os.path.expanduser("~")
APP_NAME = "screen.desktop"


def get_installation_paths() -> tuple[str, str]:
    source = os.path.dirname(os.path.abspath(__file__))
    destination = f"{HOME}{PATH}"
    
    return (source, destination)
    
    
def create_installation_directory(source: str, destination: str) -> bool:   
    # cambiar eso para file     
    print(f"Desired Path: {destination}")
    print(f"Current Path: {source}")
    
    # if file not in path, create directories and move files
    # oju! it doesn't check if all files are in the path.
    if source != destination:
        print(f"Directories don't match.\nCheckin directory at: {destination}")
        
        # check if path exists
        if not os.path.exists(destination):
            print(f"Directory not exists. Creatring directory at: {destination}")
            try:
                os.makedirs(destination)
            except OSError:
                print(f"Creation of path {destination} failed.")
                return False
            else:
                print(f"Succefully created directory at: {destination}")
        else:
            print("Directory already exists.")
        
        #move files
        #return move_files(source, destination)
        
    
    return True           
    


def move_files(source: str, destination: str) -> bool:
    print("Copying files...")
    
    for file in os.listdir(source):
        full_sr = source + file
        full_dest = destination + file
        
        if os.path.isfile(full_sr):
            try:
                shutil.copy(full_sr, full_dest)
                print(f"Copied from {full_sr} to {full_dest}")
            except FileNotFoundError:
                print("File not found")
                return False
            except shutil.SameFileError:
                print("Origin and destination are the same")
                return True # true 'cause the files are but don't know if the app is
            except:
                print("Error")
                return False
                
    
    return True

CMD_ADD_LAUNCHER = "xfce4-panel --add=launcher"

CMD_GET_PANELS = "xfconf-query -c xfce4-panel -p /panels"
CMD_GET_IDS = "xfconf-query -c xfce4-panel -p /panels/panel-%s/plugin-ids"
CMD_GET_TYPE = "xfconf-query -c xfce4-panel -p /plugins/plugin-%s"
CMD_GET_ITEMS = "xfconf-query -c xfce4-panel -p /plugins/plugin-%s/items "


def register_to_panel() -> str:
    
    print("Adding launcher to panel")
    resp = subprocess.run(CMD_ADD_LAUNCHER, shell=True)   
    
    # get all the plugins id
    raw_ids= subprocess.check_output(CMD_GET_PANELS, shell=True).decode("UTF-8")
    print(raw_ids)
    panel_ids = [line for line in raw_ids.splitlines() if line.isdigit()]            
    
    print(panel_ids)
    final_id = ""
    
    # for each panel, look all the plugins that are launcher
    for panel in panel_ids:
        num = str(panel);
        
        raw_ids = subprocess.check_output(CMD_GET_IDS % num, shell=True).decode("UTF-8")
        plugins = [i for i in raw_ids.splitlines() if i.isdigit()]
        
        for id in plugins:
            resp = subprocess.check_output(CMD_GET_TYPE % str(id), shell=True)
            
            print(resp)
            
            if b"launcher" in resp:
                print(f"Found launcher at {id}")
                # llamamos a ver si tiene items
                resp_it = subprocess.run(CMD_GET_ITEMS % str(id), shell=True)
                
                if resp_it.returncode == 1:
                    print("Found id for new launcher")
                    return id
                
    return ""

def set_launcher(id: str, source: str, destination:str, filename:str) -> bool:
    
    try:
        os.makedirs(destination)
        shutil.copy(f"{source}/{filename}", f"{destination}/{filename}")
    except Exception as e:
        print(e)
        return False

    return True
    
    
def main():
    (source, destination) = get_installation_paths()
    created = create_installation_directory(source, destination)  
      
    if created:
        if move_files(source, destination) == False:
            return          
            
        panel_id = register_to_panel()
        
        if panel_id == "":
            return
        
        destination = HOME + "/.config/xfce4/panel/launcher-%s" % panel_id  
        set_launcher(panel_id, source, destination, APP_NAME)
         
    
if __name__ == "__main__":
    main()
    
        
        
        
        