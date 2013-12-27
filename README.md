# dragonfly-scripts

__Note: There is currently a lot of heavy experimenting going on in this repository, so it is not stable. And there will most likely be a lot of tweaking in the weeks to come.__


So far, this repository contains mostly modules provided with the Dragonfly [command-modules repository](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html).

My additions are a Git commands module and a debug module.



---

## What?

This repository contains my collection of [Dragonfly](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html) Python-scripts, that I use with [Dragon NaturallySpeaking Professional](http://www.nuance.com/for-business/by-product/dragon/dragon-for-the-pc/dragon-professional/index.htm).

##### What is [Dragonfly](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html)?
* A speech recognition framework
* A Python package, that can be used in conjuction with Natlink and Dragon NaturallySpeaking.

##### So what's Natlink?
Natlink is an extension to Dragon NaturallySpeaking to allow scripting beyond the Visual Basic Scripts that the speech recognition program normally supports.

##### I heard of Vocola 2, Unimacro and Voicecode, what's that?
Like Dragonfly, they are extensions for writing macros/scripts for Dragon NaturallySpeaking, built on top of Natlink. They can be used simultaneously with Dragonfly, but it is unclear to what extent, and how stable that is.
The installation file for Natlink mentioned below, contains Vocola 2 and Unimacro, but they can easily be activated/deactivated through configuration.

## Why?

#### Why speech recognition?
Due to repetitive strain injury (RSI), I started using speech recognition to be able to control my computer, especially for coding.
Dragonfly used in conjunction with Natlink, adds some powerful tools to the speech recognition program.

#### Why Dragonfly?
* It seems to execute much faster than the Visual Basic scripts that Dragon NaturallySpeaking normally supports.
* I never could get external files working in Visual Basic scripts, making it hard to write reusable code.
* Python, even older versions, trumps Visual Basic scripts any day of the week.

## Who?

I am a software engineer, lately focused mostly on web development, with Python on the backend.
I am currently running Dragon NaturallySpeaking 11 (soon to be 12), on Windows XP 32-bit (soon to be Windows 7, 64-bit).
I would rather be sitting on Linux using Vim, but ended up on Windows mostly using Eclipse.

## How?

For starters I'm using [Dragon NaturallySpeaking](http://www.nuance.com/for-business/by-product/dragon/dragon-for-the-pc/dragon-professional/index.htm) 11, for speech recognition.

Dragonfly is also supposed to be compatible with Windows Speech Recognition (WSR), but I haven't tried that so it won't be covered here.

### Installing Natlink and Dragonfly
> I recommend avoiding 64-bit on any of the packages you install, including Python. Also avoid 64-bit Java, on any applications you want to use when running Dragon naturally speaking. I have experienced problems with Dragon NaturallySpeaking when it comes to 64-bit. Particularly with Eclipse.
> The problems was caused by the Java virtual machine, that was in 64-bit. The most annoying problem I had, double typing of the first character or loss of the first character, was fixed by installing the Java virtual machine 32-bit version instead.
> I'm about to switch to Windows 7 64-bit, but will still stick to 32-bit Python and Java VM 32-bit. I'm hoping Dragon NaturallySpeaking 12 have fixed some of the 64-bit issues.

I am using Python 2.6, because using NatLink and Dragonfly with 2.7 still seems untested and undocumented. 
([See the bottom part of this post](http://www.speechcomputing.com/node/5345))

*NOTE: If you have multiple Python versions, make sure you install all packages into the correct python version.*

#### Installing Python 2.6 and Pythonwin

##### Alternative 1:
* The pure Python package for 2.6 can be downloaded here: http://www.python.org/download/releases/2.6.6/
* Pythonwin / Python Win32 Extensions: http://sourceforge.net/projects/pywin32/files/pywin32/. Choose the latest build (218 at the time of writing this), then select the correct installer for your system. I use pywin32-218.win32-py2.6.exe (even though the system is 64-bit).
* If you will be running scripts that use GUI functionality, you need wxPython. http://wxpython.org/download.php#stable. I used `wxPython2.8-win32-unicode-py26`.

##### Alternative 2:
* A package containing Python 2.6, Pythonwin, wxPython and PyXML can be found here: http://sourceforge.net/projects/natlink/files/pythonfornatlink/python2.6/pythonneededfornatlink2.6.exe/download.
*wxPython is only needed if you will be running scripts that use GUI functionality. PyXML is only used for VoiceCode*

#### Installing Natlink:
This site, [Unimacro](http://qh.antenna.nl/unimacro/installation/installation.html), has a lot of information on the installation and configuration of Natlink. The site is mostly focused on Unimacro and Vocola 2.

You can get Natlink here: [Natlink repository](http://sourceforge.net/projects/natlink/files/natlink/)

Once Natlink is installed, two configuration utilities will show up in the start menu. One is a command line tool, the other is a GUI tool.

> On my windows XP 32-bit machine, when I was following the instructions from the Unimacro site, when I started the "Configure Natlink Via GUI" program, I got several warning messages.
> However, restarting Dragon NaturallySpeaking (or perhaps just reloading Natlink), then running the configuration program again, solved that issue.
> I have seen the GUI configuration tool freeze completely on Windows 7 64-bit, but the command line tool worked fine.

#### Installing Dragonfly:
Python library site: [Dragonfly](https://pypi.python.org/pypi/dragonfly)

I used the `dragonfly-0.6.5.win32.exe` installer.
Dragonfly’s installer will install the library in your Python’s local site-packages directory under the dragonfly subdirectory.


*NOTE: If you have multiple Python versions, make sure you install all packages into the correct python version.*

## And then?
...
