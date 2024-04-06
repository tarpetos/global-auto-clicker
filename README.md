# GUI Auto Clicker 
Rewritten multithreaded version of CLI auto-clicker with graphical interface created with tkinter. 
There is no possibility to hold buttons unlike the CLI interface. But now auto-clicking process
is attached to mouse movement and can be configured much more in GUI version. 
Also, this version of clicker allows to click with very high speed.


## PyInstaller
Creating executable with `PyInstaller`:

```shell
pyinstaller -F -w --name "GUI Auto Clicker v0.1" --icon "app_icon/mouse-click-icon.ico" main.py
```
