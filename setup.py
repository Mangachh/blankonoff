import subprocess
import os
import shutil

# check the route of this files
# if files are NOT in the folder, move them
# when files are in folder create the launcher
# use copy, not mv.

PATH = "/.local/share/blankonoff/"


def create_directory() -> bool:    
    home = os.path.expanduser('~')
    source = f"{os.getcwd()}/"
    destination = f"{home}{PATH}"
    
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
        return move_files(source, destination)
        
    
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
            except:
                print("Error")
                return False
                
    
    return True



if __name__ == "__main__":
    created = create_directory()
    
    if created:
        # register the launcher
        pass
    
        
        
        
        