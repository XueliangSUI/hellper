import time
from pynput import keyboard
import pyautogui

def on_press(key):
    if key == keyboard.Key.f10:
        print("F10 pressed, simulating F2 key hold for 2.1 seconds...")
        pyautogui.keyDown('f2')
        time.sleep(2.1)
        pyautogui.keyUp('f2')

        print("Simulating R key press...")
        pyautogui.press('r')
        
        time.sleep(2)

        print("Simulating F1 key hold for 2.1 seconds...")
        pyautogui.keyDown('f1')
        time.sleep(2.1)
        pyautogui.keyUp('f1')

        print("Sequence completed.")

# The listener will be running in the background
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Keep the program running
print("Program running, press F10 to trigger the sequence.")
listener.join()