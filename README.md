# dragonfly-scripts

---

>**NO WARRANTY!**
>All code and information in this repository is provided "AS IS". Your use of its content is at your own risk. The author/authors are not liable for any consequences from using it. **ALWAYS** make sure to keep backups before making any changes!

---

>All code in this repository is licensed under LGPL3, if not explicitly stated otherwise.

---

__Note: There is currently a lot of heavy experimenting going on in this repository, so it is not stable. Some of the information is not updated. Once the repository contents starts to stabilize, I will try to update the information texts.__


### What is dragonfly-scripts?

This repository contains a collection of [Dragonfly](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html) Python-scripts, that can be used with [Dragon NaturallySpeaking Professional](http://www.nuance.com/for-business/by-product/dragon/dragon-for-the-pc/dragon-professional/index.htm).

##### What is [Dragonfly](http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/index.html)?
* A speech recognition framework
* A Python package, that can be used in conjuction with Natlink and Dragon NaturallySpeaking.

##### So what's Natlink?
Natlink is an extension to Dragon NaturallySpeaking to allow scripting beyond the Visual Basic Scripts that the speech recognition program normally supports.

#### Why Dragonfly?
* It seems to execute much faster than the Visual Basic scripts that Dragon NaturallySpeaking normally supports.
* I never could get external files working in Visual Basic scripts (in Dragon Naturally Speaking Professional), making it hard to write reusable code.
* Python, even older versions, trumps Visual Basic scripts any day of the week.

### Installing Natlink and Dragonfly
> I recommend avoiding 64-bit on any of the packages you install, including Python. Also avoid 64-bit Java, on any applications you want to use when running Dragon naturally speaking. I have experienced problems with Dragon NaturallySpeaking when it comes to 64-bit. Particularly with Eclipse.
> The problems was caused by the Java virtual machine, that was in 64-bit. The most annoying problem I had, double typing of the first character or loss of the first character, was fixed by installing the Java virtual machine 32-bit version instead.

*NOTE: If you have multiple Python versions, make sure you install all packages into the correct python version.*

#### Installing Python 2.7 and Pythonwin

##### Alternative 1:
* The pure Python package for 2.7 can be downloaded here: http://www.python.org/download/releases/2.7.7/
* Pythonwin / Python Win32 Extensions: http://sourceforge.net/projects/pywin32/files/pywin32/. Choose the latest build (219 at the time of writing this), then select the correct installer for your system. Use pywin32-219.win32-py2.7.exe (even if your system is 64-bit).
* The config GUI needs wxPython, or you can run the command prompt version.
http://wxpython.org/download.php#stable. I used `wxPython2.8-win32-unicode-py27`.

##### Alternative 2:
* A package containing Python 2.7, Pythonwin, wxPython and PyXML can be found here: 
http://sourceforge.net/projects/natlink/files/pythonfornatlink/
(PyXML is only used for VoiceCode)*

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


