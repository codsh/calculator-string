"""
virtual_keyboard.py — экранная клавиатура-шпаргалка для строки-калькулятора.
"""
import itertools
import math
import re
import sys
import ctypes
import traceback
from pathlib import Path
from tkinter import Tk, Toplevel, Canvas, TclError, font as tkfont


def get_palette(theme_is_light):
    pick = lambda dark, light: light if theme_is_light else dark
    return {
        'panel_bg': pick('#101010', '#f2f2f2'),
        'win_bg': pick('#262626', '#dcdcdc'),
        'fg': pick('#ffffff', '#000000'),
        'sel': pick('#505050', '#b0b0b0'),
        'thumb': pick('#a0a0a0', '#666666'),
        'btn_fg': pick('#c8c8c8', '#444444'),
        'close_hover': '#e81123',
        'close_icon': '#ffffff',
        'help': {
            'black': pick('#f0f0f0', '#1f1f1f'),
            'green': pick('#e0e0e0', '#2e2e2e'),
            'blue': pick('#d2d2d2', '#3d3d3d'),
            'gray': pick('#c4c4c4', '#4c4c4c'),
            'red': pick('#b6b6b6', '#5a5a5a'),
        },
    }


HELP_COLOR_ORDER = ('black',) * 4 + ('blue', 'green', 'gray') + ('red',) * 4


def help_line_color_name(lines, i):
    tag_rows = (3, 4) + tuple(n + 1 for n, line in enumerate(lines) if not line)
    return HELP_COLOR_ORDER[min(sum(i >= el for el in tag_rows), len(HELP_COLOR_ORDER) - 1)]


HINTS = {
    'normal': {
        'q': (r'(Quantize)', 'quantize округлить'),
        'w': (r'(poWer степень)', 'poWer степень'),
        'e': (r'(e≈2.718)', 'e≈2.718'),
        'r': (r'(Root / Radical корень)', 'root / radical корень'),
        't': (r'(tg тангенс)', 'tg тангенс'),
        'y': (r'(E-)', 'E-'),
        'u': (r'(sqUare x^2)', 'square x^2'),
        'i': (r'(phI)', 'phI / factorIal'),
        'o': (r'(\(\))', '() round brackets'),
        'p': (r'(pi)', 'pi'),
        'a': (r'(Arc обратная триг.функция)', 'arc обратная тригонометрия'),
        's': (r'(sin)', 'sin'),
        'd': (r'(d антиугловая функция)', 'd антиугловая функция'),
        'f': (r'(Factorial факториал !)', 'factorial факториал !'),
        'g': (r'(lG log10)', 'lG log10'),
        'h': (r'(history память, half)', 'history память истории, half'),
        'j': (r'(куб, \(парабола x^3\))', 'куб x^3'),
        'k': (r'(Kilo тысяча)', 'Kilo тысяча'),
        'l': (r'(Log)', 'Log'),
        'z': (r'(Zeros 3 нуля)', 'Zeros 3 нуля'),
        'x': (r'(Умножить)', 'Умножить'),
        'c': (r'(cos)', 'cos'),
        'v': (r'(variable переменная)', 'variable переменная'),
        'b': (r'(base основание)', 'base основание'),
        'n': (r'(lN)', 'lN Natural logarythm'),
        'm': (r'(mod)', 'mod'),
    },
    'shift': {
        'w': (r'(переменная суммы w)', 'переменная суммы w'),
        'q': (r'(quadrillion)', 'Quadrillion 10^15'),
        'e': (r'(exp)', 'exp экспонента'),
        't': (r'(Trillion)', 'Trillion 10^12'),
        'u': (r'(биквадрат x^4)', 'биквадрат x^4'),
        'p': (r'(phi)', 'phi'),
        'f': (r'(Fi)', 'Fi'),
        'c': (r'(Ctg котангенс)', 'Ctg котангенс'),
        'd': (r'(div деление нацело)', 'div деление нацело'),
        'j': (r'(кубическая)', 'суперкуб x^5'),
        'b': (r'(billion)', 'billion миллиард'),
        'm': (r'(Million миллион)', 'Million миллион'),
        'a': (r'(Abs)', 'abs модуль'),
    },
    'ctrl': {
        'q': (r'ctrl\+q \((question)\)', 'question'),
        'i': (r'ctrl\+i \((instruction инструкция)\)', 'instruction инструкция'),
        'h': (r'ctrl\+h\s*—\s*[^(]*\((history история)\)', 'history история'),
        'w': (r'(закрыть окно)', 'закрыть окно'),
        'e': (r'ctrl\+e \((edge край)', 'edge край'),
        'u': (r'ctrl\+u \((up вверх)', 'up вверх'),
        'd': (r'ctrl\+d \((down вниз)', 'down вниз'),
        't': (r'ctrl\+t \((theme поменять тему)\)', 'theme поменять тему'),
        'b': (r'ctrl\+b \((big крупный)', 'big крупный'),
        'n': (r'ctrl\+n \((notes вкл/откл автосохранение в историю)', 'notes вкл/откл автосохранение в историю'),
        'm': (r'ctrl\+m \((middle средний)', 'middle средний'),
        'l': (r'ctrl\+l \((little мелкий)', 'little мелкий'),
        'f': (r'ctrl\+f (find сортирует по похожести)', 'find сортирует по похожести'),
        's': (r'ctrl\+s.*?(save сохранить в историю)', 'save сохранить в историю'),
        'z': (r'ctrl\+z перемещает на 1 действие (назад)', 'назад'),
        'y': (r'ctrl\+y\s*—\s*(вперёд)', 'вперёд'),
        'k': (r'ctrl\+k \((keyboard)\)', 'keyboard открыть/закрыть клавиатуру'),
    },
}


