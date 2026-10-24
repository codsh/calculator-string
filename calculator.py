import time
import datetime

from tkinter import *
from tkinter import font, ttk, SEL_FIRST, SEL_LAST

from collections import Counter
from functools import lru_cache, wraps

import re
import json

import random
import math
from decimal import *
getcontext().prec = 1402

import winreg
import ctypes
import ctypes.wintypes
user32 = ctypes.WinDLL("user32", use_last_error=True)


# import pyautogui
# pyautogui.PAUSE = 0

_mp = None
def _get_mp():
    global _mp
    if _mp is None:
        from mpmath import mp
        mp.dps = 402
        _mp = mp
    return _mp


# Пример подключения внизу calculator.py (перед main_win.mainloop()):
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
AttachThreadInput = user32.AttachThreadInput
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))
IsWindowVisible = user32.IsWindowVisible
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextW = user32.GetWindowTextW
GetClassNameW = user32.GetClassNameW
SetForegroundWindow = user32.SetForegroundWindow

def create_fake_main_win():
    global fake_main_win
    fake_main_win = Toplevel()
    fake_main_win.title(main_win.title())
    fake_main_win['bg'] = main_win['bg']

    fake_main_win.wm_attributes('-topmost', main_win.wm_attributes('-topmost'))
    fake_main_win.attributes('-alpha', main_win.attributes('-alpha'))
    fake_main_win.overrideredirect(main_win.overrideredirect())

    fake_entry_box = Entry(fake_main_win, font=entry_box.cget('font'), fg=entry_box.cget('fg'), bg=entry_box.cget('bg'), borderwidth=0, insertwidth=1)
    fake_result = Entry(fake_main_win, font=entry_box.cget('font'), fg=entry_box.cget('fg'), bg=entry_box.cget('bg'), borderwidth=0, insertwidth=1)
    (fake_entry_box.insert(END, entry_box.get()), fake_result.insert(END, result.get()))
    entry_box_place_info, result_place_info = entry_box.place_info(), result.place_info()
    entry_box_place_info.pop('in'), result_place_info.pop('in')
    (fake_entry_box.place(entry_box_place_info), fake_result.place(result_place_info))
    fake_main_win.geometry(main_win.geometry())


def switch_to_next_window():
    # Прячем калькулятор с экрана: в этот момент Windows находится в шоке и ПРИНУДИТЕЛЬНО отдает фокус и каретку окну, которое было под ним.
    main_win.after(50, create_fake_main_win)
    main_win.after(70, main_win.withdraw)
    # Через 200 миллисекунд возвращаем калькулятор обратно. Он появится на том же месте, но фокус останется в чужом окне, а каретка там гарантированно активируется!
    main_win.after(150, main_win.deiconify)
    main_win.after(170, lambda: fake_main_win.destroy())
    if added_win.focus_displayof():
        main_win.after(200, lambda: main_win.event_generate('<FocusOut>'))

    return 'break'


calculator_greeting = 'нажми [?] или ctrl+[/], чтобы узнать как работать с калькулятором'

def highlight_i_history_text_and_centralize(i_history):  # здесь была подсветка, которая была неудачна из-за foreground-а
    text_entry.tag_remove(SEL, '1.0', 'end')
    if type(i_history) is int:
        text_entry.update_idletasks()  # обновление геометрии, чтобы ткинтер смог всё рассчитать
        text_entry.focus_force()
        text_entry.tag_add(SEL, f'{i_history + 1}.0', f'{i_history + 4}.0')
        
        sel_center = (int(text_entry.index('sel.last').split('.')[0]) + int(text_entry.index('sel.first').split('.')[0])) // 2
        first_line = int(text_entry.index("@0,0").split('.')[0])
        last_line = int(text_entry.index(f"@0,{text_entry.winfo_height()}").split('.')[0])
        center_line_shift = (last_line - first_line) // 2
        text_entry.yview_pickplace(sel_center - center_line_shift)
    return i_history

def clean_pattern_empty_scopes(example_to_clean):
    example_to_clean = re.sub(r'√(\s*)\)', r'√(\1))', example_to_clean)
    while re.search(pattern_checking_on_empty_scopes, example_to_clean):
        example_to_clean = re.sub(pattern_checking_on_empty_scopes, '', example_to_clean)
    return example_to_clean


def get_text_length(text, entry):
    font_obj = font.Font(font=entry.cget("font"))
    return font_obj.measure(text)


def setting_y(coord):
    settings['y'] = coord
    try:
        change_width_of_entry(entry_box.get(), entry_box, result)
    except NameError:
        pass


def setting_x(coord):
    settings['x'] = coord


def change_width_of_entry(text, entry1, entry2):
    entry_text_length = get_text_length(text, entry1)
    if main_win.focus_get() in (main_win, entry_box, result):
        entry1.place(x=1, y=1, width=entry_text_length + 4, height=HEIGHT - (2, 1)[settings['y'] == MAX_COORD])
        entry2.place(x=entry_text_length + 2, y=1, width=(WIDTH - 2) - (entry_text_length + 1), height=HEIGHT - (2, 1)[settings['y'] == MAX_COORD])
    else:
        entry1.place(x=1, y=0, width=entry_text_length + 4, height=HEIGHT)
        entry2.place(x=entry_text_length + 2, y=0, width=(WIDTH - 2) - (entry_text_length + 1), height=HEIGHT)
    
    
