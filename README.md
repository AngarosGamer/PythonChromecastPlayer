<p align="center">
    ChromeCast Player
</p>

Chromecast Player is a python-developped application acting as an interface for playing music on Chromecast sources.

## Installation

### From source

Verified to work on Windows - other operating systems are unverified

If you plan to install Chromecast Player directly from the source code, here's a reminder of the steps to take:
 - Download the code from GitHub
 - Using pip: `pip install -r requirements.txt` to install package and libraries
 - Run the `functions/main.py` file to start the application
 
If running that last file doesn't work, `start_application.bat` might help

### From releases

There are currently no releases for the project, please use it from source

## Configuration

Chromecast Player offers some level of customization for you to modify the app's visual settings and file type
If you wish to make changes, edit the `settings.config` file

 - APP_NAME
 - WINDOW_X
 - WINDOW_Y
 - COLOR
 - ACCENT
 - FILE_TYPE

Be sure to keep format precisely the same and only use supported options. Any other parameter might fail and use default settings.

## Features and notes

Chromecast Player currently only supports YouTube links.

 - Automatic file server creation for music repository
 - Download / Delete videos automatically
 - Multiple audio formats supported
 - Visual Customization in-app

## Images and visuals

Main Menu after booting to the app
<img src="https://i.imgur.com/RiVdBAi.png">

While using the application
<img src="https://i.imgur.com/59Wfth2.png">

Latest Version with Current song showing
<img src="https://i.imgur.com/BVXl6Ui.png">