def load_help_text(help_text=None):
    if help_text:
        return help_text
    try:
        with open('data/help.txt', 'r', encoding='utf-8') as help_file:
            info_help_text = help_file.read()
        if info_help_text:
            return info_help_text
    except Exception:
        pass
    for path in (Path(__file__).with_name('help.txt'), Path('help.txt')):
        try:
            return path.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeDecodeError):
            continue
    return ''


def resolve_hints(help_text):
    lines = help_text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    resolved = {}
    for layer, table in HINTS.items():
        resolved[layer] = {}
        for key, (needle, fallback) in table.items():
            word, color_name = fallback, 'black'
            for i, line in enumerate(lines if needle else ()):
                if match := re.search(needle, line):
                    word, color_name = match.group(1), help_line_color_name(lines, i)
                    break
            resolved[layer][key] = (word, color_name)
    return resolved


def pick_highlight(word, key):
    found = [i for i, ch in enumerate(word) if ch.lower() == key.lower()]
    return ([i for i in found if word[i].isupper()] or found or [None])[0]


def display_word(word):
    return word.lower() if re.fullmatch(r'[A-Za-zА-Яа-яЁё ]+', word) else word


def detect_dark_theme():
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize') as reg_key:
            return winreg.QueryValueEx(reg_key, 'AppsUseLightTheme')[0] == 0
    except Exception:
        return True


def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    pts = [x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y1 + r,
           x2, y2 - r, x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2,
           x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1]
    return canvas.create_polygon(pts, smooth=True, splinesteps=24, **kw)


