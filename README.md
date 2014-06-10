#AutoimportSignature

## Installation

* create a new Dir in your Packages folder, mine is /home/{*****}/.config/sublime-text-2
* place `autoimport_signature.py` inside this new folder
* bind your key of choice to the command `autoimport_signature` inside KeyBinding-User file, mine is `{ "keys": ["f2"], "command": "autoimport_signature" }` 
* OPTIONALLY, you can clone the repo and give a try to the different cases.

## the first draft:

* cursor hover or selection of the implemented class (or namespace word)
* pressing a button (actual is f2)
* autoimporting of all the methods implemented and docblockr created (if none present)  