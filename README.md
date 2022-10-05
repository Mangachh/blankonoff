
# BlankOnOff

A simple plugin for the ``xfce4 panel`` that add's an icon to the selected panel and when clicking it enables/disables 
the monitor blanking and computer suspension. This way, if the blanking is disabled, neither the screen saver neither the lock on monitor
will turn on. 
It's perfect for working, watching some Youtube videos or needing the desktop fully ON regardless not inserting input.


## How to use it & how it works

Click on the panel launcher icon to set on/off the screen blinking. When clicking checks the
current state of the monitor blinking and reverse it. So, if it's enable, then disables it
and viceversa.


All the operations are done by the ``finalSaver.py`` script that calls differents ``subprocess`` 
to enable/disable the settings via ``xset s`` commands and ``xfconf-query``

The icon reflects the state of the monitor:
- black moon: no-blanking, the screen saver won't turn on and the computer won't go to slee modep.
- yellow moon: blanking, the screen saver will turn on if activated and computer will go to sleep mode.

The script doesn't care if the screen saver is enabled or not, neither it's existence. 
It uses ``xset s`` commands to be compatible with every xfce4 desktopt regardless the screensaver 
app.

In addition, it turns on/off the ``Presentation Mode`` in the Power Management to disable
it's settings. This way the computer won't turn off, go to sleep mode and so on.


## Installation

Download the zip and decompress wherever. Then, run the script ``setup.py``. If the desktop has more than 
one panel a screen will show up asking for the panel to show the icon. Once chosen, the script continues
without interaction.

The ``setup.py`` will copy all the data to **HOME/.local/share/blankonoff** . This includes the code in the zip,
the icons and a ``.desktop`` file. 

To remove, use the remove menu from the panel.


## Known issues:

 - The "xset s XX" shares the state between sessions. There is a launcher on ``$HOME/.config/autostart`` that calls
 ``start.py ``, checks the state and enables/disables the blanking, saving, etc. For some reason, the launcher located
 in ``$HOME/.config/autostart`` has to had the ``Console=true`` property to work properly. I don't really know why,
 but I guess there's something with the ``subprocess.run()`` that doesn't run on autostart.

 ## TODO:
 - Create a state on the panel launcher instead of reading the name of the icon


## Liscense:
Check LISCENSE.md on this repository.
	

## Icons Links

The icons used are from https://www.reshot.com
- On Icon: Sligtly modified to be bigger. This is the base of the off icon too.  https://www.reshot.com/free-svg-icons/item/moon-RA2V5ZSDFE/
- Original Off Icon: https://www.reshot.com/free-svg-icons/item/moon-crescent-SD4ENBAV8K/
	

[License](https://www.reshot.com/license/) for the icons.
