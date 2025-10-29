import tkinter as tk
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
        
        # 绘制初始界面
        self.draw_interface()
        
        # 开始监听按键
        self.start_key_listener()
        self.start_mouse_listener()
        
    def draw_key(self, x, y, width, height, text, is_pressed):
        """绘制按键"""
        color = '#FFFFFF' if is_pressed else '#969696'
        
        # 绘制按键
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline='#323232', width=2)
        
        # 绘制文字
        self.canvas.create_text(x+width/2, y+height/2, text=text, font=('Arial', 12, 'bold'), fill='#000000')
    
    def draw_mouse_button(self, x, y, width, height, text, is_pressed, cps):
        """绘制鼠标按键和CPS"""
        color = '#FFFFFF' if is_pressed else '#969696'
        
        # 绘制按键
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline='#323232', width=2)
        
        # 绘制文字
        self.canvas.create_text(x+width/2, y+height/2-6, text=text, font=('Arial', 10, 'bold'), fill='#000000')
        
        # 绘制CPS
        self.canvas.create_text(x+width/2, y+height/2+8, text=f"{cps:.1f} CPS", 
                               font=('Arial', 8), fill='#006400')
    
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
        self.canvas.create_text(250, 15, text="Key Strike", font=('Arial', 12, 'bold'), fill='#000000')
        self.canvas.create_text(250, 35, text="Press F9 to exit", font=('Arial', 8), fill='#000000')
        
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
    
    def close_app(self):
        """关闭应用程序"""
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyDisplayApp(root)
    root.mainloop()