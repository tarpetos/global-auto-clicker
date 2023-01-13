import pyautogui
import time
import keyboard


def time_beetwen_clicks() -> int:
    error_message = 'Invalid input! Must be positive integer number.\n'

    while True:
        try:
            duration = int(input('Enter time delay beetwen clicks: '))
            if duration <= 0:
                print(error_message)
                continue
            else:
                return duration
        except ValueError:
            print(error_message)
            continue


def click_cycle():
    duration = time_beetwen_clicks()

    print(
        '\nApplication will start after 10 seconds. \nOpen the window where you want to automate the clicking process.'
    )

    for second in range(10):
        time.sleep(1)
        time_to_wait = 10 - second
        print('Wait', time_to_wait, 's...')

    print('\nClicker was started!!!\nTo exit, hold the "Ctrl" button until the application stops.\n')

    x, y = pyautogui.position()
    while True:
        if keyboard.is_pressed('Ctrl'):
            print('=' * 10, 'EXITING PROGRAM', '=' * 10)
            return

        pyautogui.click(x, y)
        pyautogui.PAUSE = duration


if __name__ == '__main__':
    click_cycle()
