import tkinter as tk
import keyboard
import threading
import time

# ================ 全局变量 ================
liamu = ['<@1084790425598033950> 你妈死了']  # 消息列表（默认消息）
running = False            # 控制循环发送的标志
hotkey_ids = []            # 存储当前注册的所有热键的 ID

# 默认发送间隔（秒）
time_interval_with_enter = 0.5   # 带 Enter 的循环发送间隔
time_interval_without_enter = 1    # 不带 Enter 的循环发送间隔

# ================ 功能函数 ================
def update_message_list():
    """
    从消息文本框中获取多行数据，每行作为一条消息，更新全局列表 liamu。
    """
    global liamu
    text = text_box.get("1.0", tk.END).strip()
    if text:
        liamu = text.splitlines()
    else:
        liamu = []

def send_once():
    """单次发送：依次发送消息列表中的所有消息。"""
    update_message_list()
    for msg in liamu:
        keyboard.write(msg)

def loop_send_with_enter():
    """
    循环发送，每条消息发送后模拟回车，间隔时间由 time_interval_with_enter 决定。
    在独立线程中执行，直到调用 stop_sending() 停止。
    """
    global running
    if running:
        return
    running = True
    update_message_list()
    def task():
        while running:
            for msg in liamu:
                keyboard.write(msg)
                keyboard.press_and_release('enter')
                time.sleep(time_interval_with_enter)
                if not running:
                    break
    threading.Thread(target=task, daemon=True).start()

def loop_send_without_enter():
    """
    循环发送，每条消息发送后不模拟回车，
    间隔时间由 time_interval_without_enter 决定，直到调用 stop_sending() 停止。
    """
    global running
    if running:
        return
    running = True
    update_message_list()
    def task():
        while running:
            for msg in liamu:
                keyboard.write(msg)
                time.sleep(time_interval_without_enter)
                if not running:
                    break
    threading.Thread(target=task, daemon=True).start()

def stop_sending():
    """停止循环发送动作。"""
    global running
    running = False

def update_hotkeys():
    """
    更新热键和时间间隔设置：
      1. 先移除先前注册的所有热键；
      2. 从时间间隔输入框中读取数值，更新全局时间间隔变量；
      3. 根据每个热键的复选框状态（启用/禁用），若启用则读取热键输入框内容并注册相应热键。
    """
    global hotkey_ids, time_interval_with_enter, time_interval_without_enter

    # 清除之前注册的热键
    for hk_id in hotkey_ids:
        keyboard.remove_hotkey(hk_id)
    hotkey_ids = []

    # 尝试更新时间间隔（输入不合法则使用默认值）
    try:
        time_interval_with_enter = float(entry_interval_with.get().strip())
    except Exception:
        time_interval_with_enter = 0.5
    try:
        time_interval_without_enter = float(entry_interval_without.get().strip())
    except Exception:
        time_interval_without_enter = 1.0

    # 根据复选框状态决定是否注册热键
    hk1 = entry_hk1.get().strip()
    if var_hk1.get():
        hotkey_ids.append(keyboard.add_hotkey(hk1, send_once))
    hk2 = entry_hk2.get().strip()
    if var_hk2.get():
        hotkey_ids.append(keyboard.add_hotkey(hk2, loop_send_with_enter))
    hk3 = entry_hk3.get().strip()
    if var_hk3.get():
        hotkey_ids.append(keyboard.add_hotkey(hk3, loop_send_without_enter))
    hk4 = entry_hk4.get().strip()
    if var_hk4.get():
        hotkey_ids.append(keyboard.add_hotkey(hk4, stop_sending))

# ================ 创建界面 ================
root = tk.Tk()
root.title("自动打字机")
root.configure(bg="#282c34")  # 主窗口背景色

# 主体布局：采用深色背景
main_frame = tk.Frame(root, padx=10, pady=10, bg="#282c34")
main_frame.pack()

# 消息编辑区域
msg_label = tk.Label(main_frame, text="消息内容（每行一条）：", bg="#282c34", fg="white")
msg_label.pack(anchor='w')
text_box = tk.Text(main_frame, height=4, width=50, bg="#3e4451", fg="white", insertbackground="white")
text_box.insert(tk.END, "填字")
text_box.pack(pady=5)

# 操作按钮区域
btn_frame = tk.Frame(main_frame, bg="#282c34")
btn_frame.pack(pady=10)
btn_send_once = tk.Button(btn_frame, text="单次发送", width=20, command=send_once, bg="#61afef", fg="white")
btn_loop_enter = tk.Button(btn_frame, text="循环发送带Enter", width=20, command=loop_send_with_enter, bg="#61afef", fg="white")
btn_loop_no_enter = tk.Button(btn_frame, text="循环发送不带Enter", width=20, command=loop_send_without_enter, bg="#61afef", fg="white")
btn_stop = tk.Button(btn_frame, text="停止发送", width=20, command=stop_sending, bg="#e06c75", fg="white")
btn_send_once.grid(row=0, column=0, padx=5, pady=5)
btn_loop_enter.grid(row=0, column=1, padx=5, pady=5)
btn_loop_no_enter.grid(row=1, column=0, padx=5, pady=5)
btn_stop.grid(row=1, column=1, padx=5, pady=5)