def change_size_of_everything(scale, scale_was_zero=False, change_result=True):
    global max_character_amount, place_coords, last_time_main_win_geometry_change, val_before_last_main_win_geometry_change, tape
    global WIDTH, HEIGHT, MIN_X_COORD, MAX_COORD, MAX_X_COORD
    max_character_amount = (174, 174, 152, 120, 99, 71)[scale]
    
    HEIGHT = screen_width // (201, 81, 71, 61, 51, 41)[scale]
    MIN_X_COORD = screen_width // 12

    WIDTH = screen_width - 2 * MIN_X_COORD
    MAX_COORD = screen_height - get_taskbar_height() - HEIGHT
    MAX_X_COORD = screen_width - MIN_X_COORD - 8 * 2
    if abs(settings['y'] - recents['mid']) <= HEIGHT and (settings['scale'] != scale or scale_was_zero):
        setting_y(MAX_COORD // 2)
    if abs(settings['y'] - recents['low']) <= HEIGHT and (settings['scale'] != scale or scale_was_zero):
        setting_y(MAX_COORD)

    recents['low'], recents['mid'], recents['top'] = MAX_COORD, MAX_COORD // 2, 0
    place_coords = (recents['low'], recents['mid'], recents['top'])
    
    entry_box.config(font=('Arial', HEIGHT // 2))
    result.config(font=('Arial', HEIGHT // 2))

    if added_win.title() != invisible_win_title and scale:
        is_help = added_win.title() == 'инструкция'
        text_entry.config(font=('Arial', int(HEIGHT // (2.3, 2)[is_help]), 'bold'))
        if is_help:
            finish_to_help_win()
    change_width_of_entry(entry_box.get(), entry_box, result)
    main_win.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{settings['y']}')
    if tape:
        tape.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{settings['y'] - HEIGHT}')
        resize_and_retheme_canvas_drawings()
    close_label.place(x=WIDTH - HEIGHT // 3, y=1, width=HEIGHT // 3 - 1, height=HEIGHT // 3 - 1)
    close_label.config(font=('Arial', HEIGHT // 3 - 1))
    hide_label.place(x=WIDTH - 2 * HEIGHT // 3 + 1, y=1, width=HEIGHT // 3 - 1, height=HEIGHT // 3 - 1)
    hide_label.config(font=('Arial', HEIGHT // 3 - 1))
    
    if change_result:
        if not re.search(calc_geometry_state_change_expression, result.get()):
            val_before_last_main_win_geometry_change = result.get()
        result.delete(0, END)
        result.insert(END, f'{' ' * bool(example_value)}Максимум {max_character_amount} символ{get_correct_ending(max_character_amount, word_ends2)}')
        last_time_main_win_geometry_change = time.time()
    if scale:
        settings['scale'] = scale


history_of_calculations, recents, settings = None, None, None
def rewrite_json(file):
    with open(f'{FILES}/{file}.json', 'w') as json_file:
            json.dump({'history': history_of_calculations, 'settings': settings, 'recents': recents}[file], json_file)
            
            
def create_greeting():
    global calculator_greeting
    with open(f'{FILES}/greetings.json', 'r', encoding='utf-8') as greetings_file:
        calculator_greeting = random.choice(json.load(greetings_file))
        

FILES = 'data'
DAY = 60 * 60 * 24

screen_width, screen_height = map(user32.GetSystemMetrics, (0, 1))

# Получить высоту панели задач
def get_taskbar_height():
    SPI_GETWORKAREA = 48
    rect = ctypes.wintypes.RECT()
    user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    taskbar_height = screen_height - (rect.bottom - rect.top)
    return taskbar_height

def is_dark_theme():
    # Путь к ключу реестра, где хранятся настройки темы
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    value_name = "AppsUseLightTheme"  # Значение, которое определяет светлую или тёмную тему

    try:
        # Открываем ключ реестра
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path)
        
        # Читаем значение
        value, _ = winreg.QueryValueEx(registry_key, value_name)
        
        # Закрываем ключ
        winreg.CloseKey(registry_key)
        
        # Если значение 0, то тема тёмная, иначе светлая
        return value == 0
    except FileNotFoundError:
        # Если ключ или значение не найдены, предполагаем светлую тему (или обработайте ошибку по-другому)
        return False

TASKBAR_HEIGHT = get_taskbar_height()
MAX_COORD = screen_height - TASKBAR_HEIGHT - screen_width // 61
MAX_LOW_COORD = screen_height - TASKBAR_HEIGHT
MIN_X_COORD = screen_width // 12

with open(f'{FILES}/history.json', 'r') as history_file:
    try:
        history_of_calculations = json.load(history_file)
    except json.decoder.JSONDecodeError:
        history_of_calculations = 'Пример\nРезультат вычислений\nДата время вычисления (точность округления): 1-й запуск программы ' + str(datetime.datetime.today())[:-7].replace('-', '.') + ' (округление по умолчанию)'
        rewrite_json('history')
with open(f'{FILES}/recents.json', 'r') as recents_file:
    try:
        recents = json.load(recents_file)
    except json.decoder.JSONDecodeError:
        recents = {'closing time': [0 for _ in range(3)], 'example before closing': '', 'cursor before closing': 0, 'cursor before moving calc': 0,
                   'recent examples': [['', '', '', ''] for _ in range(100)], 'last examples': [['', '', '', '', '', ''],],
                   'low': MAX_COORD, 'mid': MAX_COORD // 2, 'top': 0, 'mouse coords': {'x': 0, 'y': 0}, 'win theme alike calc': True, 'rounding info longer': 3}
        rewrite_json('recents')
with open(f'{FILES}/settings.json', 'r') as settings_file:
    try:
        settings = json.load(settings_file)
    except json.decoder.JSONDecodeError:
        settings = {'y': MAX_COORD, 'x': 0, 'history length': 4000, 'history type': 'history', 'theme': ('dark', 'light')[not is_dark_theme()], 'scale': 3, 'round': 'по умолчанию'}
        rewrite_json('settings')
if recents['rounding info longer'] == 0:
    recents['rounding info longer'] = (time.time() - recents['closing time'][-1] > 28 * DAY) * 2


def opening_animation():
    # ==========================================
    # ЧАСТЬ 1: Математическая модель и генерация галактики
    # ==========================================
    class GalaxyTopology:
        def __init__(self, scale, cx, cy):
            self.scale = scale
            self.cx = cx
            self.cy = cy
            self.bar_angle = math.radians(-30)
            self.galaxy_branches = []
            self.galaxy_stars = []
            self.sky_stars = []
            self.core_particles = []
            self.back_rings = []
            self.front_rings = []
            self.bottom_rings = []

        def get_gradient_color(self, t):
            if t < 0.12: return "#F0F8FF"
            if t < 0.35: return f"#{int(240 - 40*t/0.35):02x}{int(248 - 65*t/0.35):02x}ff"
            if t < 0.70: p = (t - 0.35) / 0.35; return f"#{int(190 - 150*p):02x}{int(212 - 140*p):02x}ff"
            return f"#{int(40 - 40*((t - 0.70)/0.30)):02x}{int(72 - 60*((t - 0.70)/0.30)):02x}{int(255 - 180*((t - 0.70)/0.30)):02x}"

        def build(self, canvas, logo_r, bar_offset):
            pool = ["#FFFFFF"] * 12 + ["#FFD54F"] * 5 + ["#64B5F6"] * 3
            max_bg_dist = 280 * self.scale
            
            for _ in range(200):
                ang, dist, col = random.uniform(0, 2*math.pi), random.uniform(0, max_bg_dist), random.choice(pool)
                x, y = self.cx + dist * math.cos(ang), self.cy + dist * math.sin(ang)
                self.sky_stars.append({
                    "id": canvas.create_oval(x, y, x + 2, y + 2, fill=col, outline=""), 
                    "blink_speed": random.uniform(0.05, 0.12), "blink_phase": random.uniform(0, 10), "base_color": col
                })
                
            for i in range(140):
                arm_phase, is_milk, segments = (i * 2 * math.pi) / 140, (i % 4 == 0), []
                for j in range(40):
                    t_seg = j / 40
                    color = "#F0F8FF" if is_milk and t_seg < 0.35 else (f"#{int(240 - 35*(t_seg/0.7)):02x}{int(248 - 50*(t_seg/0.7)):02x}ff" if is_milk else self.get_gradient_color(t_seg))
                    w_max, w_min = (6.0 * self.scale, 2.5 * self.scale) if is_milk else (4.5 * self.scale, 1.5 * self.scale)
                    width_val = max(w_min, w_max * (1.0 - t_seg * (0.5 if is_milk else 0.7)))
                    segments.append(canvas.create_line(0, 0, 0, 0, fill=color, width=width_val, capstyle="round"))
                    
                branch_data = {"segments": segments, "phase": arm_phase, "r_max": (195 + (i % 3) * 12) * self.scale, "is_milk": is_milk}
                self.galaxy_branches.append(branch_data)
                for _ in range(16 if is_milk else 5):
                    t_star = random.uniform(0.01, 1.0)
                    self.galaxy_stars.append({
                        "id": canvas.create_oval(0, 0, 0, 0, fill=random.choice(pool) if (is_milk or random.random() > 0.4) else self.get_gradient_color(t_star), outline=""), 
                        "branch": branch_data, "t": t_star, "size": random.choice([1, 2, 2]) * self.scale
                    })
            
            cols = ["#1f0700", "#381001", "#541902", "#732403", "#913004", "#b03e05", "#cf4d06", "#ed5e08", "#ff7311", "#ff8624", "#ff9b3b", "#ffb154", "#ffc670", "#ffd98c", "#ffe9a6", "#fff4c2", "#fffada", "#ffffff"]
            for idx in range(70):
                thick_cfg = {"fill": cols[min(idx // 4, 17)], "width": max(0.25 * self.scale, (1.3 - idx * 0.015) * self.scale), "capstyle": "round", "state": "hidden"}
                front_cfg = {"fill": cols[min(idx // 4, 17)], "width": max(1.5 * self.scale, (6.0 - idx * 0.07) * self.scale), "capstyle": "round", "state": "hidden"}
                
                r_outer = (95 + idx * 0.6) * self.scale
                r_front = (68 + idx * 0.4) * self.scale
                
                self.back_rings.append({"id": canvas.create_line(0, 0, 0, 0, **thick_cfg), "base_r": r_outer})
                self.bottom_rings.append({"id": canvas.create_line(0, 0, 0, 0, **thick_cfg), "base_r": r_outer})
                self.front_rings.append({"id": canvas.create_line(0, 0, 0, 0, **front_cfg), "base_r": r_front})

            for _ in range(800):
                ang, dist = random.uniform(0, 2 * math.pi), random.uniform(0, 1.0) ** 1.6
                self.core_particles.append({
                    "id": canvas.create_oval(0, 0, 0, 0, fill=random.choice(["#FFFFFF", "#FFFDE7"]) if dist < 0.35 else random.choice(["#FFF9C4", "#FFF59D"]), outline=""), 
                    "local_x": 45 * self.scale * dist * math.cos(ang), "local_y": 18 * self.scale * dist * math.sin(ang), 
                    "branch": random.choice(self.galaxy_branches), "t_factor": dist * 0.15
                })

        def sample_spiral_path(self, t, branch, progress, frame, logo_r, bar_offset):
            r_space = t * branch["r_max"]
            angle_vortex = self.bar_angle + branch["phase"] + 6.8 * (t ** 0.5) + (frame * 0.10) + ((35 * self.scale) / (r_space + 12 * self.scale)) * progress
            if branch["phase"] < math.pi / 2 or (math.pi <= branch["phase"] < 3 * math.pi / 2):
                tx = self.cx - 100 * self.scale + t * 200 * self.scale
                ty = self.cy - bar_offset if branch["phase"] < math.pi else self.cy + bar_offset
            else:
                tx = self.cx + logo_r * math.cos(self.bar_angle + branch["phase"] + t * 2 * math.pi)
                ty = self.cy + logo_r * math.sin(self.bar_angle + branch["phase"] + t * 2 * math.pi)
            sp = progress * progress * (3.0 - 2.0 * progress)
            return (1.0 - sp) * (self.cx + r_space * math.cos(angle_vortex)) + sp * tx, (1.0 - sp) * (self.cy + r_space * math.sin(angle_vortex)) + sp * ty

    # ==========================================
    # ЧАСТЬ 2: Адаптивное окно и гравитационные кольца
    # ==========================================
    class ElegantGalacticTransform:
        def __init__(self, root):
            self.root = root
            root.wm_attributes("-transparentcolor", "#00FF00", "-topmost", True)
            root.overrideredirect(True)
            
            sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
            self.base_size = min(sw, sh) // 4
            
            x_pos = (sw - self.base_size) // 2
            y_pos = (sh - self.base_size) // 2
            root.geometry(f"{self.base_size}x{self.base_size}+{x_pos}+{y_pos}")
            
            self.canvas = Canvas(root, width=self.base_size, height=self.base_size, bg="#00FF00", highlightthickness=0)
            self.canvas.pack()
            
            self.scale = self.base_size / 600.0
            self.cx = self.cy = self.base_size // 2
            self.frame = 0
            
            self.logo_r = 185 * self.scale
            self.bar_offset = 48 * self.scale
            
            self.topo = GalaxyTopology(self.scale, self.cx, self.cy)
            self.topo.build(self.canvas, self.logo_r, self.bar_offset)
            
            self.shadow_id = self.canvas.create_oval(0, 0, 0, 0, fill="#000000", outline="", state="hidden")
            self.logo_circle = self.canvas.create_oval(0, 0, 0, 0, outline="#F0F8FF", width=12 * self.scale, state="hidden")
            self.logo_bar1 = self.canvas.create_line(0, 0, 0, 0, fill="#F0F8FF", width=44 * self.scale, capstyle="round", state="hidden")
            self.logo_bar2 = self.canvas.create_line(0, 0, 0, 0, fill="#F0F8FF", width=44 * self.scale, capstyle="round", state="hidden")
            
            self.flare_elements = []
            self.flare_frame = 0
            self.flare_triggered = False  # Контроль однократного запуска вспышки
            
            self.animate()

        def draw_lensed_rings(self, rings, wave, dy, mode):
            for ring in rings:
                self.canvas.itemconfigure(ring["id"], state="normal")
                r, pts = ring["base_r"] * wave, []
                for step in range(41):
                    ang = -math.pi + (step / 40) * 2 * math.pi
                    cos_val, sin_val = math.cos(ang), math.sin(ang)
                    is_behind = (sin_val < 0)
                    
                    zoom_x = 1.45
                    target_x = self.cx + r * cos_val * zoom_x
                    
                    tight_pinch = sin_val * sin_val
                    round_dome = math.pow(abs(sin_val), 1.85) * tight_pinch
                    
                    if mode == "back" and is_behind:
                        pts.extend([target_x, self.cy - abs(r * 0.75 * round_dome) * dy])
                    elif mode == "bottom" and is_behind:
                        pts.extend([target_x, self.cy + abs(r * 0.75 * round_dome) * dy])
                    elif mode == "front" and not is_behind:
                        pts.extend([target_x, self.cy + abs(r * 0.25 * round_dome) * dy])
                if len(pts) >= 4: self.canvas.coords(ring["id"], *pts)

    # ==========================================
    # ЧАСТЬ 3: Реалистичная вспышка звезды и основной цикл
    # ==========================================
        def trigger_star_flare(self):
            for item in self.flare_elements:
                self.canvas.delete(item)
            self.flare_elements.clear()

            self.flare_frame += 1
            max_flare_frames = 12  
            
            if self.flare_frame <= max_flare_frames:
                intensity = (max_flare_frames - self.flare_frame) / max_flare_frames
                
                # Фотометрическое ядро (наслоение мягких дисков свечения)
                steps = 5
                for s in range(steps):
                    r_core = (50 * self.scale * intensity) * ((s + 1) / steps)
                    c_val = int(210 + 45 * (s / steps))
                    glow_color = f"#{c_val:02x}{int(c_val*0.95):02x}{int(c_val*0.95):02x}" if s > 2 else "#FFFFFF"
                    core_id = self.canvas.create_oval(self.cx - r_core, self.cy - r_core, self.cx + r_core, self.cy + r_core, fill=glow_color, outline="")
                    self.flare_elements.append(core_id)

                # Формирование дифракционных лучей звезды (плавные вытянутые конусы)
                ray_length = 240 * self.scale * math.pow(intensity, 1.4)
                ray_thickness = 7 * self.scale * intensity
                ray_color = f"#{int(220*intensity):02x}{int(235*intensity):02x}ff"
                
                h_ray = self.canvas.create_polygon(
                    self.cx - ray_length, self.cy,
                    self.cx, self.cy - ray_thickness,
                    self.cx + ray_length, self.cy,
                    self.cx, self.cy + ray_thickness,
                    fill=ray_color, outline=""
                )
                v_ray = self.canvas.create_polygon(
                    self.cx, self.cy - ray_length,
                    self.cx - ray_thickness, self.cy,
                    self.cx, self.cy + ray_length,
                    self.cx + ray_thickness, self.cy,
                    fill=ray_color, outline=""
                )
                self.flare_elements.extend([h_ray, v_ray])
                
                # Поднимаем вспышку на передний план над всеми элементами
                for item in self.flare_elements:
                    self.canvas.tag_raise(item)
                    
                self.root.after(55, self.trigger_star_flare)

        def animate(self):
            self.frame += 1
            dt = 2.2  
            virtual_frame = self.frame * dt
            
            start_frame = 10        
            transform_duration = 18 
            
            progress = 0.0 if self.frame <= start_frame else min(1.0, (self.frame - start_frame) / transform_duration)
            
            for star in self.topo.sky_stars:
                if progress >= 0.3: self.canvas.itemconfigure(star["id"], state="hidden")
                else: self.canvas.itemconfigure(star["id"], fill="#00FF00" if ((math.sin(virtual_frame * star["blink_speed"] + star["blink_phase"]) + 1) / 2) < 0.08 else star["base_color"])
            
            # ТОЧНЫЙ ТАЙМИНГ: Черная дыра активна строго в диапазоне 0.10 < progress < 0.75
            in_black_hole = (0.10 < progress < 0.75)
            
            for b in self.topo.galaxy_branches:
                for i in range(39):
                    x1, y1 = self.topo.sample_spiral_path(i / 40, b, progress, virtual_frame, self.logo_r, self.bar_offset)
                    x2, y2 = self.topo.sample_spiral_path((i + 1) / 40, b, progress, virtual_frame, self.logo_r, self.bar_offset)
                    self.canvas.coords(b["segments"][i], x1, y1, x2, y2)
                    orig_w = max(2.5 * self.scale, (6.0 * self.scale if b["is_milk"] else 4.5 * self.scale) * (1.0 - (i / 40) * (0.5 if b["is_milk"] else 0.7)))
                    target_w = (44 * self.scale) if (b["phase"] < math.pi / 2 or (math.pi <= b["phase"] < 3 * math.pi / 2)) else (12 * self.scale)
                    self.canvas.itemconfigure(b["segments"][i], width=orig_w + (target_w - orig_w) * progress)
                    if progress > 0.0: self.canvas.itemconfigure(b["segments"][i], fill="#F0F8FF")
                    
            for star in self.topo.galaxy_stars:
                if in_black_hole and star["t"] < 0.22:
                    self.canvas.coords(star["id"], -10, -10, -10, -10)
                    continue
                sx, sy = self.topo.sample_spiral_path(star["t"], star["branch"], progress, virtual_frame, self.logo_r, self.bar_offset)
                if progress > 0.2: self.canvas.itemconfigure(star["id"], fill="#F0F8FF")
                self.canvas.coords(star["id"], sx, sy, sx + star["size"], sy + star["size"])
            
            cos_a, sin_a = math.cos(virtual_frame * 0.12), math.sin(virtual_frame * 0.12)
            for pt in self.topo.core_particles:
                if progress == 0.0:
                    bx, by = self.cx + (pt["local_x"] * cos_a - pt["local_y"] * sin_a), self.cy + (pt["local_x"] * sin_a + pt["local_y"] * cos_a)
                else:
                    if in_black_hole and pt["t_factor"] < 0.22:
                        self.canvas.coords(pt["id"], -10, -10, -10, -10)
                        continue
                    bx, by = self.topo.sample_spiral_path(pt["t_factor"], pt["branch"], progress, virtual_frame, self.logo_r, self.bar_offset)
                    bx = bx + (pt["local_x"] * cos_a - pt["local_y"] * sin_a) * (1.0 - progress)
                    by = by + (pt["local_x"] * sin_a + pt["local_y"] * cos_a) * (1.0 - progress)
                    self.canvas.itemconfigure(pt["id"], fill="#F0F8FF")
                self.canvas.coords(pt["id"], bx, by, bx + 2, by + 2)
            
            if in_black_hole:
                wave = math.pow(math.sin(((progress - 0.10) / 0.65) * math.pi), 0.5) * (1.0 + 0.15 * progress)
                dy = 1.0 + 0.15 * math.sin(virtual_frame * 0.3)
                
                self.draw_lensed_rings(self.topo.back_rings, wave, dy, "back")
                self.draw_lensed_rings(self.topo.bottom_rings, wave, dy, "bottom")
                self.canvas.itemconfigure(self.shadow_id, state="normal")
                sh_size = 66 * self.scale * (wave / (1.0 + 0.15 * progress))
                self.canvas.coords(self.shadow_id, self.cx - sh_size, self.cy - sh_size, self.cx + sh_size, self.cy + sh_size)
                self.canvas.tag_raise(self.shadow_id)
                self.draw_lensed_rings(self.topo.front_rings, wave, dy, "front")
                for ring in self.topo.front_rings:
                    self.canvas.tag_raise(ring["id"])
            else:
                # МГНОВЕННЫЙ СХЛОП: Как только progress преодолевает 0.75, черная дыра удаляется,
                # и звезда вспыхивает РОВНО в этот же кадр, закрывая собой ядро.
                self.canvas.itemconfigure(self.shadow_id, state="hidden")
                for r in self.topo.back_rings + self.topo.front_rings + self.topo.bottom_rings: 
                    self.canvas.itemconfigure(r["id"], state="hidden")
                
                if progress >= 0.75 and not self.flare_triggered:
                    self.flare_triggered = True
                    self.canvas.delete(self.shadow_id)
                    self.trigger_star_flare()
                
            if progress == 1.0:
                for el in [self.logo_circle, self.logo_bar1, self.logo_bar2]: self.canvas.itemconfigure(el, state="normal")
                self.canvas.coords(self.logo_circle, self.cx - self.logo_r, self.cy - self.logo_r, self.cx + self.logo_r, self.cy + self.logo_r)
                self.canvas.coords(self.logo_bar1, self.cx - 100 * self.scale, self.cy - self.bar_offset, self.cx + 100 * self.scale, self.cy - self.bar_offset)
                self.canvas.coords(self.logo_bar2, self.cx - 100 * self.scale, self.cy + self.bar_offset, self.cx + 100 * self.scale, self.cy + self.bar_offset)
                for b in self.topo.galaxy_branches:
                    for s in b["segments"]: self.canvas.itemconfigure(s, state="hidden")
                for s in self.topo.galaxy_stars: self.canvas.itemconfigure(s["id"], state="hidden")
                for pt in self.topo.core_particles: self.canvas.itemconfigure(pt["id"], state="hidden")
                
                # Ожидание перед закрытием перенесено в окончание анимации вспышки
                self.root.after(600, lambda: self.blink_logo(step=0))
                return

            if progress < 1.0: self.root.after(180, self.animate)

        def blink_logo(self, step):
            logo_elements = [self.logo_circle, self.logo_bar1, self.logo_bar2]
            if step == 0:
                self.root.after(0, lambda: self.blink_logo(1))
            elif step == 1:
                for el in logo_elements: self.canvas.itemconfigure(el, state="hidden")
                self.root.after(50, lambda: self.blink_logo(2))
            elif step == 2:
                for el in logo_elements: self.canvas.itemconfigure(el, state="normal")
                self.root.after(350, self.root.destroy)

    root = Tk()
    app = ElegantGalacticTransform(root)
    root.mainloop()


draw_animation = time.time() - recents['closing time'][-2] >= 60 * DAY
if draw_animation:
    opening_animation()


ROUND_ANSWER_TO_MANUALLY = settings['round']

# Временная штука для программы работы без ошибки
max_character_amount = (174, 174, 152, 120, 99, 71)[settings['scale']]

HEIGHT = screen_width // (201, 81, 71, 61, 51, 41)[settings['scale']]

WIDTH = screen_width - 2 * MIN_X_COORD
MAX_COORD = screen_height - TASKBAR_HEIGHT - HEIGHT

if recents['low'] != MAX_COORD:
    if abs(settings['y'] - recents['mid']) <= HEIGHT * 4:
        setting_y(MAX_COORD // 2)
    elif settings['y'] - recents['mid'] > HEIGHT * 4:
        setting_y(MAX_COORD)
    else:
        setting_y(0)
    setting_y(min(MAX_COORD, settings['y']))

recents['low'], recents['mid'], recents['top'] = MAX_COORD, MAX_COORD // 2, 0
place_coords = (recents['low'], recents['mid'], recents['top'])


def is_num(symbols, num_symbs=list('0123456789.-Ee+')):
    return all((i in num_symbs for i in symbols))


# def change_scopes_to_modules():
#     global example_value
#     example_value = delete_in_example(example_value, 1)
#     example_value = delete_in_example(example_value, -1)
#     example_value = insert_in_example(example_value, '|')
#     example_value = insert_in_example(example_value, '|', right=True)
    
    
# def find_the_most_useful_symbol_to_paste(example, last_is_digit, first=True):
#     often_meeting_parts = []
#     for i in range(len(example) - 2):
#         if (example[i] in '0123456789πφe.' and last_is_digit or example[i] not in '0123456789πφe.' and (not last_is_digit)):
#             continue
#         for j in range(i + 2, len(example) + 1):
#             if example.count(example[i:j]) < 2 or example[j - 1] in '0123456789πφe.' or not re.search(r'[0-9πφe]', example[i:j]):
#                 continue
#             often_meeting_parts.append(example[i:j])
#     for i in range(len(often_meeting_parts)):
#         for j in range(len(often_meeting_parts)):
#             if often_meeting_parts[i] in often_meeting_parts[j] and i != j and example.replace(often_meeting_parts[j], '').count(often_meeting_parts[i]) < 2:
#                 often_meeting_parts[i] = ''
#     often_meeting_parts = sorted(often_meeting_parts, key=lambda x: len(x), reverse=True)
#     if often_meeting_parts:
#         return often_meeting_parts[0 if len(often_meeting_parts) < 2 or first else 1]
#     else:
#         number_expression = r'-?(?:[0-9]+(?:\.[0-9]+)?|[πφe])'
#         example_numbers = list(re.finditer(fr'{number_expression}|\({number_expression}\)|\|{number_expression}\|', example))
#         if len(example_numbers) > 1:
#             the_often_meeting_part = example[example_numbers[0].end():example_numbers[-1].start()]
#             for right_index in range(len(the_often_meeting_part)):
#                 part_of_the_often_meeting_part = the_often_meeting_part[:right_index]
#                 if part_of_the_often_meeting_part.count('(') < part_of_the_often_meeting_part.count(')'):
#                     the_often_meeting_part = '#' * right_index + the_often_meeting_part[right_index:]
#             the_often_meeting_part = the_often_meeting_part.replace('#', '')
#             if the_often_meeting_part[:1] not in '0123456789πφe.' and not last_is_digit:
#                 the_often_meeting_part = the_often_meeting_part[list(re.finditer(r'[0-9πφe.]', the_often_meeting_part))[0].start():]
#             if re.search(r'[0-9πφe]', the_often_meeting_part):
#                 return the_often_meeting_part
#             else:
#                 return ''
#         else:
#             return ''


def zeros(x):
    return Decimal('.' + x * '0') if x > 0 else Decimal(f'1e{abs(x)}')

rounds = [zeros(_) for _ in (400, 380, 360, 305, 100)]
max_denominator = 10000

def rond(num, rounding_accuracy):
    return num.quantize(rounds[rounding_accuracy], ROUND_HALF_UP)


def classmethod_with_cache(func):
    func = lru_cache()(func)
    
    @wraps(func)    
    def wrapper(cls, *args, **kwargs):
        return func(cls, *args, **kwargs)
    
    return classmethod(wrapper)


# --- --- --- was info.py --- --- ---
invisible_win_title = 'невидимое окно'
temp_scopes, temp_scopes_with_smth = r'(?:\(-?\)|U-?u)', r'(?:\(.*?\)|U.*?u)'
oper_for_empty_scopes = r'(?:[+\-/•:^√]|mod|div)'
func_for_empty_scopes = r'(?:(?:d(?!iv))?(?:arc)?(?:sin|cos|c?tg)|d?arc|lg|ln|d)'
empty_funcs_scopes_construction = fr'(?:{func_for_empty_scopes}{temp_scopes}|log{temp_scopes}by{temp_scopes_with_smth}|log{temp_scopes_with_smth}by{temp_scopes}|{temp_scopes})'
calc_geometry_state_change_expression = r'Максимум \d+ символ(?:|а|ов)|Калькулятор теперь (?:вверху|в центре|внизу)'
pattern_checking_on_empty_scopes = fr'(?:{oper_for_empty_scopes}*{empty_funcs_scopes_construction}(?={oper_for_empty_scopes})|{empty_funcs_scopes_construction})'


def count_matches(list1, list2):
    intersection = Counter(list1) & Counter(list2)
    return sum(intersection.values())


def reunite(words):
    return [f'{(r'\s*').join(['\\' + symb if symb in '()|' else symb for symb in word])}' for word in words]

darc_generator = tuple([f'{i}{j}' for i in ('darc', 'arc', 'd') for j in ('sin', 'cos', 'ctg', 'tg', '')])
ddarc_gen = tuple([f'{i}{j}' for i in ('darc', 'arc', 'd', '') for j in ('sin', 'cos', 'ctg', 'tg')])

united_symbols = ('div', 'mod') + darc_generator + ('log', 'sin', 'cos', 'ctg') + ('ln', 'lg', 'tg', 'by')
composite_trig_funcs = tuple(i for i in darc_generator if i not in ('d', 'arc', 'darc')) + ()
united_symbols_with_scopes = (tuple(f'{i}{j}' for j in ('|', '(') for i in darc_generator)
     + ('log(', 'sin(', 'cos(', 'ctg(', ')by(') + ('log|', 'sin|', 'cos|', 'ctg|', '|by|', '|by(', ')by|') + ('by(', ')by', '|by', 'by|') + ('ln|', 'lg|', 'tg|') + ('ln(', 'lg(', 'tg('))
united_symbols_without_scopes = darc_generator + ('sin', 'cos', 'ctg', 'tg', 'ln', 'lg')  # порядок важен, сначала котангенс а лишь потом тангенс, чтобы удалялся ctg а не c tg
full_funcs_with_Uu = tuple((f'{i}{j}' for i in ('sin', 'cos', 'tg', 'ctg', 'lg', 'ln') for j in ('()', 'Uu'))) + tuple((f'log{i}by{j}' for i in ('()', 'Uu') for j in ('()', 'Uu')))

special_keys = ('Up', 'Down', 'Left', 'Right', 'Control_L', 'Return', 'grave', 'Tab', 'changed text', 'Win_L'
                'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Escape', 'Caps_Lock', 'apostrophe', 'quotedbl', 'braceleft', 'braceright')
ghost_keys = ('Up', 'Down', 'Left', 'Right', 'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Caps_Lock')
keys_after_dot = ('minus', 'equal', 'slash', 'semicolon', 'backslash', 'bracketleft', 'bracketright')
last_keys = ['' for _ in range(20)]

ending_symbols = list('+-•:^,%@k.') + list(united_symbols)
correct_answer_num_symbols = '0123456789Ee-+.•^() '
letters_and_inwords, letters_and_not_example_like_inwords, syntax = r'[а-яА-ЯЁё"\'«»“”()-]', r'[а-яА-ЯЁё"\'«»“”]', r'(?:[.,!?;:/—–]|\s[—–]|\s-\s(?=\w|\d+-\w))'
last_time_main_win_geometry_change = 0
last_val_before_geometry_change = 'если это вставится, значение использовали до его определения !!!техническая ошибка разработчиков!!!'
last_time_round_change = 0
num_construct = r'((?:\d+[.,]?\d*|[.,]\d+)(?:[eE]-?\d*[.,]?\d*)?|[φπeE])'
num_construct_with_spaces = r'((?:(?:\d\s*)+(?:[.,]\s*)?(?:\d\s*)*|(?:[.,]\s*)(?:\d\s*)+)(?:[eE]\s*(?:-\s*)?(?:\d\s*)*(?:[.,]\s*)?(?:\d\s*)*)?|[φπeE])'
num_construct_with_spaces_and_factorials = r'(?:(?:(?:(?:\d\s*)+(?:[.,]\s*)?(?:\d\s*)*|(?:[.,]\s*)(?:\d\s*)+)(?:[eE]\s*(?:-\s*)?(?:\d\s*)*(?:[.,]\s*)?(?:\d\s*)*)?|[φπeE])(\s*!)*)'
word_construct = '[а-яА-ЯЁё]+'
tokenator = r'(d?(?:arc)?(?:sin|cos|c?tg)|d?arc|ln|lg|√|log|by|(?<![\d.])e(?![\d.])|d(?!iv)|\+|=|!|div|mod|\||•|/|:|\^|(?:(?<!\()(?<![\d.]e))\-|\(|\))'
super_tokenator = r'(sin|cos|c?tg|arc|ln|lg|√|log|by|(?<![\d.])e(?![\d.])|d(?!iv)|\+|=|!|div|mod|\||•|/|:|\^|(?:(?<!\()(?<![\d.]e))\-|\(|\)|[\dφπeE.])'
ultra_tokenator = fr'([а-яА-ЯЁё]|\d|{super_tokenator})'

max_history_length, min_history_length = 10000, 100
tick_symbol_time, after_tick_symbol_time = 330, 500
word_ends1 = ('е', 'я', 'й')
word_ends2 = ('', 'а', 'ов')


def relatives(arg1, arg2):
    relative = 0
    for (arg1, arg2) in ((arg1, arg2), (arg2, arg1)):
        if arg1 == arg2:
            relative = max(relative, 1)
        if (arg1, arg2) in (('sin', 'cos'), ('tg', 'ctg'), ('lg', 'ln')):
            relative = max(relative, 0.9)
        if 'arc' + arg1 == arg2 or 'd' + arg1 == arg2 or arg1 == 'arc' and arg2 == 'd' or (arg1, arg2) in (('sin', 'tg'), ('cos', 'ctg'), ('lg', 'log'), ('ln', 'log')):
            relative = max(relative, 0.85)
        if 'darc' + arg1 == arg2:
            relative = max(relative, 0.8)
        if re.search(r'sin|cos|c?tg|d|arc', arg1) and re.search(r'sin|cos|c?tg|d|arc', arg2):
            relative = max(relative, 0.65)
        if re.search(fr'-?{num_construct}', arg1) and re.search(fr'-?{num_construct}', arg2):
            relative = max(relative, count_matches(arg1, arg2) / max(len(arg1), len(arg2)))
        for indx, i in enumerate(('√', '!', 'mod', 'div', '^', '|', '•', ':', '+', '-')):
            if arg1 == i != arg2:
                relative = max(relative, 1 - (0.98, 0.95, 0.9, 0.6, 0.35)[indx // 2])

    relative = max(relative, 0.1)
    return relative


def clear_q_with_content(example, cursor_place):
    return re.sub(r'(?:q.*|q?)$', '', example[:cursor_place]) + example[cursor_place:]


def clear_space_and_bracks_with_content(example):
    return re.sub(r' ?\[.*\]', '', example)


def get_correct_ending(num, word_endings):
    if num % 10 in [0, 5, 6, 7, 8, 9] or num % 100 in [11, 12, 13, 14]:
        return word_endings[2]
    elif num % 10 == 1:
        return word_endings[0]
    else:
        return word_endings[1]

with open(f'{FILES}/help.txt', 'r', encoding='utf-8') as help_file:
    help_text = help_file.read()


class FakeWindow():
    def focus_get(self):
        return
    
    def focus_set(self):
        pass
    
    def destroy(self):
        pass
    
    def winfo_viewable(self):
        return False
    
    def title(self):
        return invisible_win_title
    
    def wm_state(self):
        return 'iconic'

    def focus_displayof(self):
        return


def is_russian_layout() -> bool:
    """
    Проверяет, активна ли русская раскладка клавиатуры в текущем окне.
    Возвращает True для русской раскладки, False для остальных случаев.
    """
    
    # Получаем дескриптор активного окна и его поток
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    
    # Получаем идентификатор раскладки клавиатуры
    keyboard_layout = user32.GetKeyboardLayout(thread_id)
    language_id = keyboard_layout & 0xFFFF  # Извлекаем младшие 16 бит
    
    # Русская раскладка имеет код 0x0419
    return language_id == 0x0419


keyboard_layout_memory = ('en', 'ru')[is_russian_layout()]

# --- --- --- was maths.py --- --- ---

class C:
    e = Decimal('2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274274663919320030599218'
                '1741359662904357290033429526059563073813232862794349076323382988075319525101901157383418793070215408914993488416750924476146'
                '06680822648001684774118537423454424371075390777449920695517027618386062613313845830007520449338265602976067371132007093287091'
                '27443747047230696977209310141692836819025515108657463772111252389784425056953696770785449969967946864454905987931636889230098')
    
    pi = Decimal('3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647'
                 '093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165'
                 '271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360'
                 '011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724')
    
    fi = Decimal('1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374'
                 '847540880753868917521266338622235369317931800607667263544333890865959395829056383226613199282902678806752'
                 '087668925017116962070322210432162695486262963136144381497587012203408058879544547492461856953648644492410')
    
    @classmethod_with_cache
    def factorial(cls, num):
        num = Decimal(num)
        if num < 0 and rond(num, 3) % 1 == 0:
            return f'Факториал целого отрицательного числа смысла не имеет! (±ထ)'
        return Decimal(str(_get_mp().factorial(num)))
        
    @classmethod_with_cache
    def pow(cls, num, power, power_type):
        num, power = Decimal(num), Decimal(power)
        if power_type == '^-':
            power = -power
        if power < 0:
            if type(power_result := cls.pow(num, -power, power_type[0])) is str:
                return power_result
            return rond(1 / power_result, 2)
        if power_type == 'k':
            power = rond(1 / Decimal(power), 0)
        if num >= 0 or rond(power, 1) % 1 == 0:
            return rond(Decimal(str(_get_mp().power(num, power))), 0)
        for odd_num in range(4999, 10000, 2):
            reversed_pow = 1 / Decimal(odd_num)
            rounded_reversed_pow = rond(reversed_pow, 1)
            maybe_num_about_zero = rond(power, 1) % rounded_reversed_pow
            if rond(maybe_num_about_zero, 2) == 0:
                num = rond(Decimal(-(abs(num) ** reversed_pow)), 1)
                power = (power / rounded_reversed_pow).quantize(Decimal('0'), ROUND_HALF_UP)
                res = num ** power
                return f'Результат вычисления {'степени' if power_type != 'k' else 'корня'} крайне неточен, поскольку результат числа слишком небольшой!' if res == 0 and num != 0 else res
        else:
            return 'Чётный, дробный или слишком большой знаменатель у степени числа!' if power_type != 'k' else 'Нет решения среди действительных чисел, либо слишком большой числитель или степень у корня числа!'
        
    @classmethod_with_cache
    def radical(cls, num, power):
        num, power = Decimal(num), Decimal(power)
        if num >= 0:
            return Decimal(str(_get_mp().power(num, 1 / power)))
        elif rond(abs(power), 1) % 2 == 1 and num < 0:
            return rond(-Decimal(str(_get_mp().root(abs(num), power))), 0)
        else:
            return cls.pow(num, power, power_type='k')
    
    @classmethod_with_cache
    def log(cls, num_by_log, base):
        num_by_log, base = Decimal(num_by_log), Decimal(base)
        
        base_rond1, num_by_log_rond1 = rond(base, 1), rond(num_by_log, 1)
        if base_rond1 in (-1, 0, 1):
            return f'Не существует логарифма по основанию {int(rond(base, 1))} (бесконечное, либо пустое множество)!'
        if abs(abs(base_rond1) - 1) < 10 ** -20:
            return 'Поскольку основание логарифма слишком близко к единице ответ сильно неточный!'
        if num_by_log_rond1 == 0:
            return 'Не существует логарифма, если логарифмируемое число – ноль!'
        if abs(num_by_log) > 10 ** 1001 or abs(num_by_log) < 10 ** -305:
            return 'Слишком большое или маленькое логарифмируемое число логарифма!'
        if abs(base) > 10 ** 1001 or abs(base) < 10 ** -305:
            return 'Слишком большое или маленькое основание логарифма!'
        if base_rond1 > 0 and num_by_log_rond1 < 0:
            return 'Логарифм отрицательного числа по положительному основанию невозможен!'
        log_result_if_both_args_positive = Decimal(str(_get_mp().log(abs(num_by_log)) / _get_mp().log(abs(base))))
        log_result_if_both_args_positive_rond4 = rond(log_result_if_both_args_positive, 4)
        if base_rond1 < 0 and num_by_log_rond1 < 0 and abs(log_result_if_both_args_positive_rond4 % 2) != 1:
            return 'Логарифм числа меньше нуля по основанию меньше нуля может вернуть только нечётное число!'
        if base_rond1 < 0 and num_by_log_rond1 > 0 and log_result_if_both_args_positive_rond4 % 2 != 0:
            return 'Логарифм числа больше нуля по основанию меньше нуля может вернуть только чётное число!'
        return log_result_if_both_args_positive if base_rond1 > 0 and num_by_log_rond1 > 0 else log_result_if_both_args_positive_rond4
    
    @classmethod
    def is_rational(cls, angle):
        angle = angle.rstrip('0')
        if '.' not in angle or len(angle.split('.')[-1]) < 10 or bool(re.findall(r'(\d+)\1{7}', angle.split('.')[-1][:100])):
            return True
        angle = Decimal(angle)
        for i in range(max_denominator // 2, max_denominator):
            reversed_angle = 1 / Decimal(i)
            rounded_reversed_angle = rond(reversed_angle, 1)
            maybe_num_about_zero = rond(angle, 1) % rounded_reversed_angle
            if rond(maybe_num_about_zero, 2) == 0:
                return True
        else:
            return False

    
    @classmethod_with_cache
    def rad_to_deg(cls, angle, fake_degree_info):
        is_rat = cls.is_rational(angle)
        angle = Decimal(angle)
        if not (is_rat, not is_rat)[fake_degree_info]:
            angle = cls.deg(angle)
           
        if angle > 360 or angle < 360:
            angle %= 360
        if angle < 0:
            angle += 360
        return angle
    
    @classmethod
    def deg(cls, angle):
        angle = Decimal(angle)
        # предподготовка числа, чтобы оно было высчитано более аккуратно
        if angle > 2 * C.pi or angle < 2 * C.pi:
            angle %= 2 * C.pi
        if angle < 0:
            angle += 2 * C.pi
            
        # аккуратное высчитывание числа
        return rond(angle / C.pi * 180, 0)
    
    @classmethod
    def rad(cls, angle):
        angle = Decimal(angle)
        if angle > 360 or angle < 360:
            angle %= 360
        if angle < 0:
            angle += 360
        angle = rond(angle / 180 * C.pi, 0)
        return angle
    

    @classmethod
    def atrig(cls, func, val):
        make_info_deg = 'd' not in func
        func = func.replace('d', '')
        val = Decimal(val)
        unc = func[3:]
        if unc in ('sin', 'cos') and not -1 <= val <= 1:
            return f'значения {'ко' * (unc == 'cos')}синуса не определены вне промежутка от -1 до 1'
        angle = {'sin': _get_mp().asin, 'cos': _get_mp().acos, 'tg': _get_mp().atan, 'ctg': _get_mp().acot}[unc](val)
        if make_info_deg: angle = cls.deg(str(angle))
        if angle > 180 and unc in ('tg', 'ctg'): angle -= 180
        return angle
    
    
    @classmethod_with_cache
    def trig(cls, func, raw_angle):
        fake_degree_info = 'd' in func
        func = func.replace('d', '')
        # is_rat = cls.is_rational(raw_angle)
        # new_degree_info = (is_rat, not is_rat)[fake_degree_info]
        # angle = cls.rad_to_deg(raw_angle, fake_degree_info)
        angle = Decimal(raw_angle)
        if not fake_degree_info:
            angle = rond(angle / C.pi * 180, 0)
        if func in ('tg', 'cos') and rond(angle, 1) % 180 == 90:
            return f'Тангенс углов {('π/2, 3π/2, 5π/2, ...', '90, 270, 450, ...')[fake_degree_info]} смысла не имеет! (±ထ)' if func != 'cos' else 0  # new_degree_info вместо fake_degree_info было
        if func in ('sin', 'ctg') and rond(angle, 1) % 180 == 0:
            return f'Котангенс углов {('0, π, 2π, ...', '0, 180, 360, ...')[fake_degree_info]} смысла не имеет! (±ထ)' if func != 'sin' else 0  # new_degree_info вместо fake_degree_info было
        angle = rond(angle / 180 * C.pi, 1)
        if func == 'sin':
            return _get_mp().sin(angle)
        if func == 'cos':
            return _get_mp().cos(angle)
        if func == 'tg':
            return _get_mp().sin(angle) / _get_mp().cos(angle)
        if func == 'ctg':
            return _get_mp().cos(angle) / _get_mp().sin(angle)


# --- --- --- ends maths.py --- --- ---


def create_perfect_example(non_perfect_example):
    non_perfect_example = rescope_example(non_perfect_example)
    
    if not non_perfect_example:
        return
    
    non_perfect_example = re.sub(r'(?<![а-яА-ЯЁё"\'«»“”])(?<![а-яА-ЯЁё"\'«»“”]\))\s+(?!\(?[а-яА-ЯЁё"\'«»“”])', '', non_perfect_example)
    non_perfect_example = non_perfect_example.replace('by', ')by').replace('log', 'log(')
    non_perfect_example = f'({non_perfect_example})'.replace('-)', ')')[1:-1]
    non_perfect_example = re.sub(r'(?:[\+\-•/^,\.]|mod|div)(?=\))', r'', f'({non_perfect_example})')

    for i in range(len(non_perfect_example) - 2):
        if non_perfect_example[i + 1] == '|':
            non_perfect_example = non_perfect_example[:i + 1] + 'Uu'[non_perfect_example[i] in '0123456789!)ueπφ' or bool(re.match(r'[+•:^!\)]|mod|div', non_perfect_example[i + 2:]))] + non_perfect_example[i + 2:]
    
    old_non_perf_examp = non_perfect_example
    non_perfect_example = clean_pattern_empty_scopes(non_perfect_example)
    if not non_perfect_example:
        return old_non_perf_examp
    non_perfect_example = f'({non_perfect_example})'
    
    split_non_perfect_example = []
    for no_brack, brack in zip(re.split(r'[()Uu]', non_perfect_example), re.findall(r'[()Uu]', non_perfect_example)):
        split_non_perfect_example.append(no_brack)
        split_non_perfect_example.append(brack)
    split_non_perfect_example = ['R', 'R', 'R'] + [i for i in split_non_perfect_example if i] + ['R', 'R', 'R']
    while '(' in split_non_perfect_example or 'U' in split_non_perfect_example:
        for i in range(1, len(split_non_perfect_example) - 3):
            if split_non_perfect_example[i] + split_non_perfect_example[i + 2] not in ('()', 'Uu'):
                continue
            try:
                while split_non_perfect_example[i - 1] + split_non_perfect_example[i + 3] in ('()', 'Uu'):
                    brack1, brack2 = 'Uu' if 'U' in split_non_perfect_example[i - 1:i + 1] else '()'
                    split_non_perfect_example[i - 1:i + 4] = [brack1] + [split_non_perfect_example[i + 1]] + [brack2]
                    split_non_perfect_example = ['R'] + split_non_perfect_example + ['R']
                split_non_perfect_example[i:i + 3] = [split_non_perfect_example[i] + split_non_perfect_example[i + 1] + split_non_perfect_example[i + 2]]
                split_non_perfect_example = ['R'] + split_non_perfect_example + ['R']
            except IndexError:
                pass
            try:
                while split_non_perfect_example[i + 2] not in '()UuR':
                    split_non_perfect_example[i + 1:i + 3] = [split_non_perfect_example[i + 1] + split_non_perfect_example[i + 2]]
                    split_non_perfect_example = split_non_perfect_example + ['R']
            except IndexError:
                pass
            try:
                while split_non_perfect_example[i] not in '()UuR':
                    split_non_perfect_example[i:i + 2] = [split_non_perfect_example[i] + split_non_perfect_example[i + 1]]
                    split_non_perfect_example = ['R'] + split_non_perfect_example
            except IndexError:
                pass
            break
    
    non_perfect_example = ''.join([i for i in split_non_perfect_example if i != 'R'])
    if re.fullmatch(r'\((?:-(?:[φπeE]|[0-9]+(?:\.[0-9]+)?))\)', non_perfect_example):
        non_perfect_example = re.sub(r'\((-(?:[φπeE]|[0-9]+(?:\.[0-9]+)?))\)', r'\1', non_perfect_example)
    non_perfect_example = re.sub(r'\(([φπeE]|[0-9]+(?:\.[0-9]+)?)\)', r'\1', non_perfect_example)
    
    non_perfect_example = re.sub(r'((?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)|ln|lg|by)(\d+(?:\.\d+)?|\.\d+|e)', r'\1(\2)', non_perfect_example)
    non_perfect_example = re.sub(r'(ln|lg)([φπeE])', r'\1(\2)', non_perfect_example)
    non_perfect_example = re.sub(r'(mod|div)([φπeE])', r'\1(\2)', non_perfect_example)
    non_perfect_example = re.sub(r'([φπeE])(mod|div)', r'(\1)\2', non_perfect_example)
    non_perfect_example = re.sub(r'log([φπeE]|\d+(?:\.\d+)?|\.\d+)by', r'log(\1)by', non_perfect_example)
    non_perfect_example = re.sub(r'((?:sin|cos|c?tg)|ln|lg|log|by)\((\d{1,4}|\d\.\d{1,3}|\d{2}\.\d{1,2}|\d{3}\.\d)\)', r'\1\2', non_perfect_example)
    
    non_perfect_example = non_perfect_example.replace('U', '|').replace('u', '|').strip('R')
    if non_perfect_example[:1] == '(' and non_perfect_example[-1:] == ')':
        non_perfect_example = non_perfect_example[1:-1]
    
    non_perfect_example = re.sub(r'(?<![a-z])\(((?:(?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|ctg|tg)|ln|lg|by)(?:\|.*?\||\(.*?\)))\)', r'\1', non_perfect_example)
    non_perfect_example = re.sub(r'(?<![a-z])\((log(?:\|.*?\||\(.*?\))by(?:\|.*?\||\(.*?\)))\)', r'\1', non_perfect_example)

    non_perfect_example = re.sub(r'(?<=[\d.)])\s*e|e\s*(?=[\d.(])', 'E', non_perfect_example)
    return non_perfect_example


def rescope_example(unscoped_example):
    unscoped_example = clear_q_with_content(unscoped_example, cursor_index)
    brackets = ''.join([i for i in unscoped_example if i in '()Uu'])
    
    scope_counter = 0
    while unscoped_example[:1] == '(' and unscoped_example[-1:] == ')':
        brackets = brackets[1:-1]
        unscoped_example = unscoped_example[1:-1]
        scope_counter += 1
        
    while '()' in brackets or 'Uu' in brackets:
        brackets = brackets.replace('()', '').replace('Uu', '')
    basic_for_start_brackets = ''.join(re.findall(r'[)u]+', brackets))
    basic_for_end_brackets = ''.join(re.findall(r'[U(]+', brackets))
    unscoped_example = basic_for_start_brackets[::-1].replace(')', '(').replace('u', 'U') + unscoped_example + basic_for_end_brackets[::-1].replace('(', ')').replace('U', 'u')
    check_example_scoping = unscoped_example
    
    while '()' in check_example_scoping or 'Uu' in check_example_scoping:
        check_example_scoping = check_example_scoping.replace('()', '').replace('Uu', '')
        
    if not check_example_scoping:
        return
    
    scopes_of_example = ''.join(re.findall(r'[()Uu]', unscoped_example))
    while '()' in scopes_of_example or 'Uu' in scopes_of_example:
        scopes_of_example = scopes_of_example.replace('()', '').replace('Uu', '')
    if scopes_of_example:
        return
    
    return '(' * scope_counter + unscoped_example + ')' * scope_counter
    

def adapt_trig_depending_if_there_is_pi_in_it(unadapted_example_with_Uu):
    modified_unadaped = unadapted_example_with_Uu.replace(f'({C.pi}+0)'.replace('.', ','), 'π')
    modified_unadaped = re.sub(r'd?(?:sin|cos|c?tg)', 'D', modified_unadaped)

    modified_unadaped = re.sub(r'[^()UuπD]', '', modified_unadaped)
    for indx, i in enumerate(modified_unadaped):
        if i != 'D':
            continue
        after_func_modified_unadaped = modified_unadaped[indx + 1:]
        if after_func_modified_unadaped[:1] == 'π':
            modified_unadaped = modified_unadaped[:indx] + 'R' + modified_unadaped[indx + 1:]
            continue
        for jndx in range(1, len(after_func_modified_unadaped) + 1):
            first_letter_after_func = after_func_modified_unadaped[:1]
            after_func_part = after_func_modified_unadaped[:jndx]
            if first_letter_after_func in ('(', 'U') and after_func_part.count(first_letter_after_func) - after_func_part.count((')', 'u')[first_letter_after_func == 'U']) == 0:
                if 'π' in after_func_part:
                    modified_unadaped = modified_unadaped[:indx] + 'R' + modified_unadaped[indx + 1:]
                break

    unadapted_example_with_Uu = re.sub(r'(d?(?:sin|cos|c?tg))', r' \1 ', unadapted_example_with_Uu)
    unadapted_example_with_Uu = unadapted_example_with_Uu.split()
    modified_unadaped = re.sub(r'[^RD]', '', modified_unadaped)
    cnt_trig = -1
    for indx, i in enumerate(unadapted_example_with_Uu):
        if re.fullmatch(r'd?(?:sin|cos|c?tg)', i):
            cnt_trig += 1
            if (modified_unadaped[cnt_trig] == 'R') == ('d' in i):
                unadapted_example_with_Uu[indx] = 'd' + i.replace('d', '')
            else:
                unadapted_example_with_Uu[indx] = i.replace('d', '')
    return ''.join(unadapted_example_with_Uu).replace('π', f'({C.pi}+0)'.replace('.', ','))


def modify_info(example):
    a = '– '
    if not example:
        return calculator_greeting
    if example == 'v':
        return '– переменная, после которой пишется порядковый номер ряда или колонки, значения которой нужно подставить вместо переменной'
    if example == calculator_greeting.lower():
        return '– приветствие'
    if example in ('ထ', '+ထ', '-ထ'):
        a += {'ထ': 'Бесконечность', '+ထ': 'положительная Бесконечность', '-ထ': 'отрицательная Бесконечность'}[example]
    if example in ('log()by()', 'ln()', 'lg()'):
        a += {'log()by()': 'log(число)by(основание)', 'ln()': 'логарифм по основанию e=2,718…', 'lg()': 'логарифм по основанию 10'}[example]
    if example in ('!', '||'):
        a += {'!': 'факториал (n!=1·2·…·n)', '||': 'модуль (делает значения неотрицательными)', '()': 'скобки'}[example]
    if example in ('√', '3√', '4√'):
        a += {'√': 'квадратный корень', '3√': 'кубический корень', '4√': 'биквадратный корень', }[example]
    if example[:-2] in ('√', '3√', '4√') and example[-2:] == '()':
        a += {'√': 'квадратный корень', '3√': 'кубический корень', '4√': 'биквадратный корень', }[example[:-2]]
    if example in ('mod', 'div'):
        a += {'mod': 'остаток от деления', 'div': 'целочисленное деление'}[example]
    if example in ('d()', 'arc()', 'darc()'):
        a += {'d()': 'градусор: преобразует всё в градусы', 'arc()': 'радиатор: преобразует всё в радианы', 'darc()': 'dark side of this calculator? it killed 3 years of my life'}[example]
    if example in (f'{i}{j}' for i in ('', 'd') for j in ('sin()', 'cos()', 'tg()', 'ctg()')):
        a += ({'sin': 'синус', 'cos': 'косинус', 'tg': 'тангенс', 'ctg': 'котангенс'}[example.replace('d', '')[:-2]] +
              f'(в радианах, если угол {'ир' * (not 'd' in example)}рациональный, иначе в градусах)')
    if example in (f'{i}{j}' for i in ('', 'd') for j in ('arcsin()', 'arccos()', 'arctg()', 'arcctg()')):
        atemp = {'sin': 'синус', 'cos': 'косинус', 'tg': 'тангенс', 'ctg': 'котангенс'}[example.replace('d', '')[3:-2]]
        a += ('арк' + atemp + f'(число, которое вернёт {atemp} от искомых {('радиан', 'градусов')['d' not in example]})')
    if example in ('^', '^2', '^3', '^4', '^5'):
        a += {'^': 'степень', '^2': 'квадрат', '^3': 'куб', '^4': 'гиперкуб', '^5': 'метакуб | петакуб'}[example]
    if example in ('+', '-', '•', '/'):
         a = ''
    if example in ('10^100', '10^303', '10^3003', '10^10^100'):
        a += {'10^100': 'гугол', '10^303': 'центиллион', '10^3003': 'миллиллион', '10^10^100': 'гуголплекс'}[example]
    if re.fullmatch(r'1(?: 000){2,8}', example):
        z3 = ' 000'
        a += {f'1{i * z3}': f'10^{3 * i}, {('миллион', 'миллиард', 'триллион', 'квадриллион', 'квинтиллион', 'секстиллион', 'септиллион')[i - 2]}' for i in range(2, 9)}[example]
    return a if a != '– ' else None


def q_solve_example(example):
    return solve_example(clear_q_with_content(example, cursor_index))
    

def solve_example(example=None, get_raw_ans=False):
    global perfect_example, ROUND_ANSWER_TO_MANUALLY, last_time_round_change
    perfect_example = ''

    example = (entry_box.get() if example is None else example).lower()
    modified_info = modify_info(example)
    if modified_info is not None:
        return modified_info
    if re.search(fr'e-?{num_construct}e', example.replace(' ', '')):
        return '"E" слева и справа от числа одновременно (в том числе отрицательного) не допускается!'

    cursor_or_selected_end_index = max(indexes_of_selection.values()) if indexes_of_selection and indexes_of_selection != 'по умолчанию' else cursor_index
    if example.count('q') == 1 and cursor_or_selected_end_index >= example.index('q') + 1:
        last_time_round_change = time.time()
        bind_left_button()
        mn, mx = min_rounding, max_rounding
        info_if_rounding = "не удаляй 'q' 10 секунд, чтобы пример округлился"
        info_if_start_rounding = f' (допиши число знаков: от {mn} до {mx} (перед/после запятой), {info_if_rounding})'
        info_if_continue_rounding = f" ({info_if_rounding})"
        if a := re.fullmatch(r'-?', example[example.index('q') + 1:cursor_or_selected_end_index]):
            ROUND_ANSWER_TO_MANUALLY = settings['round'] = 'по умолчанию'
            return f'{f'{q_solve_example(example)} ' * (not recents['rounding info longer'] > 0)}[округление по умолчанию{info_if_start_rounding * (recents['rounding info longer'] > 0)}]'

        rounding_num = re.fullmatch(r'-?\d+', example[example.index('q') + 1:cursor_or_selected_end_index])
        if not rounding_num:
            return 'Неверная запись округления! Между q и кареткой должно быть целое число'
        rounding_num = int(rounding_num[0])
        if rounding_num > mx or rounding_num < mn:
            return f'{q_solve_example(example)} [Необходимо задать количество знаков после запятой не более {mx}, но и не менее {mn}!]'
        ROUND_ANSWER_TO_MANUALLY = settings['round'] = rounding_num
        manual_round_abs = abs(ROUND_ANSWER_TO_MANUALLY)
        num_of_ending_symbols = (0 < manual_round_abs % 10 < 5 and manual_round_abs // 10 != 1) + (manual_round_abs % 10 == 1 and manual_round_abs != 11)
        return (f'{f'{q_solve_example(example)} ' * (not recents['rounding info longer'] > 0)}[{manual_round_abs} знак{('ов', 'а', '')[num_of_ending_symbols]}' +
                f' {('перед', 'после')[ROUND_ANSWER_TO_MANUALLY > 0]} запятой{info_if_continue_rounding * (recents['rounding info longer'] > 0)}]')
    
    for i in range(2):
        for j in range(-3, 0):
            if example[j:] in ending_symbols:
                example = example[:j]
                break
    
    for j in range(-3, 0):
        if example[j:] in ending_symbols:
            return 'Ошибка в конце примера!'

    if ' ' in example and len(set(example)) == 1:
        return 'Зачем тебе пробелы?'
    elif ')(' in example:
        return 'Сочетание символов ")(" может быть неправильно растолковано. Возможно, ты имеешь ввиду ")•("?'
    elif example == 'h':
        return f'Задай размер памяти истории (от {min_history_length} до {max_history_length})'
    elif example[:1] == 'h' and example[-1:] == '#':
        if not example[1:-1].isdigit():
            return 'Ошибка! Длина истории вычислений должна быть числом!'
        num = int(example[1:-1])
        if min_history_length <= num <= max_history_length:
            settings['history length'] = 4 * num
            return f'С следующего сохранения примера: длина истории вычислений — {num} примеров.'
        return f'Необходимо задать количество примеров в истории не более {max_history_length}, но и не менее {min_history_length}!'
    elif re.fullmatch(r'-?[^#]*#', example.replace(' ', '')):
        unit_of_distance = False
        if example.replace(' ', '') == '-#':
            example = '-0#'
            unit_of_distance = True
        if re.fullmatch(r'-?1-#', example.replace(' ', '')):
            y_coord = (-1, 1)[example.replace(' ', '') == '1-#'] * MAX_COORD
            unit_of_distance = True
        else:
            if not re.fullmatch(r'-?(?:[0-9]+(?:\.[0-9]+)?)#', example):
                example = solve_example(example[:-1]).replace(' ', '') + '#'
            if not re.fullmatch(r'-?(?:[0-9]+(?:\.[0-9]+)?)#', example):
                return 'Координата должна быть числом!'
            y_coord = float(example[:-1])
            if -1 < y_coord < 1:
                y_coord *= MAX_COORD
                unit_of_distance = True
            y_coord = int(str(Decimal(y_coord).quantize(Decimal('.0'), ROUND_HALF_UP))[:-2])
        if abs(y_coord) > MAX_COORD:
            return f'Либо сделай координату в диапазоне от -{MAX_COORD} до {MAX_COORD}, либо нажми на "Ctrl+Shift" и стрелку "Вверх" или "Вниз" на клавиатуре!'
        setting_y(y_coord + (0, MAX_COORD)[example[0] == '-'])
        main_win.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{settings['y']}')
        return 'место калькулятора в ' + ('пикселях', f'"доле от его максимального расстояния от {('верхнего', 'нижнего')[y_coord < 0]} края"')[unit_of_distance]
    if '$' in example:
        return 'Почему символ "$" есть в примере?'
    pi_replaced, e_replaced, fi_replaced = f'({C.pi}+0)', f'({C.e}+0)', f'({C.fi}+0)'

    pre_example = f'({example})'
    
    example = replace_abs_signs(pre_example[1:-1])

    if text_tokens := re.findall(fr'\s*(?:(?:[0-9]*-)?{letters_and_not_example_like_inwords}+[0-9]*{syntax}*|{letters_and_inwords}*{syntax}+)', example):
        for text_token in text_tokens:
            if re.search(r'[а-яА-ЯЁё]', text_token):
                example = example.replace(text_token, '', 1)  # меняем по токену, а не несколько, пусть даже одинаковых, иначе появится баг
    example = example.replace(' ', '')

    example = clean_pattern_empty_scopes(example)

    example = re.sub(r'[Uu]', '|', example)
    example = re.sub(r'(?<!^)(?<![+\-•/:^(])(?<!d)(?<!tg|ln|lg|by)(?<!mod|div|sin|cos|ctg|log|arc)e-(\d*\.?\d*)', r'$(-\1)', example)
    example = re.sub(r'e(\d+\.?\d*|\.\d+|\()', r'$\1', example)
    if re.search(r'[eπφ][eπφ(]|[eπφ)][eπφ]', example):
        return 'Рядом с константой не может быть ни скобки, ни константы!'
    example = example.replace('π', pi_replaced).replace('φ', fi_replaced).replace('e', e_replaced).replace('$', 'e')
    example = re.sub(r'v(?=[^0-9]|$)', 'v1', example)
    example = example.replace('.', ',').replace(' ', '').replace('/', ':')
    example = re.sub(r'(?<!a)r(?!c)', '$', example.replace('√', '$').replace('k', '$'))
    example = example.replace('by', ')by').replace('log', 'log(')
    example = f'({example})'.replace('-)', ')')[1:-1]
    example = re.sub(r'(?:(?<=d)|(?<=mod|div|sin|cos|ctg|log|arc)|(?<=[+\-•/:^(√])|(?<=ln|lg|by|tg)),', r'0,', example)
    example = re.sub(r',(?=mod|div|d(?!i)|arc|sin|cos|c?tg|log|ln|lg|by|[+\-•:^)!])', r',0', example)
    example = re.sub(r'(?:[\+\-•:^,]|mod|div)(?=\))', r'', f'({example})')
    for i in range(len(example) - 2):
        if example[i + 1] == '|':
            example = example[:i + 1] + 'Uu'[example[i] in '0123456789!)ueπφ' or bool(re.match(r'[+•:^!\)]|mod|div', example[i + 2:]))] + example[i + 2:]
    those_symbols_cannot_be_near = re.findall(r'(?:(?:[+\-•:^,]|mod|div)(?:[+•:^,]|mod|div)|,-)', example)
    if those_symbols_cannot_be_near:
        those_symbols_cannot_be_near = those_symbols_cannot_be_near[0].replace(',', '.').replace(':', '/')
        if those_symbols_cannot_be_near == '//':
            return f'Сочетание "//" в примере недопустимо! Нужно деление нацело (дважды нажми на клавишу \'/\')?'
        return f'Сочетание "{those_symbols_cannot_be_near}" в примере недопустимо!'
    pre_example_brackets = ''.join([i for i in example if i in '()Uu'])
    example_brackets = ''.join([i for i in example.replace('log', '<').replace('by', '>') if i in '()Uu<>'])
    e_replaced, pi_replaced, fi_replaced = [i.replace('(', '\\(').replace(')', '\\)').replace('.', ',').replace('+', '\\+') for i in (e_replaced, pi_replaced, fi_replaced)]
    consts_expression = fr'(?:{e_replaced}|{pi_replaced}|{fi_replaced})'
    if re.search(fr'{consts_expression}U|u{consts_expression}', example):
        return 'Рядом с константой не может быть модуля!'
    # while example_brackets[:1] == '(' and example_brackets[-1:] == ')':  # сомнительный код
    #     example_brackets = example_brackets[1:-1]
    while any([i in example_brackets for i in ('()', 'Uu', '<>')]):
        example_brackets = example_brackets.replace('()', '').replace('Uu', '').replace('<>', '')
    if re.fullmatch(r'(?:U|u|\(|\))+', example):
        return '0'

    if re.search(r'\(\)', example):
        return 'В примере есть скобки без чисел внутри'
    if re.search(r'Uu', example):
        return 'В примере есть модули без чисел внутри'
    
    if not re.fullmatch(r'[\)u]*[U\(]*', example_brackets):
        return 'Что-то не так со скобками, модулем или логарифмом!'
    
    example = rescope_example(example)
    if not example:
        return 'Что-то не так со скобками, модулем или логарифмом!'
    while '$' in example or 'e' in example:
        for i in range(len(example) - 1):
            if example[i + 1] in ('$', 'e'):
                example = f'{example[:i + 1]}{(('2', '1')[example[i + 1] == 'e'], '')[example[i] in '0123456789,)u!']}{('k', '&')[example[i + 1] == 'e']}{example[i + 2:]}'
    example = example.replace('&', 'e')
    if example and example[1] in '+•' and example[2:3] != '-':
        example = example[:1] + example[2:]
    example = example.replace('+-', '-').replace('--', '+').replace('•-', '•(0-1)•').replace(':-', ':(0-1):')
    saved_example = example
    example = example.replace('arc', '1+1-').replace('mod', 'MOD').replace('div', 'DIV').replace('d', '1+1-').replace('DIV', 'div').replace('MOD', 'mod')
    example = example.replace('sin', '1+1-').replace('cos', '1+1-').replace('ctg', '1+1-').replace('tg', '1+1-')
    example = example.replace('lg', '1+1-').replace('ln', '1+1-').replace('by', '+')
    example = example.replace('k', '+1-').replace('log', '1+1-').replace('2.718281828459045', '1+1')
    example = example.replace('^-', '+').replace('+-', '-').replace('--', '+')
    if err_msg := re.search(r'(sin|cos|c?tg|k|(?<!mo)d(?!iv)|arc|by|log)(?:[+•:^,)!u]|mod|div)', saved_example):
        return f'В примере после функции {(err_msg[1], 'корня')[err_msg[1][:1] == 'k']} стоит не тот символ, либо отсутствует что-либо!'
    for i in (list('+•:^,)-0!u') + ['mod', 'div']):
        for j in ('lg', 'ln', 'log', 'by'):
            if j + '-' in saved_example:
                return f'Число, находящееся после функции {j}, со знаком минус берётся в скобки!'
            if ((j + i) in saved_example) and ((j + '0,') not in saved_example):
                return 'В примере после логарифмической функций стоит не тот символ!'
    if err_msg := re.search(r'[0-9,\.](sin|cos|c?tg|lg|ln|log|arc|d(?!i))', saved_example):
        return f"В примере перед функцией {err_msg[1]} стоит не тот символ! (возможно перед этой функцией нужно поставить '•')"
    example = example.replace('mod', '%').replace('div', '@')
    if 'ထ' in example:
        return 'К сожалению, строка не поддерживает бесконечности'
    if '#' in example:  # Отладочная информация, нельзя допустить # от других символов, оставив его для E и других замен
        return ''
    example = example.replace('e', '#')
    bad_symbols = re.findall(r'[^0-9v+\-•:^,@%!()Uu#]', example)
    if bad_symbols:
        return f'Почему символ "{bad_symbols[0] if bad_symbols[0] not in ('@', '%') else ('mod', 'div')[bad_symbols[0] == '@']}" есть в примере?'
    example = example.replace('#', 'e')
    if example and example[1] in '+•:^,@%!':
        if example[1] == ',':
            example = f'(0{example[1:]}'
        else:
            return 'Ошибка в начале примера!'
    example = example.replace('%', 'mod').replace('@', 'div')
    if bad_var := re.search(r'[0-9,]v|v[,0]', example):
        return f'Сочетание "{bad_var}" в примере недопустимо!'
    if re.search(r'(?<!di)v', example):
        example_without_div = example.replace('div', 'dithoutvees')
        vars = set(map(int, re.findall(r'(?<=v)\d+', example_without_div)))
        example = example_without_div.replace('dithoutvees', 'div')
        mxvr = max(vars)
        return f'– вставь таблицу из {mxvr} ряд{('ов', 'а')[mxvr == 1]} или колон{('ок', 'ки')[mxvr == 1]}. Далее вставь в Ворд скопированную за тебя таблицу ответов'
    
    if re.search(r'[(U](?:[+•:^),u]|mod|div)|(?:[+•:^(,U-]|mod|div)[u)!]|[0-9,][(U]|[u)!][0-9,]', example):
        return 'Около скобки, модуля, факториала, символа "E" или числа e, π, φ — ошибка!'
    
    if re.search(r',\d+,', example):
        return 'Почему в одном числе две запятые или точки?'
    elif len(example) >= 3:
        for i in range(len(example) - 2):
            if (example[i] in '(+-•:^' or example[i - 2:i + 1] in ('mod', 'div')) and (example[i + 1] == '0') and example[i + 2].isdigit():
                return f'Почему в примере введено "{example[i + 1:i + 3]}"?'
    example = saved_example
    
    if err_msg := re.search(r'(k|sin|cos|c?tg|by|d(?!i)|arc)-', example):
        return f'Нельзя число или выражение со знаком минус брать без скобок! Минус после функции {(err_msg[1], 'корня')[err_msg[1][:1] == 'k']}'
    
    for i in range(len(example) - 2):
        if example[i + 1] == '|':
            example = example[:i + 1] + 'Uu'[example[i] in '0123456789!)ueπφ' or bool(re.match(r'[+•:^!\)]|mod|div', example[i + 2:]))] + example[i + 2:]

    example = rescope_example(example)
    if not example:
        return 'Что-то не так со скобками, модулем или логарифмом!'
    
    while '()' in example_brackets or 'Uu' in example_brackets:
        example_brackets = example_brackets.replace('()', '').replace('Uu', '')
    example = adapt_trig_depending_if_there_is_pi_in_it(example)
    example = f'({example})'.replace('^-', '&').replace(',', '.').replace('(-', '(0-').replace('U-', 'U0-')
    example = re.sub(r'(\+|!|div|mod|U|u|•|:|\^|-|\(|\)|(?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)|ln|lg|k|log|by|e|d|arc)', r' \1 ', example)
    example_for_calculations = [i for i in example.replace('&', ' ^- ').split() if i]

    perfect_example = create_perfect_example(pre_example)
    
    if not perfect_example:
        return 'Что-то не так со скобками, модулем или логарифмом!'
    
    try:
        i_stop, i_start = 0, -1
        for i in range(1, len(example_for_calculations)):
            if example_for_calculations[i - 1] in (')', 'u') and example_for_calculations[i] in ('!', 'k'):
                example_for_calculations[i] = f'LowPrior"{example_for_calculations[i]}"'
        while '(' in example_for_calculations or 'U' in example_for_calculations:
            for i in range(len(example_for_calculations)):
                if example_for_calculations[i] in ('(', 'U'):
                    i_start = i
                if example_for_calculations[i_start] + example_for_calculations[i] in ('()', 'Uu'):
                    i_stop = i
                    break
            inner_example = example_for_calculations[i_start + 1:i_stop]
            while any((element in inner_example for element in ('sin cos tg ctg ln lg e k ! log LowPrior"!" LowPrior"k"'.split() + list(darc_generator)))):
                for i in range(len(inner_example) - 3, -1, -1):
                    if not (inner_example[i + 1] == 'e' and is_num(inner_example[i]) and is_num(inner_example[i + 2])):
                        continue
                    inner_example[i:i + 3] = ['R', 'R', Decimal(f'{inner_example[i]}') * C.pow(num='10', power=inner_example[i + 2], power_type='^')]
                    if type(inner_example[i + 2]) is str:
                        return inner_example[i + 2]
                    inner_example[i + 2] = str(inner_example[i + 2])
                inner_example = [i for i in inner_example if i != 'R']
                for i in range(len(inner_example) - 1):
                    if not (inner_example[i + 1] == '!' and is_num(inner_example[i])):
                        continue
                    inner_example[i:i + 2] = ['R', C.factorial(num=inner_example[i])]
                    if type(inner_example[i + 1]) is str:
                        return inner_example[i + 1]
                    inner_example[i + 1] = str(inner_example[i + 1])
                inner_example = [i for i in inner_example if i != 'R']
                for i in range(len(inner_example) - 3, -1, -1):
                    if not (inner_example[i + 1] == 'k' and is_num(inner_example[i + 2])):
                        continue
                    inner_example[i:i + 3] = [C.radical(num=inner_example[i + 2], power=inner_example[i]), 'R', 'R']
                    if type(inner_example[i]) is str:
                        return inner_example[i]
                    inner_example[i] = str(inner_example[i])
                inner_example = [i for i in inner_example if i != 'R']
                for i in range(len(inner_example) - 4, -1, -1):
                    if inner_example[i] == 'log' and inner_example[i + 2] == 'by' and is_num(inner_example[i + 1]) and is_num(inner_example[i + 3]):
                        inner_example[i:i + 4] = [C.log(inner_example[i + 1], inner_example[i + 3]), 'R', 'R', 'R']
                        if type(inner_example[i]) is str:
                            return inner_example[i]
                        inner_example[i] = str(inner_example[i])
                inner_example = [i for i in inner_example if i != 'R']
                for i in range(len(inner_example) - 1):
                    if inner_example[i] in ('d', 'arc', 'ln', 'lg') + ddarc_gen and is_num(inner_example[i + 1]):
                        if inner_example[i] in ('dsin', 'dcos', 'dtg', 'dctg', 'sin', 'cos', 'tg', 'ctg'):
                            inner_example[i] = C.trig(inner_example[i], inner_example[i + 1])
                        elif inner_example[i] in ('arcsin', 'arccos', 'arctg', 'arcctg', 'darcsin', 'darccos', 'darctg', 'darcctg'):
                            inner_example[i] = C.atrig(inner_example[i], inner_example[i + 1])
                        elif inner_example[i] in ('d', 'arc'):
                            inner_example[i] = C.deg(inner_example[i + 1]) if inner_example[i] == 'd' else C.rad(inner_example[i + 1])
                        elif inner_example[i] in ('ln', 'lg'):
                            inner_example[i] = C.log(inner_example[i + 1], (10, C.e)[inner_example[i] == 'ln'])
                        if type(inner_example[i]) is str:
                            return inner_example[i]
                        inner_example[i] = str(inner_example[i])
                        inner_example[i + 1] = 'R'
                inner_example = [i for i in inner_example if i != 'R']
                for i in range(len(inner_example) - 2):
                    if not (inner_example[i + 1] == 'LowPrior"k"' and is_num(inner_example[i + 2])):
                        continue
                    inner_example[i:i + 3] = ['R', 'R', C.radical(num=inner_example[i + 2], power=inner_example[i])]
                    if type(inner_example[i + 2]) is str:
                        return inner_example[i + 2]
                    inner_example[i + 2] = str(inner_example[i + 2])
                inner_example = [i for i in inner_example if i != 'R']
                for i in range(len(inner_example) - 1):
                    if not (inner_example[i + 1] == 'LowPrior"!"' and is_num(inner_example[i])):
                        continue
                    inner_example[i:i + 2] = ['R', C.factorial(num=inner_example[i])]
                    if type(inner_example[i + 1]) is str:
                        return inner_example[i + 1]
                    inner_example[i + 1] = str(inner_example[i + 1])
                inner_example = [i for i in inner_example if i != 'R']

            while '^' in inner_example or '^-' in inner_example:
                for i in range(len(inner_example) - 3, -1, -1):
                    if not (is_num(inner_example[i]) and is_num(inner_example[i + 2]) and inner_example[i + 1] in ('^-', '^')):
                        continue
                    inner_example[i:i + 3] = [C.pow(num=inner_example[i], power=inner_example[i + 2], power_type=inner_example[i + 1]), 'R', 'R']
                    if type(inner_example[i]) is str:
                        return inner_example[i]
                    inner_example[i] = str(inner_example[i])
                inner_example = [i for i in inner_example if i != 'R']
            while '•' in inner_example or ':' in inner_example or 'mod' in inner_example or 'div' in inner_example:
                for i in range(len(inner_example) - 2):
                    if is_num(inner_example[i]) and is_num(inner_example[i + 2]) and inner_example[i + 1] in ('•', ':', 'mod', 'div'):
                        num1, num2 = Decimal(inner_example[i]), Decimal(inner_example[i + 2])
                        if inner_example[i + 1] in ('•', ':'):
                            if num1 == num2 == 0 and inner_example[i + 1] == ':':
                                return 'Неопределённость 0/0'
                            inner_example[i:i + 3] = ['R', 'R', str(rond((num1 * num2 if inner_example[i + 1] != ':' else num1 / num2), 0))]
                        if inner_example[i + 1] in ('mod', 'div'):
                            if rond(num2, 1) == 0:
                                return 'Остаток от деления, либо целочисленное деление на ноль невозможно!'
                            k_div = 1
                            if rond(num2, 1) <= 0:
                                num2 = abs(num2)
                                k_div = -1
                            num1, num2 = rond(num1, 2), rond(num2, 2)
                            div, mod = rond(num1 // num2, 3), rond(num1 % num2, 3)
                            res = (mod, div * k_div)[inner_example[i + 1] == 'div']
                            if mod < 0:
                                res = rond((mod + num2, (div - 1) * k_div)[inner_example[i + 1] == 'div'], 3)
                            inner_example[i:i + 3] = ['R', 'R', str(res)]
                inner_example = [i for i in inner_example if i != 'R']
            while '+' in inner_example or '-' in inner_example:
                for i in range(len(inner_example) - 2):
                    if is_num(inner_example[i]) and is_num(inner_example[i + 2]) and inner_example[i + 1] in ('+', '-'):
                        num1, num2 = Decimal(inner_example[i]), Decimal(inner_example[i + 2])
                        inner_example[i:i + 3] = ['R', 'R', str(rond(num1 + (-1, 1)[inner_example[i + 1] == '+'] * num2, 0))]
                inner_example = [i for i in inner_example if i != 'R']
            inner_example = inner_example[0]
            if example_for_calculations[i_start] == 'U':
                inner_example = str(abs(Decimal(inner_example)))
            example_for_calculations[i_start:i_stop + 1] = [inner_example]
        
        if len(example_for_calculations) != 1:
            return 'Где-то ошибка!'
        example_for_calculations = Decimal(example_for_calculations[0])
        if get_raw_ans:
            return example_for_calculations
        if ROUND_ANSWER_TO_MANUALLY != 'по умолчанию':
            example_for_calculations = example_for_calculations.quantize(zeros(ROUND_ANSWER_TO_MANUALLY), ROUND_HALF_UP)
        if abs(example_for_calculations) > Decimal(10) ** -(ROUND_ANSWER_TO - ROUND_ANSWER_TO_IF_POW) or abs(example_for_calculations) < Decimal(10) ** -300:
            example_for_calculations = example_for_calculations.quantize(Decimal('.' + ROUND_ANSWER_TO * '0'), ROUND_HALF_UP)
        else:
            log_num = math.log(abs(example_for_calculations), 10)
            example_for_calculations = example_for_calculations.quantize(Decimal('.' + (int(-log_num) + ROUND_ANSWER_TO_IF_POW + 1 if type(log_num) in (Decimal, int, float) else ROUND_ANSWER_TO) * '0'), ROUND_HALF_UP)
        if example_for_calculations == 0:
            return '0'
        raw_res = str(example_for_calculations.quantize(Decimal('.0'), ROUND_HALF_UP))[:-2] if example_for_calculations % 1 == 0 else str(example_for_calculations)
        if (Decimal(raw_res) > Decimal(10) ** abs(min_rounding - 1) or 0 < Decimal(raw_res) < Decimal(10) ** -6) or (Decimal(raw_res) < -Decimal(10) ** abs(min_rounding - 1) or 0 > Decimal(raw_res) > -Decimal(10) ** -6):
            fly_exp = 0
            while abs(Decimal(raw_res)) >= Decimal(10) ** 300:
                raw_res = str(Decimal(raw_res) / Decimal(10) ** 100)
                fly_exp += 100
            raw_res_exp1 = Decimal(math.log(abs(Decimal(raw_res)), 10)).quantize(Decimal('.' + 5 * '0'), ROUND_HALF_UP)
            raw_res_exp1 = raw_res_exp1.quantize(Decimal('0'), ROUND_FLOOR)
            raw_res_exp2 = Decimal(Decimal(raw_res) / Decimal(Decimal(10) ** raw_res_exp1))
            raw_res_exp2 = raw_res_exp2.quantize(Decimal('.' + '0' * (ROUND_ANSWER_TO + 2 if -(ROUND_ANSWER_TO - ROUND_ANSWER_TO_IF_POW) <= raw_res_exp1 <= 0 else ROUND_ANSWER_TO_IF_POW)), ROUND_HALF_UP)
            raw_res = f'{raw_res_exp2}E{'' if abs(Decimal(raw_res)) < 10 ** (-6) else '+'}{raw_res_exp1 + fly_exp}'
        if ('E' in raw_res or 'e' in raw_res) and '.' in raw_res:
            while '0e' in raw_res or '0E' in raw_res:
                raw_res = raw_res.replace('0E', 'E').replace('0e', 'e')
            while '.e' in raw_res or '.E' in raw_res:
                raw_res = raw_res.replace('.E', 'E').replace('.e', 'e')
        else:
            while (raw_res[-1] == '0' or raw_res[-1] == '.') and '.' in raw_res:
                raw_res = raw_res[:-1]
        if raw_res.count('e') == 1 or raw_res.count('E') == 1:
            if 'e+' in raw_res or 'E+' in raw_res or 'e' in raw_res or 'E' in raw_res:
                raw_res = raw_res.replace('e+', '•10^').replace('E+', '•10^')
            if 'e-' in raw_res or 'E-' in raw_res:
                raw_res = raw_res.replace('e-', '•10^(-').replace('E-', '•10^(-') + ')'
            if '^(-' in raw_res and (raw_res[-3] == '-' and int(raw_res[-3:-1]) in range(7, ROUND_ANSWER_TO - ROUND_ANSWER_TO_IF_POW + 1)):
                shift_or_not_first_pow_index = not raw_res[-3:-2].isdigit()
                if raw_res[0] == '-':
                    raw_res = '-0.' + (int(raw_res[-3 + shift_or_not_first_pow_index:-1]) - 1) * '0' + raw_res[:-9 + shift_or_not_first_pow_index].replace('.', '').replace('-', '')
                else:
                    raw_res = '0.' + (int(raw_res[-3 + shift_or_not_first_pow_index:-1]) - 1) * '0' + raw_res[:-9 + shift_or_not_first_pow_index].replace('.', '')
            if raw_res[:2] == '1•':
                raw_res = raw_res[2:]
            if raw_res[:3] == '-1•':
                raw_res = '-' + raw_res[3:]
        if '10^' not in raw_res:
            if '.' not in raw_res:
                lenta_split0 = ''
                for i in range(len(raw_res) - 1, -1, -1):
                    lenta_split0 = raw_res[i] + lenta_split0
                    if len(lenta_split0.replace(' ', '')) % 3 == 0 and len(lenta_split0) >= 3:
                        lenta_split0 = ' ' + lenta_split0
                if lenta_split0[0] == ' ':
                    lenta_split0 = lenta_split0[1:]
                if lenta_split0[:2] == '- ':
                    lenta_split0 = '-' + lenta_split0[2:]
                raw_res = lenta_split0
            else:
                lenta_split1 = lenta_split2 = ''
                splitted_raw_res = raw_res.split('.')
                for i in range(len(splitted_raw_res[0]) - 1, -1, -1):
                    lenta_split1 = splitted_raw_res[0][i] + lenta_split1
                    if len(lenta_split1.replace(' ', '')) % 3 == 0 and len(lenta_split1) >= 3:
                        lenta_split1 = ' ' + lenta_split1
                if lenta_split1[0] == ' ':
                    lenta_split1 = lenta_split1[1:]
                if lenta_split1[:2] == '- ':
                    lenta_split1 = '-' + lenta_split1[2:]
                for i in range(len(splitted_raw_res[1])):
                    lenta_split2 += splitted_raw_res[1][i]
                    if len(lenta_split2.replace(' ', '')) % 3 == 0 and len(lenta_split2) >= 3:
                        lenta_split2 += ' '
                if lenta_split2[-1] == ' ':
                    lenta_split2 = lenta_split2[:-1]
                raw_res = lenta_split1 + '.' + lenta_split2
        return raw_res
    except ZeroDivisionError:
        return 'На ноль или малое число делить нельзя! (±ထ)'
    except (OverflowError, Overflow, InvalidOperation):
        return 'Слишком длинные числа! Или возможно где-то ошибка!'
    except ValueError:
        return 'Где-то ошибка!'
    
    
def get_writing_form(the_example):
    return '=' if is_num(clear_space_and_bracks_with_content(the_example), correct_answer_num_symbols) and the_example else ' ' if the_example != calculator_greeting and the_example and the_example[:1] != ' ' else ''


def calculate_result():
    global example_value, cursor_index
    result.delete(0, END)
    if len(entry_box.get()) > max_character_amount:
        entry_box.delete(max_character_amount, END)
        cursor_index = entry_box.index('insert')

    example_value = re.sub(r'(?<=[\d.)])\s*e|e\s*(?=[\d.(])', 'E', entry_box.get().lower())
    example_res = solve_example()
    result.insert(END, f'{get_writing_form(example_res)}{example_res}')

    if add_to_recents(example_value):
        recents['recent examples'].append([example_value, result.get().strip('='), perfect_example, cursor_index])
    if len(recents['recent examples']) > 100:
        recents['recent examples'].pop(0)
    config_fg_and_insertbackground()
    
        
def insert_in_example(example, insert_arg, right=False):
    global cursor_index
    new_example = f'{example[:cursor_index]}{insert_arg}{example[cursor_index:]}'
    if not re.match(r'[\d.-]', insert_arg) and re.search(r'\dE-?$', example[:cursor_index]):
        new_example = re.sub(r'(?<=[\d.)])\s*E', '•e', new_example)
    new_example = re.sub(r'(?<![\d.)])\s*E', 'e', new_example)
    new_example = re.sub(r'(?<=[\d.)])\s*e|e\s*(?=[\d.(])', 'E', new_example)
    if not right:
        cursor_index += len(new_example) - len(example)
    return new_example


def delete_in_example(example, index_limit_steps):
    global cursor_index
    new_example = f'{example[:cursor_index + index_limit_steps]}{example[cursor_index:]}' if index_limit_steps < 0 else f'{example[:cursor_index]}{example[cursor_index + index_limit_steps:]}'
    new_example = re.sub(r'(?<![\d.)])\s*E', 'e', new_example)
    new_example = re.sub(r'(?<=[\d.)])\s*e|e\s*(?=[\d.(])', 'E', new_example)
    if index_limit_steps < 0:
        cursor_index += len(new_example) - len(example)
    return new_example


def disable_editing_added_win_text(key):
    if not ((key.state & 0x0004 | key.state & 0x0008) or key.keysym in ghost_keys) and not (key.state & 0x0001 and key.keysym in ('Up',' Down', 'Left', 'Right')):
        supermanage_key_event(key, True)
    # Разрешаем Control-C (копирование) и Control-A (выделение всего)
    if (key.state & 0x0004) and (key.keysym.lower() == 'a'):
        return  # Не блокируем эти события
    elif (key.state == 0x0005) and (keysym := (key.keysym.lower() if len(key.keysym) == 1 else key.keysym)) in ('y', 'z'):
        (ctrl_shift_y, ctrl_shift_z)[keysym == 'z']()
        return "break"
    elif (key.state & 0x0004) and (keysym := (key.keysym.lower() if len(key.keysym) == 1 else key.keysym)) in ('c', 'v', 'x', 's', 'y', 'z', 'BackSpace', 'Delete'):
        if keysym in ('x', 'c'):
            selected_text = text_entry.get(SEL_FIRST, SEL_LAST)
            # было так: pyperclip.copy(selected_text), стало:
            selected_text = selected_text.replace('E', '#').lower().replace('#', 'E')

            if re.search(r'2\d{3}\.(?:0\d|11|12)\.(?:[0-3]\d|31) (?:[01]\d|2[0-3])(?::[0-5]\d){2}', selected_text) and not len(selected_text.strip('\n ').split('\n')) == 1:    
                selected_text = re.sub(r'\n', '&', selected_text)
                selected_text = re.sub(r' ', '#', selected_text)
                selected_text = re.sub(r'\s', '', selected_text)
                selected_text = re.sub(r'&&', ', ', selected_text)
                selected_text = re.sub(r'&(2\d{3}\.(?:0\d|11|12)\.(?:[0-3]\d|31))#((?:[01]\d|2[0-3])(?::[0-5]\d){2})(?:#(\(\d{1,2})#(знак(?:|а|ов))#(перед|после)#(запятой\)))?', '', selected_text).replace(4 * ' ', '')
                selected_text = '\n'.join((i.replace('&', '=', 1) for i in selected_text.split(', ')))
                selected_text = selected_text.replace('&', ' ')
                selected_text = re.sub(r'#', '', selected_text)
                selected_text = re.sub(r'(\d{4}\.\d{2}\.\d{2})(\d{2}:\d{2}:\d{2})', r'\1 \2', selected_text)
            
            pyperclip.copy(selected_text)
        elif keysym == 'v':
            paste_text()
        elif keysym == 'BackSpace':
            ctrl_backspace(key)
        elif keysym == 'Delete':
            ctrl_delete(key)
        elif keysym in ('y', 'z'):
            (ctrl_y, ctrl_z)[keysym == 'z']()
        return "break"
    elif len(key.char) or key.keysym == 'Delete':  # Блокируем ввод символов
        return 'break'
    
    
def disable_left_mouse_button_clicking(key):
    return "break"


def _mouse_pos():
    pt = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def _mouse_move_to(x, y):
    user32.SetCursorPos(int(x), int(y))

def _mouse_click():
    # MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004
    user32.mouse_event(0x0002, 0, 0, 0, 0)
    user32.mouse_event(0x0004, 0, 0, 0, 0)
    
    
def scroll_text(string_shift):
    added_win.focus_set()
    text_entry['state'] = DISABLED
    if abs(string_shift) == 1:
        text_entry.yview_scroll(string_shift, 'pages')
    elif abs(string_shift) == 4:
        text_entry.yview_scroll(string_shift, 'units')
    else:
        text_entry.yview((1.0, END)[string_shift > 0])
    text_entry['state'] = NORMAL


def added_win_switch_to_string(event):
    entry_box.focus_set()
    beauty_letter_tape.wm_attributes('-topmost', 1)
    return 'break'
    
    
def added_win_control_keypress(event):
    set_last_func_is_ctrl_shift_scroll(False)
    set_del_mode(False)
    keysym = event.keysym.lower() if len(event.keysym) == 1 else event.keysym
    if keysym in ('less', 'greater'):
        key_old = event
        key = Event()
        key.keysym = ('Left', 'Right')[key_old.keysym == 'greater']
        key.state = 0x40000
        key.keycode = (37, 39)[key_old.keysym == 'greater']
        key.type = 2        # Число 2 означает KeyPress (нажатие)
        key.x = key_old.x
        key.y = key_old.y
        key.widget = key_old.widget
        key.char = ''
        set_cursor_to_the(key, define_future_of_cursor(('left', 'right')[key_old.keysym == 'greater']))
    elif keysym == 'n':
        change_history_type()
    elif keysym == 'k':
        virtual_keyboard.toggle_keyboard(main_win, help_text=help_text, theme=settings['theme'])
    elif keysym == 'w':
        manage_not_main_window_close()
    elif keysym == 'a':
        text_entry.tag_add(SEL, '1.0', 'end')
    elif keysym == 's':
        save_example_to_history(example_to_save=entry_box.get())
    elif keysym == 'slash':
        create_added_win('?')
    elif keysym == 'h':
        create_added_win('h')
    elif keysym == 'f':
        rank_text()
    else:
        return disable_editing_added_win_text(event)

        
def create_added_win(win_type):
    global added_win, scrollbar_history_calc, text_entry, cursor_index, example_value
    theme_is_light = settings['theme'] == 'light'
    
    if win_type is None:
        added_win = FakeWindow()
        return
    
    is_help = win_type == '?'
    
    try:
        added_win.destroy()
    except NameError:
        pass
    added_win = Toplevel()
    added_win.iconbitmap(f'icons/{('history', 'help')[is_help]}.ico')
    added_win.title(('история', 'инструкция')[is_help])
    
    added_win.geometry(f'{WIDTH}x{MAX_COORD - 2 * TASKBAR_HEIGHT}+{settings['x'] + 8}+0')
    if is_help:
        added_win.resizable(width=True, height=True)
        added_win.maxsize(WIDTH, MAX_COORD - 2 * TASKBAR_HEIGHT)
    
    added_win.focus_set()
    added_win.protocol('WM_DELETE_WINDOW', lambda: manage_not_main_window_close())
    added_win.attributes('-alpha', ('0.8', '0.85')[is_help])
    
    text_entry = Text(added_win, bg=('#' + '10' * 3, '#' + 'e9' * 3)[settings['theme'] == 'light'],
                      fg=entry_box.cget('fg'), font=('Arial', int(HEIGHT // (2.3, 2)[is_help]), 'bold'),
                      bd=0, exportselection=0, padx=0, pady=0)
    
    text_entry.tag_config("highlight", background=('#' + '11' * 3, '#' + 'e8' * 3)[theme_is_light])
    text_entry.place(x=14, y=0, width=WIDTH + 1, height=MAX_COORD - 2 * TASKBAR_HEIGHT)
    
    scrollbar_style = ttk.Style()
    scrollbar_style.theme_use('classic')
    # i = not theme_is_light

    scrollbar_history_calc = ttk.Scrollbar(added_win, orient='vertical', command=text_entry.yview)
    scrollbar_history_calc.configure(style='App.Vertical.TScrollbar')
    scrollbar_history_calc.pack(side=LEFT, fill=Y)
    scrollbar_history_calc.bind('<B1-Motion>', move_added_win)
    scrollbar_history_calc.bind('<ButtonPress-1>', on_pushing_left_button)

    text_entry['yscrollcommand'] = scrollbar_history_calc.set
    
    text_entry.tag_configure('sel', background=('#' + '38' * 3, '#' + 'b7' * 3)[settings['theme'] == 'light'])
    text_entry.tag_raise('sel')
    text_entry.config(insertbackground=entry_box.cget('insertbackground'), insertwidth=1) # , selectbackground=('#' + '38' * 3, '#' + 'b7' * 3)[settings['theme'] == 'light']
    scrollbar_style.configure('App.Vertical.TScrollbar', background=(("#9C9C9C", 'gray40')[theme_is_light], ('#' + '90' * 3, '#' + '5f' * 3)[theme_is_light])[added_win.title() == 'история'],
                              troughcolor=(('#' + '11' * 3, '#' + 'e8' * 3)[theme_is_light], text_entry.cget('bg'))[added_win.title() == 'инструкция'],
                              arrowcolor=text_entry.cget('bg'), relief='flat', borderwidth=0)
    scrollbar_style.map('App.Vertical.TScrollbar', background=[('active', text_entry.cget('fg'))])
    
    added_win.bind('<Key>', disable_editing_added_win_text)
    text_entry.bind('<Key>', disable_editing_added_win_text)
    
    added_win['bg'] = ('#' + '20' * 3, '#' + 'e8' * 3)[settings['theme'] == 'light']
    
    added_win.bind('<Control-Shift-Up>', lambda key: None)  # не удалять! поддерживает автономию перед <Control-Up>
    added_win.bind('<Control-Shift-Down>', lambda key: None)  # не удалять! поддерживает автономию перед <Control-Down>
    added_win.bind('<Control-Up>', lambda key: scroll_text(-4))
    added_win.bind('<Control-Down>', lambda key: scroll_text(4))
    
    for the_win in (added_win, text_entry):
        the_win.bind('<Control-t>', change_theme)
        the_win.bind('<Control-T>', change_theme)
    added_win.bind('<Control-equal>', lambda key: change_text_size(increase=True))
    added_win.bind('<Control-minus>', lambda key: change_text_size(increase=False))
    
    if cursor_index and example_value[cursor_index - 1:cursor_index].lower() == '?':
        example_value = delete_in_example(example_value, -1)
        cursor_index -= 1
    entry_box.delete(0, END)
    entry_box.insert(END, example_value)
    entry_box.icursor(cursor_index)
    if type(indexes_of_selection) is dict:
        entry_box.selection_range(*indexes_of_selection.values())
    
    added_win.bind('?', lambda key: create_added_win('?'))
    text_entry.bind('?', lambda key: create_added_win('?'))
    added_win.bind('<Control-Shift-Key>', added_win_control_keypress)
    text_entry.bind('<Control-Shift-Key>', added_win_control_keypress)
    (added_win, text_entry)[added_win.title() != 'инструкция'].bind('<Control-Key>', added_win_control_keypress)
    added_win.bind('<Control-space>', added_win_switch_to_string)
    text_entry.bind('<Control-space>', added_win_switch_to_string)
    added_win.bind('<Alt-space>', added_win_switch_to_string)
    text_entry.bind('<Alt-space>', added_win_switch_to_string)
    added_win.bind('<Tab>', added_win_switch_to_string)
    text_entry.bind('<Tab>', added_win_switch_to_string)
    
    added_win.bind('<Escape>', lambda key: manage_not_main_window_close())
    text_entry.bind('<Escape>', lambda key: manage_not_main_window_close())
    added_win.bind('<ButtonPress-3>', lambda key: manage_not_main_window_close())
    text_entry.bind('<ButtonPress-3>', lambda key: manage_not_main_window_close())
    
    added_win.bind('<Shift-MouseWheel>', move_added_win_scrolling_horizontally)
    added_win.bind('<Control-MouseWheel>', lambda key: change_text_size(increase=key.delta > 0))

    set_window_theme_border(window=added_win, is_dark_theme=settings['theme'] == 'dark')
    (finish_to_history_win, finish_to_help_win)[is_help]()


def change_help_geometry():
    widget_font = font.Font(font=('Arial', int(HEIGHT // 2)))
    lines = text_entry.get("1.0", "end-1c").split('\n')
    line_with_max_pixels = None if not lines else max(widget_font.measure(line) for line in lines)
    added_win.geometry(f'{min(line_with_max_pixels + 8 * 2 + 1, WIDTH + 8 * 2 + 1)}x{MAX_COORD - 2 * TASKBAR_HEIGHT}+{settings['x']}+0')


def finish_to_help_win():
    theme_is_light = settings['theme'] == 'light'
    title, text = ('Arial', int(HEIGHT // 2), 'bold'), ('Arial', int(HEIGHT // 2))
    
    black = ("#aaaaaa", 'black')[theme_is_light]
    green = ("#429442", 'green')[theme_is_light]
    blue = ("#5e9eb6", 'blue')[theme_is_light]
    gray = ("#9C9C9C", 'gray40')[theme_is_light]
    red = ("#b42020", 'red4')[theme_is_light]
    colors = (black, green, blue, gray, red)
    [text_entry.tag_config(f'help_{color}_{('normal', 'bold')[flag]}', font=(text, title)[flag], foreground=color) for color in colors for flag in (True, False)]
    
    splitted_text_entry = help_text.split('\n')
    text_entry.delete(1.0, END)
    tag_rows = (3, 4) + tuple(line_indx + 1 for line_indx, text_line in enumerate(splitted_text_entry) if not text_line)
    for i in range(len(splitted_text_entry)):
        val = splitted_text_entry[i] + '\n'
        weight = ('normal', 'bold')[i in tag_rows]
        val = ('', '✓', 4 * ' ')[(weight == 'bold') + (i == tag_rows[1])] + val
        color = ((black,) * 4 + (blue, green, gray) + (red,) * 4)[sum([i >= el for el in tag_rows])]
        text_entry.insert(END, val, f'help_{color}_{weight}')

    change_help_geometry()


def finish_to_history_win():
    theme_is_light = settings['theme'] == 'light'
    
    added_win.wm_attributes("-transparentcolor", ('#' + '10' * 3, '#' + 'e9' * 3)[settings['theme'] == 'light'])
    added_win.bind('<Control-Alt-Up>', lambda key: scroll_text(-1))
    added_win.bind('<Control-Alt-Down>', lambda key: scroll_text(1))
    added_win.overrideredirect(True)
    added_win.wm_attributes('-topmost', 1)
    added_win.geometry(f'{WIDTH + 8 * 2 + 1}x{MAX_COORD - 2 * TASKBAR_HEIGHT}+{settings['x']}+0')
    
    
    color1 = ('#' + 'b0' * 3, '#' + '2f' * 3)[theme_is_light]
    color2 = ('#' + '90' * 3, '#' + '5f' * 3)[theme_is_light]
    [text_entry.tag_config(f'history_{color1}', foreground=color1), text_entry.tag_config(f'history_{color2}', foreground=color2)]
    tags = (None, f'history_{color1}', f'history_{color1}', f'history_{color2}')
    [text_entry.insert(END, val + '\n', tags[(i + 1) % 4]) for i, val in enumerate(history_of_calculations.split('\n'))]
    for i in range(history_of_calculations.count('\n') + 1):
        text_entry.tag_add('highlight', f'{i + 1}.0', f'{i + 1}.end')
    text_entry.focus_set()
    text_entry.tag_add(SEL, '1.0', 'end')


def get_tape_scale():
    return range((WIDTH // 2 + 1 - HEIGHT // 2) % HEIGHT - HEIGHT, WIDTH, HEIGHT)


def set_tape_creation_time(event):
    global tape_creation_time
    tape_creation_time = time.time()


def move_on_lasts(x, y):
    global tape_creation_time
    if (x - (WIDTH - oval_center_x)) ** 2 - (y - oval_center_y) ** 2 < oval_radius ** 2:
        for _ in range(49):
            if ctrl_y('no drawing'):
                break
        else:
            ctrl_y()
    elif (x - oval_center_x) ** 2 - (y - oval_center_y) ** 2 < oval_radius ** 2:
        for _ in range(49):
            if ctrl_z('no drawing'):
                break
        else:
            ctrl_z()
    elif x > WIDTH // 2 + HEIGHT // 2:
        i_last_shift = (x - (WIDTH // 2 + HEIGHT // 2)) // HEIGHT
        for _ in range(i_last_shift):
            if ctrl_y('no drawing'):
                break
        else:
            ctrl_y()
    elif x < WIDTH // 2 - HEIGHT // 2:
        i_last_shift = ((WIDTH // 2 - HEIGHT // 2) - x) // HEIGHT
        for _ in range(i_last_shift):
            if ctrl_z('no drawing'):
                break
        else:
            ctrl_z()
    tape_creation_time = time.time()


def shift_info_for_more_comftable_reading(key):
    set_tape_creation_time(key)
    tape_label_width = tape_info_label.winfo_width()
    tape_info_label.place(x=0 if tape_label_width < WIDTH else a if (b := -abs(WIDTH - tape_label_width) - WIDTH // 120) <= (a := (tape_info_label.winfo_x() + WIDTH // 51 * (1, -1)[key.delta < 0])) <= 0 else (b - WIDTH // 120, 0)[a > 0], y=0)


def create_tape(tape_type='undo-redo', info_blit=''):
    global tape, tape_canvas, tape_creation_time, tape_info_label, example_value
    if (not tape or int(tape_canvas.cget('width')) == 0) and tape_type == 'undo-redo':
        if tape and int(tape_canvas.cget('width')) == 0:
            destroy_tape()
        create_tape_base(main_win['bg'])
        
        tape_canvas = Canvas(tape, width=WIDTH, height=HEIGHT, bg=entry_box.cget('bg'), borderwidth=0, highlightthickness=0)
        tape_canvas.pack()
        resize_and_retheme_canvas_drawings()
        tape.bind('<ButtonPress-1>', lambda event: move_on_lasts(event.x, event.y))
        tape.bind('<Motion>', set_tape_creation_time)
        tape.bind('<Shift-MouseWheel>', smart_accelerated_scroll)  # для удобного потягивания по тачпаду
        tape.bind('<MouseWheel>', smart_accelerated_scroll)  # для удобной прокрутки колеса мыши без прожатия shift
    elif (not tape or int(tape_canvas.cget('width')) > 0) and tape_type == 'info':
        if tape and int(tape_canvas.cget('width')) > 0:
            destroy_tape()
        create_tape_base(entry_box.cget('bg'))
        
        tape_canvas = Canvas(tape, width=0, height=0, bg=entry_box.cget('bg'), borderwidth=0, highlightthickness=0)
        tape_canvas.pack()
        tape_info_label = Label(tape, text=info_blit, font=('Arial', HEIGHT // 2), fg=entry_box.cget('fg'), bg=entry_box.cget('bg'))
        tape_info_label.place(x=0, y=0)
        resize_and_retheme_canvas_drawings()
        tape.bind('<ButtonPress-1>', lambda event: None if not (a := ' – нажми меня, чтобы поменять местами аргументы логарифмов') in info_blit
                  else (entry_box.delete(0, END), entry_box.insert(END, info_blit.split(' – ')[0]), calculate_result(), _mouse_move_to(event.x_root, event.y_root + (-HEIGHT, HEIGHT)[settings['y'] - HEIGHT > 0]), destroy_tape()))
        tape.bind('<Motion>', set_tape_creation_time)
        tape.bind('<Shift-MouseWheel>', shift_info_for_more_comftable_reading)  # для удобного потягивания по тачпаду
        tape.bind('<MouseWheel>', shift_info_for_more_comftable_reading)  # для удобной прокрутки колеса мыши без прожатия shift

    tape_creation_time = time.time()


def create_tape_base(tape_color):
    global tape
    tape = Toplevel()
    tape.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{settings['y'] - HEIGHT}')
    tape.overrideredirect(True)
    tape.wm_attributes('-topmost', 1)
    tape.attributes('-alpha', '0.95')
    tape['bg'] = tape_color


def destroy_tape():
    global tape, tape_creation_time
    if tape:
        tape.destroy()
    tape = None
    tape_creation_time = 10 ** 100


def tape_text_color(light_up_indxs, lst, indx):
    return entry_box.cget('fg') if (len(lst) // 2 - (len(lst) - indx - 1)) in light_up_indxs else ('#' + '70' * 3, '#' + '6f' * 3)[settings['theme'] == 'light']

def on_hover_oval(arrow_tag): tape_canvas.itemconfig(arrow_tag, fill=('#909054', '#5f5f9b')[settings['theme'] == 'light'])
def on_leave_oval(arrow_tag): tape_canvas.itemconfig(arrow_tag, fill=('white', 'black')[settings['theme'] == 'light'])
def on_hover_rect(rect_tag, i):
    tape_canvas.create_text(i + HEIGHT // 2 + 1, 3 * HEIGHT // 8, font=('Arial', HEIGHT // 2), anchor=CENTER, state=DISABLED, fill=('white', 'black')[settings['theme'] == 'light'],
                            text=rect_tag[4:] if int(rect_tag[4:]) == 0 else '-' + rect_tag[4:] if '-' not in rect_tag else rect_tag[1 + 4:], tags='text' + rect_tag)
def on_leave_rect(rect_tag):
    tape_canvas.delete('text' + rect_tag)

def resize_and_retheme_canvas_drawings(info_blit=''):
    global tape_canvas, tape_creation_time, tape_info_label, oval_center_x, oval_center_y, oval_radius
    tape.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{settings['y'] - HEIGHT if settings['y'] - HEIGHT > 0 else settings['y'] + HEIGHT}')
    if int(tape_canvas.cget('width')) > 0:
        tape_canvas.config(width=WIDTH, height=HEIGHT, bg=entry_box.cget('bg'))
        tape_canvas.delete('all')
        lst = get_tape_scale()
        i_num_last_example = (-1, len(recents['last examples']) - 1)[i_last_example == 'future'] if type(i_last_example) == str else i_last_example
        
        for indx, i in enumerate(lst):
            if i_num_last_example in range(-1, len(recents['last examples'])) and len(lst) // 2 != len(lst) - indx - 1:
                indx_info = (len(recents['last examples']) - (i_num_last_example + 1)) - len(lst) // 2 + (len(lst) - indx - 1)
                the_rect_tag = 'rect' + str(indx_info)

                tape_canvas.create_rectangle(i + 1, 0, i + HEIGHT - 1, HEIGHT, tags=the_rect_tag, fill=entry_box.cget('bg'), outline='')
                tape_canvas.tag_bind(the_rect_tag, '<Enter>', lambda event, rect_tag=the_rect_tag, i=i: on_hover_rect(rect_tag, i))
                tape_canvas.tag_bind(the_rect_tag, '<Leave>', lambda event, rect_tag=the_rect_tag: on_leave_rect(rect_tag))
                
        for indx, i in enumerate(lst):
            if i_num_last_example in range(-1, len(recents['last examples'])):
                indx_info = (len(recents['last examples']) - (i_num_last_example + 1)) - len(lst) // 2 + (len(lst) - indx - 1)
                if indx_info in range(-1, len(recents['last examples']) + 1):
                    tape_canvas.create_line(i, 7 * HEIGHT // 8, i, HEIGHT, fill=tape_text_color((0, 1), lst, indx), width=1)
                if len(lst) // 2 == len(lst) - indx - 1:
                    tape_canvas.create_line(i, 7 * HEIGHT // 8, i + HEIGHT, 7 * HEIGHT // 8, fill=tape_text_color((0, 1), lst, indx), width=1)
                if indx_info % 10 == 0 or len(lst) // 2 == len(lst) - indx - 1:
                    strdx_info = str(indx_info)
                    the_rect_tag = 'rect' + str(indx_info)
                    
                    tape_canvas.create_text(i + HEIGHT // 2 + 1, 3 * HEIGHT // 8, font=('Arial', HEIGHT // 2), anchor=CENTER, fill=tape_text_color((0,), lst, indx),
                                            text=strdx_info if indx_info == 0 else '-' + strdx_info if '-' not in strdx_info else strdx_info[1:], tags='text' + str(indx_info))
                    tape_canvas.tag_bind('text' + str(indx_info), '<Enter>', lambda event, rect_tag=the_rect_tag, i=i: on_hover_rect(rect_tag, i))
                    tape_canvas.tag_bind('text' + str(indx_info), '<Leave>', lambda event, rect_tag=the_rect_tag: on_leave_rect(rect_tag))

        
        oval_center_x = oval_center_y = HEIGHT // 2
        oval_radius = 3 * HEIGHT // 8
        tape_canvas.create_oval(oval_center_x - oval_radius, oval_center_y - oval_radius,
                            oval_center_x + oval_radius, oval_center_y + oval_radius, fill=('black', 'white')[settings['theme'] == 'light'], tags='left_oval')
        tape_canvas.create_oval(WIDTH - (oval_center_x + oval_radius), oval_center_y - oval_radius,
                                WIDTH - (oval_center_x - oval_radius), oval_center_y + oval_radius, fill=('black', 'white')[settings['theme'] == 'light'], tags='right_oval')
        
        tape_canvas.create_line(oval_center_x - oval_radius + 1, HEIGHT // 2, oval_center_x + oval_radius, HEIGHT // 2,
                                fill=('white', 'black')[settings['theme'] == 'light'], width=3,
                                arrow=LAST, arrowshape=(HEIGHT // 4, 3 * HEIGHT // 8, HEIGHT // 6),  tags='left_tape_arrow')
        tape_canvas.create_line(WIDTH - (oval_center_x + oval_radius - 1), HEIGHT // 2, WIDTH - (oval_center_x - oval_radius), HEIGHT // 2,
                                fill=('white', 'black')[settings['theme'] == 'light'], width=3,
                                arrow=FIRST, arrowshape=(HEIGHT // 4, 3 * HEIGHT // 8, HEIGHT // 6),  tags='right_tape_arrow')
        for (oval_tag, tape_arrow_tag) in (('left_oval', 'left_tape_arrow'), ('right_oval', 'right_tape_arrow')):
            tape_canvas.tag_bind(oval_tag, '<Enter>', lambda event, tape_arr_tag=tape_arrow_tag: on_hover_oval(tape_arr_tag))
            tape_canvas.tag_bind(oval_tag, '<Leave>', lambda event, tape_arr_tag=tape_arrow_tag: on_leave_oval(tape_arr_tag))
            tape_canvas.tag_bind(tape_arrow_tag, '<Enter>', lambda event, tape_arr_tag=tape_arrow_tag: on_hover_oval(tape_arr_tag))
            tape_canvas.tag_bind(tape_arrow_tag, '<Leave>', lambda event, tape_arr_tag=tape_arrow_tag: on_leave_oval(tape_arr_tag))

    else:
        tape.config(bg=entry_box.cget('bg'))
        tape_info_label.config(text=info_blit if info_blit else tape_info_label.cget('text'), fg=entry_box.cget('fg'), bg=entry_box.cget('bg'), font=('Arial', HEIGHT // 2))

    tape_creation_time = time.time()
    
    
def manage_not_main_window_close():
    set_last_func_is_ctrl_shift_scroll(False)
    set_del_mode(False)
    added_win.withdraw()
    added_win.title(invisible_win_title)
    entry_box.focus_set()
    beauty_letter_tape.wm_attributes('-topmost', 1)


ROUND_ANSWER_TO = 18
ROUND_ANSWER_TO_IF_POW = 12
max_rounding = ROUND_ANSWER_TO - 1
min_rounding = -(24 - 1)

main_win = Tk()
main_win.overrideredirect(True) # Убрать заголовок окна


def force_entry_copy(key):
    global indexes_of_selection
    main_win.after(150, lambda: main_win.event_generate('<apostrophe>'))  # минимальное значение в миллисекундах, чтобы прекратить выделение копируемого окна
    return 'break'
entry_box = Entry(main_win, font=('Arial', HEIGHT // 2), borderwidth=0, insertwidth=1, insertontime=700, insertofftime=500, exportselection=0)
entry_box.bind('<Double-Button-1>', force_entry_copy)
entry_box.insert(END, recents['example before closing'])
entry_box.icursor(recents['cursor before closing'])
entry_box.focus_set()
cursor_index = entry_box.index('insert')
indexes_of_selection = None
can_backspace = entry_box.index('insert') != 0

result = Entry(main_win, font=('Arial', HEIGHT // 2), borderwidth=0, insertwidth=1, insertontime=700, insertofftime=500, exportselection=0)
result.bind('<Double-Button-1>', lambda key: main_win.event_generate('<quotedbl>'))
change_width_of_entry(recents['example before closing'], entry_box, result)
example_value = entry_box.get()

tape_creation_time = 10 ** 100
tape = None
create_added_win(None)

close_label = Label(main_win, text='×', font=('Arial', HEIGHT // 3 - 1), padx=0, pady=0, borderwidth=0, highlightthickness=0)
close_label.place(x=WIDTH - HEIGHT // 3, y=1, width=HEIGHT // 3 - 1, height=HEIGHT // 3 - 1) 
close_label.bind('<Enter>', lambda key: close_label.config(bg='red'))
close_label.bind('<Leave>', lambda key: close_label.config(bg=result.cget('bg')))

hide_label = Label(main_win, text='−', font=('Arial', HEIGHT // 3 - 1), padx=0, pady=0, borderwidth=0, highlightthickness=0)
hide_label.place(x=WIDTH - 2 * HEIGHT // 3 + 1, y=1, width=HEIGHT // 3 - 1, height=HEIGHT // 3 - 1) 
hide_label.bind('<Enter>', lambda key: hide_label.config(bg=main_win['bg']))
hide_label.bind('<Leave>', lambda key: hide_label.config(bg=result.cget('bg')))

change_size_of_everything(scale=settings['scale'])

main_win.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{settings['y']}')


def set_focus_from_not_my_application():
    if not main_win.focus_get():
        change_size_of_everything(scale=settings['scale'], scale_was_zero=True, change_result=False)
        length = get_text_length(entry_box.get()[:cursor_index], entry_box) + 3
        width_plus_x_coord = WIDTH + MIN_X_COORD
        length_plus_x_coord = length + MIN_X_COORD
        last_pos = _mouse_pos()
        x = length_plus_x_coord if length_plus_x_coord < width_plus_x_coord - 5 else width_plus_x_coord - 5
        y = settings['y'] + HEIGHT // 2
        _mouse_move_to(x, y)
        _mouse_click()
        _mouse_move_to(*last_pos)


if draw_animation:
    main_win.after(10, lambda: set_focus_from_not_my_application())
        
        
def set_keyboard_layout_memory():
    global keyboard_layout_memory
    keyboard_layout_memory = ('en', 'ru')[not is_russian_layout()]


def add_hotkeys_from_other_wins_and_import():
    global pyperclip, virtual_keyboard
    import virtual_keyboard
    import pyperclip  # тоже самое
    import keyboard  # дохрена жрёт
    keyboard.add_hotkey('ctrl+space', set_focus_from_not_my_application)
    keyboard.add_hotkey('alt+space', set_focus_from_not_my_application)
    keyboard.add_hotkey('shift+alt', set_keyboard_layout_memory)
    keyboard.add_hotkey('win+space', set_keyboard_layout_memory)
    main_win.wm_attributes('-topmost', 1)  # Сделать окно несворачиваемым при нажатии на другие окна
    main_win.attributes('-alpha', '0.975')
    main_win.title('Калькулятор.')


main_win.after(200, add_hotkeys_from_other_wins_and_import)


def matching_when_cursor_on_regex(left_regex, right_regex):
    global example_value
    if left_regex == right_regex == '|':
        modUle_example_value = re.sub(r'^(\s*)(.*)(\s*)$', r'\1(\2)\3', example_value)
        for i in range(len(modUle_example_value) - 1):
            if modUle_example_value[i + 1] == '|':
                module_type = 'Uu'[modUle_example_value[i] in '0123456789!)ueπφE' or bool(re.match(r'[+•/^!\)]|mod|div', modUle_example_value[i + 2:]))]
                modUle_example_value = modUle_example_value[:i + 1] + module_type + modUle_example_value[i + 2:]
                example_value = example_value.replace('|', module_type, 1)
        modUle_example_value = re.sub(r'^(\s*)\((.*)\)(\s*)$', r'\1\2\3', modUle_example_value)

    left_match = re.search(fr'{left_regex}\s*$', example_value[:cursor_index])
    right_match = re.match(fr'\s*{right_regex}', example_value[cursor_index:])
    if left_match and right_match:
        return (left_match, right_match)
    return


def delete_to_the(k):
    global example_value, cursor_index
    last_keys_not_having_keytype_changed = list(filter(lambda key: key != 'changed', last_keys))
    last_key_without_mul = bool(re.fullmatch(r'(?:[sctCdalngo\\]|BackSpace)', last_keys_not_having_keytype_changed[-1]) and last_keys_not_having_keytype_changed[-2] not in ('x', 'asterisk'))
    last_key_without_mul2 = bool(re.fullmatch(r'[sctC\\]', last_keys_not_having_keytype_changed[-2]) and last_keys_not_having_keytype_changed[-1] == 'BackSpace')
    last_key_without_scope_for_minus = bool(last_keys_not_having_keytype_changed[-1] == 'minus' and last_keys_not_having_keytype_changed[-2] not in ('parenleft', 'o'))
    last_key_without_minus_for_root = bool(last_keys_not_having_keytype_changed[-1] == 'r' and last_keys_not_having_keytype_changed[-2] != 'minus')
    for i in reunite(composite_trig_funcs):
        if ((matches := matching_when_cursor_on_regex(fr'{r'•?\s*' * last_key_without_mul}{i}\s*\(', r'\)') or matching_when_cursor_on_regex(fr'{i}\s*\|', r'\|'))
            and last_keys_not_having_keytype_changed[-1] in ('a', 's', 'c', 't', 'C') and k == -1):
            if (re.search(r'a\\s\*r\\s\*c\\s\*\S', i) and last_keys_not_having_keytype_changed[-1] in ('s', 'c', 't', 'C') or re.search(r'd\s*\S', i)
                and (last_keys_not_having_keytype_changed[-1] in ('a', 's', 'c', 't', 'C') or last_key_without_mul2)):
                example_value = delete_in_example(example_value, -len(re.search(r'(?:sin|cos|tg|(?<!ar)ctg)\s*\(\s*$' if not (last_keys_not_having_keytype_changed[-1] == 'a' or last_key_without_mul2) else r'arc\s*\(\s*$', example_value[:cursor_index])[0]))
                example_value = delete_in_example(example_value, len(re.match(r'\s*\)', example_value[cursor_index:])[0]))
                example_value = insert_in_example(example_value, '(')
                example_value = insert_in_example(example_value, ')', right=True)
                return
            example_value = delete_in_example(example_value, -len(matches[0][0]))
            if after_1_condition := re.search(r'(?:[^0-9veE\.]|^)\s*1\s*(\-\s*)$', example_value[:cursor_index]):
                example_value = delete_in_example(example_value, -len(after_1_condition[1]))
            example_value = delete_in_example(example_value, len(matches[1][0]))
            if re.search(r'm\s*o\s*$', example_value[:cursor_index]):
                example_value = insert_in_example(example_value, 'd')
            return
    for i in reunite(united_symbols_without_scopes):
        if (matches := matching_when_cursor_on_regex(fr'{r'•?\s*' * last_key_without_mul}{i}\s*\(', r'\)') or matching_when_cursor_on_regex(fr'{i}\s*\|', r'\|')) and k == -1:
            example_value = delete_in_example(example_value, -len(matches[0][0]))
            if after_1_condition := re.search(r'(?:[^0-9veE\.]|^)\s*1\s*(\-\s*)$', example_value[:cursor_index]):
                example_value = delete_in_example(example_value, -len(after_1_condition[1]))
            example_value = delete_in_example(example_value, len(matches[1][0]))
            if re.search(r'm\s*o\s*$', example_value[:cursor_index]):
                example_value = insert_in_example(example_value, 'd')
            return
    if (after_1_minus_root_condition := re.fullmatch(r'(?:[^0-9veE\.]|^)\s*1\s*(\-\s*√)', example_value[:cursor_index])) and last_key_without_minus_for_root:
        example_value = delete_in_example(example_value, -len(after_1_minus_root_condition[1]))
        return
    for indx, left_match_check in enumerate(reunite(('log(', 'log|', 'log'))):
        for right_match_check in reunite(((')by()', ')by||', ')by'), ('|by||', '|by()', '|by'), ('by||', 'by()', 'by'))[indx]):
            if ((matches := matching_when_cursor_on_regex(fr'{r'•?\s*' * last_key_without_mul}{left_match_check}', right_match_check)) and
                (k == -1 or left_match_check.replace('s*', '').replace('\\', '') + right_match_check.replace('s*', '').replace('\\', '') in ('logby', 'logby()', 'logby||'))):
                example_value = delete_in_example(example_value, -len(matches[0][0]))
                if (after_1_condition := re.search(r'(?:[^0-9veE\.]|^)\s*1\s*(\-\s*)$', example_value[:cursor_index])) and left_match_check + right_match_check != 'logby':
                    example_value = delete_in_example(example_value, -len(after_1_condition[1]))
                example_value = delete_in_example(example_value, len(matches[1][0]))
                return
    for indx, left_match_check in enumerate(reunite(('log()by(', 'log||by(', 'log||by|', 'log()by|', 'log()by', 'log||by'))):
        right_match_check = (r'\)', r'\|', r'')[indx // 2]
        if (matches := matching_when_cursor_on_regex(fr'{r'•?\s*' * last_key_without_mul}{left_match_check}', right_match_check)) and k == -1:
            example_value = delete_in_example(example_value, -len(matches[0][0]))
            if after_1_condition := re.search(r'(?:[^0-9veE\.]|^)\s*1\s*(\-\s*)$', example_value[:cursor_index]):
                example_value = delete_in_example(example_value, -len(after_1_condition[1]))
            example_value = delete_in_example(example_value, len(matches[1][0]))
            return
    if matches := matching_when_cursor_on_regex(fr'{r'•?\s*' * last_key_without_mul}\({r'\s*-' * last_key_without_scope_for_minus}', r'\)') or matching_when_cursor_on_regex(fr'{r'•?\s*' * last_key_without_mul}\|', r'\|'):
        example_value = delete_in_example(example_value, -len(matches[0][0]))
        example_value = delete_in_example(example_value, len(matches[1][0]))
    elif not re.search(fr'E-?{num_construct}•e$', exampled_value()[:cursor_index]) and (i := re.search(r'(?<=[\d.])•(?:√|e\s*-?)\s*$', example_value[:cursor_index])) and last_keys_not_having_keytype_changed[-1] == ('r', 'e', 'minus')[('e' in i[0]) + ('-' in i[0])] and k == -1:
        example_value = delete_in_example(example_value, -len(i[0]))
        example_value = insert_in_example(example_value, ('√', 'e' + '-' * (last_keys_not_having_keytype_changed[-1] == 'minus'))[last_keys_not_having_keytype_changed[-1] != 'r'])
    elif cursor_index > 0 and k == -1 or cursor_index < len(example_value) and k == 1:
        add_0_point_1_slash = bool(re.search(r'(?:[^0-9veE\.]|^)\s*1\s*[+/]\s*|(?:[^0-9\.]\s*|^)[01]\s*\.\s*', example_value[:cursor_index])) and bool(re.search(r'\s*(?:$|\))', example_value[cursor_index:]))
        special_cases_2plus = bool(re.search(r'(?:(?:[+-•/^√(]|^)\s*2\s*[•^]|[•/^√]\s*2\s*[+/])\s*', example_value[:cursor_index])) and bool(re.match(r'\s*(?:$|)', example_value[cursor_index:]))
        pre_length = -len(re.search(fr'(?:\S|{fr'\^\s*{'ujUJ'.index(last_keys_not_having_keytype_changed[-1]) + 2}\s*|' if last_keys_not_having_keytype_changed[-1] in 'ujUJ' else ''}' + 
                                    fr'{r'(?:\S|(?:(?<!^)1\s*)?/\s*2\s*)|' if last_keys_not_having_keytype_changed[-1] == 'h' else ''}' + 
                                    fr'{fr'•?\s*[Ee](?:\s*-)?\s*(?:{(3, 6, 9, 12, 15)['kMBTQkm'.index(last_keys_not_having_keytype_changed[-1]) % 5]})\s*|' if last_keys_not_having_keytype_changed[-1] in 'kMBTQkm' else ''}' +
                                    fr'{r'1\s*[+/]|[01]\s*\.|' * bool(add_0_point_1_slash and re.match(r'\s*(?:$|\))', example_value[cursor_index:]))}' +
                                    fr'{r'2\s*[+•^/]|' * bool(special_cases_2plus and re.match(r'\s*(?:$|\))', example_value[cursor_index:]))}' + 
                                    fr'(?<=π)\s*/\s*\d|(?<=[φ)])\s*(?:/\s*(?:\d|0\.)|•\s*1\.)|(?<=[e!])\s*•\s*(?:\d|[01]\.)|(?<=[\d.πφe])\s*•\s*[πφe]|^)\s*$', example_value[:cursor_index])[0])

        past_length = len(re.match(fr'\s*(?:\S|$)', example_value[cursor_index:])[0])
        example_value = delete_in_example(example_value, (pre_length, past_length)[k > 0])


def get_selection(the_entry=entry_box):
    try:
        return {'start': the_entry.index(SEL_FIRST), 'end': the_entry.index(SEL_LAST)}
    except TclError:
        return
    
    
def add_to_recents(value):
    return value != recents['recent examples'][-1][0]


def clean_from_scopes_with_emptyness(value):
    value = replace_abs_signs(value)
    value = clean_pattern_empty_scopes(value)
    value = re.sub(r'[Uu]', '|', value)
    value = re.sub(r'(?:[\+\-•:^,]|mod|div)(?=\))', r'', f'({value})')[1:-1]
    return value


def make_it_future(example_after_q=False):
    entry_box.delete(0, END)
    entry_box.insert(END, example_value)
    entry_box.icursor(cursor_index)
    calculate_result()
    change_width_of_entry(entry_box.get(), entry_box, result)
    return_rounding_to_future_state_while_making_i_last_example_future()


def return_rounding_to_future_state_while_making_i_last_example_future():
    global i_last_example
    if i_last_example != 'future' and i_history == 'future':
        settings['round'] = settings['rounding in future state']
    i_last_example = 'future'


def return_rounding_to_future_state_while_making_i_history_future():
    global i_history
    if i_history != 'future' and i_last_example == 'future':
        settings['round'] = settings['rounding in future state']
    try:
        i_history = highlight_i_history_text_and_centralize('future')
    except NameError:
        i_history = 'future'


# return_rounding_to_future_state_while_making_i_history_future()
i_history = 'future'
# return_rounding_to_future_state_while_making_i_last_example_future()
i_last_example = 'future'
    
    
def get_difference(old, new):
    start = 0
    # Находим, до какого момента строки абсолютно одинаковы с начала
    while start < len(old) and start < len(new) and old[start] == new[start]:
        start += 1
        
    end_old = len(old)
    end_new = len(new)
    # Находим, с какого момента они одинаковы с конца (не заходя за точку start)
    while end_old > start and end_new > start and old[end_old - 1] == new[end_new - 1]:
        end_old -= 1
        end_new -= 1
        
    # Вырезаем то, что изменилось
    deleted = old[start:end_old]
    
    return deleted


def destroy_nearby_bracks(example, arg):
    examped = exampled_value(example)
    if re.search(fr'(?:d{r'|arc' * (arg != 'arc')})\($', examped[:cursor_index]) and re.match(r'\)', examped[cursor_index:]):
        example = delete_in_example(example, -len(re.search(r'(?:\S|^)\s*$', example_value[:cursor_index])[0]))
        example = delete_in_example(example, len(re.match(r'\s*(?:\S|$)', example_value[cursor_index:])[0]))
        return insert_in_example(example, arg)
    return insert_in_example(example, arg)


def insertion_if_division_of_one(left_symbol, arg, example, destroy_nearby_scopes=False, without_one=False):
    division_after_1_condition = re.fullmatch(r'(?:[^0-9veE\.]|^\s*)1', exampled_value(example)[max(cursor_index - 2, 0):cursor_index])
    division_after_num_condition = re.search(r'(?<![ev])(?<![0-9.]e-)(?:\d+\.?\d*|\.\d+)/$', exampled_value(example)[:cursor_index])
    const_to_pow_condition = re.search(fr'({re.escape(arg)}\s*\^\s*)(\(?\s*-?\s*)((?:\d\s*)+\s*\.?\s*(?:\d\s*)*\s*|\.\s*(?:\d\s*)+\s*)((?(1)\s*\)?\s*|))$', example[:cursor_index])
    const_condition = re.search(fr'({re.escape(arg)}\s*)$', example[:cursor_index])
    if re.search(r'[φπe]', arg) and const_to_pow_condition:
        example = delete_in_example(example, -len(const_to_pow_condition[2]) - len(const_to_pow_condition[3]) - len(const_to_pow_condition[4]))
        example = insert_in_example(example, const_to_pow_condition[2] + str(Decimal(const_to_pow_condition[3].replace(' ', '')) + 1) + const_to_pow_condition[4])
        return example
    elif re.search(r'[φπe]', arg) and const_condition:
        example = insert_in_example(example, '^2')
        return example
    elif arg in ('E3', 'E6', 'E9', 'E12', 'E15', 'E18'):
        if division_after_1_condition and not without_one:
            example = delete_in_example(example, -len(re.search(r'(?:\S|^)\s*$', example[:cursor_index])[0]))
            return insert_in_example(example, f'1E-{arg[1:]}')
        elif division_after_num_condition:
            example = delete_in_example(example, -len(re.search(r'(?<=[0-9.])\s*/\s*$', example[:cursor_index])[0]))
            return insert_in_example(example, f'e-{arg[1:]}')
        else:
            return insert_in_example(example, f'{'•' if left_symbol in 'φπevEထ)!' else ''}e{arg[1:]}')
    elif division_after_1_condition:
        return (insert_in_example, destroy_nearby_bracks)[destroy_nearby_scopes](example, f'{('/', '-')[arg in ('d', 'arc', 'sin', 'cos', 'tg', 'ctg', 'log(', 'ln', 'lg', '√')]}{arg}')
    elif arg == 'φ':
        return (insert_in_example, destroy_nearby_bracks)[destroy_nearby_scopes](example, '!' if left_symbol in '0123456789φπevEထ)!' else 'φ')
    else:
        return (insert_in_example, destroy_nearby_bracks)[destroy_nearby_scopes](example, f'{'•' if left_symbol in '0123456789φπevEထ)!' and not re.search(r'div$', exampled_value(example)) else ''}{arg}')


def set_window_theme_border(window, is_dark_theme):
    """
    Принудительно делает системную рамку окна темной или светлой (Windows 10/11).
    """
    window.update() # Гарантируем, что Windows успела выдать окну ID
    
    # Получаем HWND (дескриптор окна)
    try:
        hwnd = user32.GetParent(window.winfo_id())
    except:
        return
        
    # Код атрибута DWMWA_USE_IMMERSIVE_DARK_MODE
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    
    # Передаем 1 для темной темы, 0 — для светлой
    value = ctypes.c_int(1 if is_dark_theme else 0)
    
    # Вызываем системную функцию DWM
    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        hwnd, 
        DWMWA_USE_IMMERSIVE_DARK_MODE, 
        ctypes.byref(value), 
        ctypes.sizeof(value)
    )


def close_main_win_with_layout_switching(*key):
    if virtual_keyboard._vkb and not virtual_keyboard._vkb.destroyed and virtual_keyboard._vkb.visible:
        virtual_keyboard.delete_keyboard()
    else:
        close_main_win()
        if not is_russian_layout() and keyboard_layout_memory == 'ru':
            hwnd = user32.GetForegroundWindow()
            user32.PostMessageW(hwnd, 0x50, 0, user32.LoadKeyboardLayoutW("00000419", 0x1))


def auto_change_size_of_everything(key=None, size_definition=True):
    change_size_of_everything(**(({'scale': 0} if (key.y_root in (*range(3), *range(MAX_LOW_COORD + TASKBAR_HEIGHT // 2, screen_height)), HEIGHT > screen_width // 180)[size_definition]
                                  else {'scale': settings['scale'], 'scale_was_zero': True}) | {'change_result': False}))


def change_text_size(increase):
    change_size_of_everything(scale=(max(settings['scale'] - 1, 1), min(settings['scale'] + 1, 5))[increase], scale_was_zero=HEIGHT <= screen_width // 180)


close_label.bind('<ButtonPress-1>', close_main_win_with_layout_switching)
hide_label.bind('<ButtonPress-1>', auto_change_size_of_everything)


def symbol_left_from_cursor():
    return symb_left[1] if (symb_left := re.search(r'(\S)\s*$', example_value[:cursor_index])) else '#'


def symbol_right_from_cursor():
    return symb_left[1] if (symb_left := re.match(r'\s*(\S)', example_value[cursor_index:])) else '#'


def exampled_value(example=None):
    if example is None:
        example = example_value
    return f'{' ' * example[:cursor_index].count(' ')}{example.replace(' ', '')}{' ' * example[cursor_index:].count(' ')}'


def manage_key_event(key, just_from_added_win=False):
    global history_of_calculations, i_history, i_last_example, added_win, settings, example_value, cursor_index, can_backspace, indexes_of_selection, keyboard_layout_memory
    global last_keys
    grave_destroy_win = False
    if hasattr(key, 'keysym') and key.keysym in ('less', 'greater'):
        key_old = key
        key = Event()
        key.keysym = ('Left', 'Right')[key_old.keysym == 'greater']
        key.state = 0x40000
        key.keycode = (37, 39)[key_old.keysym == 'greater']
        key.type = 2  # Число 2 означает KeyPress (нажатие)
        key.x = key_old.x
        key.y = key_old.y
        key.widget = key_old.widget
        key.char = ''
    bypass = bypass2 = False
    if i_last_example != 'future' and hasattr(key, 'keysym') and key.keysym not in ('Control_L', 'Control_R', 'Shift_L', 'Shift_R'):
        add_to_last_examples_if_selection_or_cursor_change()
        make_it_future()
        bypass2 = True
    
    if type(key) is tuple:
        cursor_index = key[0]
        start, end = key
        keysym = 'changed text'
        keysym_char = None
        bypass = True
        entry_box.delete(0, END)
        entry_box.insert(END, example_value)
        calculate_result()
        entry_box.icursor(cursor_index)
        change_width_of_entry(entry_box.get(), entry_box, result)
        add_to_last_examples_if_selection_or_cursor_change()
    
    if not bypass:
        keysym = key.keysym if len(key.keysym) > 1 or key.keysym in 'MBTQIPUJCFDA' else key.keysym.lower()
        keysym_char = key.char if hasattr(key, 'char') else None
            
        if keysym in ('Tab', 'Up', 'Down', 'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Caps_Lock', 'Win_L'):
            return
        if not bypass2 and not just_from_added_win:
            if type(indexes_of_selection) is dict:
                pass
            elif keysym in ('BackSpace', 'Left'):
                cursor_index = entry_box.index('insert') + (1 if can_backspace else 0)
            elif keysym not in special_keys and keysym != 'Delete' or keysym in ('Right', 'apostrophe', 'quotedbl'):
                cursor_index = entry_box.index('insert') - 1
            else:
                cursor_index = entry_box.index('insert')
        
        entry_box.delete(0, END)
        example_value = recents['recent examples'][-1][0]
        
        if type(indexes_of_selection) is dict and (keysym not in ('Return', 'grave', 'Escape', 'Tab') and keysym_char != 'ё'):
            start, end = indexes_of_selection.values()
            if keysym in ('Left', 'Right'):
                cursor_index = start if keysym == 'Left' else end
                entry_box.insert(END, example_value)
                entry_box.icursor(cursor_index)
                indexes_of_selection = None
                bypass = True
            elif keysym not in special_keys:
                example_value = example_value[:start] + example_value[end:]
                cursor_index = start
                indexes_of_selection = None
                if keysym in ('Delete', 'BackSpace'):
                    entry_box.insert(END, example_value)
                    entry_box.icursor(cursor_index)
                    calculate_result()
                    change_width_of_entry(entry_box.get(), entry_box, result)
                    bypass = True
    if not bypass:
        if (symbol_left_from_cursor() == '.' and (len(keysym) == 1 and keysym in 'sctlngpefraodmxbivyujwIkMBTQPEUJCF' or keysym in keys_after_dot)):
            example_value = insert_in_example(example_value, '5')
        if keysym == 'BackSpace':
            greedy_deletion = tuple(f'{k}{j}' for j in ('(', '|') for k in ('sin', 'cos', 'ctg', 'tg'))
            for i in reunite(greedy_deletion + united_symbols):
                if (((i_got_pattern := re.search(fr'{i}\s*$', example_value[:cursor_index])) and (i not in reunite(greedy_deletion) or re.fullmatch(r'\s*', example_value[cursor_index:])))
                    and not (re.search(fr'log\s*$', example_value[:cursor_index]) and re.match(fr'\s*by', example_value[cursor_index:]))):
                    example_value = delete_in_example(example_value, -len(i_got_pattern[0]))
                    break
            else:
                if (i_got_pattern := re.search(fr'(?:\S|^)\s*$', example_value[:cursor_index])):
                    delete_to_the(k=-1)
        elif keysym == 'Delete':
            for i in reunite(united_symbols):
                if (i_got_pattern := re.match(fr'\s*{i}', example_value[cursor_index:])) and not (re.search(fr'log\s*$', example_value[:cursor_index]) and re.match(fr'\s*by', example_value[cursor_index:])):
                    example_value = delete_in_example(example_value, len(i_got_pattern[0]))
                    break
            else:
                if (i_got_pattern := re.match(fr'\s*(?:\S|$)', example_value[cursor_index:])):
                    delete_to_the(k=1)
        elif keysym == 'grave' or keysym_char == 'ё':
            if example_value:
                example_value = ''
                cursor_index = 0
            else:
                grave_destroy_win = True
        elif keysym == '??' or re.fullmatch(r'[А-Яа-яЁё]', symbol_left_from_cursor()) and key.char in list(letters_and_inwords + syntax):
            example_value = insert_in_example(example_value, key.char)
        elif keysym == 'v':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'v', example_value)
            # elif keysym == 'v':
            #     example_value = insert_in_example(example_value, f'{find_the_most_useful_symbol_to_paste(example_value, symbol_left_from_cursor() in '0123456789πφe.)!ထ')}')
            #     example_value = example_value[:max_character_amount]
            # elif keysym == 'V':
            #     example_value = insert_in_example(example_value, f'{find_the_most_useful_symbol_to_paste(example_value, symbol_left_from_cursor() in '0123456789πφe.)!ထ', first=False)}')
            #     example_value = example_value[:max_character_amount]
        elif keysym == 'h':
            example_value = insert_in_example(example_value, 'h' if not example_value else '/2' if symbol_left_from_cursor() in '0123456789φπevEထ)!' else '1/2')
        elif keysym == 'space':
            example_value = insert_in_example(example_value, ' ')
        elif keysym == 'I':
            example_value = insert_in_example(example_value, 'ထ')
        elif keysym == 'b':
            examped = exampled_value()
            left_find = re.match(r'\s*[)|]?\s*by\s*[(|]?\s*', example_value[cursor_index:])
            if left_find:
                cursor_index += len(left_find[0])
            else:
                examped = re.sub(r'^(\s*)(.*)(\s*)$', r'\1(\2)\3', examped)
                for i in range(len(examped) - 1):
                    if examped[i + 1] == '|':
                        module_type = 'Uu'[examped[i] in '0123456789!)ueπφE' or bool(re.match(r'[+•/^!\)]|mod|div', examped[i + 2:]))]
                        examped = examped[:i + 1] + module_type + examped[i + 2:]
                        example_value = example_value.replace('|', module_type, 1)
                examped = re.sub(r'^(\s*)\((.*)\)(\s*)$', r'\1\2\3', examped)
                examped_brackets, left_examped_brackets, right_examped_brackets = (''.join([i for i in j.replace('log', '<').replace('by', '>') if i in '()Uu<>']) for j in (examped, examped[:cursor_index], examped[cursor_index:]))

                insert_billion_flag = False
                for j in range(len(a := [examped_brackets, left_examped_brackets, right_examped_brackets])):
                    while any([i in a[j] for i in ('()', 'Uu', '<>')]):
                        a[j] = a[j].replace('()', '').replace('Uu', '').replace('<>', '')
                examped_brackets, left_examped_brackets, right_examped_brackets = a

                insert_by = ')by' if examped_brackets[-2:] == '<(' else '|by' if examped_brackets[-2:] == '<U' else 'by'
                if '<' not in examped_brackets:
                    if examped[:cursor_index][-1:] in (')', 'u'):
                        start_scope, end_scope = ('()', 'Uu')[examped[:cursor_index][-1:] != ')']
                        last_indx_of_part = len(example_value[:cursor_index])
                        for indx in range(last_indx_of_part - 1, -1, -1):
                            example_value_part = example_value[indx:last_indx_of_part]
                            if example_value_part.count(start_scope) == example_value_part.count(end_scope):
                                cursor_index_shift = (last_indx_of_part - indx)
                                cursor_index -= cursor_index_shift
                                example_value = insert_in_example(example_value, 'log')
                                cursor_index += cursor_index_shift
                                break
                    else:
                        if a := re.search(fr'{num_construct_with_spaces}\s*$', example_value[:cursor_index]):
                            cursor_index_shift = len(a[0])
                            example_value = insert_in_example(example_value, ')')
                            cursor_index -= (cursor_index_shift + 1)
                            example_value = insert_in_example(example_value, 'log(')
                            cursor_index += (cursor_index_shift + 1)
                        elif not re.search(fr'[.,\dφπeE)]$', exampled_value()[:cursor_index]):
                            insert_billion_flag = True

                scope_condition = right_examped_brackets.count(')') - left_examped_brackets.count('(') > 0
                module_condition = right_examped_brackets.count('u') - left_examped_brackets.count('U') > 0
                insert_by_addition = '(' if scope_condition else '|' if module_condition else ''
                insert_by += insert_by_addition
                example_value = example_value.replace('U', '|').replace('u', '|')
                if insert_billion_flag:
                    should_delete_mul_or_exp = bool(re.search(r'(?:(?:\d\s*)*(?:[.,]\s*))?(?:\d\s*)+[eE]\s*(?:-\s*)?(?:\d\s*)+(?:[.,]\s*)?(?:\d\s*)*', example_value[:cursor_index]))
                    example_value = delete_in_example(example_value, -len(a := re.search(fr'{r'•?' * should_delete_mul_or_exp}\s*$', example_value[:cursor_index])[0]))
                    example_value = insertion_if_division_of_one(symbol_left_from_cursor(), f'E9', example_value, without_one='•' in a)
                else:
                    example_value = insert_in_example(example_value, insert_by)
        elif keysym == 'dollar':
            pass  # Этот символ можно использовать для пустого нажатия, удалять запрещено!
        elif keysym in ('ampersand', 'greater', 'less', 'braceleft', 'braceright', 'underscore'):
            pass
        elif keysym in ('apostrophe', 'quotedbl'):
            indexes_of_selection = None
            pyperclip.copy(re.sub(r'E\(-(\d+)\)?', r'E-\1', result.get().replace('•10^', 'E').replace('10^', '1E')).replace('•', '*').replace('ထ', 'inf').replace('=', '') if keysym == 'quotedbl' else example_value.replace('•', '*').replace('ထ', 'inf'))
            if keysym == 'quotedbl':
                result.delete(bool(example_value), END)
                result.insert(END, '⮺')
                # main_win.after(tick_symbol_time, lambda: (result.delete(0, END), result.insert(END, ' ' * bool(example_value) + '✓')))
                main_win.after(after_tick_symbol_time, lambda: (result.delete(0, END), calculate_result()))
            else:
                entry_box.delete(0, END)
                entry_box.insert(END, '⮺')
                # main_win.after(tick_symbol_time, lambda: (entry_box.delete(0, END), entry_box.insert(END, '✓'), change_width_of_entry(entry_box.get(), entry_box, result)))
                main_win.after(after_tick_symbol_time, lambda: (entry_box.delete(0, END), entry_box.insert(END, example_value), entry_box.icursor(cursor_index), change_width_of_entry(entry_box.get(), entry_box, result)))
            original_cursor_color = entry_box.cget('insertbackground')
            entry_box.config(insertbackground=entry_box.cget('bg'))
            main_win.after(after_tick_symbol_time, lambda: entry_box.config(insertbackground=original_cursor_color))
        elif len(keysym) == 1 and keysym in 'izkMBTQPEbUJ':
            if keysym == 'J':
                example_value = insert_in_example(example_value, '^5')
            elif keysym == 'U':
                example_value = insert_in_example(example_value, '^4')
            elif keysym == 'z':
                if symbol_left_from_cursor() == '.' or re.search(r'(?:[^0-9\.]|^)0$', example_value):
                    example_value = insert_in_example(example_value, '.' * (symbol_left_from_cursor() != '.') + '00')
                elif symbol_left_from_cursor().isdigit():
                    example_value = insert_in_example(example_value, '000')
                else:
                    example_value = insert_in_example(example_value, '•' * (symbol_left_from_cursor() in 'φπeEထ)!') + f'1000')
            elif keysym in 'kMBTQ':
                power_addons = ('kMBTQ'.index(keysym) + 1) * 3
                if not (e_power := re.search(fr'E-?{num_construct}$', exampled_value()[:cursor_index])):
                    example_value = insertion_if_division_of_one(symbol_left_from_cursor(), f'E{power_addons}', example_value)
                else:
                    example_value = delete_in_example(example_value, -len(e_power[1]))
                    example_value = insert_in_example(example_value, str(Decimal(e_power[1]) + power_addons))
            # elif re.fullmatch(r'(?:[^0-9veE.]|^\s*)1/e$', exampled_value()[max(cursor_index - 4, 0):cursor_index]):
            #     example_value = delete_in_example(example_value, -len(re.search(r'1\s*/\s*e\s*$', example_value[:cursor_index])[0]))
            #     example_value = insert_in_example(example_value, f'1e-{keysym}')
            #     if re.search(fr'(?:(?<=^)|(?<![\dφπeE]))\s*(?:\d+\.?\d*|\.\d+)•1[Ee]-{keysym}$', exampled_value()[:cursor_index]):
            #         example_value = delete_in_example(example_value, -len(re.search(fr'•\s*1\s*e\s*-\s*{keysym}$', example_value[:cursor_index])[0]))
            #         example_value = insert_in_example(example_value, f'e-{keysym}')
            # elif re.search(r'(?<![ev])(?<![0-9.]e-)(?:\d+\.?\d*|\.\d+)/e$', exampled_value()[:cursor_index]):
            #     example_value = delete_in_example(example_value, -len(re.search(r'(?<=[0-9.])\s*/\s*e\s*$', example_value[:cursor_index])[0]))
            #     example_value = insert_in_example(example_value, f'e-{keysym}')
            elif keysym in ('P', 'i'):
                # example_value = insert_in_example(example_value, f'{'/100' if symbol_left_from_cursor() in '0123456789φπeEထ)!' else '1/100'}')
                example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'φ', example_value)
        elif keysym in ('period', 'comma'):
            if re.search(r'\.\d+$', exampled_value()[:cursor_index]):
                example_value = insert_in_example(example_value, '•1.')
            elif symbol_left_from_cursor() != '.':
                example_value = insert_in_example(example_value, '/' if symbol_left_from_cursor() == 'π' else '•' if symbol_left_from_cursor() in 'φe)!' else '')
                example_value = insert_in_example(example_value, '.' if symbol_left_from_cursor().isdigit() else '1.')
            else:
                example_value = delete_in_example(example_value, -len(re.search(r'\.\s*$', example_value[:cursor_index])[0]))
                example_value = insert_in_example(example_value, '•1.')
        elif keysym in ('s', 'c', 't', 'C'):
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), {'s': 'sin', 'c': 'cos', 't': 'tg', 'C': 'ctg'}[keysym], example_value, destroy_nearby_scopes=True)
            if symbol_right_from_cursor() != '(':
                example_value = insert_in_example(example_value, '(')
                example_value = insert_in_example(example_value, ')', right=True)
        elif keysym == 'D':
            example_value = insert_in_example(example_value, 'div')
        elif keysym == 'm':
            if not re.search(fr'[.,\dφπeE)]$', exampled_value()[:cursor_index]):
                should_delete_mul_or_exp = bool(re.search(r'(?:(?:\d\s*)*(?:[.,]\s*))?(?:\d\s*)+[eE]\s*(?:-\s*)?(?:\d\s*)+(?:[.,]\s*)?(?:\d\s*)*', example_value[:cursor_index]))
                example_value = delete_in_example(example_value, -len(a := re.search(fr'{r'•?' * should_delete_mul_or_exp}\s*$', example_value[:cursor_index])[0]))
                example_value = insertion_if_division_of_one(symbol_left_from_cursor(), f'E6', example_value, without_one='•' in a)
            else:
                example_value = insert_in_example(example_value, 'mod')
        elif keysym == 'd':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'd', example_value)
            if not re.match(r'\(|sin|cos|c?tg|arc', exampled_value(example_value)[cursor_index:]):
                example_value = insert_in_example(example_value, '(')
                example_value = insert_in_example(example_value, ')', right=True)
        elif keysym == 'l':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'log(', example_value)
            example_value = insert_in_example(example_value, ')by' if symbol_right_from_cursor() == '(' else ')by()', right=True)
        elif keysym in ('n', 'g'):
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), {'n': 'ln', 'g': 'lg'}[keysym], example_value)
            if symbol_right_from_cursor() != '(':
                example_value = insert_in_example(example_value, '(')
                example_value = insert_in_example(example_value, ')', right=True)
        elif keysym == 'p':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'π', example_value)
        elif keysym == 'r':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), '√', example_value)
        elif keysym == 'bar':
            example_value = insert_in_example(example_value, '|')
        elif keysym in ('backslash', 'A'):
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), '|', example_value)
            example_value = insert_in_example(example_value, '|', right=True)
        elif keysym == 'a':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'arc', example_value, destroy_nearby_scopes=True)
            if not re.match(r'\(|sin|cos|c?tg', exampled_value(example_value)[cursor_index:]):
                example_value = insert_in_example(example_value, '(')
                example_value = insert_in_example(example_value, ')', right=True)
        elif keysym in ('exclam', 'f'):
            if keysym != 'f':
                example_value = insert_in_example(example_value, '!')
            else:
                example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'φ', example_value)
        elif keysym == 'percent':
            example_value = insert_in_example(example_value, 'mod')
        elif keysym == 'at':
            example_value = insert_in_example(example_value, 'div')
        elif keysym in ('asciicircum', 'w'):
            if symbol_left_from_cursor() not in '0123456789φπeEvထ)|!' and keysym != 'asciicircum':
                example_value = insert_in_example(example_value, '2')
            example_value = insert_in_example(example_value, '^')
        elif keysym == 'y':
            if symbol_left_from_cursor() not in '0123456789φπeEvထ)|!' and keysym != 'asciicircum':
                example_value = insert_in_example(example_value, '1')
            example_value = insert_in_example(example_value, 'E-')
        elif keysym == 'u':
            example_value = insert_in_example(example_value, '^2')
        elif keysym == 'j':
            example_value = insert_in_example(example_value, '^3')
        elif keysym in ('x', 'asterisk'):
            if symbol_left_from_cursor() == '•' and keysym != 'asterisk':
                example_value = delete_in_example(example_value, -len(re.search(r'•\s*$', example_value[:cursor_index])[0]))
                example_value = insert_in_example(example_value, '^')
            elif symbol_left_from_cursor() not in '0123456789φπeEvထ)|!' and keysym != 'asterisk':
                example_value = insert_in_example(example_value, '2•')
            else:
                example_value = insert_in_example(example_value, '•')
        elif keysym == 'minus':
            for i in reunite(united_symbols):
                if (i_got_pattern := re.search(fr'{i}\s*$', example_value[:cursor_index])):
                    example_value = insert_in_example(example_value, '(-')
                    example_value = insert_in_example(example_value, ')', right=True)
                    break
            else:
                # if re.search(r'•e$', exampled_value()[:cursor_index]):
                #     example_value = delete_in_example(example_value, -len(re.search(r'•\s*e\s*$', example_value[:cursor_index])[0]))
                #     example_value = insert_in_example(example_value, f'e-')
                if symbol_left_from_cursor() not in '^+-•/√':
                    example_value = insert_in_example(example_value, '-')
                else:
                    example_value = insert_in_example(example_value, '(-')
                    example_value = insert_in_example(example_value, ')', right=True)
        elif keysym in ('equal', 'plus'):
            if symbol_left_from_cursor() in '•/^√' and keysym != 'plus':
                example_value = insert_in_example(example_value, '2')
                example_value = insert_in_example(example_value, '+')
            elif symbol_left_from_cursor() not in '0123456789φπeEvထ)|!' and keysym != 'plus':
                example_value = insert_in_example(example_value, '1+')
            else:
                example_value = insert_in_example(example_value, '+')
        elif keysym in ('slash', 'colon', 'semicolon'):
            if symbol_left_from_cursor() == '/' and keysym == 'slash':
                example_value = delete_in_example(example_value, -len(re.search(r'/\s*$', example_value[:cursor_index])[0]))
                example_value = insert_in_example(example_value, 'div')
            elif symbol_left_from_cursor() not in '0123456789φπeEvထ)|!' and keysym in ('semicolon', 'slash'):
                if keysym == 'semicolon':
                    example_value = insert_in_example(example_value, '(1/')
                    example_value = insert_in_example(example_value, ')', right=True)
                elif symbol_left_from_cursor() in '√•^':
                    example_value = insert_in_example(example_value, '2/')
                else:
                    example_value = insert_in_example(example_value, '1/')
            else:
                example_value = insert_in_example(example_value, '/')
        elif keysym == 'e':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'e', example_value)
        elif keysym == 'F':
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), 'φ', example_value)
        elif keysym in ('parenleft', 'bracketleft'):
            example_value = insertion_if_division_of_one(symbol_left_from_cursor(), '(', example_value)
        elif keysym == 'o':
            example_value = insert_in_example(example_value, f'{'/' if re.search(r'(?:[^0-9\.]|^)1$', exampled_value()[:cursor_index]) else '•' if symbol_left_from_cursor() in '0123456789φπeEvထ)!' else ''}(')
            example_value = insert_in_example(example_value, ')', right=True)
        elif keysym in ('parenright', 'bracketright'):
            example_value = insert_in_example(example_value, ')')
        elif keysym == 'numbersign':
            example_value = insert_in_example(example_value, '#')
        elif keysym.isdigit():
            last_keys_not_having_keytype_changed = list(filter(lambda key: key != 'changed', last_keys))
            if re.search(r'(?:[^0-9.]|^)\s*0\s*$', exampled_value(example_value)[:cursor_index]):
                example_value = insert_in_example(example_value, f'.{keysym}')
            elif symbol_left_from_cursor() in 'πφ)':
                example_value = insert_in_example(example_value, f'/{keysym}')
            elif re.search(fr'{num_construct}$', exampled_value()[:cursor_index]) and last_keys_not_having_keytype_changed[-1] in ('kMmBbTQ'):
                example_value = insert_in_example(example_value, f'•{keysym}')
            elif re.search(fr'{num_construct}•e$', exampled_value()[:cursor_index]) and last_keys_not_having_keytype_changed[-2] not in ('x', 'asterisk') and not re.search(fr'[Ee]-?{num_construct}•e$', exampled_value()[:cursor_index]):
                example_value = delete_in_example(example_value, -len(re.search(r'•\s*e\s*$', example_value[:cursor_index])[0]))
                example_value = insert_in_example(example_value, f'e{keysym}')
            elif re.fullmatch(r'(?:[^0-9veE.]|^\s*)1/e$', exampled_value()[max(cursor_index - 4, 0):cursor_index]) and last_keys_not_having_keytype_changed[-2] not in ('slash', 'colon', 'semicolon'):
                example_value = delete_in_example(example_value, -len(re.search(r'1\s*/\s*e\s*$', example_value[:cursor_index])[0]))
                example_value = insert_in_example(example_value, f'1e-{keysym}')
                if re.search(fr'(?:(?<=^)|(?<![\dφπeE]))\s*(?:\d+\.?\d*|\.\d+)•1[Ee]-{keysym}$', exampled_value()[:cursor_index]):
                    example_value = delete_in_example(example_value, -len(re.search(fr'•\s*1\s*[Ee]\s*-\s*{keysym}\s*$', example_value[:cursor_index])[0]))
                    example_value = insert_in_example(example_value, f'e-{keysym}')
            elif re.search(r'(?<![Eev])(?<![0-9.]e-)(?:\d+\.?\d*|\.\d+)/e$', exampled_value()[:cursor_index]) and last_keys_not_having_keytype_changed[-2] not in ('slash', 'colon', 'semicolon'):
                example_value = delete_in_example(example_value, -len(re.search(r'(?<=[0-9.])\s*/\s*e\s*$', example_value[:cursor_index])[0]))
                example_value = insert_in_example(example_value, f'e-{keysym}')
            elif symbol_left_from_cursor() == 'e':
                example_value = insert_in_example(example_value, keysym)
            elif symbol_left_from_cursor() == '!':
                example_value = insert_in_example(example_value, f'•{keysym}')
            else:
                example_value = insert_in_example(example_value, keysym)
        elif keysym == 'Left':
            for i in reunite(united_symbols_with_scopes + united_symbols):  # сначала united_symbols_withscopes и только потом united_symbols
                if (i_got_pattern := re.search(fr'\s*{i}\s*$', example_value[:cursor_index])):
                    cursor_index -= len(i_got_pattern[0])
                    break
            else:
                if (i_got_pattern := re.search(fr'(?: *[а-яА-ЯЁё]|^) *$', example_value[:cursor_index])):
                    cursor_index -= len(i_got_pattern[0])
                elif (i_got_pattern := re.search(fr'(?:\s*\S|^)\s*$', example_value[:cursor_index])):
                    cursor_index -= len(i_got_pattern[0])
        elif keysym == 'Right':
            for i in reunite(united_symbols_with_scopes + united_symbols):
                if (i_got_pattern := re.match(fr'\s*{i}', example_value[cursor_index:])):
                    cursor_index += len(i_got_pattern[0])
                    break
            else:
                if (i_got_pattern := re.match(fr'\s*(?:\S|$)', example_value[cursor_index:])):
                    cursor_index += len(i_got_pattern[0])
        elif keysym == 'Return':
            if settings['history type'] != 'history': 
                example_value = solve_example(example_value)
                cursor_index = len(example_value)
                keysym = 'dollar'
                keysym_char = '$'
        elif keysym == 'asciitilde':
            example_value = insert_in_example(example_value, 'q')
        elif keysym not in special_keys and len(keysym) == 1:
            example_value = insert_in_example(example_value, f'{keysym}')
        if not (keysym.isdigit() or keysym in ('minus', 'BackSpace', 'Delete')) and ('q' in example_value and keysym not in ('q', 'asciitilde') or example_value.count('q') ==  2):
            example_value, _, _, cursor_index, indexes_of_selection, _ = recents['last examples'][-1]
        if keysym != 'apostrophe':
            entry_box.insert(END, example_value)
        if keysym not in ('apostrophe', 'quotedbl'):
            calculate_result()
        if keysym not in ('grave', 'Return', 'Escape', 'apostrophe', 'quotedbl') and keysym_char != 'ё':
            add_to_last_examples_if_selection_or_cursor_change()

    recent_examples = recents['recent examples']
    difference2 = ''
    for i in range(-2, -len(recent_examples), -1):
        if ((len(recent_examples[i][0]) >= len(recent_examples[i - 1][0]) or
             re.search(r'[0-9φπe.]', recent_examples[i][0]) and not re.search(r'[0-9φπe.]', recent_examples[i - 1][0]) or
             'q' in recent_examples[i - 1][0] and 'q' not in recent_examples[i][0])
             and not ('q' in recent_examples[i - 1][0] and 'q' in recent_examples[i][0])):
            list_differ = [get_difference(old=recent_examples[-j][0], new=recent_examples[-j + 1][0]) for j in range(abs(i), 2, -1)]
            difference2 = ''.join((list_differ, reversed(list_differ))[keysym == 'BackSpace'])
            break
    diff_2sub1 = get_difference(old=recent_examples[-2][0], new=recent_examples[-1][0])
    difference1 = (difference2 + diff_2sub1, diff_2sub1 + difference2)[keysym == 'BackSpace']
    num_is_part_of_deleted = re.search(r'[0-9φπe.]', difference1) and not re.search(r'[0-9φπe.]', difference2)
    if added_win.title() == 'инструкция' and keysym_char:
        text_entry.tag_config('highlight', background=text_entry.tag_cget('sel', 'background'))
        highlight_all_words(text_entry, re.sub(r'[^\s0-9φπeа-яА-ЯЁё"\'«»“”()/•+a-zA-z-√|!^]', r'', example_value), 'highlight')

    if settings['history type'] == 'history' and (keysym in ('grave', 'Return', 'BackSpace', 'Delete', 'apostrophe', 'quotedbl') or
        keysym_char == 'ё' or num_is_part_of_deleted and is_num(recent_examples[-2][1], correct_answer_num_symbols)):
        indexes_of_selection = None
        perfect_ex_for_ans = ''
        if num_is_part_of_deleted and (keysym in ('Delete', 'BackSpace', 'grave', 'changed text') or keysym_char == 'ё'):
            perfect_ex_for_ans = recent_examples[-2][2]
        elif keysym in ('apostrophe', 'quotedbl', 'Return'):
            perfect_ex_for_ans = recent_examples[-1][2]

        for i in range(2):
            for j in range(-3, 0):
                if perfect_ex_for_ans[j:] in ending_symbols:
                    perfect_ex_for_ans = perfect_ex_for_ans[:j]
                    break
        perfect_ex_for_ans = clean_from_scopes_with_emptyness(perfect_ex_for_ans)
        
        split_old_history_of_calculations = history_of_calculations.split('\n')
        history_res = solve_example(perfect_ex_for_ans)
        rounding_in_history = ''
        if str(ROUND_ANSWER_TO_MANUALLY).strip('-').isdigit():
            manual_round_abs = abs(ROUND_ANSWER_TO_MANUALLY)
            num_of_ending_symbols = (0 < manual_round_abs % 10 < 5 and manual_round_abs // 10 != 1) + (manual_round_abs % 10 == 1 and manual_round_abs != 11)
            rounding_in_history = f' ({manual_round_abs} знак{('ов', 'а', '')[num_of_ending_symbols]} {('перед', 'после')[ROUND_ANSWER_TO_MANUALLY > 0]} запятой)'
        
        temporary_data_and_rounding = split_old_history_of_calculations[2]

        if perfect_ex_for_ans and (perfect_ex_for_ans != split_old_history_of_calculations[0] or (rounding_in_history not in temporary_data_and_rounding or '(' in temporary_data_and_rounding and rounding_in_history == '')):
            history_input = perfect_ex_for_ans
            if is_num(history_res, correct_answer_num_symbols) and history_res != history_input.replace(' ', ''):
                if keysym in ('Return', 'grave') or keysym_char == 'ё':
                    entry_box.delete(0, END)
                    entry_box.insert(END, str(history_res) if keysym == 'Return' else example_value)
                    example_value = entry_box.get()
                    cursor_index = entry_box.index('insert')
                value_to_add = [example_value, result.get().strip('='), perfect_example, cursor_index]
                value_to_add_plus = [example_value, clear_space_and_bracks_with_content(result.get().strip('=')) if example_value else '', '', cursor_index, indexes_of_selection if indexes_of_selection else None, settings['round']]
                if add_to_recents(example_value):
                    recents['recent examples'].append(value_to_add)
                if value_to_add_plus != recents['last examples'][-1]:
                    recents['last examples'].append(value_to_add_plus)
                if len(recents['last examples']) > 1000:
                    recents['last examples'].pop(0)
                if len(recents['recent examples']) > 100:
                    recents['recent examples'].pop(0)
                
                if history_input and added_win.title() in ('инструкция', 'история', invisible_win_title):
                    return_rounding_to_future_state_while_making_i_last_example_future()
                    return_rounding_to_future_state_while_making_i_history_future()
                    date_time = str(datetime.datetime.today())[:-7].replace('-', '.')
                    date_time_rounding = f'{date_time}{rounding_in_history}'
                    new_history = f'{perfect_example}\n{history_res}\n{date_time_rounding}\n\n{history_of_calculations}'
                    split0_history_of_calculations = new_history.split('\n')
                    
                    too_much_history_data = len(split0_history_of_calculations) > settings['history length']
                    history_of_calculations = '\n'.join(split0_history_of_calculations if not too_much_history_data else split0_history_of_calculations[:settings['history length']])
                    if added_win.title() == 'история':
                        try:
                            theme_is_light = settings['theme'] == 'light'
                            color1 = ('#' + 'b0' * 3, '#' + '2f' * 3)[theme_is_light]
                            color2 = ('#' + '90' * 3, '#' + '5f' * 3)[theme_is_light]
                            text_entry.insert(0.0, date_time_rounding + f'\n\n', f'history_{color2}')
                            text_entry.insert(0.0, history_res + '\n', f'history_{color1}')
                            text_entry.insert(0.0, perfect_example + '\n', f'history_{color1}')
                            for i in range(4):
                                text_entry.tag_add('highlight', f'{i + 1}.0', f'{i + 1}.end')
                            if too_much_history_data:
                                text_entry.delete(1.0, END)
                                tags = (None, f'history_{color1}', f'history_{color1}', f'history_{color2}')
                                [text_entry.insert(END, val + '\n', tags[(i + 1) % 4]) for i, val in enumerate(history_of_calculations.split('\n'))]
                                for i in range(history_of_calculations.count('\n') + 1):
                                    text_entry.tag_add('highlight', f'{i + 1}.0', f'{i + 1}.end')
                            text_entry.tag_add(SEL, '1.0', 'end')
                        except NameError:
                            pass
        elif keysym == 'Return':
            solve_res = solve_example(perfect_ex_for_ans)
            if is_num(solve_res, correct_answer_num_symbols):
                entry_box.delete(0, END)
                entry_box.insert(END, solve_res)
                example_value = entry_box.get()
                cursor_index = entry_box.index('insert')
            value_to_add = [example_value, result.get().strip('='), perfect_example, cursor_index]
            value_to_add_plus = [example_value, clear_space_and_bracks_with_content(result.get().strip('=')) if example_value else '', '', cursor_index, indexes_of_selection if indexes_of_selection else None, settings['round']]
            if add_to_recents(example_value):
                recents['recent examples'].append(value_to_add)
            if value_to_add_plus != recents['last examples'][-1]:
                recents['last examples'].append(value_to_add_plus)
            if len(recents['last examples']) > 1000:
                recents['last examples'].pop(0)
            if len(recents['recent examples']) > 100:
                recents['recent examples'].pop(0)
    
    last_keys.append(keysym)
    entry_box.icursor(cursor_index)
    if modify_info(example_value) is not None and keysym not in ('apostrophe', 'quotedbl'):
        calculate_result()
    can_backspace = entry_box.index('insert') != 0
    
    change_width_of_entry(entry_box.get(), entry_box, result)

    if keysym == 'Escape' or grave_destroy_win:
        close_main_win_with_layout_switching()

        
def supermanage_key_event(key, just_from_added_win=False):
    set_last_func_is_ctrl_shift_scroll(False)
    if hasattr(key, 'keysym') and key.keysym not in ('Escape', 'Tab', 'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Caps_Lock', 'Win_L'):
        set_del_mode(False)
    manage_key_event(key, just_from_added_win)
    if hasattr(key, 'keysym') and key.keysym not in ('apostrophe', 'quotedbl', 'Escape', 'Tab', 'Up', 'Down', 'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Caps_Lock', 'Win_L', 'y', 'z', 'Y', 'Z'):
        add_to_last_examples_if_selection_or_cursor_change()
        if tape and int(tape_canvas.cget('width')) == 0:
            destroy_tape()
        
        
def save_example_to_history(*key, example_to_save=None):
    global history_of_calculations, i_history, i_last_example, added_win, settings, example_value, cursor_index, can_backspace, indexes_of_selection, keyboard_layout_memory
    set_last_func_is_ctrl_shift_scroll(False)
    set_del_mode(False)
    indexes_of_selection = None
    perfect_ex_for_ans = (recents['recent examples'][-1][2], example_to_save)[example_to_save is not None]
    for i in range(2):
        for j in range(-3, 0):
            if perfect_ex_for_ans[j:] in ending_symbols:
                perfect_ex_for_ans = perfect_ex_for_ans[:j]
                break

    perfect_ex_for_ans = clean_from_scopes_with_emptyness(perfect_ex_for_ans)

    split_old_history_of_calculations = history_of_calculations.split('\n')
    history_res = solve_example(perfect_ex_for_ans)
    rounding_in_history = ''
    if str(ROUND_ANSWER_TO_MANUALLY).strip('-').isdigit():
        manual_round_abs = abs(ROUND_ANSWER_TO_MANUALLY)
        num_of_ending_symbols = (0 < manual_round_abs % 10 < 5 and manual_round_abs // 10 != 1) + (manual_round_abs % 10 == 1 and manual_round_abs != 11)
        rounding_in_history = f' ({manual_round_abs} знак{('ов', 'а', '')[num_of_ending_symbols]} {('перед', 'после')[ROUND_ANSWER_TO_MANUALLY > 0]} запятой)'

    temporary_data_and_rounding = split_old_history_of_calculations[2]

    if perfect_ex_for_ans and (perfect_ex_for_ans != split_old_history_of_calculations[0] or (rounding_in_history not in temporary_data_and_rounding or '(' in temporary_data_and_rounding and rounding_in_history == '')):
        history_input = perfect_ex_for_ans
        if is_num(history_res, correct_answer_num_symbols) and history_res != history_input.replace(' ', ''):
            value_to_add = [example_value, result.get().strip('='), perfect_example, cursor_index]
            value_to_add_plus = [example_value, clear_space_and_bracks_with_content(result.get().strip('=')) if example_value else '', '', cursor_index, indexes_of_selection if indexes_of_selection else None, settings['round']]
            if add_to_recents(example_value):
                recents['recent examples'].append(value_to_add)
            if value_to_add_plus != recents['last examples'][-1]:
                recents['last examples'].append(value_to_add_plus)
            if len(recents['last examples']) > 1000:
                recents['last examples'].pop(0)
            if len(recents['recent examples']) > 100:
                recents['recent examples'].pop(0)
            if history_input and added_win.title() in ('инструкция', 'история', invisible_win_title):
                return_rounding_to_future_state_while_making_i_last_example_future()
                return_rounding_to_future_state_while_making_i_history_future()
                date_time = str(datetime.datetime.today())[:-7].replace('-', '.')
                date_time_rounding = f'{date_time}{rounding_in_history}'
                new_history = f'{perfect_example}\n{history_res}\n{date_time_rounding}\n\n{history_of_calculations}'
                split0_history_of_calculations = new_history.split('\n')
                (entry_box.delete(0, END), entry_box.insert(END, 'Сохранено в историю'), change_width_of_entry(entry_box.get(), entry_box, result))
                main_win.after(after_tick_symbol_time, lambda: (entry_box.delete(0, END), entry_box.insert(END, example_value), change_width_of_entry(entry_box.get(), entry_box, result)))
                
                too_much_history_data = len(split0_history_of_calculations) > settings['history length']
                history_of_calculations = '\n'.join(split0_history_of_calculations if not too_much_history_data else split0_history_of_calculations[:settings['history length']])
                if added_win.title() not in (invisible_win_title, 'инструкция'):
                    try:
                        theme_is_light = settings['theme'] == 'light'
                        color1 = ('#' + 'b0' * 3, '#' + '2f' * 3)[theme_is_light]
                        color2 = ('#' + '90' * 3, '#' + '5f' * 3)[theme_is_light]
                        text_entry.insert(0.0, date_time_rounding + f'\n\n', f'history_{color2}')
                        text_entry.insert(0.0, history_res + '\n', f'history_{color1}')
                        text_entry.insert(0.0, perfect_example + '\n', f'history_{color1}')
                        for i in range(4):
                            text_entry.tag_add('highlight', f'{i + 1}.0', f'{i + 1}.end')
                        if too_much_history_data:
                            text_entry.delete(1.0, END)
                            tags = (None, f'history_{color1}', f'history_{color1}', f'history_{color2}')
                            [text_entry.insert(END, val + '\n', tags[(i + 1) % 4], 'highlight') for i, val in enumerate(history_of_calculations.split('\n'))]
                        text_entry.tag_add(SEL, '1.0', 'end')
                    except NameError:
                        pass


def insert_values_in_inputs_without_date(new_entry_box_value, new_result_value, date_time_rounding, symbol, new_cursor_index, new_indexes_of_selection, rounding_to='по умолчанию'):
    global example_value, cursor_index, can_backspace, indexes_of_selection
    entry_box.insert(END, new_entry_box_value)
    subbed_new_result_value = re.sub(r' ?\[.+\]', r'', new_result_value) if not re.search(r'\[.\]|\[[A-Z]?[a-z]{,9}\]', new_result_value) else new_result_value
    
    rounding_in_history = ''
    if str(rounding_to).strip('-').isdigit():
        manual_round_abs = abs(rounding_to)
        num_of_ending_symbols = (0 < manual_round_abs % 10 < 5 and manual_round_abs // 10 != 1) + (manual_round_abs % 10 == 1 and manual_round_abs != 11)
        rounding_in_history = f' ({manual_round_abs} знак{('ов', 'а', '')[num_of_ending_symbols]} {('перед', 'после')[rounding_to > 0]} запятой)'
    
    result.insert(END, f'{symbol}{subbed_new_result_value}{' ' * bool(subbed_new_result_value)}[{date_time_rounding}{rounding_in_history}]')
    
    example_value = re.sub(r'(?<=[\d.)])\s*e|e\s*(?=[\d.(])', 'E', entry_box.get().lower())
    cursor_index = entry_box.index('insert')
    indexes_of_selection = new_indexes_of_selection
    if type(new_cursor_index) is int:
        cursor_index = new_cursor_index
        entry_box.icursor(cursor_index)
    if type(indexes_of_selection) is dict:
        entry_box.select_range(*indexes_of_selection.values())
    can_backspace = cursor_index != 0
    
    
def insert_values_in_inputs(new_entry_box_value, new_result_value, date_time_rounding, symbol, new_cursor_index=None):
    global example_value, cursor_index, can_backspace, indexes_of_selection
    entry_box.insert(END, new_entry_box_value)
    date_time_rounding = re.sub(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', r'\3.\2.\1-\4:\5:\6', date_time_rounding)
    result.insert(END, f'{symbol}{re.sub(r' ?\[.+\]', r'', new_result_value) if not re.search(r'\[.\]|\[[A-Z]?[a-z]{,9}\]', new_result_value) else new_result_value} [{date_time_rounding}]')
    
    example_value = re.sub(r'(?<=[\d.)])\s*e|e\s*(?=[\d.(])', 'E', entry_box.get().lower())
    cursor_index = entry_box.index('insert')
    if type(new_cursor_index) is int:
        cursor_index = new_cursor_index
        entry_box.icursor(cursor_index)
    can_backspace = cursor_index != 0
    indexes_of_selection = None
    
    value_to_add = [example_value, result.get().strip('='), perfect_example, cursor_index]
    value_to_add_plus = [example_value, clear_space_and_bracks_with_content(result.get().strip('=')) if example_value else '', '', cursor_index, indexes_of_selection if indexes_of_selection else None, settings['round']]
    if add_to_recents(example_value):
        recents['recent examples'].append(['', calculator_greeting, '', 0, '', 'по умолчанию'])
        recents['recent examples'].append(value_to_add)
    if value_to_add_plus != recents['last examples'][-1]:
        recents['last examples'].append(value_to_add_plus)
    if len(recents['last examples']) > 1000:
        recents['last examples'].pop(0)
    while len(recents['recent examples']) > 100:
        recents['recent examples'].pop(0)


last_scroll_action_time = 0
# Глобальные переменные для отслеживания времени скролла
last_wheel_time = 0

def smart_accelerated_scroll(key):
    global last_wheel_time, tape_creation_time
    tape_creation_time = time.time()  # Продлеваем жизнь ленты
    
    current_time = time.time()
    time_delta = current_time - last_wheel_time
    last_wheel_time = current_time
    
    steps = 1
    
    # Смягчаем порог времени до 0.35 секунд. Если вы крутите колесико активнее, скорость увеличится до x3 без пропусков логики
    if time_delta < 0.35 and key.state & 0x0001:
        steps = 5
        
    if key.delta > 0:
        for _ in range(steps):
            ctrl_z()
    else:
        for _ in range(steps):
            ctrl_y()

        
def ctrl_y(*self):
    global i_history, i_last_example, last_example_value
    last_examples = recents['last examples']
    if i_last_example == 'future':
        return
    i_history = 'future'
    entry_box.delete(0, END)
    result.delete(0, END)
    if i_last_example == 'past':
        i_last_example = 0
        settings['round'] = last_examples[i_last_example][5]
        if not self or 'no drawing' not in self:
            insert_values_in_inputs_without_date(
                *last_examples[i_last_example][:2], f'{len(last_examples) - (i_last_example + 1)} действи{get_correct_ending(len(last_examples) - (i_last_example + 1), word_ends1)} назад',
                get_writing_form(re.sub(r' ?\[.+\]', r'', last_examples[i_last_example][1])), *last_examples[i_last_example][3:6])
    elif i_last_example < len(last_examples) - 2:
        i_last_example += 1
        settings['round'] = last_examples[i_last_example][5]
        if not self or 'no drawing' not in self:
            insert_values_in_inputs_without_date(
                *last_examples[i_last_example][:2], f'{len(last_examples) - (i_last_example + 1)} действи{get_correct_ending(len(last_examples) - (i_last_example + 1), word_ends1)} назад',
                get_writing_form(re.sub(r' ?\[.+\]', r'', last_examples[i_last_example][1])), *last_examples[i_last_example][3:6])
    else:
        return_rounding_to_future_state_while_making_i_last_example_future()
        solved_example = solve_example(last_example_value)
        insert_values_in_inputs_without_date(
            last_example_value, solved_example, 'Последний введённый пример', '=' if is_num(solved_example, correct_answer_num_symbols) else ' ' * bool(last_example_value),
            last_example_cursor, last_example_selection, ROUND_ANSWER_TO_MANUALLY)
    if i_last_example == 'future' or not self or 'no drawing' not in self:
        change_width_of_entry(entry_box.get(), entry_box, result)
        config_fg_and_insertbackground()
        create_tape()
        resize_and_retheme_canvas_drawings()
    if i_last_example == 'future':
        return 1
        
        
def ctrl_z(*self):
    global i_history, i_last_example, last_example_value, last_example_cursor, last_example_selection
    last_examples = recents['last examples']
    if i_last_example == 'past':
        return
    if i_last_example == 'future':
        last_example_cursor = cursor_index
        last_example_selection = indexes_of_selection
    entry_box.delete(0, END)
    result.delete(0, END)
    if i_last_example == 'future':
        if i_history == 'future':
            last_example_value = example_value
            settings['rounding in future state'] = settings['round']
        i_last_example = len(last_examples) - 2
        settings['round'] = last_examples[i_last_example][5]
        if not self or 'no drawing' not in self:
            insert_values_in_inputs_without_date(
                *last_examples[i_last_example][:2], f'{len(last_examples) - (i_last_example + 1)} действи{get_correct_ending(len(last_examples) - (i_last_example + 1), word_ends1)} назад',
                get_writing_form(re.sub(r' ?\[.+\]', r'', last_examples[i_last_example][1])), *last_examples[i_last_example][3:6])
    elif i_last_example > 0:
        i_last_example -= 1
        settings['round'] = last_examples[i_last_example][5]
        if not self or 'no drawing' not in self:
            insert_values_in_inputs_without_date(
                *last_examples[i_last_example][:2], f'{len(last_examples) - (i_last_example + 1)} действи{get_correct_ending(len(last_examples) - (i_last_example + 1), word_ends1)} назад',
                get_writing_form(re.sub(r' ?\[.+\]', r'', last_examples[i_last_example][1])), *last_examples[i_last_example][3:6])
    else:
        i_last_example = 'past'
        insert_values_in_inputs_without_date('Более ранняя история ваших действий не сохранилась!', 'Неизвестно, что было', 'Много действий назад', ' ', None, 'по умолчанию')
    i_history = 'future'
    if i_last_example == 'past' or not self or 'no drawing' not in self:
        change_width_of_entry(entry_box.get(), entry_box, result)
        config_fg_and_insertbackground()
        create_tape()
        resize_and_retheme_canvas_drawings()
    if i_last_example == 'past':
        return 1


last_func_is_ctrl_shift_scroll = False
def set_last_func_is_ctrl_shift_scroll(last_is_ctrl_shift_scroll=True):
    global last_func_is_ctrl_shift_scroll

    last_func_is_ctrl_shift_scroll = last_is_ctrl_shift_scroll
    if not is_window_ghost(added_win) and last_func_is_ctrl_shift_scroll:
        make_window_ghost(added_win)
    elif is_window_ghost(added_win) and not last_func_is_ctrl_shift_scroll:
        make_window_normal(added_win)
    else:
        pass

def set_del_mode(del_mode=True):
    global deletion_mode, cursor_shift_intermediate_steps_at_del_mode
    deletion_mode = del_mode
    if not del_mode:
        cursor_shift_intermediate_steps_at_del_mode = []


def get_rounding_num(rond_info):
    return (-1, 1)['после' in rond_info] * int(re.search(r'(\d+) знак', rond_info)[1]) if 'знак' in rond_info else 'по умолчанию'


close_history_after_scroll = None
def ctrl_shift_z(*self):
    global i_last_example, i_history, last_example_value, close_history_after_scroll
    if i_history == 'past':
        return 'break'
    if added_win.title() != 'история':
        create_added_win('h')
    entry_box.delete(0, END)
    result.delete(0, END)
    split_history_of_calculations = history_of_calculations.split('\n')
    if i_history == 'future':
        if i_last_example == 'future':
            last_example_value = example_value
            settings['rounding in future state'] = settings['round']
        i_history = highlight_i_history_text_and_centralize(0)
        settings['round'] = get_rounding_num(split_history_of_calculations[i_history + 2])
        insert_values_in_inputs(*split_history_of_calculations[i_history:i_history + 3], '=')
    elif i_history < len(history_of_calculations.split('\n')) - 4:
        i_history = highlight_i_history_text_and_centralize(i_history + 4)
        settings['round'] = get_rounding_num(split_history_of_calculations[i_history + 2])
        insert_values_in_inputs(*split_history_of_calculations[i_history:i_history + 3], '=')
    else:
        i_history = highlight_i_history_text_and_centralize('past')
        insert_values_in_inputs('В этом промежутке времени история вычислений была пустой!', 'Доисторический период', 'Время до первого запуска калькулятора', ' ')
    i_last_example = 'future'
    change_width_of_entry(entry_box.get(), entry_box, result)
    config_fg_and_insertbackground()
    # if close_history_after_scroll: added_win.after_cancel(close_history_after_scroll)
    # close_history_after_scroll = added_win.after(2000, manage_not_main_window_close)


def ctrl_shift_y(*self):
    global i_last_example, i_history, last_example_value, close_history_after_scroll
    if i_history == 'future':
        return 'break'
    if added_win.title() != 'история':
        create_added_win('h')
    i_last_example = 'future'
    entry_box.delete(0, END)
    result.delete(0, END)
    split_history_of_calculations = history_of_calculations.split('\n')
    if len(split_history_of_calculations) <= 5:
        return
    if i_history == 'past':
        i_history = highlight_i_history_text_and_centralize(len(split_history_of_calculations) - 4)
        if not split_history_of_calculations[i_history]:
            i_history = highlight_i_history_text_and_centralize(i_history + 1)
        settings['round'] = get_rounding_num(split_history_of_calculations[i_history + 2])
        insert_values_in_inputs(*split_history_of_calculations[i_history:i_history + 3], '=')
    elif i_history > 3:
        i_history = highlight_i_history_text_and_centralize(i_history - 4)
        settings['round'] = get_rounding_num(split_history_of_calculations[i_history + 2])
        insert_values_in_inputs(*split_history_of_calculations[i_history:i_history + 3], '=')
    else:
        return_rounding_to_future_state_while_making_i_history_future()
        solved_example = solve_example(last_example_value)
        insert_values_in_inputs(last_example_value, solved_example, 'Последний введённый пример', '=' if is_num(solved_example, correct_answer_num_symbols) else ' ' * bool(last_example_value))
    change_width_of_entry(entry_box.get(), entry_box, result)
    config_fg_and_insertbackground()
    # if close_history_after_scroll: added_win.after_cancel(close_history_after_scroll)
    # close_history_after_scroll = added_win.after(2000, manage_not_main_window_close)
    
    
def move_calculator_to_standard_positions():
    global main_win, entry_box, result, last_time_main_win_geometry_change, val_before_last_main_win_geometry_change
    main_win.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{settings['y']}')
    if not re.search(calc_geometry_state_change_expression, result.get()):
        val_before_last_main_win_geometry_change = result.get()
    result.delete(0, END)
    result.insert(END, f'{' ' * bool(example_value)}Калькулятор теперь {('внизу', 'в центре', 'вверху')[place_coords.index(settings['y'])]}')
    last_time_main_win_geometry_change = time.time()
    

def move_up(key):
    setting_y(recents['mid'] if recents['mid'] < settings['y'] else recents['top'] if settings['y'] != recents['top'] else recents['low'])
    move_calculator_to_standard_positions()


def move_to_edges(key):
    if settings['y'] not in (recents['top'], recents['low']):
        setting_y(recents[('top', 'low', ('top', 'low')[settings['y'] > recents['low'] // 2])[2 * (key.keysym == 'e') + (key.keysym == 'd')]])
    else:
        setting_y(recents[('top', 'low')[settings['y'] != recents['low']]])
    move_calculator_to_standard_positions()
    
    
def add_to_last_examples_if_selection_or_cursor_change():
    global last_keys
    if 'q' in example_value:
        return
    value_to_add_plus = [example_value, clear_space_and_bracks_with_content(result.get().strip('=')) if example_value else '', '', cursor_index, indexes_of_selection if indexes_of_selection else None, settings['round']]
    if value_to_add_plus != recents['last examples'][-1]:
        recents['last examples'].append(value_to_add_plus)
        last_keys.append('changed')
    if len(recents['last examples']) > 1000:
        recents['last examples'].pop(0)
    
    
def set_main_focus(event):
    global can_backspace, indexes_of_selection, cursor_index
    indexes_of_selection = get_selection()
    is_selected = False
    if main_win.focus_get() == result:
        result_selection = get_selection(result)
        is_selected = type(result_selection) is dict and result_selection['start'] != result_selection['end']
        if is_selected:
            temp_result_value = result.get()
            value_pre_copy = re.sub(r'E\(-(\d+)\)?', r'E-\1', temp_result_value[result_selection['start']:result_selection['end']].replace('•10^', 'E').replace('10^', '1E')).replace('•', '*').replace('ထ', 'inf')
            if value_pre_copy == '=' and result_selection['end'] == 1:
                pyperclip.copy(entry_box.get() + temp_result_value)
                result.delete(0, END)
                temp_entry_value = entry_box.get()
                entry_box.delete(0, END)
                entry_box.insert(END, '⮺ всё скопировано')
                main_win.after(after_tick_symbol_time, lambda: (entry_box.delete(0, END), entry_box.insert(END, temp_entry_value), result.delete(0, END), calculate_result(), change_width_of_entry(entry_box.get(), entry_box, result)))
            elif re.fullmatch(r'=[^Ee]+', value_pre_copy.replace('-', '')) and re.match(r'\s*\.?\s*\d', temp_result_value[result_selection['end']:]):
                raw_entry_box_ans = str(solve_example(entry_box.get(), get_raw_ans=True))
                raw_entry_box_ans_digits = (raw_entry_box_ans + '.0' * ('.' not in raw_entry_box_ans)).replace(' ', '').lstrip('-').strip('0').replace('.', '')
                value_pre_copy_digits = (value_pre_copy + '.0' * ('.' not in value_pre_copy)).replace(' ', '').lstrip('=-').strip('0').replace('.', '')
                if not value_pre_copy_digits:
                    value_pre_copy_digits = '0'
                if int(raw_entry_box_ans_digits[len(value_pre_copy_digits)]) >= 5:
                    value_pre_copy_digits = str(int(value_pre_copy_digits) + 1)

                digit_cnt = 0
                for indx in range(len(value_pre_copy) - 1, -1, -1):
                    if value_pre_copy[indx].isdigit():
                        digit_cnt += 1
                        if digit_cnt > len(value_pre_copy_digits):
                            break
                        value_pre_copy = f'{value_pre_copy[:indx]}{value_pre_copy_digits[-digit_cnt]}{value_pre_copy[indx + 1:]}'

                if digit_cnt == len(value_pre_copy_digits) - 1:
                    digit_cnt += 1
                    value_pre_copy = re.sub(r'^(=?-?)', r'\g<1>' + f'{value_pre_copy_digits[-digit_cnt]}', value_pre_copy)  # защита от слипания единичек в \11 (такой группы нет)
                    value_pre_copy = re.sub(r'(\d)(\d\d\d)', r'\1 \2', value_pre_copy)
                digit_amount_in_after_copy_range = len(re.findall(r'\d', temp_result_value[result_selection['end']:temp_result_value.find('.') if ('.' in temp_result_value) else len(temp_result_value)]))
                temp_result_value_E_modified = re.sub(r'E\(-(\d+)\)?', r'E-\1', temp_result_value.replace('•10^', 'E').replace('10^', '1E'))
                if '.' in value_pre_copy:
                    value_pre_copy = value_pre_copy.rstrip('0 ').rstrip('.')  # точку позже так как она вместе с нулем сотрется пред ней
                    if E_part := re.search(fr'E-?\d+', temp_result_value_E_modified):
                        value_pre_copy += E_part[0]
                else:
                    if E_part := re.search(fr'E(-?\d+)', temp_result_value_E_modified):
                        value_pre_copy += 'E' + str(int(E_part[1]) + digit_amount_in_after_copy_range)
                    else:
                        value_pre_copy += f'{digit_amount_in_after_copy_range % 3 * '0'}{(digit_amount_in_after_copy_range // 3) * ' 000'}'
                        value_pre_copy = value_pre_copy.replace(2 * ' ', ' ')
                value_pre_copy = value_pre_copy.replace('=', '')
                pyperclip.copy(value_pre_copy)
                result.delete(0, END)
                result.insert(END, f'≈{value_pre_copy} ⮺ скопировано с округлением')
                main_win.after(3 * after_tick_symbol_time, lambda: (result.delete(0, END), calculate_result()))
            else:
                value_pre_copy = value_pre_copy.replace('=', '')
                pyperclip.copy(value_pre_copy)
                result.delete(0, END)
                result.insert(END, temp_result_value[:result_selection['start']] + '⮺' + temp_result_value[result_selection['end']:])
                main_win.after(after_tick_symbol_time, lambda: (result.delete(0, END), calculate_result()))
            # main_win.after(tick_symbol_time, lambda: (result.delete(0, END), result.insert(END, temp_result_value[:result_selection['start']] + '✓' + temp_result_value[result_selection['end']:])))

            original_cursor_color = entry_box.cget('insertbackground')
            entry_box.config(insertbackground=entry_box.cget('bg'))
            main_win.after(after_tick_symbol_time, lambda: entry_box.config(insertbackground=original_cursor_color))
        entry_box.select_range(END, END)
        indexes_of_selection = None
        entry_box.icursor(END)
    entry_box.focus_set()
    if beauty_letter_tape:
        beauty_letter_tape.wm_attributes('-topmost', 1)
    cursor_index = entry_box.index('insert')
    can_backspace = cursor_index != 0

    if not is_selected:
        add_to_last_examples_if_selection_or_cursor_change()


def replace_abs_signs(val):
    val = f'({val})'
    for i in range(len(val) - 2):
        if val[i + 1] == '|':
            val = val[:i + 1] + 'Uu'[val[i] in '0123456789!)uπφeE' or bool(re.match(r'[+•/^!\)]|mod|div', val[i + 2:]))] + val[i + 2:]
    return val[1:-1]
    

cursor_shift_intermediate_steps_at_del_mode = []
def define_future_of_cursor(side):
    replaced_abs_value = replace_abs_signs(example_value)
    temp_cursor_index = max(0, cursor_index)
    text_token = (re.match(fr'\s*(?:(?:[0-9]*-)?{letters_and_not_example_like_inwords}+[0-9]*{syntax}*|{letters_and_inwords}*{syntax}+)', replaced_abs_value[temp_cursor_index:]),
                  re.search(fr'(?:(?:[0-9]*-)?{letters_and_not_example_like_inwords}+[0-9]*{syntax}*|{letters_and_inwords}*{syntax}+)\s*$', replaced_abs_value[:temp_cursor_index]))[side == 'left']
    
    i = len(text_token[0]) if text_token is not None and text_token[0] not in ('-', '/', '!') else None
    if side in ('right', 'left') and i:
        temp_cursor_index += (i, -i)[side == 'left']
        return temp_cursor_index
    elif side == 'right':
        i = len(re.match(r'q.*#|q*', replaced_abs_value[temp_cursor_index:])[0])
        if i:
            temp_cursor_index += i
            return temp_cursor_index
        temp_cursor_index += len(re.match(r'(?:[+\-•/:^√!= ]|mod|div)*(?:(?:\)\s*)*\s*b\s*y)?', replaced_abs_value[temp_cursor_index:])[0])
        i = len(re.match(r'(?:\)|u|\])*', replaced_abs_value[temp_cursor_index:])[0])
        temp_cursor_index += i
        if i < 2:
            temp_cursor_index += len(re.match(r'(?:[+\-•/:^√!= ]|mod|div)*', replaced_abs_value[temp_cursor_index:])[0])
        if re.match(r'log', replaced_abs_value[temp_cursor_index:]):
            for i in range(3, len(replaced_abs_value[temp_cursor_index:]) + 1):
                if len(re.findall(r'l\s*o\s*g', replaced_abs_value[temp_cursor_index:temp_cursor_index + i])) == len(re.findall(r'b\s*y', replaced_abs_value[temp_cursor_index:temp_cursor_index + i])):
                    break
            temp_cursor_index += i
        temp_cursor_index += len(re.match(r'(?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)?|ln|lg|by|', replaced_abs_value[temp_cursor_index:])[0])
        if replaced_abs_value[temp_cursor_index:temp_cursor_index + 1] in list('U(['):
            nxt_scope = replaced_abs_value[temp_cursor_index:temp_cursor_index + 1]
            open_brack, closed_brack = nxt_scope, 'u)]'[(nxt_scope == '(') + 2 * (nxt_scope == '[')]
            for i in range(1, len(replaced_abs_value[temp_cursor_index:]) + 1):
                if replaced_abs_value[temp_cursor_index:temp_cursor_index + i].count(open_brack) == replaced_abs_value[temp_cursor_index:temp_cursor_index + i].count(closed_brack):
                    break
            temp_cursor_index += i
            return temp_cursor_index
        
        temp_cursor_index += len(a := re.match(r'v\d*|\d*\.?\d*(?:[Ee]-?\d*\.?\d*)?|[φπe]', replaced_abs_value[temp_cursor_index:])[0])
        return temp_cursor_index
    
    elif side == 'left':
        i = len(re.search(r'(?:q.*|q?)$', replaced_abs_value[:temp_cursor_index])[0])
        if i:
            temp_cursor_index -= i
            return temp_cursor_index
        temp_cursor_index -= len(re.search(r'(?:[+\-•/:^√!= ]|mod|div)*$', replaced_abs_value[:temp_cursor_index])[0])
        i = len(re.search(r'(?:\(|U|\[)*$', replaced_abs_value[:temp_cursor_index])[0])
        temp_cursor_index -= i
        if i < 2:
            temp_cursor_index -= len(re.search(r'(?:[+\-•/:^√!= ]|mod|div)*$', replaced_abs_value[:temp_cursor_index])[0])
        if replaced_abs_value[temp_cursor_index - 1:temp_cursor_index] in list('u)]'):
            prv_scope = replaced_abs_value[temp_cursor_index - 1:temp_cursor_index]
            open_brack, closed_brack = 'U(['[(prv_scope == ')') + 2 * (prv_scope == ']')], prv_scope
            for i in range(len(replaced_abs_value[:temp_cursor_index]) - 1, -1, -1):
                if replaced_abs_value[i:temp_cursor_index].count(open_brack) == replaced_abs_value[i:temp_cursor_index].count(closed_brack):
                    break
            temp_cursor_index = i

        else:
            temp_cursor_index -= len(re.search(r'(?:(?<![a-df-uw-zA-DF-UW-Z])v\d*|\d*\.?\d*(?:[Ee]-?\d*\.?\d*)?|[φπe])$', replaced_abs_value[:temp_cursor_index])[0])
            if re.search(r'(?:\(|U|\[|^)-$', replaced_abs_value[:temp_cursor_index]):
                temp_cursor_index -= 1
        temp_cursor_index -= len(re.search(r'(?:(?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)?|ln|lg|)$', replaced_abs_value[:temp_cursor_index])[0])
        if re.search(r'by$', replaced_abs_value[:temp_cursor_index]):
            for i in range(len(replaced_abs_value[:temp_cursor_index]) - 2, -1, -1):
                if replaced_abs_value[i:temp_cursor_index].count('log') == replaced_abs_value[i:temp_cursor_index].count('by'):
                    break
            temp_cursor_index = i
        if re.search(r'log$', replaced_abs_value[:temp_cursor_index]):
            temp_cursor_index -= 3
        return temp_cursor_index
    
def set_cursor_to_the(key, start_or_end_or_num):
    global can_backspace, indexes_of_selection, cursor_index
    if 'q' in example_value:
        return
    make_it_future()
    if type(start_or_end_or_num) is str:
        entry_box.icursor((0, END)[start_or_end_or_num == 'end'])
    else:
        entry_box.icursor(start_or_end_or_num)
    indexes_of_selection = None
    cursor_index = entry_box.index('insert')
    can_backspace = cursor_index != 0
    
    add_to_last_examples_if_selection_or_cursor_change()
    
    
def set_cursor_shift_to_the(key, side_or_num, text_will_be_changed=False):
    global indexes_of_selection, cursor_index
    if 'q' in example_value:
        return
    make_it_future()

    if type(side_or_num) is str:
        is_right_side = side_or_num == 'right'
        for i in reunite(united_symbols):
            if (i_got_pattern := (re.search, re.match)[is_right_side]((fr'{i}\s*$', fr'\s*{i}')[is_right_side], (entry_box.get()[:cursor_index], entry_box.get()[cursor_index:])[is_right_side])):
                i = len(i_got_pattern[0])
                break
        else:
            if (i_got_pattern := (re.search(fr'(?:\s*\S|^)\s*$', example_value[:cursor_index]), re.match(fr'\s*(?:\S|$)', example_value[cursor_index:]))[is_right_side]):
                i = len(i_got_pattern[0])
        i = (-i, i)[side_or_num == 'right']
        new_cursor_index = cursor_index + i
    else:
        new_cursor_index = side_or_num
    if new_cursor_index not in range(len(entry_box.get()) + 2):
        new_cursor_index = (cursor_index, 0)[new_cursor_index < 0]
    if type(indexes_of_selection) is not dict:
        entry_box.select_range(*((new_cursor_index, cursor_index) if new_cursor_index < cursor_index else (cursor_index, new_cursor_index)))
    else:
        if new_cursor_index < indexes_of_selection['start']:
            entry_box.select_range(new_cursor_index, indexes_of_selection['end'])
        elif new_cursor_index > indexes_of_selection['end']:
            entry_box.select_range(indexes_of_selection['start'], new_cursor_index)
        else:
            entry_box.select_range(*((indexes_of_selection['start'], new_cursor_index) if new_cursor_index < cursor_index else (new_cursor_index, indexes_of_selection['end'])))
    entry_box.icursor(new_cursor_index)
    cursor_index = entry_box.index('insert')
    indexes_of_selection = get_selection()
    
    if not text_will_be_changed:
        add_to_last_examples_if_selection_or_cursor_change()
    

def set_cursor_shift_to_the_edge(key, start_or_end):
    global indexes_of_selection, cursor_index
    if type(start_or_end) is str:
        new_cursor_index = (0, len(entry_box.get()))[start_or_end == 'end']
    else:
        new_cursor_index = start_or_end
    if type(indexes_of_selection) is not dict:
        indexes_of_selection = {'start': cursor_index, 'end': cursor_index}
    has_edges = indexes_of_selection['start'] == 0 or indexes_of_selection['end'] == len(entry_box.get())
    entry_box.select_range(*((new_cursor_index, indexes_of_selection[('end', 'start')[has_edges]]) if start_or_end == 'start' or new_cursor_index < cursor_index else (indexes_of_selection[('start', 'end')[has_edges]], new_cursor_index)))
    entry_box.icursor(new_cursor_index)
    cursor_index = entry_box.index('insert')
    indexes_of_selection = get_selection()
    
    add_to_last_examples_if_selection_or_cursor_change()
    

def select_all(key):
    global indexes_of_selection, cursor_index
    cursor_index = len(entry_box.get())
    entry_box.select_range(0, cursor_index)
    entry_box.icursor(cursor_index)
    indexes_of_selection = get_selection()
    
    add_to_last_examples_if_selection_or_cursor_change()
 

def copy_text(key):
    global indexes_of_selection, cursor_index, example_value, i_last_example
    if type(indexes_of_selection) is dict:
        if indexes_of_selection['start'] == indexes_of_selection['end']:
            indexes_of_selection = None
        else:
            pyperclip.copy(example_value[indexes_of_selection['start']:indexes_of_selection['end']].replace('•', '*').replace('ထ', 'inf'))
        
        
def cut_text(key):
    global indexes_of_selection, example_value, can_backspace
    if type(indexes_of_selection) is dict and indexes_of_selection['start'] == indexes_of_selection['end']:
        indexes_of_selection = None
    if type(indexes_of_selection) is not dict:
        return
    pyperclip.copy(example_value[indexes_of_selection['start']:indexes_of_selection['end']].replace('•', '*').replace('ထ', 'inf'))
    change_text('')


def replace_paste_symbols(string):
    return string.replace('x', '•').replace('*', '•').replace('inf', 'ထ').replace('∞', 'ထ').replace('–', '-').replace('–', '-').replace('×', '•').replace('−', '-').replace('⋅', '•').replace('••', '^').replace(' ', ' ')


def get_alternate_log_var(pasted_log_val):
    while re.search(r'\(([^()]*)\)', pasted_log_val):
        old_pasted_log_val = pasted_log_val
        pasted_log_val = re.sub(r'log\(([^()]*)\)by\(([^()]*)\)', r'log&@@&@@\2@&&@&&by&@@&@@\1@&&@&&', pasted_log_val)
        pasted_log_val = re.sub(r'(?<!by)(?<!log)\(([^()]*)\)', r'&@@&@@\1@&&@&&', pasted_log_val)
        if old_pasted_log_val == pasted_log_val:
            return 'непарность скобок мешает вставке логарифма! ' + pasted_log_val.replace('(', '<').replace(')', '>').replace('&@@&@@', '(').replace('@&&@&&', ')')

    return pasted_log_val.replace('&@@&@@', '(').replace('@&&@&&', ')')

# def modified_pasted_logarythm(log_string, alter=False):  # недоработана и бесит багами
#     func_construct = r'(?:\s*(?:(?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)?|ln+|lg+|√+|))'
#     func_construct_no_empt = r'(?:\s*(?:(?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)+|(?:(?<!mo)d(?!iv))?arc|(?:(?<!mo)d(?!iv))|ln+|lg+|√+))'

#     log_string = re.sub(r';', r')by(', log_string)
#     old_log_string = None
#     while old_log_string != log_string:
#         scope_not_ended_flag = False
#         old_log_string = log_string
#         for i in range(len(log_string)):
#             if a := re.search(r'log(.*)by$', log_string[:i]):
#                 if not re.search(r'[()]', a[1]):
#                     break
#                 scope_cnt = 0
#                 for indx, j in enumerate(a[1]):
#                     if j in '()':
#                         scope_cnt += (-1, 1)[j == '(']
#                     if scope_cnt == 0 and re.search(r'\S', a[1][indx + 1:]) and re.search(r'[()]', a[1][:indx + 1]) or not re.search(r'\s*\(', a[1][:indx + 1]):
#                         log_string = re.sub(fr'log({re.escape(a[1])})by', r'log(\1)by', log_string)
#                         scope_not_ended_flag = True
#                         break
#             if scope_not_ended_flag:
#                 break

#     log_string = re.sub(r';', ')by(', log_string)
#     log_string = re.sub(fr'log({func_construct_no_empt})\(([^;()]*)\)', r'log(\1&@@&@@\2@&&@&&)', log_string)
#     log_string = re.sub(fr'(?:(?:by|base)({func_construct_no_empt})\()([^;()]*)\)', r'by(\1&@@&@@\2@&&@&&)', log_string)
#     log_string = re.sub(fr'log\(([^;()]*)(?:\)(?:by|base)\()([^;()]*)\)', (r'log&@@&@@\1@&&@&&by&@@&@@\2@&&@&&', r'log&@@&@@\2@&&@&&by&@@&@@\1@&&@&&')[alter], log_string) 
#     log_string = re.sub(r'&@@&@@(\s*)\((.*?)\)(\s*)@&&@&&', r'&@@&@@\1\2\3@&&@&&', log_string)
    
#     log_string = re.sub(fr'log\s*{num_construct_with_spaces}\s*\(([^;()]*?)\)', r'log&@@&@@\2@&&@&&by&@@&@@\1@&&@&&', log_string)
#     a = re.finditer(fr'\([^();]*\)', log_string)
#     b = re.finditer(fr'(?:log(?:\s*{num_construct_with_spaces})?\s*\([^();]*\)|log\s*\(([^();]*)\)\s*by|by\s*\(([^();]*)\)\s*)', log_string)
#     for indx_i, i in enumerate(a):
#         if not any(i.start() >= j.start() and i.end() <= j.end() for j in b):
#             log_string = log_string[:i.start()] + f'<{log_string[i.start() + 1:i.end() - 1]}>' + log_string[i.end():]
#     log_string = log_string.replace('<', '&@@&@@').replace('>', '@&&@&&')
#     return log_string


def paste_text(*key):
    global indexes_of_selection, cursor_index, can_backspace, example_value
    if indexes_of_selection is None:
        indexes_of_selection = {'start': cursor_index, 'end': cursor_index}

    replaced_paste = re.sub(r'E0+(\d)', r'E\1', pyperclip.paste().replace('E+', 'E').replace('#', '')).replace('E', '#').lower().replace('#', 'E')

    if re.search(r'2\d{3}\.(?:0\d|11|12)\.(?:[0-3]\d|31) (?:[01]\d|2[0-3])(?::[0-5]\d){2}', replaced_paste):
        # Алгоритм замены для истории
        
        replaced_paste = re.sub(r'\n', '&', replaced_paste)
        replaced_paste = re.sub(r' ', '#', replaced_paste)
        replaced_paste = re.sub(r'\s', '', replaced_paste)
        replaced_paste = re.sub(r'&&', ', ', replaced_paste)
        replaced_paste = re.sub(r'&(2\d{3}\.(?:0\d|11|12)\.(?:[0-3]\d|31))#((?:[01]\d|2[0-3])(?::[0-5]\d){2})(?:#(\(\d{1,2})#(знак(?:|а|ов))#(перед|после)#(запятой\)))?', r' [\1 \2 \3 \4 \5 \6]', replaced_paste).replace(4 * ' ', '')
        replaced_paste = ', '.join((i.replace('&', '=', 1) for i in replaced_paste.split(', ')))
        replaced_paste = replaced_paste.replace('&', ' ')
        replaced_paste = re.sub(r'#', '', replaced_paste)
    elif re.search(r'\t|.+\n.+', replaced_paste):
        replaced_paste = [re.sub(r'\t{2,}', r'\t', i).strip('\t') for i in replaced_paste.splitlines() if i]
        replaced_paste = [i.strip('\t').split('\t') if i.strip('\t').count('\t') else [i] for i in replaced_paste]

        for index1, item1 in enumerate(replaced_paste):
            for index2, item2 in enumerate(item1):
                item2 = item2.replace(' ', '')
                while re.search(r'[а-яА-ЯЁё\s]+', item2):
                    item2 = re.sub(r'[а-яА-ЯЁё\s]+', r'', item2)
                item2 = re.sub(fr'({num_construct})(?:radical|root|r)', r'\1#√', item2)
                for i in (('sqrt', '√'), ('cbrt', '3#√')):
                    item2 = re.sub(fr'({num_construct}){i[0]}', fr'\1•{i[1]}', item2)
                item2 = re.sub(r'radical|root|sqrt|cbrt|(?<!a)r(?!c)', r'√', item2)
                item2 = item2.replace('pi', 'π').replace('fi', 'φ')

                item2 = item2.replace('tan', 'tg').replace('cot', 'ctg')
                item2 = re.sub(r'a(sin|cos|c?tg)', r'arc\1', item2)
                item2 = re.sub(fr'({num_construct})%([0-9φπe.(]|sin|cos|c?tg|ln|lg|log|√)', r'\1/100•\2', item2)
                item2 = re.sub(fr'({num_construct})%', r'\1/100', item2)
                item2 = re.sub(r' {2,}', r' ', item2.replace('÷', '/').replace(':', '/').replace('//', 'div').replace('%', 'mod'))
                item2 = re.sub(r' ?([^0-9\.]) ?', r'\1', item2)

                while re.search(a := r'\(([^()]*)\)', item2):
                    old_cycle_step_item2 = item2
                    item2 = re.sub(r'log\(([^;()]*)(?:;|\)by\(|\)base\()([^;()]*)\)', r'log&@@&@@\1@&&@&&by&@@&@@\2@&&@&&', item2)
                    item2 = re.sub(fr'log{num_construct}\(([^()]*)\)', r'log&@@&@@\2@&&@&&by&@@&@@\1@&&@&&', item2)
                    item2 = re.sub(r'(?<!by)(?<!log)\(([^()]*)\)', r'&@@&@@\1@&&@&&', item2)
                    if old_cycle_step_item2 == item2:
                        item2 = 'ошибка вставки! ' + item2.replace('(', '<').replace(')', '>').replace('&@@&@@', '(').replace('@&&@&&', ')')
                        break
                item2 = item2.replace('&@@&@@', '(').replace('@&&@&&', ')') # log(2+log(25)by(5);log100(15+(log4(1/64)+log8(64))*(5+5))+log(r69;69))
                item2 = item2.replace('base', 'by')  # log(log100(15+(log4(1/64)+log8(64))*(5+5))+log(69;r69);2+log(5)by(25))

                # item2 = re.sub(r'(?<=[0-9φπeထ)!])E', r'•10^', item2)
                # item2 = re.sub(r'(?<=[^√])E', r'1•10^', item2).replace('E', '•10^')
                
                item2 = re.sub(r'((?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)?|ln|lg|log)(\d+\.?\d*|\.\d+)(\()', r'\1#\2#\3', item2)
                while re.search(mul_between_digits_and_constants := r'([φπe\)])([0-9φπe\.\(])', item2):
                    item2 = re.sub(mul_between_digits_and_constants, r'\1•\2', item2)
                while re.search(mul_between_digits_and_constants := r'([0-9φπe\.\)])([φπe\(]|d(?!iv)|arc|sin|cos|c?tg|ln|lg|log)', item2):
                    item2 = re.sub(mul_between_digits_and_constants, r'\1•\2', item2)
                item2 = re.sub(r'(\d)√', r'\1•√', item2)
                i = item2.replace('#', '')
                insert_in_example(example_value, '•10^' if symbol_left_from_cursor() in '0123456789φπeထ)!' else '1•10^' if symbol_left_from_cursor() in '^√' else '10^')

                if i == f'|{i[1:-1]}|':  # допустим максимум 2-й уровень вложенности, чтобы зрение читателя не запуталось, иначе обернётся в скобки, подсказывая ему, как правильно поступить
                    value = replace_abs_signs(value)
                    replaced_paste[index1][index2] = (f'({i})', i)[re.fullmatch(r'U(?:Uu)*u', re.sub(r'[^Uu]', '', value)) is not None]
                else:
                    replaced_paste[index1][index2] = (f'({i})', i)[re.fullmatch(fr'{num_construct}|\(-?{num_construct}\)', i) is not None]

        for index1, item1 in enumerate(replaced_paste):
            for index2, item2 in enumerate(item1):
                if not re.search(r'[а-яА-ЯЁё]', item2):
                    replaced_paste[index1][index2] = replace_paste_symbols(replaced_paste[index1][index2])

        if len(set(list(map(len, replaced_paste)))) == 1 and re.search(r'(?<!di)v', example_value):
            table_data_size = {1: len(replaced_paste[0]), 0: len(replaced_paste)}  # 1 - width, 0 - height (for comftable boolean logic work)
            prior_side = table_data_size[1] > table_data_size[0]
            if not f'v{table_data_size[prior_side]}' in example_value:
                prior_side = not prior_side
            copied_results = []
            old_examp_val = example_value
            for item1 in (zip(*replaced_paste), replaced_paste)[prior_side]:
                example_value = re.sub(r'(?<!di)v(?!\d)', 'v1', example_value)
                for index2, item2 in enumerate(item1):
                    # if re.fullmatch(num_construct, item2) is None: item2 = f'({item2})'
                    example_value = re.sub(fr'(?<!di)v{index2 + 1}', item2, example_value)
                cursor_index = len(example_value)
                make_it_future()
                if settings['history type'] == 'history':
                    save_example_to_history()
                copied_results.append(result.get().replace('=', ''))
                new_examp_val = example_value
                example_value = old_examp_val
            example_value = new_examp_val

            for indx, copied_res in enumerate(copied_results):
                copied_res = copied_res.replace('•10^', 'e').replace('10^', '1e').replace(' ', '')
                copied_res = copied_res.split('e')
                if len(copied_res) > 1:
                    copied_res[1] = copied_res[1].replace('(', '').replace(')', '')

                print(copied_res[0])
                if 0 < abs(float(copied_res[0])) < 1 and len(copied_res) == 1:
                    copied_res[0] = re.search(r'-?\d*\.0*\d{,3}', copied_res[0])[0]
                    if re.search(r'-?\d*\.0*[1-9]\d[1-9]', copied_res[0]):
                        copied_res[0] = copied_res[0][:-3] + str(Decimal('0.' + copied_res[0][-3:]).quantize(Decimal('.00'), ROUND_HALF_UP))[2:]  # не округляет децимал пред запятой, идиот он
                    copied_res[0] = copied_res[0].rstrip('0')
                else:
                    copied_res[0] = str(Decimal(copied_res[0]).quantize(Decimal('.00'), ROUND_HALF_UP))
                if copied_res[0][-3:] in ('.00', ',00'):
                    copied_res[0] = copied_res[0][:-3]
                    
                copied_results[indx] = 'E'.join(copied_res)
                if 'E' not in copied_results[indx] and abs(float(copied_results[indx])) >= 10 ** 15:
                    copied_results[indx] = f'{float(copied_results[indx]):.2e}'.replace('e+', 'E')
            pyperclip.copy(('\t', '\n')[prior_side].join(copied_results))
            return

        matrix_1x1 = [[replaced_paste[0][0]]] == replaced_paste
        replaced_paste = [f'({'+'.join([item2 for item2 in item1])})' if len(item1) > 1 else item1[0] for item1 in replaced_paste]
        
        replaced_paste = ('+' * (cursor_index > 0 and symbol_left_from_cursor() in '0123456789φπeEvထ)!.') + '(' * (not matrix_1x1) +
                          ('+'.join(replaced_paste) if len(replaced_paste) > 1 else replaced_paste[0][1:-1] if not matrix_1x1 else replaced_paste[0]) +
                          ')' * (not matrix_1x1) + '+' * (cursor_index < len(example_value) and symbol_right_from_cursor() in '0123456789φπeEvထ(√.'))
        
        change_text(replaced_paste)
        return 'break'
    else:
        replaced_paste = re.sub(r' ', '#', replaced_paste)
        replaced_paste = re.sub(r'\s', '', replaced_paste)
        replaced_paste = re.sub(r'#', ' ', replaced_paste)
        if not re.search(r'[а-яА-ЯЁё]', replaced_paste):
            replaced_paste = re.sub(fr'({num_construct_with_spaces})\s*(?:radical|root|r)', r'\1#√', replaced_paste)
            for i in (('sqrt', '√'), ('cbrt', '3#√')):
                replaced_paste = re.sub(fr'({num_construct_with_spaces})\s*{i[0]}', fr'\1•{i[1]}', replaced_paste)
            replaced_paste = re.sub(r'radical|root|sqrt|cbrt|(?!a)r(?!c)', r'√', replaced_paste)
            replaced_paste = replaced_paste.replace('pi', 'π').replace('fi', 'φ')
            
            replaced_paste = replaced_paste.replace('tan', 'tg').replace('cot', 'ctg')
            replaced_paste = re.sub(r'a(sin|cos|c?tg)', r'arc\1', replaced_paste)
            replaced_paste = re.sub(fr'({num_construct_with_spaces})\s*%\s*([0-9φπeE.(]|d(?!i)|arc|sin|cos|c?tg|ln|lg|log|√)', r'\1/100•\2', replaced_paste)
            replaced_paste = re.sub(fr'({num_construct_with_spaces})\s*%', r'\1/100', replaced_paste)
            replaced_paste = re.sub(r' {2,}', r' ', replaced_paste.replace('÷', '/').replace(':', '/').replace('//', 'div').replace('%', 'mod'))
            replaced_paste = re.sub(r' ?([^0-9\.]) ?', r'\1', replaced_paste)

            while re.search(a := r'\(([^()]*)\)', replaced_paste):
                old_cycle_step_replaced_paste = replaced_paste
                replaced_paste = re.sub(r'log\(([^;()]*)(?:;|\)by\(|\)base\()([^;()]*)\)', r'log&@@&@@\1@&&@&&by&@@&@@\2@&&@&&', replaced_paste)
                replaced_paste = re.sub(fr'log{num_construct_with_spaces}\s*\(([^;()]*)\)', r'log&@@&@@\2@&&@&&by&@@&@@\1@&&@&&', replaced_paste)
                replaced_paste = re.sub(r'(?<!by)(?<!log)\(([^();]*)\)', r'&@@&@@\1@&&@&&', replaced_paste)
                if old_cycle_step_replaced_paste == replaced_paste:
                    replaced_paste = 'ошибка вставки! ' + replaced_paste.replace('(', '<').replace(')', '>').replace('&@@&@@', '(').replace('@&&@&&', ')')
                    break

            replaced_paste = re.sub(r'log\(([^;()]*)(?:;|\)by\(|\)base\()([^;()]*)\)', r'log&@@&@@\1@&&@&&by&@@&@@\2@&&@&&', replaced_paste)
            replaced_paste = re.sub(fr'log{num_construct_with_spaces}\(([^;()]*)\)', r'log&@@&@@#log(2;log100(15+(log4(1/64)+log8(64))*(5+5))+log(r69;69))\2@&&@&&by&@@&@@\1@&&@&&', replaced_paste) #log(log100(15+(log4(1/64)+log8(64))*(5+5))+log(69;r69);2)
            replaced_paste = replaced_paste.replace('&@@&@@', '(').replace('@&&@&&', ')') #log(2;log100(15+(log4(1/64)+log8(64))*(5+5))+log(r69;69))
            replaced_paste = replaced_paste.replace('base', 'by')

            # replaced_paste = re.sub(r'(?<=[0-9φπeထ)!])E', '•10^', replaced_paste)
            # replaced_paste = re.sub(r'(?<=[^√])E', '1•10^', replaced_paste).replace('E', '•10^')
            replaced_paste = re.sub(r'((?:(?<!mo)d(?!iv))?(?:arc)?(?:sin|cos|c?tg)?|ln|lg|log)(\d+\.?\d*|\.\d+)(\()', r'\1#\2#\3', replaced_paste)
            while re.search(mul_between_digits_and_constants := r'([φπe\)])([0-9φπe\.\(])', replaced_paste):
                replaced_paste = re.sub(mul_between_digits_and_constants, r'\1•\2', replaced_paste)
            while re.search(mul_between_digits_and_constants := r'([0-9φπe\.\)])([φπe\(]|d(?!i)|arc|sin|cos|c?tg|ln|lg|log)', replaced_paste):
                replaced_paste = re.sub(mul_between_digits_and_constants, r'\1•\2', replaced_paste)
            # print(replaced_paste)
            replaced_paste = re.sub(r'(\d)√', r'\1•√', replaced_paste)
            replaced_paste = replaced_paste.replace('#', '')

    if not re.search(r'[а-яА-ЯЁё]', replaced_paste):
        replaced_paste = replace_paste_symbols(replaced_paste)
    start, end = change_text(replaced_paste)
    if 'log' in replaced_paste:
        create_tape('info', f'{re.sub(fr'{re.escape(replaced_paste)}$', get_alternate_log_var(replaced_paste), example_value[:cursor_index])}{example_value[cursor_index:]}' + ' – нажми меня, чтобы поменять местами аргументы логарифмов')
    return 'break'

    
def change_text(pasted, start=None, end=None):
    global indexes_of_selection, cursor_index, can_backspace, example_value
    
    make_it_future()
    if start is None:
        start = indexes_of_selection['start']
    if end is None:
        end = indexes_of_selection['end']
    example_value = example_value[:start] + pasted + example_value[end:]
    cursor_index = start + len(pasted)
    indexes_of_selection = None
    can_backspace = cursor_index != 0
    manage_key_event((cursor_index, end), False)

    example_value = re.sub(r'(?<![\d.)])\s*E', 'e', example_value)
    example_value = re.sub(r'(?<=[\d.)])\s*e|e\s*(?=[\d.(])', 'E', example_value)
    add_to_last_examples_if_selection_or_cursor_change()
    return start, end
    
    
def change_selection_colors_to_normal(theme_is_light):
    entry_box.config(insertbackground=('#e0e0e0', '#1f1f1f')[theme_is_light], selectforeground=entry_box.cget('fg'), selectbackground=('#' + '50' * 3, '#' + 'ab' * 3)[theme_is_light])
    result.config(insertbackground=entry_box.cget('insertbackground'), selectforeground=entry_box.cget('fg'), selectbackground=entry_box.cget('selectbackground'))
    
    
def change_selection_colors_to_invisible():
    fg, bg = entry_box.cget('fg'), entry_box.cget('bg')
    entry_box.config(insertbackground=bg, selectforeground=fg, selectbackground=bg)
    result.config(insertbackground=bg, selectforeground=fg, selectbackground=bg)
    
    
def saved_state_index(event):
    set_last_func_is_ctrl_shift_scroll(False)
    set_del_mode(False)
    if not ((event.state & 0x0001) or (event.state & 0x0002) or (event.state & 0x0003)):  # не (левая кнопка (Button1) или средняя кнопка (Button2) или правая кнопка (Button3) мыши зажата)
        recents['cursor before moving calc'] = entry_box.index('insert')
    
    
def on_pushing_left_button(event):
    global last_y
    set_last_func_is_ctrl_shift_scroll(False)
    set_del_mode(False)
    recents['mouse coords'] = {'x': event.x_root, 'y': event.y_root}
    last_y = event.y_root
    
    
def on_freeing_left_button(event):
    global indexes_of_selection, cursor_index
    if recents['mouse coords']['x'] == -2:
        indexes_of_selection, cursor_index = None, recents['cursor before moving calc']
        entry_box.select_range(*[cursor_index for _ in range(2)])
        entry_box.icursor(cursor_index)
        main_win.event_generate('<dollar>')
        change_selection_colors_to_normal(settings['theme'] == 'light')
    set_main_focus(event)
    recents['cursor before moving calc'] = entry_box.index('insert')


def move_main_win(event):
    global indexes_of_selection, cursor_index
    x, y, pre_x, pre_y = event.x_root, event.y_root, *recents['mouse coords'].values()

    if pre_x == -2 and abs(event.y_root - last_y) < 2 * TASKBAR_HEIGHT:
        auto_change_size_of_everything(event, size_definition=False)

    if pre_x not in (-1, -2):
        if (pre_y - y) ** 2 + (pre_x - x) ** 2 < (HEIGHT // 2) ** 2 and not (y < HEIGHT // 8 and pre_y > HEIGHT // 4):
            return
        recents['mouse coords'] = {'x': -1, 'y': -1} if x != pre_x and abs((y - pre_y) / (x - pre_x)) < 2.7 else {'x': -2, 'y': -2}
        pre_x, pre_y = recents['mouse coords'].values()
    if pre_x == -1:
        return
    y_coord = event.y_root - HEIGHT // 2
    if y_coord < 0:
        y_coord = 0
    if y_coord > MAX_COORD:
        y_coord = MAX_COORD
    setting_y(y_coord)
    main_win.geometry(f'{WIDTH}x{HEIGHT}+{MIN_X_COORD}+{y_coord}')
    change_selection_colors_to_invisible()
    entry_box.focus_set()
    beauty_letter_tape.wm_attributes('-topmost', 1)
    result.delete(0, END)
    # стрелки не из ascii дофига жрут (1200 мс), так что теперь из ascii
    result.insert(END, f'{' ' * bool(entry_box.get())}y={f'{y_coord}↑'.ljust(len(str(MAX_COORD)) + 1)}  –{MAX_COORD - y_coord}↓ (пара значений y="пикселей от верха"  –"низа")')
    if tape: resize_and_retheme_canvas_drawings()


def move_added_win(event):
    x, y, pre_x, pre_y = event.x_root, event.y_root, *recents['mouse coords'].values()
    if pre_x not in (-1, -2):
        if (pre_y - y) ** 2 + (pre_x - x) ** 2 < (HEIGHT // 2) ** 2:
            return
        recents['mouse coords'] = {'x': -1, 'y': -1} if y != pre_y and abs((x - pre_x) / (y - pre_y)) < 2.7 else {'x': -2, 'y': -2}
        pre_x, pre_y = recents['mouse coords'].values()
    if pre_x == -1:
        return
    x_coord = event.x_root - 8
    if x_coord < 0:
        x_coord = 0
    if x_coord > MAX_X_COORD:
        x_coord = MAX_X_COORD
    setting_x(x_coord)
    added_win.geometry(f'{added_win.winfo_width()}x{MAX_COORD - 2 * TASKBAR_HEIGHT}+{x_coord}+0')
    return 'break'


def move_added_win_scrolling_horizontally(event):
    pre_x_coord = x_coord = added_win.winfo_x()
    delta_event = event.delta // 3
    x_coord += delta_event
    if x_coord < 0:
        x_coord = 0
    if x_coord > MAX_X_COORD:
        x_coord = MAX_X_COORD
    if x_coord not in (0, MAX_X_COORD):
        x_coord -= (x_coord - (MIN_X_COORD - 8 * 2)) % delta_event  # чтобы окно истории встало точно над строкой со смещение в полоску
    x_coord_diff = x_coord - pre_x_coord
    setting_x(x_coord)
    
    added_win.geometry(f'{added_win.winfo_width()}x{MAX_COORD - 2 * TASKBAR_HEIGHT}+{x_coord}+0')
    _mouse_move_to(event.x_root + x_coord_diff, event.y_root)
    
    
def has_selection():
    return type(indexes_of_selection) is dict and indexes_of_selection['start'] != indexes_of_selection['end']


def filter_from_empty_and_sort_row(var):
    return list(filter(lambda x: x, sorted(list(var), reverse=True)))


def tokenate(var, supersplit=False, ultrasplit=False):
    return re.sub((tokenator, super_tokenator, ultra_tokenator)[supersplit + 2 * ultrasplit], r' \1 ', var).split()


def get_coeff_of_token_overlaying(tokened_query, tokened_data):
    tokened_query = tokened_query[:]
    tokened_data = tokened_data[:]
    coeff = 0
    for overlaying_token_length in range(len(tokened_query), 0, -1):
        is_overlayed = False
        for i in range(len(tokened_query) - overlaying_token_length + 1):
            query_part = tokened_query[i:i + overlaying_token_length]
            for j in range(len(tokened_data) - overlaying_token_length + 1):
                if query_part == tokened_data[j:j + overlaying_token_length]:
                    coeff += 4 ** Decimal(overlaying_token_length - (query_part.count('(') + query_part.count(')'))) + 4 ** (Decimal(overlaying_token_length - (query_part.count('(') + query_part.count(')'))) - Decimal(len(tokened_data)))
                    tokened_query[i:i + overlaying_token_length], tokened_data[j:j + overlaying_token_length] = [], []
                    is_overlayed = True
                    break
            if is_overlayed:
                break
    return coeff


def highlight_all_words(text_widget, word_to_find, tag_name="highlight"):
    # 1. Сначала очищаем старые выделения этого тега (если они были)
    text_widget.tag_remove(tag_name, "1.0", "end")
    
    # Если строка поиска пустая, ничего не делаем
    if not word_to_find:
        return

    start_pos = "1.0"
    
    # 2. Запускаем цикл поиска совпадений
    while True:
        # Ищем слово от текущей позиции start_pos до конца текста ('end')
        pos = text_widget.search(word_to_find, start_pos, stopindex="end", nocase=True)
        
        # Если совпадений больше нет, search() вернет пустую строку — выходим из цикла
        if not pos:
            break
            
        # Вычисляем конечную позицию (индекс начала + длина искомого слова)
        # Формат строки "+Xc" означает "+X символов"
        end_pos = f"{pos}+{len(word_to_find)}c"
        
        # 3. Добавляем тег к найденному участку
        text_widget.tag_add(tag_name, pos, end_pos)
        
        # Сдвигаем позицию старта для следующей итерации цикла за найденное слово
        start_pos = end_pos

    ranges = text_widget.tag_ranges("highlight")

    if ranges:
        # Переводим Tcl_Obj первого совпадения в обычную строку Python
        first_match_str = str(ranges[0])
        
        # Достаем номер строки
        line_number = first_match_str.split('.')[0]
        
        # Прокручиваем к самому верху
        text_widget.yview(int(line_number) - 1)


def rank_text(key=None):
    itogo_matches_power_sums = []
    create_added_win('h')
    param, text_param = create_perfect_example(entry_box.get()), re.sub(r' (?![\(\[]?\w|\d{2}:)', r'', text_entry.get('1.0', 'end'))
    if not param:
        return
    tokened_param = tokenate(param)
    microtokened_param = tokenate(param, supersplit=True)
    ultratokened_param = tokenate(param, ultrasplit=True)
    num_tokens_of_param = [i for i in tokened_param if re.fullmatch(num_construct_with_spaces, i)]
    word_tokens_of_param = [i for i in tokened_param if re.fullmatch(word_construct, i)]
    # digit_tokens_of_param = list(''.join(num_tokens_of_param))
    param = re.sub(r'(\d{2})(\.|/|-)(\d{2})\2(\d{4})', r'\4.\3.\1', param)
    param = re.sub(r'(\d{2})/(\d{2})/(\d{2})', r'\1:\2:\3', param)
    
    splitted_txt_param = text_param.split('\n')
    for indx in range(0, len(splitted_txt_param), 4):
        txt_row = f'{'='.join(splitted_txt_param[indx:indx + 2])}'
        tokened_txt_row = tokenate(txt_row)
        microtokened_txt_row = tokenate(txt_row, supersplit=True)
        ultratokened_txt_row = tokenate(txt_row, ultrasplit=True)
        num_tokens_of_txt_row = [i for i in tokened_txt_row if re.fullmatch(num_construct_with_spaces, i)]
        word_tokens_of_txt_row = [i for i in tokened_txt_row if re.fullmatch(word_construct, i)]
        # digit_tokens_of_txt_row = list(''.join(num_tokens_of_txt_row))

        # the_most_powerul_sorting_algorythm
        points = [0, 0, 0]
        if txt_row:
            # Альфа класс: совпадение выражения
            points[0] += (1 - len(txt_row.replace(param, '', 1)) / len(txt_row))
            # Бета класс: совпадают части выражения, причём порядок кусков не важен, более того, могут совпадать числа, при сравнении частей чисел на совпадение алгоритм слишком долгим становится
            points[1] += get_coeff_of_token_overlaying(tokened_param, tokened_txt_row) + get_coeff_of_token_overlaying(microtokened_param, microtokened_txt_row)
            points[1] += get_coeff_of_token_overlaying(num_tokens_of_param, num_tokens_of_txt_row)
            points[1] += get_coeff_of_token_overlaying(word_tokens_of_param, word_tokens_of_txt_row)
            # Мета класс: совпадает хотя бы символьный состав чисел и букв
            points[2] += get_coeff_of_token_overlaying(ultratokened_param, ultratokened_txt_row)

        if indx % 4 == 0:
            val = re.sub(r'(\d{4})\.(\d{2})\.(\d{2})(\d{2}):(\d{2}):(\d{2})', r'\1.\2.\3 \4:\5:\6', '\n'.join(splitted_txt_param[indx:indx + 4]))
            itogo_matches_power_sums.append((val, points))
    text_entry.delete(1.0, END)
    # for i in sorted(itogo_matches_power_sums, key=lambda x: (x[1], len(x[0])), reverse=False):
    #     print(i)

    color1 = ('#' + 'b0' * 3, '#' + '2f' * 3)[settings['theme'] == 'light']
    color2 = ('#' + '90' * 3, '#' + '5f' * 3)[settings['theme'] == 'light']
    [text_entry.tag_config(f'history_{color1}', foreground=color1), text_entry.tag_config(f'history_{color2}', foreground=color2)]
    tags = (None, f'history_{color1}', f'history_{color1}', f'history_{color2}')
    ranked_info = '\n'.join(map(lambda x: x[0], sorted(itogo_matches_power_sums, key=lambda x: (x[1], len(x[0])), reverse=True)))
    [text_entry.insert(END, val + '\n', tags[(i + 1) % 4]) for i, val in enumerate(ranked_info.split('\n'))]
    for i in range(ranked_info.count('\n') + 1):
        text_entry.tag_add('highlight', f'{i + 1}.0', f'{i + 1}.end')
    text_entry.focus_set()
    text_entry.tag_add(SEL, '1.0', 'end')
    (entry_box.delete(0, END), entry_box.insert(END, 'Результаты поиска ранжированы'), change_width_of_entry(entry_box.get(), entry_box, result))
    main_win.after(after_tick_symbol_time + 200, lambda: (entry_box.delete(0, END), entry_box.insert(END, example_value), change_width_of_entry(entry_box.get(), entry_box, result)))


def change_history_type(*key):
    settings['history type'] = ('notes', 'history')[settings['history type'] == 'notes']
    result.insert(END, f' автосохранение примеров {('вкл', 'откл')[settings['history type'] == 'notes']}ючено')
    main_win.after(1000, calculate_result)


for val, func in {'a': select_all, 'c': copy_text, 'x': cut_text, 'v': paste_text, 'y': ctrl_y, 'z': ctrl_z,
                  's': lambda key: save_example_to_history(example_to_save=entry_box.get()), 'w': close_main_win_with_layout_switching,
                  'h': lambda key: create_added_win('h'), 'f': rank_text, **{i: (lambda key: main_win.event_generate('<question>')) for i in ('q', 'i')},
                  'l': lambda key: change_size_of_everything(1), 'm': lambda key: change_size_of_everything(3), 'b': lambda key: change_size_of_everything(5),
                  **{i: move_to_edges for i in 'eud'}, 'k': lambda key: virtual_keyboard.toggle_keyboard(main_win, help_text=help_text, theme=settings['theme']),
                  'n': change_history_type}.items():
    for key in (val, val.upper()):
        main_win.bind(f'<Control-{key}>', func)

def manage_all_of_that_right_button_shit(key):
    if deletion_mode:
        cut_text(key)
        set_del_mode(False)
    elif added_win.title() != invisible_win_title:
        manage_not_main_window_close()
    else:
        create_added_win('h')
main_win.bind('<ButtonPress-3>', manage_all_of_that_right_button_shit)
        
        
def ctrl_backspace(key, no_cut=False):
    (change_text('', define_future_of_cursor('left'), cursor_index) if not has_selection() or no_cut else cut_text(key))
    
def ctrl_delete(key):
    (change_text('', cursor_index, define_future_of_cursor('right')) if not has_selection() else cut_text(key))

    
main_win.bind('<Shift-Up>', lambda key: set_cursor_shift_to_the_edge(key, 'start'))
main_win.bind('<Shift-Down>', lambda key: set_cursor_shift_to_the_edge(key, 'end'))
main_win.bind('<Control-Shift-Left>', lambda key: set_cursor_shift_to_the(key, define_future_of_cursor('left')))
main_win.bind('<Control-Shift-Right>', lambda key: set_cursor_shift_to_the(key, define_future_of_cursor('right')))
main_win.bind('<Shift-Left>', lambda key: set_cursor_shift_to_the(key, 'left'))
main_win.bind('<Shift-Right>', lambda key: set_cursor_shift_to_the(key, 'right'))
main_win.bind('<Up>', lambda key: set_cursor_to_the(key, 'start'))
main_win.bind('<Down>', lambda key: set_cursor_to_the(key, 'end'))
main_win.bind('<Control-Left>', lambda key: set_cursor_to_the(key, define_future_of_cursor('left')))
main_win.bind('<Control-Right>', lambda key: set_cursor_to_the(key, define_future_of_cursor('right')))
main_win.bind('<Control-BackSpace>', ctrl_backspace)
main_win.bind('<Control-Delete>', ctrl_delete)
main_win.bind('<Control-Shift-y>', ctrl_shift_y)
main_win.bind('<Control-Shift-z>', ctrl_shift_z)
main_win.bind('<Control-Shift-Y>', ctrl_shift_y)
main_win.bind('<Control-Shift-Z>', ctrl_shift_z)
main_win.bind('?', lambda key: create_added_win('?'))
main_win.bind('<Control-slash>', lambda key: create_added_win('?'))


def press_tape_by_keyboard(key):
    if tape and int(tape_canvas.cget('width')) == 0 and 'нажми меня' in tape_info_label.cget('text'):
        _mouse_move_to(key.x_root, settings['y'] + HEIGHT // 2 + (HEIGHT, -HEIGHT)[settings['y'] - HEIGHT > 0])
        _mouse_click()
        main_win.after(50, lambda: _mouse_move_to(key.x_root, key.y_root))
    return 'break'


main_win.bind('<Tab>', lambda key: switch_to_next_window())
main_win.bind('<Shift-Tab>', press_tape_by_keyboard)
main_win.bind('<Control-Tab>', press_tape_by_keyboard)
main_win.bind('<Alt-space>', lambda key: switch_to_next_window())
main_win.bind('<Control-space>', lambda key: switch_to_next_window())

main_win.bind('<Motion>', saved_state_index)
main_win.bind('<Control-MouseWheel>', lambda key: change_text_size(increase=key.delta > 0))


scroll_timeout = 0
def scroll_handler(key):
    global scroll_timeout, last_scroll_action_time
    if time.time() - last_scroll_action_time < scroll_timeout:
        last_scroll_action_time = time.time()
        return
    last_scroll_action_time = time.time()
    if HEIGHT <= screen_width // 180 and (i_history == 'past' and key.delta > 0 or i_history == 'future' and key.delta < 0):
        change_size_of_everything(scale=settings['scale'], scale_was_zero=True)
        scroll_timeout = 0.25
    elif (i_history == 'past' and key.delta < 0 or i_history == 'future' and key.delta > 0) and not last_func_is_ctrl_shift_scroll:
        change_size_of_everything(scale=0, change_result=False)
        scroll_timeout = 0
    else:
        (ctrl_shift_y, ctrl_shift_z)[key.delta < 0]()
        set_last_func_is_ctrl_shift_scroll()
        scroll_timeout = 0


cursor_shift_intermediate_steps_at_del_mode = []
deletion_mode = False
def backspace_undo_handler(key):
    global scroll_timeout, last_scroll_action_time, cursor_shift_intermediate_steps_at_del_mode
    if time.time() - last_scroll_action_time < scroll_timeout:
        last_scroll_action_time = time.time()
        return
    if not example_value or key.delta > 0 and '[Последний введённый пример]' in result.get():
        set_del_mode(False)
    elif key.delta < 0 and i_last_example == 'future':
        set_del_mode(True)
    last_scroll_action_time = time.time()
    if not deletion_mode:
        if i_last_example == len(recents['last examples']) - 2 and key.delta < 0:
            set_del_mode(True)
            ctrl_y()
            scroll_timeout = 0.1
        else:
            (ctrl_z, ctrl_y)[key.delta < 0]()
            scroll_timeout = 0
    else:
        for _ in range(abs(key.delta) // 120):
            if cursor_shift_intermediate_steps_at_del_mode == [len(example_value)] and key.delta > 0 and i_last_example == 'future':
                set_cursor_shift_to_the(key, cursor_shift_intermediate_steps_at_del_mode[-1])
                set_del_mode(False)
                scroll_timeout = 0.1
                break
            elif cursor_shift_intermediate_steps_at_del_mode and key.delta and (key.delta > 0) == (cursor_shift_intermediate_steps_at_del_mode[-1] > cursor_index):
                set_cursor_shift_to_the(key, cursor_shift_intermediate_steps_at_del_mode[-1])
                cursor_shift_intermediate_steps_at_del_mode.pop()
            elif key.delta and ((key.delta < 0) != (cursor_index == 0) or (key.delta > 0) != (cursor_index == len(example_value))):
                if cursor_shift_intermediate_steps_at_del_mode[-1:] != [cursor_index]:
                    cursor_shift_intermediate_steps_at_del_mode.append(cursor_index)
                set_cursor_shift_to_the(key, define_future_of_cursor(('left', 'right')[key.delta > 0]))
        else:
            scroll_timeout = 0
        config_fg_and_insertbackground()
        if indexes_of_selection and indexes_of_selection['start'] != indexes_of_selection['end']:
            sel_del_info = f'удалить {example_value[indexes_of_selection['start']:indexes_of_selection['end']]} правой кнопкой'
            create_tape(tape_type='info', info_blit=sel_del_info)
            resize_and_retheme_canvas_drawings(info_blit=sel_del_info)
        elif not indexes_of_selection or indexes_of_selection['start'] == indexes_of_selection['end']:
            destroy_tape()


main_win.bind('<Shift-MouseWheel>', backspace_undo_handler) # lambda key: (ctrl_z, ctrl_y)[key.delta < 0]())
main_win.bind('<MouseWheel>', scroll_handler)

main_win.bind('<ButtonRelease-1>', on_freeing_left_button)
main_win.bind('<ButtonRelease-2>', set_main_focus)
# main_win.bind('<ButtonRelease-3>', set_main_focus)

main_win.bind('<ButtonPress-1>', on_pushing_left_button)
main_win.bind('<B1-Motion>', move_main_win)

main_win.bind('<Control-Shift-Up>', lambda key: None)  # не удалять! поддерживает автономию перед <Control-Up>
main_win.bind('<Control-Shift-Down>', lambda key: None)  # не удалять! поддерживает автономию перед <Control-Down>

main_win.bind('<Control-Key>', lambda key: None)
main_win.bind('<Alt-Key>', lambda key: None)
main_win.bind('<Key>', lambda key: supermanage_key_event(key, True))


main_win.bind('<Control-equal>', lambda key: change_text_size(increase=True))
main_win.bind('<Control-minus>', lambda key: change_text_size(increase=False))
main_win.bind('<Control-Up>', move_up)
main_win.bind('<Control-Down>', auto_change_size_of_everything)


def on_enter(event):
    global keyboard_layout_memory
    keyboard_layout_memory = ('en', 'ru')[is_russian_layout()]
    entry_box.config(bg=('#' + '27' * 3, '#' + 'e2' * 3)[settings['theme'] == 'light'])
    result.config(bg=entry_box.cget('bg'))
    change_width_of_entry(entry_box.get(), entry_box, result)
    
    
def on_leave(event):
    if main_win.focus_get() not in (main_win, entry_box, result):
        entry_box.config(bg=('#' + '1f' * 3, '#' + 'ea' * 3)[settings['theme'] == 'light'])
        result.config(bg=entry_box.cget('bg'))
    
    
def focus_in(event):
    if added_win.title() == 'инструкция':
        top_text_index = text_entry.index("@0,0")
        current_text_index = text_entry.index(INSERT)
        has_selection = False
        try:
            sel_start = text_entry.index("sel.first")
            sel_end = text_entry.index("sel.last")
            has_selection = True
        except TclError:
            pass

    if is_russian_layout():
        hwnd = user32.GetForegroundWindow()
        user32.PostMessageW(hwnd, 0x50, 0, user32.LoadKeyboardLayoutW("00000409", 0x1))
    main_win['bg'] = ('#' + '51' * 3, '#' + 'a0' * 3)[settings['theme'] == 'light']

    close_label.config(fg=entry_box.cget('fg'), bg=result.cget('bg'))
    hide_label.config(fg=entry_box.cget('fg'), bg=result.cget('bg'))

    entry_box.config(bg=('#' + '27' * 3, '#' + 'e2' * 3)[settings['theme'] == 'light'])
    result.config(bg=entry_box.cget('bg'))
    change_size_of_everything(scale=settings['scale'], scale_was_zero=True, change_result=False)
    config_fg_and_insertbackground()
    if added_win.focus_displayof() is not None:
        main_win.after(50, lambda: blink_fake_cursor(None))
    if added_win.title() == 'инструкция':   
        main_win.after(50, lambda: text_entry.yview(top_text_index))
        text_entry.mark_set(INSERT, current_text_index)
        if has_selection:
            text_entry.tag_add("sel", sel_start, sel_end)
    
    
def focus_out(event):
    global keyboard_layout_memory
    if not is_russian_layout() and keyboard_layout_memory == 'ru':
        hwnd = user32.GetForegroundWindow()
        user32.PostMessageW(hwnd, 0x50, 0, user32.LoadKeyboardLayoutW("00000419", 0x1))
    entry_box.config(bg=('#' + '1f' * 3, '#' + 'ea' * 3)[settings['theme'] == 'light'])
    result.config(bg=entry_box.cget('bg'))
    change_width_of_entry(entry_box.get(), entry_box, result)
    if added_win.focus_displayof() is not None:
        blink_fake_cursor()


def delete_temp_cursor(temp_cursor):
    if entry_box.get()[entry_box.index("insert") - 1:entry_box.index("insert")] == temp_cursor:
        entry_box.delete(entry_box.index("insert") - 1)
    change_width_of_entry(entry_box.get(), entry_box, result)


def blink_fake_cursor(state=True):
    temp_cursor = 'I'
    if state is None:
        main_win.after(350, lambda: delete_temp_cursor(temp_cursor))
        return
    if state and entry_box.get()[entry_box.index("insert") - 1:entry_box.index("insert")] != temp_cursor:
        entry_box.insert('insert', temp_cursor)
    elif not state and entry_box.get()[entry_box.index("insert") - 1:entry_box.index("insert")] == temp_cursor:
        entry_box.delete(entry_box.index("insert") - 1)
    if main_win.focus_get() not in (entry_box, result):
        change_width_of_entry(entry_box.get(), entry_box, result)
        entry_box.after((250, 350)[state], lambda: blink_fake_cursor(state=not state))


def is_window_ghost(window):
    """Возвращает True, если окно полностью игнорирует мышь (призрак), иначе False"""
    try:
        if not window or not window.winfo_exists():
            return False
            
        # Получаем системный дескриптор окна (HWND)
        hwnd = user32.GetParent(window.winfo_id())
        
        GWL_EXSTYLE = -20
        # Считываем текущие системные флаги окна
        current_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        
        # Проверяем наличие флага WS_EX_TRANSPARENT (0x20) с помощью побитового "И" (&)
        # Если результат не равен 0, значит флаг установлен
        return (current_style & 0x20) != 0
    except:
        return False


def make_window_ghost(window):
    """Делает окно полностью неосязаемым для курсора мыши"""
    try:
        # Получаем системный идентификатор окна (HWND) в Windows
        hwnd = user32.GetParent(window.winfo_id())
        
        # Получаем текущие расширенные стили окна
        GWL_EXSTYLE = -20
        old_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        
        # WS_EX_LAYERED (0x80000) + WS_EX_TRANSPARENT (0x20)
        # Этот набор флагов заставляет Windows игнорировать координаты мыши на этом окне
        new_style = old_style | 0x80000 | 0x20
        
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
    except:
        pass

def make_window_normal(window):
    """Возвращает окну нормальное осязание мыши"""
    try:
        hwnd = user32.GetParent(window.winfo_id())
        GWL_EXSTYLE = -20
        old_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        
        # Отключаем флаг прозрачности для мыши
        new_style = old_style & ~0x20
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
    except:
        pass


GWL_EXSTYLE = -20
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED = 0x00080000

def make_click_through(window):
    """Этот хак заставляет Windows пропускать клики вашей мыши сквозь окно"""
    window.update() # Сначала принудительно обновляем окно, чтобы ОС выдала ему ID
    hwnd = user32.GetParent(window.winfo_id())
    old_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    new_style = old_style | WS_EX_TRANSPARENT | WS_EX_LAYERED
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)


main_win.bind('<FocusOut>', focus_out)
main_win.bind('<FocusIn>', focus_in)
main_win.bind('<Enter>', on_enter)
main_win.bind('<Leave>', on_leave)


def close_main_win():
    global added_win
    if added_win.winfo_viewable() and added_win.title() == 'инструкция':
        create_added_win('h')
        manage_not_main_window_close()
    elif added_win.winfo_viewable():
        manage_not_main_window_close()
    else:
        recents['win theme alike calc'] = is_dark_theme() == (settings['theme'] == 'dark')
        recents['example before closing'] = example_value   
        recents['cursor before closing'] = cursor_index
        recents['closing time'].append(time.time())
        recents['closing time'].pop(0)
        rewrite_json('history')
        rewrite_json('settings')
        rewrite_json('recents')
        main_win.destroy()
        

def config_fg_and_insertbackground():
    theme_is_light = settings['theme'] == 'light'
    entry_box.config(fg=('#' + 'd0' * 3, '#' + '0f' * 3)[theme_is_light] if example_value not in ('ထ', '+ထ', '-ထ') else ('#b0b054', '#3f3f8b')[theme_is_light])
    result.config(fg=('#' + 'b0' * 3, '#' + '2f' * 3)[theme_is_light] if example_value not in ('ထ', '+ထ', '-ထ') else ('#909054', '#5f5f9b')[theme_is_light])
    
    if result.get() == calculator_greeting or modify_info(entry_box.get()) is not None and example_value not in ('ထ', '+ထ', '-ထ'):
        result.config(fg=('#' + '70' * 3, '#' + '6f' * 3)[theme_is_light])
    elif not is_num(result.get().replace('=', ''), correct_answer_num_symbols) and example_value not in ('ထ', '+ထ', '-ထ'):
        result.config(fg=('#' + 'a8' * 3, '#' + '37' * 3)[theme_is_light])
    change_selection_colors_to_normal(theme_is_light)
        

def change_theme(event):
    global tape, beauty_letter_tape, beauty_letter_tape_canvas, coord_x_beauty_shift, last_time_main_win_were_focused, space_initialized
    global space_bg_stars, space_bright_stars, space_meteors
    theme_is_light = settings['theme'] == 'light'
    settings['theme'] = ('light', 'dark')[theme_is_light]
    
    added_win_in_focus, text_entry_in_focus = False, False
    if added_win.title() != invisible_win_title:
        scroll_pos = text_entry.yview()[0]
        cursor_pos = text_entry.index(INSERT)
        start_sel, end_sel = (text_entry.index(SEL_FIRST), text_entry.index(SEL_LAST)) if text_entry.tag_ranges(SEL) else (cursor_pos, cursor_pos)
        added_win_in_focus, text_entry_in_focus = main_win.focus_get() == added_win, main_win.focus_get() == text_entry
    
    selected = recents['last examples'][-1][4]
    focus_in(event)
    virtual_keyboard.recreate_keyboard(settings['theme'])
    create_added_win((None, 'h', '?')[(added_win.title() == 'история') + (added_win.title() == 'инструкция') * 2])
    
    # Важно для не смены курсора и самого примера
    entry_box.delete(0, END)
    entry_box.insert(END, example_value)
    entry_box.icursor(cursor_index)
    # конец коммента важности
    
    if selected:
        entry_box.select_range(*selected.values())
    
    if not (added_win_in_focus or text_entry_in_focus):
        entry_box.focus_set()
        if not beauty_letter_tape:
            beauty_letter_tape = Toplevel()
            beauty_letter_tape.overrideredirect(True)
            beauty_letter_tape_canvas = Canvas(beauty_letter_tape, bg=result.cget('bg'), borderwidth=0, highlightthickness=0)
            beauty_letter_tape_canvas.pack(fill="both", expand=True)
        beauty_letter_tape.wm_attributes('-topmost', 1)
    else:
        text_entry.yview_moveto(scroll_pos)
        if added_win_in_focus or text_entry_in_focus:
            added_win.focus_force()
        if text_entry_in_focus:
            text_entry.focus_force()
        text_entry.mark_set(INSERT, cursor_pos)
        text_entry.tag_remove(SEL, '1.0', 'end')
        text_entry.tag_add(SEL, start_sel, end_sel)

        if added_win.title() != invisible_win_title: set_window_theme_border(window=added_win, is_dark_theme=settings['theme'] == 'dark')
    if tape: resize_and_retheme_canvas_drawings()
    close_label.config(fg=entry_box.cget('fg'), bg=result.cget('bg'))
    hide_label.config(fg=entry_box.cget('fg'), bg=result.cget('bg'))
        
        
def unbind_left_button():
    entry_box.unbind('<ButtonPress-1>')
    entry_box.unbind('<B1-Motion>')
    entry_box.bind('<ButtonPress-1>', on_pushing_left_button)
    entry_box.bind('<B1-Motion>', move_main_win)
    
    
def bind_left_button():
    entry_box.unbind('<ButtonPress-1>')
    entry_box.unbind('<B1-Motion>')
    entry_box.bind('<ButtonPress-1>', disable_left_mouse_button_clicking)
    entry_box.bind("<B1-Motion>", disable_left_mouse_button_clicking)
        

def check_theme_or_geometry_change():
    global last_theme, example_value, indexes_of_selection, tape_creation_time
    current = is_dark_theme()
    if current != last_theme:
        last_theme = current
        if (settings['theme'] == 'dark') != current:
            set_focus_from_not_my_application()
            change_theme(None)
            main_win.event_generate('<Control-space>')
    res_val, entry_val = result.get(), entry_box.get()

    curr_time = time.time()
    if tape:
        widget_under_mouse = tape.winfo_containing(tape.winfo_pointerx(), tape.winfo_pointery())
        if widget_under_mouse and widget_under_mouse.winfo_toplevel() == tape:
            tape_creation_time = time.time()
        
    if curr_time - last_time_main_win_geometry_change > 1 and re.search(calc_geometry_state_change_expression, res_val):
        result.delete(0, END)
        result.insert(END, val_before_last_main_win_geometry_change)
    elif curr_time - last_time_round_change > (10 if recents['rounding info longer'] > 0 else 0.75) and 'q' in entry_val:
        if recents['rounding info longer'] > 0:
            recents['rounding info longer'] -= 1
        if has_selection():
            main_win.event_generate('<Right>' if cursor_index == get_selection()['start'] else '<Left>')
        if 'q' in entry_val and main_win.focus_get() == entry_box:
            ctrl_backspace('', no_cut=True)
            main_win.after(20, unbind_left_button)
            example_value = entry_box.get()
    elif bool(tape) and int(tape_canvas.cget('width')) == 0 and 'абсолютно любое окно закрывают esc и ctrl+w' in tape_info_label.cget('text'):
        if curr_time - tape_creation_time > 15:
            destroy_tape()
    elif curr_time - tape_creation_time > (1.5, 5)[bool(tape) and int(tape_canvas.cget('width')) == 0 and ' – нажми меня, чтобы поменять местами аргументы логарифмов' in tape_info_label.cget('text')]:
        destroy_tape()

    main_win.after((50, 30)[0.49 < curr_time - last_time_round_change < 0.51], check_theme_or_geometry_change)  # проверять каждую двадцатую секунды
last_theme = is_dark_theme()
check_theme_or_geometry_change()
        
if recents['win theme alike calc'] and is_dark_theme() != (settings['theme'] == 'dark'):
    change_theme(None)


# ==============================================================================
# НАСТРОЙКИ РЕАЛИСТИЧНОГО ЗВЕЗДНОГО НЕБА ДЛЯ СТРОКИ КАЛЬКУЛЯТОРА
# ==============================================================================
beauty_letter_tape = None
coord_x_beauty_shift = -WIDTH // 5

# Астрономические пастельные цвета звёзд
space_star_colors = (["#f8f7ff", "#ffffff", "#fff4ea", "#9bb0ff", "#aabfff", "#cad7ff", "#ffd2a1"])
# Серебристо-стальной градиент для угасания метеоров
space_meteor_fade = (["#ffffff", "#eef4fa", "#d2dae0", "#b4bcc2", "#939aa0", "#6f757a", "#4b4f52", "#272a2b"])



space_bg_stars = []    # Мелкие звёзды
space_bright_stars = []# Крупные звёзды с лучами
space_meteors = []     # Активные метеоры
space_initialized = False

def spawn_single_bg_star(canvas_widget):
    global space_bg_stars
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    
    size = 2 if random.random() > 0.80 else 1
    base_color = random.choice(space_star_colors)
    
    star_id = canvas_widget.create_rectangle(x, y, x + size, y + size, fill=base_color, outline="")
    
    # "life" — яркость, новые звезды рождаются невидимыми (0.0) для плавного проявления
    space_bg_stars.append({
        "id": star_id,
        "base_color": base_color,
        "phase": random.uniform(0, math.pi * 2),
        "speed": random.uniform(0.024, 0.048),
        "life": 0.0, 
        "target_life": 1
    })


def init_star_sky(canvas_widget, star_amount=100):
    """Генерирует звёзды один раз при старте 10-секундного таймаута."""
    global space_initialized, space_bg_stars, space_bright_stars, space_meteors
    space_bg_stars.clear()
    space_bright_stars.clear()
    space_meteors.clear()
    
    # 1. Фоновые звёзды (100 штук, разреженно для узкой строки)
    for _ in range(star_amount):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        
        # ИСПРАВЛЕНО: делаем шанс появления звёзд 1х1 и 2х2 строго равным (50/50).
        # Это убирает визуальные проплешины и распределяет массу звёзд равномерно.
        size = 2 if random.random() > 0.80 else 1
        base_color = random.choice(space_star_colors)
        
        star_id = canvas_widget.create_rectangle(x, y, x + size, y + size, fill=base_color, outline="")
        space_bg_stars.append({
            "id": star_id,
            "base_color": base_color,
            "phase": random.uniform(0, math.pi * 2),
            "speed": random.uniform(0.024, 0.048)
        })

        
    # 2. Крупные звёзды со строго ПРЯМЫМИ короткими лучами (6 штук)
    for _ in range(star_amount // 5 + 1):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(3, HEIGHT - 3)
        color = random.choice(space_star_colors)
        
        # 4 перпендикулярных направления (Право, Лево, Вниз, Вверх)
        angles = [0, math.pi, math.pi / 2, 3 * math.pi / 2]
        lines = []
        for ang in angles:
            line_id = canvas_widget.create_line(x, y, x, y, fill=color, width=1)
            lines.append((line_id, ang))
            
        core_id = canvas_widget.create_rectangle(x - 1, y - 1, x + 2, y + 2, fill=("#ffffff", '#000000')[settings['theme'] == 'light'], outline="")
        space_bright_stars.append({
            "x": x, "y": y, "core_id": core_id, "color": color, "lines": lines,
            "phase": random.uniform(0, math.pi * 2),
            "speed": random.uniform(0.16, 0.28),
            "max_ray_len": random.randint(2, 4) # Маленький размер для ультра-узкой строки
        })
    space_initialized = True

def spawn_space_meteor(canvas_widget):
    """Вспышка метеора, летящего полого вдоль длинной строки."""
    start_x = random.randint(int(WIDTH * 0.1), int(WIDTH * 0.8))
    start_y = random.randint(-5, 5)
    
    # Очень пологий угол полёта (165-175 градусов) под пропорции калькулятора
    angle = random.uniform(math.radians(165), math.radians(175))
    speed = random.uniform(12, 16)
    
    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed
    
    length = random.randint(25, 40)
    lx = math.cos(angle) * length
    ly = math.sin(angle) * length
    
    meteor_id = canvas_widget.create_line(start_x, start_y, start_x - lx, start_y - ly, fill="#ffffff", width=1)
    space_meteors.append({
        "id": meteor_id, "x": start_x, "y": start_y, "vx": vx, "vy": vy, "lx": lx, "ly": ly,
        "life": 1.0, "fade_speed": random.uniform(0.08, 0.14)
    })

def destroy_beauty_letter_tape():
    global coord_x_beauty_shift, space_initialized
    coord_x_beauty_shift = -WIDTH // 5
    space_initialized = False # Сбрасываем небо при обнулении анимации

def increment_hex_color(hex_str):    
    new_num = int(hex_str.lstrip('#'), 16) + 1
    if new_num > 0xFFFFFF:
        new_num -= 1
    return f"#{new_num:06X}"

# ==============================================================================
# ЕДИНАЯ АНИМАЦИОННАЯ ФУНКЦИЯ (КАДР ВСЕЙ СИСТЕМЫ)
# ==============================================================================
last_time_main_win_were_focused = time.time()


def animate_light_letters():
    global beauty_letter_tape, beauty_letter_tape_canvas, coord_x_beauty_shift, last_time_main_win_were_focused, space_initialized
    global space_bg_stars, space_bright_stars, space_meteors
    theme_is_light = settings['theme'] == 'light'
    
    # Инициализация окна-холста при первом запуске
    if not beauty_letter_tape:
        beauty_letter_tape = Toplevel()
        beauty_letter_tape.overrideredirect(True)
        beauty_letter_tape_canvas = Canvas(beauty_letter_tape, bg=result.cget('bg'), borderwidth=0, highlightthickness=0)
        beauty_letter_tape_canvas.pack(fill="both", expand=True)

    # Условие активности пользователя (180 секунд ещё не прошло)
    if result.winfo_height() != HEIGHT or time.time() < last_time_main_win_were_focused + 180:
        beauty_letter_tape.attributes('-alpha', '0')
        if result.winfo_height() != HEIGHT:
            last_time_main_win_were_focused = time.time()
        main_win.after(59, lambda: ((destroy_beauty_letter_tape(), animate_light_letters()) if coord_x_beauty_shift > WIDTH - WIDTH // 5 else animate_light_letters()))
        return

    # Включаем отображение холста ("эффект призрака" поверх строки)
    beauty_letter_tape.attributes('-alpha', str(min((0.8, 0.4)[theme_is_light], 0.001 * (time.time() - (last_time_main_win_were_focused + 180)) ** 2)))
    make_click_through(beauty_letter_tape)
    beauty_letter_tape.geometry(f'{WIDTH - 2}x{HEIGHT - 2}+{MIN_X_COORD + 1}+{settings['y'] + 1}')
    
    # Динамическая подстройка цвета фона под тему калькулятора
    bg_color = result.cget('bg')
    beauty_letter_tape_canvas.config(bg=bg_color)
    beauty_letter_tape['bg'] = bg_color
    beauty_letter_tape.wm_attributes('-transparentcolor', increment_hex_color(bg_color))

    # Создаем звёзды один раз при входе в режим бездействия
    if not space_initialized:
        # ТЕПЕРЬ БЕЗ ПОЛНОЙ ОЧИСТКИ: Сохраняем то, что уже было на холсте
        # Рассчитываем целевое количество звезд в зависимости от времени бездействия
        target_star_amount = min(int(time.time() - (last_time_main_win_were_focused + 180)), WIDTH * HEIGHT // 700)
        
        if not theme_is_light:
            # 1. Корректируем фоновые звёзды
            current_bg_count = len(space_bg_stars)
            if current_bg_count < target_star_amount:
                # Если звёзд не хватает — ДОБАВЛЯЕМ новые к старым
                for _ in range(target_star_amount - current_bg_count):
                    spawn_single_bg_star(beauty_letter_tape_canvas)
            elif current_bg_count > target_star_amount:
                # Если вдруг лимит уменьшился — аккуратно удаляем лишние с конца списка
                for _ in range(current_bg_count - target_star_amount):
                    star = space_bg_stars.pop()
                    beauty_letter_tape_canvas.delete(star["id"])

            # 2. Корректируем крупные звёзды (с лучами)
            target_bright_amount = target_star_amount // 6 + 1
            current_bright_count = len(space_bright_stars)
            if current_bright_count < target_bright_amount:
                # Добавляем новые крупные звёзды взамен недостающих
                for _ in range(target_bright_amount - current_bright_count):
                    x = random.randint(50, WIDTH - 50)
                    y = random.randint(3, HEIGHT - 3)
                    color = random.choice(space_star_colors)
                    
                    angles = [0, math.pi, math.pi / 2, 3 * math.pi / 2]
                    lines = []
                    for ang in angles:
                        line_id = beauty_letter_tape_canvas.create_line(x, y, x, y, fill=color, width=1)
                        lines.append((line_id, ang))
                        
                    core_id = beauty_letter_tape_canvas.create_rectangle(
                        x - 1, y - 1, x + 2, y + 2, 
                        fill=("#ffffff", '#000000')[settings['theme'] == 'light'], outline=""
                    )
                    space_bright_stars.append({
                        "x": x, "y": y, "core_id": core_id, "color": color, "lines": lines,
                        "phase": random.uniform(0, math.pi * 2),
                        "speed": random.uniform(0.16, 0.28),
                        "max_ray_len": random.randint(2, 4)
                    })
            elif current_bright_count > target_bright_amount:
                # Удаляем лишние крупные звёзды и их лучи
                for _ in range(current_bright_count - target_bright_amount):
                    bright_star = space_bright_stars.pop()
                    beauty_letter_tape_canvas.delete(bright_star["core_id"])
                    for line_id, _ in bright_star["lines"]:
                        beauty_letter_tape_canvas.delete(line_id)

        # Пересоздаем прямоугольник бегущей полосы (только для светлой темы)
        if theme_is_light:
            # На всякий случай удаляем старую полосу, чтобы они не накладывались друг на друга
            beauty_letter_tape_canvas.delete('sol_rect')
            beauty_letter_tape_canvas.create_rectangle(
                int(coord_x_beauty_shift), 0, int(coord_x_beauty_shift) + WIDTH // 5, HEIGHT, 
                fill=increment_hex_color(bg_color), outline='', tags='sol_rect'
            )
            
        space_initialized = True


    if not theme_is_light:
        # --------------------------------------------------------------------------
        # ВЫЧИСЛЕНИЕ СЛЕДУЮЩЕГО СОСТОЯНИЯ КОСМОСА (ПРЯМО В ЭТОМ КАДРЕ)
        # --------------------------------------------------------------------------
        # 1. Рассчитываем мерцание фоновых звёзд
        for star in space_bg_stars:
            star["phase"] += star["speed"]
            factor = (math.sin(star["phase"]) + 1) / 2
            beauty_letter_tape_canvas.itemconfig(star["id"], fill=bg_color if factor < 0.2 else star["base_color"])
            
        # 2. Рассчитываем ровное дыхание прямых лучей крупных звёзд
        for star in space_bright_stars:
            star["phase"] += star["speed"]
            pulse = (math.sin(star["phase"]) + 1) / 2
            current_ray = star["max_ray_len"] * (0.2 + 0.8 * pulse)
            
            x, y = star["x"], star["y"]
            for line_id, ang in star["lines"]:
                lx = x + math.cos(ang) * current_ray
                ly = y + math.sin(ang) * current_ray
                beauty_letter_tape_canvas.coords(line_id, x, y, lx, ly)
                
            beauty_letter_tape_canvas.itemconfig(star["core_id"], fill=("#ffffff", '#000000')[theme_is_light] if pulse > 0.35 else star["color"])
            
        # 3. Рассчитываем полёт и стальное затухание метеоров
        if random.random() < 0.003 and len(space_meteors) < 2:
            spawn_space_meteor(beauty_letter_tape_canvas)
            
        active_meteors = []
        for m in space_meteors:
            m["x"] += m["vx"]
            m["y"] += m["vy"]
            m["life"] -= m["fade_speed"]
            
            # Проверяем корректные границы жизни и координат полёта
            if m["life"] > 0 and -100 < m["x"] < WIDTH + 100 and -10 < m["y"] < HEIGHT + 10:
                beauty_letter_tape_canvas.coords(m["id"], m["x"], m["y"], m["x"] - m["lx"], m["y"] - m["ly"])
                color_idx = int((1.0 - m["life"]) * (len(space_meteor_fade) - 1))
                color_idx = max(0, min(color_idx, len(space_meteor_fade) - 1))
                beauty_letter_tape_canvas.itemconfig(m["id"], fill=space_meteor_fade[color_idx])
                active_meteors.append(m)
            else:
                # Гарантированное удаление объекта с холста Canvas при любых условиях остановки/вылета
                beauty_letter_tape_canvas.delete(m["id"])
        space_meteors[:] = active_meteors
        # --------------------------------------------------------------------------

    # Рассчитываем движение оригинальной светлой полосы калькулятора
    coord_x_beauty_shift += WIDTH / (40, 160)[theme_is_light]
    if theme_is_light:
        beauty_letter_tape_canvas.coords('sol_rect', int(coord_x_beauty_shift), 0, int(coord_x_beauty_shift) + WIDTH // 5, HEIGHT)
        beauty_letter_tape_canvas.itemconfig('sol_rect', fill=increment_hex_color(bg_color))
    
        # Принудительно опускаем полосу на задний план кадра
        beauty_letter_tape_canvas.tag_lower('sol_rect')

    # Рекурсивный вызов этого же кадра анимации через 59 мс
    main_win.after(59, lambda: ((destroy_beauty_letter_tape(), animate_light_letters()) if coord_x_beauty_shift > WIDTH - WIDTH // 5 else animate_light_letters()))



def change_greeting():
    create_greeting()
    if not entry_box.get():
        calculate_result()
    main_win.after(12000, change_greeting)


if time.time() - recents['closing time'][-3] < 14 * DAY:
    change_greeting()
    animate_light_letters()
    main_win.after(100, lambda: beauty_letter_tape.wm_attributes('-topmost', 1))
else:
    create_tape('info', 'абсолютно любое окно закрывают esc и ctrl+w, клавиатуру-помощника откроет/закроет ctrl+k')
    

main_win.bind('<Control-t>', change_theme)
main_win.bind('<Control-T>', change_theme)

calculate_result()
main_win.mainloop()