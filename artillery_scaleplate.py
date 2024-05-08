import tkinter as tk
from PIL import Image, ImageTk
import win32gui
import win32con

def show_image_on_top(image_path):
    # 创建一个Tkinter窗口
    root = tk.Tk()
    root.title("Image on Top")

    # 移除窗口的边框，这样只显示图片
    root.overrideredirect(True)

    # 加载图片
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # 创建一个标签并放置图片
    label = tk.Label(root, image=photo)
    label.pack()

    # 将窗口置于最上层
    root.attributes("-topmost", True)

    # 获取屏幕尺寸以计算布局
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = image.width
    window_height = image.height

    # 计算图片显示位置（此处为屏幕顶部中间）
    x = (screen_width - window_width) // 2
    y = 0

    # 更新窗口位置
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # 获取窗口的句柄
    hwnd = root.winfo_id()

    # 设置窗口样式为不可点击
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    # 添加 WS_EX_NOACTIVATE 标志以防止窗口被激活
    ex_style |= win32con.WS_EX_NOACTIVATE
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    # 运行Tkinter事件循环
    root.mainloop()

# 测试函数
show_image_on_top('./images/test.png')