# 时间间隔设置区域
interval_frame = tk.Frame(main_frame, pady=10, bg="#282c34")
interval_frame.pack(fill='x')
interval_label = tk.Label(interval_frame, text="时间间隔设置（秒）:", bg="#282c34", fg="white")
interval_label.grid(row=0, column=0, columnspan=2, sticky="w")
label_interval_with = tk.Label(interval_frame, text="带Enter间隔：", bg="#282c34", fg="white")
label_interval_with.grid(row=1, column=0, sticky="e", padx=5, pady=2)
entry_interval_with = tk.Entry(interval_frame, width=10, bg="#3e4451", fg="white", insertbackground="white")
entry_interval_with.insert(0, "0.5")
entry_interval_with.grid(row=1, column=1, sticky="w", padx=5, pady=2)
label_interval_without = tk.Label(interval_frame, text="不带Enter间隔：", bg="#282c34", fg="white")
label_interval_without.grid(row=2, column=0, sticky="e", padx=5, pady=2)
entry_interval_without = tk.Entry(interval_frame, width=10, bg="#3e4451", fg="white", insertbackground="white")
entry_interval_without.insert(0, "1")
entry_interval_without.grid(row=2, column=1, sticky="w", padx=5, pady=2)

# 热键设置区域
hotkey_frame = tk.Frame(main_frame, pady=10, bg="#282c34")
hotkey_frame.pack(fill='x')
hotkey_title = tk.Label(hotkey_frame, text="热键设置（修改后点击‘更新设置’按钮生效）：", bg="#282c34", fg="white")
hotkey_title.grid(row=0, column=0, columnspan=3, sticky="w")

# 单次发送热键
label_hk1 = tk.Label(hotkey_frame, text="单次发送热键：", bg="#282c34", fg="white")
label_hk1.grid(row=1, column=0, sticky="e", padx=5, pady=2)
entry_hk1 = tk.Entry(hotkey_frame, width=10, bg="#3e4451", fg="white", insertbackground="white")
entry_hk1.insert(0, "1")
entry_hk1.grid(row=1, column=1, sticky="w", padx=5, pady=2)
var_hk1 = tk.BooleanVar(value=True)
cb_hk1 = tk.Checkbutton(hotkey_frame, text="启用", variable=var_hk1,
                         bg="#282c34", fg="black", activebackground="#282c34", activeforeground="black")
cb_hk1.grid(row=1, column=2, padx=5, pady=2)

# 循环发送带Enter热键
label_hk2 = tk.Label(hotkey_frame, text="循环发送带Enter热键：", bg="#282c34", fg="white")
label_hk2.grid(row=2, column=0, sticky="e", padx=5, pady=2)
entry_hk2 = tk.Entry(hotkey_frame, width=10, bg="#3e4451", fg="white", insertbackground="white")
entry_hk2.insert(0, "2")
entry_hk2.grid(row=2, column=1, sticky="w", padx=5, pady=2)
var_hk2 = tk.BooleanVar(value=True)
cb_hk2 = tk.Checkbutton(hotkey_frame, text="启用", variable=var_hk2,
                         bg="#282c34", fg="black", activebackground="#282c34", activeforeground="black")
cb_hk2.grid(row=2, column=2, padx=5, pady=2)

# 循环发送不带Enter热键
label_hk3 = tk.Label(hotkey_frame, text="循环发送不带Enter热键：", bg="#282c34", fg="white")
label_hk3.grid(row=3, column=0, sticky="e", padx=5, pady=2)
entry_hk3 = tk.Entry(hotkey_frame, width=10, bg="#3e4451", fg="white", insertbackground="white")
entry_hk3.insert(0, "3")
entry_hk3.grid(row=3, column=1, sticky="w", padx=5, pady=2)
var_hk3 = tk.BooleanVar(value=True)
cb_hk3 = tk.Checkbutton(hotkey_frame, text="启用", variable=var_hk3,
                         bg="#282c34", fg="black", activebackground="#282c34", activeforeground="black")
cb_hk3.grid(row=3, column=2, padx=5, pady=2)

# 停止发送热键
label_hk4 = tk.Label(hotkey_frame, text="停止发送热键：", bg="#282c34", fg="white")
label_hk4.grid(row=4, column=0, sticky="e", padx=5, pady=2)
entry_hk4 = tk.Entry(hotkey_frame, width=10, bg="#3e4451", fg="white", insertbackground="white")
entry_hk4.insert(0, "backspace")
entry_hk4.grid(row=4, column=1, sticky="w", padx=5, pady=2)
var_hk4 = tk.BooleanVar(value=True)
cb_hk4 = tk.Checkbutton(hotkey_frame, text="启用", variable=var_hk4,
                         bg="#282c34", fg="black", activebackground="#282c34", activeforeground="black")
cb_hk4.grid(row=4, column=2, padx=5, pady=2)

btn_update = tk.Button(hotkey_frame, text="更新设置", command=update_hotkeys, bg="#98c379", fg="white")
btn_update.grid(row=5, column=0, columnspan=3, pady=5)

# 初始化时注册热键与时间间隔设置
update_hotkeys()

# ================ 启动 GUI 主循环 ================
root.mainloop()