class VirtualKeyboard:
    ROWS = ('qwertyuiop', 'asdfghjkl', 'zxcvbnm')
    ROW_OFFSETS = (0.0, 0.25, 0.75)
    KEY_ASPECT = 1.6
    PAD, GAP = 0.08, 0.09
    WIDTH_FRACTION = 0.9
    HEIGHT_FRACTION = 0.5
    FONT_FAMILY = 'Arial'
    COLOR_KEY = '#ff00ff'
    TICK_MS = 40
    MOUSE_MS = 15
    BIG_SCALE = 1.3
    NOTES = {('normal', 'p'): ' π', ('normal', 'i'): ' φ',
             ('shift', 'p'): ' φ', ('shift', 'f'): ' φ'}

    VK_SHIFT, VK_CONTROL, VK_MENU = 0x10, 0x11, 0x12

    def __init__(self, master=None, help_text=None, theme='auto', alpha=0.75, anchor='bottom',
                 margin=0.06, click_through=True, close_hotkey=False):
        self.own_root = master is None
        self.master = Tk() if self.own_root else master
        self.win = self.master if self.own_root else Toplevel(self.master)
        self.win.withdraw()
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', 1)
        self.win.attributes('-alpha', alpha)

        self.theme_arg, self.anchor, self.margin = theme, anchor, margin
        self.click_through, self.close_hotkey = click_through, close_hotkey
        self.k_was_down = False
        self.hints = resolve_hints(load_help_text(help_text))
        self.has_colorkey = True
        try:
            self.win.wm_attributes('-transparentcolor', self.COLOR_KEY)
        except TclError:
            self.has_colorkey = False

        self.canvas = Canvas(self.win, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill='both', expand=True)

        self.u32 = self._load_user32()
        self.layer, self.pressed, self.fonts = 'normal', set(), {}
        self.key_ids, self.visible, self.destroyed, self.job = {}, False, False, None
        self.hover, self.mouse_job = None, None
        self.buttons, self.btn_items, self._pass_clicks = {}, {}, True
        self.theme_name, self.screen_sig = self._current_theme(), None
        self.canvas.bind('<Button-1>', self._on_click)
        if not self.u32:
            self.canvas.bind('<Motion>', lambda e: self._set_hover(self._hit_button(e.x, e.y)))
            self.canvas.bind('<Leave>', lambda e: self._set_hover(None))
        self.rebuild()
        self._apply_window_styles()
        self.job = self.win.after(self.TICK_MS, self._tick)
        if self.u32:
            self.mouse_job = self.win.after(self.MOUSE_MS, self._mouse_tick)

    @staticmethod
    def _load_user32():
        if sys.platform != 'win32':
            return None
        try:
            from ctypes import wintypes
            u32 = ctypes.WinDLL('user32', use_last_error=True)
            u32.GetAsyncKeyState.argtypes, u32.GetAsyncKeyState.restype = [ctypes.c_int], ctypes.c_short
            u32.GetParent.argtypes, u32.GetParent.restype = [wintypes.HWND], wintypes.HWND
            u32.GetWindowLongW.argtypes, u32.GetWindowLongW.restype = [wintypes.HWND, ctypes.c_int], ctypes.c_long
            u32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
            u32.SetWindowLongW.restype = ctypes.c_long
            u32.SystemParametersInfoW.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
            u32.GetCursorPos.argtypes, u32.GetCursorPos.restype = [ctypes.POINTER(wintypes.POINT)], wintypes.BOOL
            return u32
        except Exception:
            return None

    def _down(self, vk):
        return bool(self.u32 and self.u32.GetAsyncKeyState(vk) & 0x8000)

    def _apply_window_styles(self):
        if not self.u32:
            return
        try:
            self.win.update_idletasks()
            hwnd = self.u32.GetParent(self.win.winfo_id())
            style = self.u32.GetWindowLongW(hwnd, -20)
            style |= 0x00080000 | 0x08000000 | 0x00000080
            if self.click_through and self._pass_clicks:
                style |= 0x00000020
            else:
                style &= ~0x00000020
            self.u32.SetWindowLongW(hwnd, -20, style)
        except Exception:
            pass

    def _work_area(self):
        screen_w, screen_h = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        if self.u32:
            try:
                from ctypes import wintypes
                rect = wintypes.RECT()
                if self.u32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0):
                    if rect.right > rect.left and rect.bottom > rect.top:
                        return rect.left, rect.top, rect.right, rect.bottom
            except Exception:
                pass
        return 0, 0, screen_w, screen_h

    def _current_theme(self):
        theme = self.theme_arg() if callable(self.theme_arg) else self.theme_arg
        if theme == 'auto':
            theme = 'dark' if detect_dark_theme() else 'light'
        return 'light' if theme == 'light' else 'dark'

    def _compute_metrics(self):
        left, top, right, bottom = self._work_area()
        area_w, area_h = right - left, bottom - top
        cols, rows = max(map(len, self.ROWS)), len(self.ROWS)
        units_w = 2 * self.PAD + cols * self.KEY_ASPECT + (cols - 1) * self.GAP
        units_h = 2 * self.PAD + rows + (rows - 1) * self.GAP
        key_h = max(14, int(min(area_w * self.WIDTH_FRACTION / units_w, area_h * self.HEIGHT_FRACTION / units_h)))
        key_w, gap, pad = int(key_h * self.KEY_ASPECT), max(2, round(key_h * self.GAP)), max(4, round(key_h * self.PAD))
        key_r = round(key_h * 0.24)
        btn = max(12, round(key_h * 0.40))
        panel_w = 2 * pad + cols * key_w + (cols - 1) * gap
        panel_h = 2 * pad + rows * key_h + (rows - 1) * gap
        free = round(area_h * self.margin)
        y = {'top': top + free, 'center': top + (area_h - panel_h) // 2}.get(self.anchor, bottom - panel_h - free)
        return {'key_w': key_w, 'key_h': key_h, 'gap': gap, 'pad': pad, 'key_r': key_r,
                'btn': btn,
                'panel_r': key_r + pad,
                'key_line': max(1, round(key_h / 150)),
                'font_px': round(key_h * 0.34), 'font_min': max(8, round(key_h * 0.18)),
                'w': panel_w, 'h': panel_h, 'x': left + (area_w - panel_w) // 2, 'y': y,
                'sig': (self.win.winfo_screenwidth(), self.win.winfo_screenheight(), left, top, right, bottom)}

    def _font(self, px, bold=False):
        if (px, bold) not in self.fonts:
            self.fonts[(px, bold)] = tkfont.Font(root=self.win, family=self.FONT_FAMILY, size=-px,
                                                 weight='bold' if bold else 'normal')
        return self.fonts[(px, bold)]

    def rebuild(self):
        self.theme_name = self._current_theme()
        self.pal = get_palette(self.theme_name == 'light')
        self.m = self._compute_metrics()
        self.screen_sig = self.m['sig']
        m, pal = self.m, self.pal
        self.hover = None

        w, h = m['w'], m['h']
        self.win.geometry(f"{w}x{h}+{m['x']}+{m['y']}")
        self.canvas.config(width=w, height=h, bg=self.COLOR_KEY if self.has_colorkey else pal['win_bg'])
        self.canvas.delete('all')
        self.key_ids.clear()
        self.btn_items.clear()
        self.buttons.clear()

        rounded_rect(self.canvas, 0, 0, w, h, m['panel_r'], fill=pal['panel_bg'], outline='')
        for row, (letters, offset) in enumerate(zip(self.ROWS, self.ROW_OFFSETS)):
            y1 = m['pad'] + row * (m['key_h'] + m['gap'])
            for col, letter in enumerate(letters):
                x1 = m['pad'] + (col + offset) * (m['key_w'] + m['gap'])
                self.key_ids[letter] = (rounded_rect(self.canvas, x1, y1, x1 + m['key_w'], y1 + m['key_h'], m['key_r'],
                                                     width=m['key_line']), (x1, y1, x1 + m['key_w'], y1 + m['key_h']))
        radius, r = m['panel_r'], m['btn'] / 2
        edge = max(2, round(m['pad'] * 0.6))
        cy = h - edge - r
        dy = cy - (h - radius)
        cx = radius - math.sqrt(max(0.0, (radius - r) ** 2 - dy * dy)) if dy > 0 else r + edge
        btn_x, btn_y = max(edge, round(cx - r)), round(cy - r)
        self._draw_button('close', btn_x, btn_y)
        self._draw_labels()

    def _draw_button(self, name, x1, y1):
        s = self.m['btn']
        x2, y2 = x1 + s, y1 + s
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        h, lw = s * 0.22, max(1, round(s / 15))
        fg = self.pal['btn_fg']
        bg = self.canvas.create_oval(x1, y1, x2, y2, fill=fg, outline='', state='hidden',
                                     tags='btn')
        icons = [(self.canvas.create_line(cx - h, cy - h, cx + h, cy + h, fill=fg, width=lw, tags='btn'), 'fill'),
                 (self.canvas.create_line(cx - h, cy + h, cx + h, cy - h, fill=fg, width=lw, tags='btn'), 'fill')]
        self.buttons[name] = (x1, y1, x2, y2)
        self.btn_items[name] = (bg, icons)
        self._paint_button(name)

    def _paint_button(self, name):
        if name not in self.btn_items:
            return
        pal, (bg, icons) = self.pal, self.btn_items[name]
        hover = name == self.hover
        is_close = name == 'close'
        self.canvas.itemconfigure(bg, state='normal' if hover else 'hidden',
                                  fill=pal['close_hover'] if is_close else pal['btn_hover'])
        icon_color = pal['close_icon'] if (hover and is_close) else pal['btn_fg']
        for item, option in icons:
            self.canvas.itemconfigure(item, **{option: icon_color})

    def _hit_button(self, x, y):
        for name, (x1, y1, x2, y2) in self.buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                return name
        return None

    def _set_hover(self, name):
        if name == self.hover:
            return
        old, self.hover = self.hover, name
        self._paint_button(old)
        self._paint_button(name)

    def _set_click_through(self, pass_clicks):
        if not self.click_through or pass_clicks == self._pass_clicks:
            return
        self._pass_clicks = pass_clicks
        self._apply_window_styles()

    def _mouse_tick(self):
        if self.destroyed:
            return
        try:
            if self.visible and self.u32:
                from ctypes import wintypes
                pt = wintypes.POINT()
                if self.u32.GetCursorPos(ctypes.byref(pt)):
                    name = self._hit_button(pt.x - self.win.winfo_rootx(), pt.y - self.win.winfo_rooty())
                    self._set_hover(name)
                    self._set_click_through(name is None)
        except TclError:
            self.destroyed = True
            return
        except Exception:
            traceback.print_exc()
        try:
            self.mouse_job = self.win.after(self.MOUSE_MS, self._mouse_tick)
        except TclError:
            self.destroyed = True

    def _on_click(self, event):
        name = self._hit_button(event.x, event.y)
        if name == 'close':
            try:
                self.win.after_idle(self.destroy)
            except TclError:
                self.destroy()

    def _draw_labels(self):
        self.canvas.delete('label')
        for letter, (item, box) in self.key_ids.items():
            self._paint_key(letter)
            if letter in self.hints[self.layer]:
                self._draw_label(letter, box, *self.hints[self.layer][letter])

    def _paint_key(self, letter):
        pal = self.pal
        pressed, hinted = letter in self.pressed, letter in self.hints[self.layer]
        self.canvas.itemconfigure(self.key_ids[letter][0], fill=pal['sel'] if pressed else pal['win_bg'],
                                  outline=pal['thumb'] if pressed else pal['sel'] if hinted else pal['win_bg'])

    @staticmethod
    def _wrap_options(text, max_lines=3):
        toks = [(m.start(), m.end()) for m in re.finditer(r'-\s\S+|\S+', text)]
        options = [[(0, len(text))]]
        n = len(toks)
        for k in range(2, min(max_lines, n) + 1):
            for cuts in itertools.combinations(range(1, n), k - 1):
                bounds = (0, *cuts, n)
                options.append([(toks[a][0], toks[b - 1][1]) for a, b in zip(bounds, bounds[1:])])
        options.sort(key=lambda o: (len(o), max(e - s for s, e in o)))
        return options

    @staticmethod
    def _segments(text, line, idx):
        s, e = line
        if idx is not None and s <= idx < e:
            return [(t, acc) for t, acc in ((text[s:idx], False), (text[idx], True), (text[idx + 1:e], False)) if t]
        return [(text[s:e], False)]

    def _fit(self, options, text, idx, max_w, max_h, caption, scale):
        m = self.m
        best = (options[0], m['font_min'], float('inf'))
        for px in range(m['font_px'], m['font_min'] - 1, -1):
            font, big = self._font(px), self._font(round(px * scale), True)
            cap_w = big.measure(caption) + px * 0.35 if caption else 0
            line_h = font.metrics('linespace')
            for opt in options:
                if line_h * len(opt) > max_h:
                    continue
                width = cap_w + max(sum((big if acc else font).measure(t)
                                        for t, acc in self._segments(text, ln, idx)) for ln in opt)
                if width <= max_w:
                    return opt, px
                if px == m['font_min'] and width < best[2]:
                    best = (opt, px, width)
        return best[0], best[1]

    def _draw_label(self, letter, box, word, color_name):
        x1, y1, x2, y2 = box
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        color, accent = self.pal['help'][color_name], self.pal['fg']
        shift = self.layer == 'shift'
        scale = self.BIG_SCALE if shift else 1.0
        idx = pick_highlight(word, letter)
        base = display_word(word)
        if shift and idx is not None:
            base = base[:idx] + base[idx].upper() + base[idx + 1:]
        text = base + self.NOTES.get((self.layer, letter), '')
        caption = None if idx is not None else (letter.upper() if shift else letter)

        lines, px = self._fit(self._wrap_options(text), text, idx,
                              (x2 - x1) * 0.93, (y2 - y1) * 0.8, caption, scale)
        font, big = self._font(px), self._font(round(px * scale), True)
        line_h = font.metrics('linespace')
        measure = lambda t, acc: (big if acc else font).measure(t)
        widths = [sum(measure(t, acc) for t, acc in self._segments(text, ln, idx)) for ln in lines]
        block_w = max(widths)

        put = lambda x, y, s, f, fill: self.canvas.create_text(x, y, text=s, font=f, fill=fill,
                                                               anchor='w', tags='label')
        if caption is not None:
            gap, cap_w = px * 0.35, big.measure(caption)
            x0 = cx - (cap_w + gap + block_w) / 2
            put(x0, cy, caption, big, accent)
            block_cx = x0 + cap_w + gap + block_w / 2
        else:
            block_cx = cx

        for n, (ln, w_line) in enumerate(zip(lines, widths)):
            y = cy + (n - (len(lines) - 1) / 2) * line_h
            x = block_cx - w_line / 2
            for t, acc in self._segments(text, ln, idx):
                put(x, y, t, big if acc else font, accent if acc else color)
                x += measure(t, acc)

    def set_layer(self, layer):
        if layer != self.layer:
            self.layer = layer
            self._draw_labels()

    def set_pressed(self, pressed):
        changed, self.pressed = pressed ^ self.pressed, pressed
        for letter in changed:
            self._paint_key(letter)

    def _sync(self):
        if self._current_theme() != self.theme_name or self._compute_metrics()['sig'] != self.screen_sig:
            self.rebuild()
        if not self.u32:
            return

        if self.close_hotkey and self._down(self.VK_CONTROL) and self._down(self.VK_MENU) and self._down(ord('Q')):
            self.destroy()
            return

        self.set_layer('ctrl' if self._down(self.VK_CONTROL) else 'shift' if self._down(self.VK_SHIFT) else 'normal')
        self.set_pressed({ch for ch in self.key_ids if self._down(ord(ch.upper()))})

    def _tick(self):
        if self.destroyed:
            return
        try:
            if self.own_root and self.u32:
                k_down = self._down(self.VK_CONTROL) and self._down(ord('K'))
                if k_down and not self.k_was_down:
                    self.toggle()
                self.k_was_down = k_down
            if self.visible:
                self._sync()
            if not self.destroyed:
                self.job = self.win.after(self.TICK_MS, self._tick)
        except TclError:
            self.destroyed = True
        except Exception:
            traceback.print_exc()
            try:
                self.job = self.win.after(self.TICK_MS, self._tick)
            except TclError:
                self.destroyed = True

    def show(self):
        if self.destroyed or self.visible:
            return
        try:
            self.visible = True
            self._apply_window_styles()
            self.win.deiconify()
            self.win.attributes('-topmost', 1)
            self._apply_window_styles()
        except TclError:
            self.destroyed = True
            self.visible = False
            raise

    def hide(self):
        if self.destroyed or not self.visible:
            return
        try:
            self.visible = False
            self._set_hover(None)
            self.win.withdraw()
            self.set_pressed(set())
            self.set_layer('normal')
        except TclError:
            self.destroyed = True
            self.visible = False

    def toggle(self):
        (self.hide if self.visible else self.show)()

    def set_theme(self, theme):
        self.theme_arg = theme
        self.rebuild()

    def destroy(self):
        if self.destroyed:
            return
        self.destroyed, self.visible = True, False
        try:
            for job in (self.job, self.mouse_job):
                if job:
                    try:
                        self.win.after_cancel(job)
                    except TclError:
                        pass
            self.win.destroy()
        except TclError:
            pass


_vkb = None
_vkb_args = None


def _is_alive():
    if _vkb is None or _vkb.destroyed:
        return False
    try:
        if not _vkb.win.winfo_exists():
            return False
        _vkb.win.wm_state()
        return True
    except (TclError, AttributeError):
        return False


def keyboard_exists():
    return _is_alive()


def _reset_vkb():
    global _vkb
    dead = _vkb
    _vkb = None
    if dead is not None:
        try:
            dead.destroy()
        except Exception:
            pass


def create_keyboard(master, help_text=None, **kwargs):
    global _vkb, _vkb_args
    if _is_alive():
        return _vkb
    _reset_vkb()
    _vkb_args = (master, help_text, kwargs)
    try:
        _vkb = VirtualKeyboard(master, help_text=help_text, **kwargs)
        _vkb.show()
    except Exception:
        _reset_vkb()
        raise
    return _vkb


def delete_keyboard():
    global _vkb
    existed = _vkb is not None
    _reset_vkb()
    return existed


def show_keyboard():
    if not _is_alive():
        _reset_vkb()
        return
    try:
        _vkb.show()
    except TclError:
        _reset_vkb()


def hide_keyboard():
    if not _is_alive():
        _reset_vkb()
        return
    try:
        _vkb.hide()
    except TclError:
        _reset_vkb()


def recreate_keyboard(theme=None):
    if not _is_alive() or _vkb_args is None:
        return False
    master, help_text, kwargs = _vkb_args
    if theme is not None:
        kwargs = {**kwargs, 'theme': theme}
    delete_keyboard()
    create_keyboard(master, help_text=help_text, **kwargs)
    return True


refresh_keyboard = recreate_keyboard


def toggle_keyboard(master, help_text=None, **kwargs):
    if not _is_alive():
        _reset_vkb()
        create_keyboard(master, help_text=help_text, **kwargs)
    else:
        delete_keyboard()
    return 'break'