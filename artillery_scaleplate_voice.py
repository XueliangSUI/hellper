import pyttsx3
from pynput import keyboard
import threading
import pygame
import time
from pynput import keyboard
import pyautogui


sem = threading.Semaphore()
pygame.mixer.init()
ok_video = pygame.mixer.Sound('./_internal/videoes/ok.wav')
keyboard_video = pygame.mixer.Sound('./_internal/videoes/keyboard.mp3')


factions = {
    1: "Allies",
    2: "German",
    3: "USSR",
    4: "British"
}


def speak(text):
    t = threading.Thread(target=speak_async, args=(text,))
    t.start()
    t.join()


def speak_async(text):
    sem.acquire()
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"在语音输出时发生异常：{e}")
    sem.release()
    pygame.mixer.Sound.play(ok_video)


def calculate(num, faction):
    num = float(num)
    if (faction == 1):
        # German & Allies
        return round(-0.2371 * num+1001.53)
    elif (faction == 2):
        # German & Allies
        return round(-0.2371 * num+1001.53)
    elif (faction == 3):
        # USSR
        return round(-0.2133 * num+1141.33333)
    elif (faction == 4):
        # Great Britain
        return round(-0.1773 * num+550.73333)


# 监听键盘输入的数字
class NumberListener:
    def __init__(self):
        self.numbers = ""  # 用于存储输入的数字
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()  # 开始监听键盘

    def on_press(self, key):
        try:
            # 检查按键是否是数字
            if hasattr(key, 'char') and key.char.isdigit():
                len_limit = 3
                if (self.numbers):
                    if (self.numbers[0] == '1'):
                        len_limit = 4

                # 添加数字到列表
                self.numbers = self.numbers+key.char
                print(self.numbers)
                # 检查是否已经输入了len_limit个数字
                if len(self.numbers) == len_limit:
                    # 执行特定函数
                    print("执行特定函数")
                    speak(calculate(self.numbers))
                    print("Waiting for next distance input...")
                    # 清空数字列表，以便重新开始计数
                    self.numbers = ""

        except AttributeError:
            pass  # 忽略非数字按键

    def stop_listening(self):
        self.listener.stop()

        # 可以设置某个按键作为退出监听的条件
        # if key == keyboard.Key.f10:
        #     # 停止监听
        #     return False


# number_listener = NumberListener()

# number_listener.listener.join()

class ArtilleryModeListener:
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.activated = False
        self.faction = 0
        self.numbers = ""
        self.listener.start()
        print("Artillery mode ready, press F10 to activate or deactivate it...")

    def on_press(self, key):
        try:
            if (not self.activated and key == keyboard.Key.f10):
                # activate artillery mode
                print("Artillery mode activated...")
                speak("Artillery mode activated...")
                print(
                    "Please select a faction, 1 for Allies,2 for German, 3 for USSR, 4 for British:")
                self.activated = True
            elif (self.activated):
                # deactivate artillery mode
                if key == keyboard.Key.f10:
                    if self.activated:
                        print("Artillery mode deactivated...")
                        speak("Artillery mode deactivated...")
                        self.activated = False
                        self.faction = 0
                        self.numbers = ""
                elif (self.faction == 0):
                    # select faction
                    if (hasattr(key, 'char') and key.char.isdigit() and key.char in ('1', '2', '3', '4')):
                        self.faction = int(key.char)
                        pygame.mixer.Sound.play(keyboard_video)
                        speak(f"{factions[self.faction]}")
                        print(f"Selected faction: {factions[self.faction]}")
                        print(
                            "Press F3 to auto reload, or input distance from 200-1600, MIL will be spoken automatically...")
                        pygame.mixer.Sound.play(ok_video)
                elif (self.faction != 0):
                    # listen for numbers of distance
                    if hasattr(key, 'char') and key.char.isdigit():
                        len_limit = 3
                        if (self.numbers != "" and self.numbers[0] == '1'):
                            len_limit = 4
                        self.numbers = self.numbers+key.char
                        pygame.mixer.Sound.play(keyboard_video)
                        if len(self.numbers) == len_limit:
                            # 执行特定函数
                            print("Distance inputed:"+self.numbers)
                            mil = calculate(self.numbers, self.faction)
                            print("MIL:"+str(mil))
                            speak(mil)
                            # 清空数字列表，以便重新开始计数
                            self.numbers = ""
                            # listen key ctrl + r
                    elif key == keyboard.Key.f3:
                        pygame.mixer.Sound.play(ok_video)
                        print("Auto reloading...")
                        pyautogui.keyDown('f2')
                        time.sleep(1.1)
                        pyautogui.keyUp('f2')
                        pyautogui.press('r')
                        time.sleep(3.5)
                        pyautogui.keyDown('f1')
                        time.sleep(1.1)
                        pyautogui.keyUp('f1')

        except AttributeError:
            pass


artillery_mode_listener = ArtilleryModeListener()
artillery_mode_listener.listener.join()


# 获取并设置语音引擎的属性，例如选择中文语音
# voices = engine.getProperty('voices')
# for voice in voices:
#     if 'chinese' in voice.languages[0]:  # 根据系统语音的支持情况可能需要调整此处条件
#         engine.setProperty('voice', voice.id)
#         break
# engine.setProperty('voice', voice.id)
