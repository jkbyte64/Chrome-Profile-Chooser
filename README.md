# Chrome Profile Chooser
A custom Google Chrome profile chooser, written in Python 3.x + Tkinter, for users with many profiles.

## Motivation
I have a PC with many profiles on Google Chrome, either linked with Google Accounts or entirely local. As my screen is rather small, the default Google Chrome profile selector quickly became cluttered, resulting in a nightmare to start up Chrome with a chosen profile. Thus, I used Python 3.x and Tkinter to build a custom Chrome Profile Selector, which condenses all profiles in a combo box, presenting to the user the currently selected account information: profile picture or avatar, type of account (Google or local), user name, email and profile name. Pressing the `Start` button will launch Chrome with the selected profile, automatically closing the utility to mimic the traditional profile selector bundled with Chrome.

## Requirements
- Python 3.x (the utility was tested with Python 3.14.5).
- `requests` library, for Google Account image download.
