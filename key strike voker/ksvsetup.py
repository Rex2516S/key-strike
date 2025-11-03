import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog, ttk
import json

class ConfigGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Strike Config Generator")
        self.root.geometry("500x750")  # 增加窗口高度以容纳新功能
        self.root.resizable(False, False)
        
        # 默认颜色值
        self.colors = {
            'key_pressed_color': '#FFFFFF',
            'key_released_color': '#969696',
            'text_color': '#000000',
            'border_color': '#323232',
            'cps_color': '#006400'
        }
        
        # 默认按键布局
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
        
        # 创建主框架
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 标题
        title_label = tk.Label(scrollable_frame, text="Key Strike Config Generator", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 颜色设置框架
        colors_frame = tk.LabelFrame(scrollable_frame, text="Color Settings", padx=10, pady=10)
        colors_frame.pack(fill=tk.X, pady=10)
        
        # 按键按下颜色设置
        pressed_frame = tk.Frame(colors_frame)
        pressed_frame.pack(fill=tk.X, pady=5)
        
        pressed_label = tk.Label(pressed_frame, text="Pressed Key Color:", font=('Arial', 10), width=20, anchor='w')
        pressed_label.pack(side=tk.LEFT)
        
        self.pressed_color_btn = tk.Button(
            pressed_frame, 
            text="Choose", 
            bg=self.colors['key_pressed_color'],
            command=lambda: self.choose_color('key_pressed_color'),
            width=10
        )
        self.pressed_color_btn.pack(side=tk.RIGHT)
        
        # 按键松开颜色设置
        released_frame = tk.Frame(colors_frame)
        released_frame.pack(fill=tk.X, pady=5)
        
        released_label = tk.Label(released_frame, text="Released Key Color:", font=('Arial', 10), width=20, anchor='w')
        released_label.pack(side=tk.LEFT)
        
        self.released_color_btn = tk.Button(
            released_frame, 
            text="Choose", 
            bg=self.colors['key_released_color'],
            command=lambda: self.choose_color('key_released_color'),
            width=10
        )
        self.released_color_btn.pack(side=tk.RIGHT)
        
        # 文字颜色设置
        text_frame = tk.Frame(colors_frame)
        text_frame.pack(fill=tk.X, pady=5)
        
        text_label = tk.Label(text_frame, text="Text Color:", font=('Arial', 10), width=20, anchor='w')
        text_label.pack(side=tk.LEFT)
        
        self.text_color_btn = tk.Button(
            text_frame, 
            text="Choose", 
            bg=self.colors['text_color'],
            command=lambda: self.choose_color('text_color'),
            width=10
        )
        self.text_color_btn.pack(side=tk.RIGHT)
        
        # 边框颜色设置
        border_frame = tk.Frame(colors_frame)
        border_frame.pack(fill=tk.X, pady=5)
        
        border_label = tk.Label(border_frame, text="Border Color:", font=('Arial', 10), width=20, anchor='w')
        border_label.pack(side=tk.LEFT)
        
        self.border_color_btn = tk.Button(
            border_frame, 
            text="Choose", 
            bg=self.colors['border_color'],
            command=lambda: self.choose_color('border_color'),
            width=10
        )
        self.border_color_btn.pack(side=tk.RIGHT)
        
        # CPS文字颜色设置
        cps_frame = tk.Frame(colors_frame)
        cps_frame.pack(fill=tk.X, pady=5)
        
        cps_label = tk.Label(cps_frame, text="CPS Text Color:", font=('Arial', 10), width=20, anchor='w')
        cps_label.pack(side=tk.LEFT)
        
        self.cps_color_btn = tk.Button(
            cps_frame, 
            text="Choose", 
            bg=self.colors['cps_color'],
            command=lambda: self.choose_color('cps_color'),
            width=10
        )
        self.cps_color_btn.pack(side=tk.RIGHT)
        
        # 按键布局设置框架
        layout_frame = tk.LabelFrame(scrollable_frame, text="Key Layout Settings", padx=10, pady=10)
        layout_frame.pack(fill=tk.X, pady=10)
        
        # 按键选择下拉菜单
        key_select_frame = tk.Frame(layout_frame)
        key_select_frame.pack(fill=tk.X, pady=5)
        
        key_label = tk.Label(key_select_frame, text="Select Key:", font=('Arial', 10), width=20, anchor='w')
        key_label.pack(side=tk.LEFT)
        
        self.selected_key = tk.StringVar()
        self.key_dropdown = ttk.Combobox(key_select_frame, textvariable=self.selected_key, state="readonly")
        self.key_dropdown['values'] = list(self.key_layout.keys())
        self.key_dropdown.current(0)
        self.key_dropdown.pack(side=tk.RIGHT)
        self.key_dropdown.bind('<<ComboboxSelected>>', self.on_key_selected)
        
        # 按键文本设置
        key_text_frame = tk.Frame(layout_frame)
        key_text_frame.pack(fill=tk.X, pady=5)
        
        key_text_label = tk.Label(key_text_frame, text="Key Text:", font=('Arial', 10), width=20, anchor='w')
        key_text_label.pack(side=tk.LEFT)
        
        self.key_text_var = tk.StringVar()
        self.key_text_entry = tk.Entry(key_text_frame, textvariable=self.key_text_var, width=15)
        self.key_text_entry.pack(side=tk.RIGHT)
        self.key_text_entry.bind('<KeyRelease>', self.on_key_text_changed)
        
        # 位置设置框架
        pos_frame = tk.Frame(layout_frame)
        pos_frame.pack(fill=tk.X, pady=5)
        
        # X坐标
        x_frame = tk.Frame(pos_frame)
        x_frame.pack(fill=tk.X, pady=2)
        
        x_label = tk.Label(x_frame, text="X Position:", font=('Arial', 10), width=20, anchor='w')
        x_label.pack(side=tk.LEFT)
        
        self.x_var = tk.IntVar()
        self.x_scale = tk.Scale(x_frame, from_=0, to=500, orient=tk.HORIZONTAL, 
                               variable=self.x_var, showvalue=True, length=200)
        self.x_scale.pack(side=tk.RIGHT)
        self.x_scale.bind('<ButtonRelease-1>', self.on_position_changed)
        
        # Y坐标
        y_frame = tk.Frame(pos_frame)
        y_frame.pack(fill=tk.X, pady=2)
        
        y_label = tk.Label(y_frame, text="Y Position:", font=('Arial', 10), width=20, anchor='w')
        y_label.pack(side=tk.LEFT)
        
        self.y_var = tk.IntVar()
        self.y_scale = tk.Scale(y_frame, from_=0, to=300, orient=tk.HORIZONTAL, 
                               variable=self.y_var, showvalue=True, length=200)
        self.y_scale.pack(side=tk.RIGHT)
        self.y_scale.bind('<ButtonRelease-1>', self.on_position_changed)
        
        # 宽度设置
        width_frame = tk.Frame(layout_frame)
        width_frame.pack(fill=tk.X, pady=2)
        
        width_label = tk.Label(width_frame, text="Width:", font=('Arial', 10), width=20, anchor='w')
        width_label.pack(side=tk.LEFT)
        
        self.width_var = tk.IntVar()
        self.width_scale = tk.Scale(width_frame, from_=10, to=200, orient=tk.HORIZONTAL, 
                                   variable=self.width_var, showvalue=True, length=200)
        self.width_scale.pack(side=tk.RIGHT)
        self.width_scale.bind('<ButtonRelease-1>', self.on_position_changed)
        
        # 高度设置
        height_frame = tk.Frame(layout_frame)
        height_frame.pack(fill=tk.X, pady=2)
        
        height_label = tk.Label(height_frame, text="Height:", font=('Arial', 10), width=20, anchor='w')
        height_label.pack(side=tk.LEFT)
        
        self.height_var = tk.IntVar()
        self.height_scale = tk.Scale(height_frame, from_=10, to=100, orient=tk.HORIZONTAL, 
                                    variable=self.height_var, showvalue=True, length=200)
        self.height_scale.pack(side=tk.RIGHT)
        self.height_scale.bind('<ButtonRelease-1>', self.on_position_changed)
        
        # 重置布局按钮
        reset_layout_btn = tk.Button(
            layout_frame,
            text="Reset Layout to Default",
            command=self.reset_layout,
            width=20
        )
        reset_layout_btn.pack(pady=10)
        
        # 预设配置框架
        preset_frame = tk.LabelFrame(scrollable_frame, text="Preset Configurations", padx=10, pady=10)
        preset_frame.pack(fill=tk.X, pady=10)
        
        # 预设按钮框架 - 使用两列布局
        preset_buttons_frame = tk.Frame(preset_frame)
        preset_buttons_frame.pack()
        
        # 第一行预设按钮
        default_btn = tk.Button(
            preset_buttons_frame,
            text="Default",
            command=self.load_default,
            width=12
        )
        default_btn.grid(row=0, column=0, padx=5, pady=5)
        
        dark_btn = tk.Button(
            preset_buttons_frame,
            text="Dark Theme",
            command=self.load_dark_theme,
            width=12
        )
        dark_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # 第二行预设按钮
        light_btn = tk.Button(
            preset_buttons_frame,
            text="Light Theme",
            command=self.load_light_theme,
            width=12
        )
        light_btn.grid(row=1, column=0, padx=5, pady=5)
        
        neon_btn = tk.Button(
            preset_buttons_frame,
            text="Neon Theme",
            command=self.load_neon_theme,
            width=12
        )
        neon_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # 第三行预设按钮 - 添加更多主题
        red_btn = tk.Button(
            preset_buttons_frame,
            text="Red Theme",
            command=self.load_red_theme,
            width=12
        )
        red_btn.grid(row=2, column=0, padx=5, pady=5)
        
        blue_btn = tk.Button(
            preset_buttons_frame,
            text="Blue Theme",
            command=self.load_blue_theme,
            width=12
        )
        blue_btn.grid(row=2, column=1, padx=5, pady=5)
        
        # 操作按钮框架
        action_frame = tk.Frame(scrollable_frame)
        action_frame.pack(fill=tk.X, pady=15)
        
        # 生成配置文件按钮 - 确保这个按钮存在且可见
        generate_btn = tk.Button(
            action_frame,
            text="Generate Config File",
            command=self.generate_config,
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            font=('Arial', 10, 'bold')
        )
        generate_btn.pack(pady=10)
        
        # 预览当前配置按钮
        preview_btn = tk.Button(
            action_frame,
            text="Preview Current Colors",
            command=self.preview_colors,
            width=20
        )
        preview_btn.pack(pady=5)
        
        # 状态标签
        self.status_label = tk.Label(scrollable_frame, text="Ready to generate configuration", 
                                    font=('Arial', 8), fg='gray')
        self.status_label.pack(pady=5)
        
        # 初始化当前选择的按键
        self.on_key_selected()
    
    def on_key_selected(self, event=None):
        """当选择新按键时更新界面"""
        key = self.selected_key.get()
        if key in self.key_layout:
            layout = self.key_layout[key]
            self.key_text_var.set(layout['text'])
            self.x_var.set(layout['x'])
            self.y_var.set(layout['y'])
            self.width_var.set(layout['width'])
            self.height_var.set(layout['height'])
    
    def on_key_text_changed(self, event=None):
        """当按键文本改变时更新布局"""
        key = self.selected_key.get()
        if key in self.key_layout:
            self.key_layout[key]['text'] = self.key_text_var.get()
    
    def on_position_changed(self, event=None):
        """当位置或尺寸改变时更新布局"""
        key = self.selected_key.get()
        if key in self.key_layout:
            self.key_layout[key]['x'] = self.x_var.get()
            self.key_layout[key]['y'] = self.y_var.get()
            self.key_layout[key]['width'] = self.width_var.get()
            self.key_layout[key]['height'] = self.height_var.get()
    
    def choose_color(self, color_type):
        """打开颜色选择器"""
        current_color = self.colors[color_type]
        
        color_code = colorchooser.askcolor(
            initialcolor=current_color,
            title=f"Choose {color_type} color"
        )
        
        if color_code[1] is not None:
            self.colors[color_type] = color_code[1]
            
            # 更新按钮颜色
            if color_type == 'key_pressed_color':
                self.pressed_color_btn.config(bg=color_code[1])
            elif color_type == 'key_released_color':
                self.released_color_btn.config(bg=color_code[1])
            elif color_type == 'text_color':
                self.text_color_btn.config(bg=color_code[1])
            elif color_type == 'border_color':
                self.border_color_btn.config(bg=color_code[1])
            elif color_type == 'cps_color':
                self.cps_color_btn.config(bg=color_code[1])
            
            self.status_label.config(text=f"Updated {color_type.replace('_', ' ')}")
    
    def load_default(self):
        """加载默认配置"""
        self.colors = {
            'key_pressed_color': '#FFFFFF',
            'key_released_color': '#969696',
            'text_color': '#000000',
            'border_color': '#323232',
            'cps_color': '#006400'
        }
        self.update_button_colors()
        self.reset_layout()
        self.status_label.config(text="Default configuration loaded!")
    
    def load_dark_theme(self):
        """加载暗色主题"""
        self.colors = {
            'key_pressed_color': '#4A4A4A',
            'key_released_color': '#2D2D2D',
            'text_color': '#FFFFFF',
            'border_color': '#666666',
            'cps_color': '#00FF00'
        }
        self.update_button_colors()
        self.status_label.config(text="Dark theme loaded!")
    
    def load_light_theme(self):
        """加载亮色主题"""
        self.colors = {
            'key_pressed_color': '#F0F0F0',
            'key_released_color': '#D0D0D0',
            'text_color': '#000000',
            'border_color': '#A0A0A0',
            'cps_color': '#0077CC'
        }
        self.update_button_colors()
        self.status_label.config(text="Light theme loaded!")
    
    def load_neon_theme(self):
        """加载霓虹主题"""
        self.colors = {
            'key_pressed_color': '#FF00FF',
            'key_released_color': '#990099',
            'text_color': '#FFFFFF',
            'border_color': '#00FFFF',
            'cps_color': '#FFFF00'
        }
        self.update_button_colors()
        self.status_label.config(text="Neon theme loaded!")
    
    def load_red_theme(self):
        """加载红色主题"""
        self.colors = {
            'key_pressed_color': '#FF6B6B',
            'key_released_color': '#CC5555',
            'text_color': '#FFFFFF',
            'border_color': '#FF3333',
            'cps_color': '#FFCC00'
        }
        self.update_button_colors()
        self.status_label.config(text="Red theme loaded!")
    
    def load_blue_theme(self):
        """加载蓝色主题"""
        self.colors = {
            'key_pressed_color': '#6B8CFF',
            'key_released_color': '#5577CC',
            'text_color': '#FFFFFF',
            'border_color': '#3366FF',
            'cps_color': '#00FFCC'
        }
        self.update_button_colors()
        self.status_label.config(text="Blue theme loaded!")
    
    def reset_layout(self):
        """重置按键布局为默认值"""
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
        self.on_key_selected()
        self.status_label.config(text="Layout reset to default!")
    
    def update_button_colors(self):
        """更新所有按钮颜色"""
        self.pressed_color_btn.config(bg=self.colors['key_pressed_color'])
        self.released_color_btn.config(bg=self.colors['key_released_color'])
        self.text_color_btn.config(bg=self.colors['text_color'])
        self.border_color_btn.config(bg=self.colors['border_color'])
        self.cps_color_btn.config(bg=self.colors['cps_color'])
    
    def generate_config(self):
        """生成配置文件"""
        file_path = filedialog.asksaveasfilename(
            title="Save Configuration As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                config = {
                    'colors': self.colors,
                    'key_layout': self.key_layout
                }
                
                with open(file_path, 'w') as file:
                    json.dump(config, file, indent=4)
                
                messagebox.showinfo("Success", f"Configuration file generated:\n{file_path}")
                self.status_label.config(text=f"Config saved to: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate configuration: {str(e)}")
                self.status_label.config(text="Error saving configuration")
    
    def preview_colors(self):
        """预览当前颜色配置"""
        preview_text = f"""
Current Color Configuration:
- Pressed Key: {self.colors['key_pressed_color']}
- Released Key: {self.colors['key_released_color']}
- Text: {self.colors['text_color']}
- Border: {self.colors['border_color']}
- CPS Text: {self.colors['cps_color']}

Current Layout:
"""
        for key, layout in self.key_layout.items():
            preview_text += f"- {key}: {layout['text']} at ({layout['x']}, {layout['y']}) size {layout['width']}x{layout['height']}\n"
        
        messagebox.showinfo("Current Configuration", preview_text.strip())


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGenerator(root)
    root.mainloop()