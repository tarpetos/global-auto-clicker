# Auto Clicker 
A simple console clicker that allows you to make a global click in your operating system 1 time in a certain period of time.  
This time period is set when the application is launched and persists until the application is stopped.  
Also there is a function that allows you to hold one button (except `CTRL`). You have to enter the value of this button like a string.  
If you enter more than 1 key value (or `CTRL`), the key hold will not work.

To stop the clicker, you need to press the `CTRL` key until the program returns to the main menu.  
To fully stop the program, you need to enter the `3` key in the main menu and press `Enter` or close your console.

## PyInstaller
```shell
pyinstaller -F -w --name "CLI Auto Clicker v0.1" --icon "app_icon/mouse-click-icon.ico" main.py
```
