import pyttsx3
from pynput import keyboard
import threading

number = 12345

# 初始化pyttsx3的语音引擎
engine = pyttsx3.init()
lock = threading.Lock()


def speak(text):
    with lock:
        try:
            engine.say(text)
            engine.runAndWait()
            print("语音输出完成")
        except Exception as e:
            print(f"在语音输出时发生异常：{e}")


def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()


def execute_function(numbers):
    print("执行了特定的函数")
    print(numbers)
    print(calculate(numbers))
    speak_async(calculate(numbers))


def calculate(num):
    return round(-0.2371 * num+1001.53)

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
                    execute_function(int(self.numbers))
                    # 清空数字列表，以便重新开始计数
                    self.numbers = ""

        except AttributeError:
            pass  # 忽略非数字按键

        # 可以设置某个按键作为退出监听的条件
        if key == keyboard.Key.esc:
            # 停止监听
            return False


# 获取并设置语音引擎的属性，例如选择中文语音
voices = engine.getProperty('voices')

# 实例化监听器并开始监听
number_listener = NumberListener()

# 保持程序运行
number_listener.listener.join()

# for voice in voices:
#     if 'chinese' in voice.languages[0]:  # 根据系统语音的支持情况可能需要调整此处条件
#         engine.setProperty('voice', voice.id)
#         break
# engine.setProperty('voice', voice.id)
