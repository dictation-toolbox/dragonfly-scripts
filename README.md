# dragonfly-scripts

**There's not much to see here, yet.**

## What?

My collection of [Dragonfly](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html) Python-scripts, that I use with [Dragon NaturallySpeaking Professional](http://www.nuance.com/for-business/by-product/dragon/dragon-for-the-pc/dragon-professional/index.htm).

##### What is [Dragonfly](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html)?
* A speech recognition framework
* A Python package
* A Natlink extension/add-on/toolkit

##### So what's Natlink?
Natlink is an extension to Dragon NaturallySpeaking to allow scripting beyond the Visual Basic Scripts that the speech recognition program normally supports.

##### What's Vocola 2, Unimacro and Voicecode?
Like Dragonfly, they are extensions for writing macros/scripts for Dragon NaturallySpeaking, built on top of Natlink. They can be used simultaneously with Dragonfly, but it is unclear to what extent, and how stable that is.
The installation file for Natlink mentioned below, contains Vocola 2 and Unimacro, but they can easily be activated/deactivated through configuration.

## Why?

Due to repetitive strain injury (RSI), I started using speech recognition to be able to control my computer, especially for coding.
Dragonfly used in conjunction with Natlink, adds some powerful tools to the speech recognition program.

## Who?

I am a software engineer, lately focused mostly on web development, with Python on the backend.
I am currently running Dragon NaturallySpeaking 11 (soon to be 12), on Windows 7 64-bit. I would rather be sitting on Linux using Vim, but ended up on Windows mostly using Eclipse.

## How?

I'm using [Dragon NaturallySpeaking](http://www.nuance.com/for-business/by-product/dragon/dragon-for-the-pc/dragon-professional/index.htm)
for speech recognition.
Dragonfly can be used with Windows Speech Recognition (WSR), but that is not covered here.

### Installing Natlink and Dragonfly

Python 2.6
http://sourceforge.net/projects/natlink/files/pythonfornatlink/python2.6/pythonneededfornatlink2.6.exe/download
* Self extracting zip.
* Install Pythonwin (click on, e.g., pywin32-212.win32-py2.6.exe).
* Install wxPython (click on, e.g., wxPython2.8-win32-ansi-2.8.10.1-py26.exe, extracts to a temporary folder.)
* Installing PyXML (PyXML-0.8.4.win32-py2.6.exe) is only needed if you are going to use VoiceCode

Installation of NatLink/Vocola 2/Unimacro:
http://qh.antenna.nl/unimacro/installation/installation.html
* Configuration.
* Information about common problems.

Natlink repository:
http://sourceforge.net/projects/natlink/files/natlink/

Note:
Following the instructions from the Unimacro site at antenna.nl,
when I started the "Configure Natlink Via GUI" program, I got several warning messages.
However, restarting Natlink or perhaps Dragon NaturallySpeaking, then running the configuration program again, solved that issue.

Dragonfly:
https://pypi.python.org/pypi/dragonfly
* Select the desired python version to install into.











