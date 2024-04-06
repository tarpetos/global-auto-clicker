import os
import platform
import pyautogui
import time
from pynput import keyboard


def os_console_clear():
    user_os = platform.uname().system
    os_options = {"Linux": "clear", "Windows": "clr"}
    os.system(os_options.get(user_os, "clear"))


def invalid_autoclicker_input():
    os_console_clear()
    print("Invalid input! Must be positive float or integer number.\n")
    input("Press Enter to continue...\n")
    os_console_clear()


def time_between_clicks() -> float:
    while True:
        try:
            user_input_str = input("Enter time delay between clicks: ")
            user_input = user_input_str.replace(",", ".")

            duration = float(user_input)

            if duration <= 0:
                invalid_autoclicker_input()
                continue
            else:
                return duration
        except ValueError:
            invalid_autoclicker_input()
            continue


def button_to_hold():
    user_button = input("Enter the key value that will be held: ")
    return user_button


def execute_program(user_input):
    os_console_clear()

    if user_input == 1:
        duration = time_between_clicks()
    else:
        user_button = button_to_hold()

    print(
        "\nApplication will start after 10 seconds. "
        "\nOpen the window where you want to automate the clicking or holding process."
    )

    for second in range(10):
        time.sleep(1)
        time_to_wait = 10 - second
        print("Wait", time_to_wait, "s...")

    print(
        (
            "\nClicker is launched!!!"
            if user_input == 1
            else "\nButton holder is launched!!!"
        ),
        '\nTo stop the program, press the "Ctrl" key until it returns to the main menu.\n',
    )

    def on_press(key):
        if key == keyboard.Key.ctrl:
            print("=" * 10, "Return to main menu...", "=" * 10, "\n")
            os_console_clear()
            listener.stop()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    if user_input == 1:
        while listener.is_alive():
            pyautogui.click()
            pyautogui.PAUSE = duration
    else:
        while listener.is_alive():
            pyautogui.press(user_button, interval=0.01, _pause=False)


def menu():
    print("1. Autoclicker")
    print("2. Button holder")
    print("3. Exit")
    print(">>>> ", sep="", end="")


def process_user_choice():
    os_console_clear()
    while True:
        try:
            menu()
            user_input = int(input())

            if user_input == 1 or user_input == 2:
                execute_program(user_input)
            elif user_input == 3:
                return
            else:
                invalid_input()
                continue
        except ValueError:
            invalid_input()
            continue


def invalid_input():
    os_console_clear()
    print("Invalid input! Possible options: 1, 2, 3. Try again.\n")
    input("Press Enter to continue...\n")
    os_console_clear()


if __name__ == "__main__":
    process_user_choice()
