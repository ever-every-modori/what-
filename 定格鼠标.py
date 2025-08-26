import pyautogui
import time
import keyboard
pyautogui.PAUSE = False
def time_sleep_us(us):
    start = time.time()
    while (time.time() - start) < us / 1_000_000:
        pass
def onon():
    while not keyboard.is_pressed('backspace'):
        pyautogui.moveTo(1920, 426)
        pyautogui.click()
        time_sleep_us(100)
keyboard.add_hotkey(']', onon)
keyboard.wait('esc')