
# BlankOnOff

A simple plugin for the xfce4 panel that add an icon to the selected panel and when clicking it enables/disables 
the monitor blanking. This way, if the blanking is disabled, neither the screen saver neither the lock on monitor
woill turn on an


## How it works

Click on the panel launcher to set on/off the screen blinking. When clicking checks the
current state of the monitor blinking and reverse it. So, if it's enable, then disables it
and viceversa.


All the operations are done by the ``finalSaver.py`` script. Calls differents ``subprocess`` 
to enable/disable via *xset s* commands.

The icon reflects the state of the monitor:
- black moon: no-blanking, the screen saver won't turn on
- yellow moon: blanking, the screen saver will turn on if activated

The script doesn't care if the screen saver is enabled or not, neither it's existence. 
It uses ``xset s`` commands to be compatible with every xfce4 desktopt regardless the screensaver 
app.


## Installation

Download the zip and decompress wherever. Then, run the script ``setup.py``. If the desktop has more than 
one panel a screen will show up asking for the panel to show the icon. Once chosen, the script continues
without interaction.

The **setup.py** will copy all the data to **HOME/.local/share/blankonoff** . This includes the code in the zip,
the icons and a ``.desktop`` file. 

To remove, use the remove menu from the panel.


## Known issues:

 - The "xset s XX" doesn't save the state between sesions. So every new sesion the xset returns to it's original state but the plugin doesn't reflect it. 
 Posible solutions:
 -- autorun app on log-in
 -- try to save the changes between sessions


## Liscense:
Check LISCENSE.md on this repository.
	

## Icons Links

The icons used are from https://www.reshot.com
- [Icon on](https://www.reshot.com/free-svg-icons/item/moon-RA2V5ZSDFE/)
- [Icon off](https://www.reshot.com/free-svg-icons/item/moon-crescent-SD4ENBAV8K/)
	

With the [license](https://www.reshot.com/license/)
