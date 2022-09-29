
# BlankOnOff

A simple plugin for the xfce4 panel that enables-disables the blanking of the screen. This way the
Screen Saver doesn't start.


## How it works

Click on the panel launcher to set on/off the screen blinking.


All the operations are done by the *finalSaver.py* script (to be renamed). 
First the script checks if the blanking is on or off with a subprocess and
**xset q** as a command. Then, if the blanking is on, it turns it off or viceversa
using **xset s on/off** via subprocesses.

Then it changes the icon of the launcher if exists. The launcher is put on hand and
an installer is on it's way.


## Installation
Put the scripts and icons in the desired folder. Then change de route of the icons in the **finalSaver.py** 
script. Then create the panel launcher and change it's name to **screen.desktop**. 


TODO: make an installer to put files on the right folder and create the launcher.


## Known issues:

**Worth checking**: it seems that the changes doesn't last when the session is over. So, if by default the blinking is **on**, 
then in every new run the blinking is going to be **on** regardless the app.


## Liscense:

	

## Icons Links

	- icon on: https://www.reshot.com/free-svg-icons/item/moon-RA2V5ZSDFE/
	- icon off: https://www.reshot.com/free-svg-icons/item/moon-crescent-SD4ENBAV8K/