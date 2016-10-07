# plasma-transparent-panel
A script and a GUI that create a new plasma with a specific panel fully trasparent based on another theme

## Introduction
The script takes as arguments the name of an installed plasma theme and in what panel we need transparency. And in that way it creates a new theme that provides that transparency. The new theme can be enabled as all the installed workspace theme from the system settings. The script disables some panel shadows in order to provide that transparency correctly and informs the user what shadows disabled, but it gives also the choice to the user to enable any shadow he wants

## Requirements
You must disable the following **Desktop Effects** in **Plasma**:
- **Blur**
- **Background Contrast**

Examples
--------
    From GUI (graphical way):
    click on, transparent.sh
    
    From command line:
    python transparentpanel.py --list
             ///shows all installed themes
  
    python transparentpanel.py breeze-dark West
             ///it will create a new Breeze Dark theme with the West panel transparent
  
    python transparentpanel.py breeze-dark South bottom topright
             ///it will create a new Breeze Dark theme with the South panel transparent and also the bottom and the topright shadows will be shown including those the script chose
