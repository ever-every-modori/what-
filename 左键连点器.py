import ctypes
import time
import atexit
from ctypes import wintypes

# 获取 user32 动态链接库
user32 = ctypes.windll.user32

# ------------------------------------
# 常量定义
# ------------------------------------
# 鼠标左键模拟事件标识
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004

# 热键消息编号
WM_HOTKEY = 0x0312

# 删除键的虚拟键码（Delete）：0x2E
VK_DELETE = 0x2E

# 注册热键所用的 ID
HOTKEY_ID = 1

# ------------------------------------
# 注册 Delete 键全局热键
# ------------------------------------
if not user32.RegisterHotKey(None, HOTKEY_ID, 0, VK_DELETE):
    print("注册 Delete 键热键失败，请检查是否已有其他程序注册或系统限制。")
    exit(1)
# 在程序退出时自动注销热键，避免残留
atexit.register(lambda: user32.UnregisterHotKey(None, HOTKEY_ID))


# ------------------------------------
# 模拟鼠标左键点击函数
# ------------------------------------
def left_click():
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# ------------------------------------
# 快速连续左键点击循环
# ------------------------------------
def rapid_click_loop():
    """
    当检测到 Delete 键持续按下时，
    以大约每秒很多次的频率不断发送鼠标左键点击事件，
    直至 Delete 键释放。
    """
    while user32.GetAsyncKeyState(VK_DELETE) & 0x8000:
        left_click()
        # 延时控制频率
        time.sleep(0.02)


# ------------------------------------
# 消息循环：等待热键触发
# ------------------------------------
msg = wintypes.MSG()

print("等待 DELETE 键按下以触发快速左键点击（每秒约 10 次）。")
while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
    if msg.message == WM_HOTKEY:
        # 当检测到全局热键消息（Delete 键被按下）后，
        # 进入点击循环，循环内部依赖 GetAsyncKeyState 检测按键状态以判断何时退出循环
        rapid_click_loop()
    user32.TranslateMessage(ctypes.byref(msg))
    user32.DispatchMessageA(ctypes.byref(msg))

