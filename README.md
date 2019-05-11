# Toontown 2013 Source

The python source code for Disney's now discontinued MMO, Toontown Online. All code is fomatted to [pycodestyle](https://github.com/PyCQA/pycodestyle) guidelines. 

### Game Dependencies

- Download and install [Panda3D-1.7.2](https://www.panda3d.org/download/sdk-1-7-2/)
- Download and install [setuptools](https://files.pythonhosted.org/packages/b8/04/be569e393006fa9a2c10ef72ea33133c2902baa115dd1d4279dae55c3b3b/setuptools-36.8.0.zip)
- Download and install [pytz (TAR file)](https://pypi.org/project/pytz/#files)

To install **setuptools** and **pytz** (in that order!) simply execute
```sh
path\to\panda\python\ppython.exe setup.py install
```

### UD/AI Dependencies
***ATTENTION!*** If you already downloaded the Panda3D version for OTP server on the OTP repository skip this step.
In order to run the AI, UD *(and the server)* you need a special Panda3D version which can be obtained [here](https://www.dropbox.com/s/0i7puwbqz9b4wt9/Panda3D-1.10.0-x64.exe?dl=1) ***(Alternatively, you can build it yourself [here](https://github.com/Astron/panda3d))***

### Running the UD
Once you've obtained the correct Panda for the UD, if you wish, create a BAT file to automate the running process.
```sh
@echo off
path\to\>>>>>>UD<<<<<<\panda\python\ppython main_ud.py
pause
```
***Make sure you have the server up and running before running the UD!***

### Running the AI
Once you've obtained the correct Panda for the AI, if you wish, create a BAT file to automate the running process.
```sh
@echo off
path\to\>>>>>>AI<<<<<<\panda\python\ppython main_ai.py
pause
```
***Make sure you have the server up and running and also the uberdog before running the AI!***

### Running the game
Once you have the server, UD, and the AI running, it's time to launch the game.
To do that, if you wish, create a BAT file to automate the running process.
```sh
@echo off
path\to\>>>>>GAME<<<<<\panda\python\ppython main.py your_username
pause
```
´
### Workflow
***Have your OTP server folder one directory up the game folder, and always leave the name of the folder as ToontownOnline, as illustrated.***
```
anywhere\
    OTP-Reboot\
        ...
    ToontownOnline\
        ...
```

This way the DC file is manageable by both projects without the needing of copy-pasting every change.