import tkinter as tk
from tkinter import colorchooser, messagebox
import keyboard
import time
import threading
from pynput import mouse

class KeyDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Strike 1.0 by kyle_A_10000")
        # 缩小窗口尺寸
        self.root.geometry("500x300")
        
        # 使用特定颜色作为透明色
        self.transparent_color = '#abcdef'  # 选择一个不常见的颜色
        self.root.configure(bg=self.transparent_color)
        self.root.attributes('-transparentcolor', self.transparent_color)
        
        # 设置窗口置顶
        self.root.attributes('-topmost', True)
        
        # 创建画布
        self.canvas = tk.Canvas(root, width=500, height=300, bg=self.transparent_color, highlightthickness=0)
        self.canvas.pack()
        
        # 按键状态
        self.key_states = {
            'w': False, 'a': False, 's': False, 'd': False, 
            'c': False, 'space': False, 'shift': False,
            'left_mouse': False, 'right_mouse': False
        }
        
        # CPS 跟踪
        self.left_cps_history = []
        self.right_cps_history = []
        
        # 颜色设置 - 默认为原始颜色
        self.key_pressed_color = '#FFFFFF'  # 按键按下颜色
        self.key_released_color = '#969696' # 按键松开颜色
        self.text_color = '#000000'         # 文字颜色
        self.border_color = '#323232'       # 边框颜色
        self.cps_color = '#006400'          # CPS文字颜色
        
        # 绘制初始界面
        self.draw_interface()
        
        # 开始监听按键
        self.start_key_listener()
        self.start_mouse_listener()
        
    def draw_key(self, x, y, width, height, text, is_pressed):
        """绘制按键"""
        color = self.key_pressed_color if is_pressed else self.key_released_color
        
        # 绘制按键
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline=self.border_color, width=2)
        
        # 绘制文字
        self.canvas.create_text(x+width/2, y+height/2, text=text, font=('Arial', 12, 'bold'), fill=self.text_color)
    
    def draw_mouse_button(self, x, y, width, height, text, is_pressed, cps):
        """绘制鼠标按键和CPS"""
        color = self.key_pressed_color if is_pressed else self.key_released_color
        
        # 绘制按键
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline=self.border_color, width=2)
        
        # 绘制文字
        self.canvas.create_text(x+width/2, y+height/2-6, text=text, font=('Arial', 10, 'bold'), fill=self.text_color)
        
        # 绘制CPS
        self.canvas.create_text(x+width/2, y+height/2+8, text=f"{cps:.1f} CPS", 
                               font=('Arial', 8), fill=self.cps_color)
    
    def calculate_cps(self, history):
        """计算CPS"""
        current_time = time.time()
        # 移除超过1秒的记录
        while history and current_time - history[0] > 1.0:
            history.pop(0)
        return len(history)
    
    def draw_interface(self):
        """绘制整个界面"""
        self.canvas.delete("all")
        
        # 绘制标题 - 添加关闭提示
        self.canvas.create_text(250, 15, text="Key Strike", font=('Arial', 12, 'bold'), fill=self.text_color)
        self.canvas.create_text(250, 35, text="Press F9 to exit, F10 for settings", font=('Arial', 8), fill=self.text_color)
        
        # 第一行：W
        self.draw_key(230, 50, 35, 30, "W", self.key_states['w'])
        
        # 第二行：A S D
        self.draw_key(195, 85, 35, 30, "A", self.key_states['a'])
        self.draw_key(230, 85, 35, 30, "S", self.key_states['s'])
        self.draw_key(265, 85, 35, 30, "D", self.key_states['d'])
        
        # 第三行：SHIFT 和 C
        self.draw_key(195, 120, 70, 30, "SHIFT", self.key_states['shift'])
        self.draw_key(275, 120, 35, 30, "C", self.key_states['c'])
        
        # 第四行：空格 - 改为 "Space"
        self.draw_key(195, 155, 150, 30, "Space", self.key_states['space'])
        
        # 第五行：鼠标按键和CPS - 改为 "LEFT" 和 "RIGHT"
        left_cps = self.calculate_cps(self.left_cps_history)
        right_cps = self.calculate_cps(self.right_cps_history)
        
        self.draw_mouse_button(195, 190, 65, 30, "LEFT", 
                              self.key_states['left_mouse'], left_cps)
        self.draw_mouse_button(280, 190, 65, 30, "RIGHT", 
                              self.key_states['right_mouse'], right_cps)
    
    def start_key_listener(self):
        """开始监听键盘按键"""
        def listen_keys():
            # 监听键盘按键
            keyboard.on_press_key('w', lambda _: self.update_key('w', True))
            keyboard.on_release_key('w', lambda _: self.update_key('w', False))
            keyboard.on_press_key('a', lambda _: self.update_key('a', True))
            keyboard.on_release_key('a', lambda _: self.update_key('a', False))
            keyboard.on_press_key('s', lambda _: self.update_key('s', True))
            keyboard.on_release_key('s', lambda _: self.update_key('s', False))
            keyboard.on_press_key('d', lambda _: self.update_key('d', True))
            keyboard.on_release_key('d', lambda _: self.update_key('d', False))
            keyboard.on_press_key('c', lambda _: self.update_key('c', True))
            keyboard.on_release_key('c', lambda _: self.update_key('c', False))
            keyboard.on_press_key('space', lambda _: self.update_key('space', True))
            keyboard.on_release_key('space', lambda _: self.update_key('space', False))
            keyboard.on_press_key('shift', lambda _: self.update_key('shift', True))
            keyboard.on_release_key('shift', lambda _: self.update_key('shift', False))
            
            # 添加F9关闭快捷键
            keyboard.on_press_key('f9', lambda _: self.close_app())
            
            # 添加F10设置快捷键
            keyboard.on_press_key('f10', lambda _: self.open_settings())
            
            # 保持线程运行
            keyboard.wait()
        
        # 在新线程中运行监听器
        thread = threading.Thread(target=listen_keys, daemon=True)
        thread.start()
    
    def start_mouse_listener(self):
        """开始监听鼠标按键"""
        def on_click(x, y, button, pressed):
            if button == mouse.Button.left:
                if pressed:
                    self.key_states['left_mouse'] = True
                    self.left_cps_history.append(time.time())
                    self.draw_interface()
                else:
                    self.key_states['left_mouse'] = False
                    self.draw_interface()
            elif button == mouse.Button.right:
                if pressed:
                    self.key_states['right_mouse'] = True
                    self.right_cps_history.append(time.time())
                    self.draw_interface()
                else:
                    self.key_states['right_mouse'] = False
                    self.draw_interface()
        
        # 在新线程中运行鼠标监听器
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.daemon = True
        mouse_listener.start()
    
    def update_key(self, key, state):
        """更新按键状态并重绘界面"""
        self.key_states[key] = state
        self.draw_interface()
    
    def open_settings(self):
        """打开设置窗口"""
        SettingsWindow(self)
    
    def close_app(self):
        """关闭应用程序"""
        self.root.quit()
        self.root.destroy()


class SettingsWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.settings_window = tk.Toplevel(parent_app.root)
        self.settings_window.title("Key Strike Settings")
        self.settings_window.geometry("300x400")
        self.settings_window.resizable(False, False)
        self.settings_window.attributes('-topmost', True)  # 设置窗口置顶
        
        # 创建主框架
        main_frame = tk.Frame(self.settings_window, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(main_frame, text="Key Strike Settings", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 按键按下颜色设置
        pressed_frame = tk.Frame(main_frame)
        pressed_frame.pack(fill=tk.X, pady=5)
        
        pressed_label = tk.Label(pressed_frame, text="Pressed Key Color:", font=('Arial', 10))
        pressed_label.pack(side=tk.LEFT)
        
        self.pressed_color_btn = tk.Button(
            pressed_frame, 
            text="Choose", 
            bg=parent_app.key_pressed_color,
            command=lambda: self.choose_color('pressed'),
            width=10
        )
        self.pressed_color_btn.pack(side=tk.RIGHT)
        
        # 按键松开颜色设置
        released_frame = tk.Frame(main_frame)
        released_frame.pack(fill=tk.X, pady=5)
        
        released_label = tk.Label(released_frame, text="Released Key Color:", font=('Arial', 10))
        released_label.pack(side=tk.LEFT)
        
        self.released_color_btn = tk.Button(
            released_frame, 
            text="Choose", 
            bg=parent_app.key_released_color,
            command=lambda: self.choose_color('released'),
            width=10
        )
        self.released_color_btn.pack(side=tk.RIGHT)
        
        # 文字颜色设置
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.X, pady=5)
        
        text_label = tk.Label(text_frame, text="Text Color:", font=('Arial', 10))
        text_label.pack(side=tk.LEFT)
        
        self.text_color_btn = tk.Button(
            text_frame, 
            text="Choose", 
            bg=parent_app.text_color,
            command=lambda: self.choose_color('text'),
            width=10
        )
        self.text_color_btn.pack(side=tk.RIGHT)
        
        # 边框颜色设置
        border_frame = tk.Frame(main_frame)
        border_frame.pack(fill=tk.X, pady=5)
        
        border_label = tk.Label(border_frame, text="Border Color:", font=('Arial', 10))
        border_label.pack(side=tk.LEFT)
        
        self.border_color_btn = tk.Button(
            border_frame, 
            text="Choose", 
            bg=parent_app.border_color,
            command=lambda: self.choose_color('border'),
            width=10
        )
        self.border_color_btn.pack(side=tk.RIGHT)
        
        # CPS文字颜色设置
        cps_frame = tk.Frame(main_frame)
        cps_frame.pack(fill=tk.X, pady=5)
        
        cps_label = tk.Label(cps_frame, text="CPS Text Color:", font=('Arial', 10))
        cps_label.pack(side=tk.LEFT)
        
        self.cps_color_btn = tk.Button(
            cps_frame, 
            text="Choose", 
            bg=parent_app.cps_color,
            command=lambda: self.choose_color('cps'),
            width=10
        )
        self.cps_color_btn.pack(side=tk.RIGHT)
        
        # 重置按钮
        reset_btn = tk.Button(
            main_frame,
            text="Reset to Default",
            command=self.reset_colors,
            width=15
        )
        reset_btn.pack(pady=10)
        
        # 应用按钮
        apply_btn = tk.Button(
            main_frame,
            text="Apply Changes",
            command=self.apply_changes,
            bg="#4CAF50",
            fg="white",
            width=15
        )
        apply_btn.pack(pady=5)
        
        # 关闭按钮
        close_btn = tk.Button(
            main_frame,
            text="Close",
            command=self.settings_window.destroy,
            width=15
        )
        close_btn.pack(pady=5)
        
        # 保存原始颜色值，用于重置
        self.original_colors = {
            'pressed': parent_app.key_pressed_color,
            'released': parent_app.key_released_color,
            'text': parent_app.text_color,
            'border': parent_app.border_color,
            'cps': parent_app.cps_color
        }
        
        # 当前选择的颜色
        self.current_colors = self.original_colors.copy()
    
    def choose_color(self, color_type):
        """打开颜色选择器"""
        # 获取当前颜色
        current_color = self.current_colors[color_type]
        
        # 打开颜色选择器
        color_code = colorchooser.askcolor(
            initialcolor=current_color,
            title=f"Choose {color_type} color"
        )
        
        # 如果用户选择了颜色（没有点击取消）
        if color_code[1] is not None:
            self.current_colors[color_type] = color_code[1]
            
            # 更新按钮颜色
            if color_type == 'pressed':
                self.pressed_color_btn.config(bg=color_code[1])
            elif color_type == 'released':
                self.released_color_btn.config(bg=color_code[1])
            elif color_type == 'text':
                self.text_color_btn.config(bg=color_code[1])
            elif color_type == 'border':
                self.border_color_btn.config(bg=color_code[1])
            elif color_type == 'cps':
                self.cps_color_btn.config(bg=color_code[1])
    
    def reset_colors(self):
        """重置颜色为默认值"""
        self.current_colors = self.original_colors.copy()
        
        # 更新按钮颜色
        self.pressed_color_btn.config(bg=self.current_colors['pressed'])
        self.released_color_btn.config(bg=self.current_colors['released'])
        self.text_color_btn.config(bg=self.current_colors['text'])
        self.border_color_btn.config(bg=self.current_colors['border'])
        self.cps_color_btn.config(bg=self.current_colors['cps'])
        
        messagebox.showinfo("Reset", "Colors reset to default values.")
    
    def apply_changes(self):
        """应用颜色更改"""
        # 更新主应用程序的颜色
        self.parent_app.key_pressed_color = self.current_colors['pressed']
        self.parent_app.key_released_color = self.current_colors['released']
        self.parent_app.text_color = self.current_colors['text']
        self.parent_app.border_color = self.current_colors['border']
        self.parent_app.cps_color = self.current_colors['cps']
        
        # 重绘界面
        self.parent_app.draw_interface()
        
        messagebox.showinfo("Success", "Color settings applied successfully!")
        self.settings_window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyDisplayApp(root)
    root.mainloop()