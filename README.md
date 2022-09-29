
# BlankOnOff

A simple plugin for the xfce4 panel that enables-disables the blanking of the screen. This way the
Screen Saver doesn't start.


## How it works

Click on the panel launcher to set on/off the screen blinking.


All the operations are done by the *finalSaver.py* script. 
When clicking the pluging, first checks if the blanking is on or off with a subprocess call and
**xset q** as a command. Then, if the blanking is on, it turns it off or viceversa
using **xset s on/off** via subprocesses.

When modified the blanking state it modifies the icon to reflect the state of the blanking:
	- black moon: no-blanking, the screen saver won't turn on
	- yellow moon: blanking, the screen saver will turn on if activated

The script doesn't care if the screen saver is enabled or not. 


## Installation

Run the script **setup.py**. In case that there is more than one panel, choose the panel to put the plugin icon.
To remove the plugin, remove it like any other plugin, right click on the icon and click remove.
The **setup.py** will copy all the data to **HOME/.local/share/blankonoff** so, for reinstalling, go there
and click on **setup.py** again.


## Known issues:

 - The "xset s XX" doesn't save the state between sesions. So every new sesion the xset returns to it's original state but the plugin doesn't reflect it. 
 -- Posible solutions:
 --- autorun on log-in
 --- try to save the changes between sessions


## Liscense:

	

## Icons Links

The icons used are from: 
	- [Icon on](https://www.reshot.com/free-svg-icons/item/moon-RA2V5ZSDFE/)
	- [Icon off](https://www.reshot.com/free-svg-icons/item/moon-crescent-SD4ENBAV8K/)
	

With the [license](https://www.reshot.com/license/)
