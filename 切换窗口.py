import win32gui
import win32con

def enum_windows_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
        windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def switch_to_window(window_name):
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)  # 获取所有窗口
    for hwnd, title in windows:
        if window_name in title:  # 根据窗口名称匹配
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 恢复窗口（如果最小化）
            win32gui.SetForegroundWindow(hwnd)  # 切换到窗口
            return True
    return False

# 使用示例
if switch_to_window("Discord"):  # 将 "记事本" 替换为目标窗口名称
    print("成功切换到目标窗口！")
else:
    print("未找到目标窗口！")
