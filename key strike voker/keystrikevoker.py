import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
import keyboard
import time
import threading
import json
import os
from pynput import mouse

class KeyDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Strike Voker-kyle_A_10000")
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
        
        # 按键布局 - 默认为原始布局
        self.key_layout = {
            'w': {'text': 'W', 'x': 230, 'y': 50, 'width': 35, 'height': 30},
            'a': {'text': 'A', 'x': 195, 'y': 85, 'width': 35, 'height': 30},
            's': {'text': 'S', 'x': 230, 'y': 85, 'width': 35, 'height': 30},
            'd': {'text': 'D', 'x': 265, 'y': 85, 'width': 35, 'height': 30},
            'shift': {'text': 'SHIFT', 'x': 195, 'y': 120, 'width': 70, 'height': 30},
            'c': {'text': 'C', 'x': 275, 'y': 120, 'width': 35, 'height': 30},
            'space': {'text': 'Space', 'x': 195, 'y': 155, 'width': 150, 'height': 30},
            'left_mouse': {'text': 'LEFT', 'x': 195, 'y': 190, 'width': 65, 'height': 30},
            'right_mouse': {'text': 'RIGHT', 'x': 280, 'y': 190, 'width': 65, 'height': 30}
        }
        
        # 绘制初始界面
        self.draw_interface()
        
        # 开始监听按键
        self.start_key_listener()
        self.start_mouse_listener()
        
    def draw_key(self, key):
        """绘制单个按键"""
        if key not in self.key_layout:
            return
            
        layout = self.key_layout[key]
        is_pressed = self.key_states[key]
        color = self.key_pressed_color if is_pressed else self.key_released_color
        
        # 绘制按键
        self.canvas.create_rectangle(
            layout['x'], layout['y'], 
            layout['x'] + layout['width'], layout['y'] + layout['height'], 
            fill=color, outline=self.border_color, width=2
        )
        
        # 绘制文字
        self.canvas.create_text(
            layout['x'] + layout['width']/2, 
            layout['y'] + layout['height']/2, 
            text=layout['text'], 
            font=('Arial', 12, 'bold'), 
            fill=self.text_color
        )
    
    def draw_mouse_button(self, key, cps):
        """绘制鼠标按键和CPS"""
        if key not in self.key_layout:
            return
            
        layout = self.key_layout[key]
        is_pressed = self.key_states[key]
        color = self.key_pressed_color if is_pressed else self.key_released_color
        
        # 绘制按键
        self.canvas.create_rectangle(
            layout['x'], layout['y'], 
            layout['x'] + layout['width'], layout['y'] + layout['height'], 
            fill=color, outline=self.border_color, width=2
        )
        
        # 绘制文字
        self.canvas.create_text(
            layout['x'] + layout['width']/2, 
            layout['y'] + layout['height']/2 - 6, 
            text=layout['text'], 
            font=('Arial', 10, 'bold'), 
            fill=self.text_color
        )
        
        # 绘制CPS
        self.canvas.create_text(
            layout['x'] + layout['width']/2, 
            layout['y'] + layout['height']/2 + 8, 
            text=f"{cps:.1f} CPS", 
            font=('Arial', 8), 
            fill=self.cps_color
        )
    
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
        
        # 绘制所有按键
        for key in ['w', 'a', 's', 'd', 'shift', 'c', 'space']:
            self.draw_key(key)
        
        # 绘制鼠标按键和CPS
        left_cps = self.calculate_cps(self.left_cps_history)
        right_cps = self.calculate_cps(self.right_cps_history)
        
        self.draw_mouse_button('left_mouse', left_cps)
        self.draw_mouse_button('right_mouse', right_cps)
    
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
        self.settings_window.geometry("400x550")
        self.settings_window.resizable(False, False)
        self.settings_window.attributes('-topmost', True)  # 设置窗口置顶
        
        # 设置透明背景
        self.settings_window.configure(bg=parent_app.transparent_color)
        self.settings_window.attributes('-transparentcolor', parent_app.transparent_color)
        
        # 创建主框架 - 设置透明背景
        main_frame = tk.Frame(self.settings_window, padx=10, pady=10, bg=parent_app.transparent_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题 - 设置透明背景
        title_label = tk.Label(main_frame, text="Key Strike Settings", font=('Arial', 16, 'bold'), 
                              bg=parent_app.transparent_color, fg=parent_app.text_color)
        title_label.pack(pady=10)
        
        # 按键按下颜色设置 - 设置透明背景
        pressed_frame = tk.Frame(main_frame, bg=parent_app.transparent_color)
        pressed_frame.pack(fill=tk.X, pady=5)
        
        pressed_label = tk.Label(pressed_frame, text="Pressed Key Color:", font=('Arial', 10), 
                                bg=parent_app.transparent_color, fg=parent_app.text_color)
        pressed_label.pack(side=tk.LEFT)
        
        self.pressed_color_btn = tk.Button(
            pressed_frame, 
            text="Choose", 
            bg=parent_app.key_pressed_color,
            command=lambda: self.choose_color('pressed'),
            width=10
        )
        self.pressed_color_btn.pack(side=tk.RIGHT)
        
        # 按键松开颜色设置 - 设置透明背景
        released_frame = tk.Frame(main_frame, bg=parent_app.transparent_color)
        released_frame.pack(fill=tk.X, pady=5)
        
        released_label = tk.Label(released_frame, text="Released Key Color:", font=('Arial', 10),
                                bg=parent_app.transparent_color, fg=parent_app.text_color)
        released_label.pack(side=tk.LEFT)
        
        self.released_color_btn = tk.Button(
            released_frame, 
            text="Choose", 
            bg=parent_app.key_released_color,
            command=lambda: self.choose_color('released'),
            width=10
        )
        self.released_color_btn.pack(side=tk.RIGHT)
        
        # 文字颜色设置 - 设置透明背景
        text_frame = tk.Frame(main_frame, bg=parent_app.transparent_color)
        text_frame.pack(fill=tk.X, pady=5)
        
        text_label = tk.Label(text_frame, text="Text Color:", font=('Arial', 10),
                             bg=parent_app.transparent_color, fg=parent_app.text_color)
        text_label.pack(side=tk.LEFT)
        
        self.text_color_btn = tk.Button(
            text_frame, 
            text="Choose", 
            bg=parent_app.text_color,
            command=lambda: self.choose_color('text'),
            width=10
        )
        self.text_color_btn.pack(side=tk.RIGHT)
        
        # 边框颜色设置 - 设置透明背景
        border_frame = tk.Frame(main_frame, bg=parent_app.transparent_color)
        border_frame.pack(fill=tk.X, pady=5)
        
        border_label = tk.Label(border_frame, text="Border Color:", font=('Arial', 10),
                              bg=parent_app.transparent_color, fg=parent_app.text_color)
        border_label.pack(side=tk.LEFT)
        
        self.border_color_btn = tk.Button(
            border_frame, 
            text="Choose", 
            bg=parent_app.border_color,
            command=lambda: self.choose_color('border'),
            width=10
        )
        self.border_color_btn.pack(side=tk.RIGHT)
        
        # CPS文字颜色设置 - 设置透明背景
        cps_frame = tk.Frame(main_frame, bg=parent_app.transparent_color)
        cps_frame.pack(fill=tk.X, pady=5)
        
        cps_label = tk.Label(cps_frame, text="CPS Text Color:", font=('Arial', 10),
                           bg=parent_app.transparent_color, fg=parent_app.text_color)
        cps_label.pack(side=tk.LEFT)
        
        self.cps_color_btn = tk.Button(
            cps_frame, 
            text="Choose", 
            bg=parent_app.cps_color,
            command=lambda: self.choose_color('cps'),
            width=10
        )
        self.cps_color_btn.pack(side=tk.RIGHT)
        
        # 配置文件管理框架
        config_frame = tk.Frame(main_frame, bg=parent_app.transparent_color)
        config_frame.pack(fill=tk.X, pady=10)
        
        config_label = tk.Label(config_frame, text="Configuration:", font=('Arial', 12, 'bold'),
                              bg=parent_app.transparent_color, fg=parent_app.text_color)
        config_label.pack(pady=5)
        
        # 导入配置按钮
        import_btn = tk.Button(
            config_frame,
            text="Import Config",
            command=self.import_config,
            width=15
        )
        import_btn.pack(pady=5)
        
        # 导出配置按钮
        export_btn = tk.Button(
            config_frame,
            text="Export Config",
            command=self.export_config,
            width=15
        )
        export_btn.pack(pady=5)
        
        # 重置按钮
        reset_btn = tk.Button(
            main_frame,
            text="Reset to Default",
            command=self.reset_colors,
            width=15
        )
        reset_btn.pack(pady=5)
        
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
        
        # 保存原始布局，用于重置
        self.original_layout = parent_app.key_layout.copy()
        
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
        
        # 重置布局
        self.parent_app.key_layout = self.original_layout.copy()
        
        messagebox.showinfo("Reset", "Colors and layout reset to default values.")
    
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
    
    def import_config(self):
        """导入配置文件"""
        file_path = filedialog.askopenfilename(
            title="Select Configuration File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    config = json.load(file)
                
                # 更新当前颜色设置
                if 'colors' in config:
                    colors = config['colors']
                    self.current_colors['pressed'] = colors.get('key_pressed_color', self.current_colors['pressed'])
                    self.current_colors['released'] = colors.get('key_released_color', self.current_colors['released'])
                    self.current_colors['text'] = colors.get('text_color', self.current_colors['text'])
                    self.current_colors['border'] = colors.get('border_color', self.current_colors['border'])
                    self.current_colors['cps'] = colors.get('cps_color', self.current_colors['cps'])
                
                # 更新布局
                if 'key_layout' in config:
                    self.parent_app.key_layout = config['key_layout']
                
                # 更新按钮颜色
                self.pressed_color_btn.config(bg=self.current_colors['pressed'])
                self.released_color_btn.config(bg=self.current_colors['released'])
                self.text_color_btn.config(bg=self.current_colors['text'])
                self.border_color_btn.config(bg=self.current_colors['border'])
                self.cps_color_btn.config(bg=self.current_colors['cps'])
                
                # 重绘界面
                self.parent_app.draw_interface()
                
                messagebox.showinfo("Success", "Configuration imported successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import configuration: {str(e)}")
    
    def export_config(self):
        """导出配置文件"""
        file_path = filedialog.asksaveasfilename(
            title="Save Configuration As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                config = {
                    'colors': {
                        'key_pressed_color': self.current_colors['pressed'],
                        'key_released_color': self.current_colors['released'],
                        'text_color': self.current_colors['text'],
                        'border_color': self.current_colors['border'],
                        'cps_color': self.current_colors['cps']
                    },
                    'key_layout': self.parent_app.key_layout
                }
                
                with open(file_path, 'w') as file:
                    json.dump(config, file, indent=4)
                
                messagebox.showinfo("Success", f"Configuration exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export configuration: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyDisplayApp(root)
    root.mainloop()