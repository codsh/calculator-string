"""
virtual_keyboard.py — почти прозрачная экранная клавиатура-шпаргалка для строки-калькулятора.

Вместо букв на клавишах — слова-подсказки, которые берутся из help_text (info.help_text
или help.txt рядом со скриптом). Буква клавиши в слове выделена жирным; если её в слове
нет (x^2, умножение, история ...), подпись клавиши стоит слева от слова.

• Цвета — все элементы выполнены в серых тонах.
• Скруглены рамки клавиш; окно почти прозрачное (-alpha) и пропускает клики мыши.
• Размеры считаются от рабочей области экрана — подходит любому разрешению.
• Перенос текста: длинные подсказки автоматически переносятся на новую строку для читаемости.
• Слои: зажми Shift — подсказки больших букв (буквы крупные), зажми Ctrl — подсказки
  для ctrl+клавиша. Нажатая клавиша подсвечивается.
• Включение/выключение: удерживай Shift или Ctrl hold_toggle_seconds секунд (пока фокус
  в калькуляторе) — клавиатура включится; ещё раз удержи дольше — выключится.
• Закрытие: нажатие клавиши Esc скрывает клавиатуру.

Подключение в calculator.py (перед main_win.mainloop()):

    from virtual_keyboard import VirtualKeyboard
    vkb = VirtualKeyboard(main_win, help_text=help_text, theme=lambda: settings['theme'],
                          hold_toggle_seconds=5)

Отдельный запуск (закрыть: Ctrl+Alt+Q или Esc):  python virtual_keyboard.py [--theme dark|light] [--alpha 0.35]
"""
import re
import sys
import time
import ctypes
import traceback
from pathlib import Path
from tkinter import Tk, Toplevel, Canvas, TclError, font as tkfont

# ==============================================================================
# ПАЛИТРА — все элементы выполнены в серых тонах
# ==============================================================================
def get_palette(theme_is_light):
    pick = lambda dark, light: light if theme_is_light else dark
    return {
        'panel_bg': pick('#1a1a1a', '#e0e0e0'),  # фон панели
        'win_bg': pick('#2b2b2b', '#d5d5d5'),    # фон окна
        'fg': pick('#cccccc', '#333333'),        # цвет текста / акцент
        'sel': pick('#444444', '#b5b5b5'),       # фон выделения
        'thumb': pick('#888888', '#777777'),     # бегунок
        'help': {                                # все цвета справки — оттенки серого
            'black': pick('#aaaaaa', '#555555'),
            'green': pick('#999999', '#666666'),
            'blue': pick('#888888', '#777777'),
            'gray': pick('#777777', '#888888'),
            'red': pick('#666666', '#555555'),
        },
    }


HELP_COLOR_ORDER = ('black',) * 4 + ('blue', 'green', 'gray') + ('red',) * 4


def help_line_color_name(lines, i):
    """Имя цвета строки i справки — та же логика, что в finish_to_help_win()."""
    tag_rows = (3, 4) + tuple(n + 1 for n, line in enumerate(lines) if not line)
    return HELP_COLOR_ORDER[min(sum(i >= el for el in tag_rows), len(HELP_COLOR_ORDER) - 1)]


# ==============================================================================
# ПОДСКАЗКИ: клавиша -> (регулярка со словом из справки в группе 1, запасное слово)
# ==============================================================================
HINTS = {
    'normal': {
        'q': (r'(Quantize)', 'Quantize - округлить'),
        'w': (r'(poWer)', 'poWer - степень'),
        'e': (r'(константа e)', 'константа e'),
        'r': (r'(Root / Radical)', 'Root / Radical - корень'),
        't': (r'(tg)', 'tg - тангенс'),
        'y': (r'(E-)', 'E-'),
        'u': (r'(парабола)', 'парабола - квадрат'),
        'i': (r'(phI)', 'phI / factorIal'),
        'o': (r'(\(\))', '() - round brackets'),
        'p': (r'(pi)', 'pi - число пи'),
        'a': (r'(abs)', 'abs'),
        's': (r'(sin)', 'sin'),
        'd': (r'(darc)', 'darc'),
        'f': (r'(Factorial)', 'Factorial - факториал !'),
        'g': (r'(lG)', 'lG - log10'),
        'h': (r'(history)', 'history, half'),
        'j': (r'(куб)', 'куб (кубическая парабола)'),
        'k': (r'(Kilo)', 'Kilo'),
        'l': (r'(Log)', 'Log'),
        'z': (r'(Zeros)', 'Zeros'),
        'x': (r'(Умножение)', 'Умножение'),
        'c': (r'(cos)', 'cos'),
        'v': (r'(variable)', 'var - variable - переменная'),
        'b': (r'(base)', 'by - base - основание'),
        'n': (r'(lN)', 'lN - Natural logarythm'),
        'm': (r'(mod)', 'mod'),
    },
    'shift': {
        'q': (r'(quadrillion)', 'Quadrillion - 10^15'),
        'e': (r'(exp)', 'exp - экспонента'),
        't': (r'(Trillion)', 'Trillion - 10^12'),
        'u': (r'(биквадрат)', 'биквадрат'),
        'p': (r'(phi)', 'phi'),
        'f': (r'(Fi)', 'Fi'),
        'c': (r'(Ctg)', 'Ctg'),
        'd': (r'(div)', 'div'),
        'j': (r'(кубическая)', 'кубическая парабола круче'),
        'b': (r'(billion)', 'billion - миллиард'),
        'm': (r'(Million)', 'Million'),
        'a': (r'(модуль)', 'модуль'),
    },
    'ctrl': {
        'q': (r'ctrl\+q \((question)\)', 'question'),
        'i': (r'ctrl\+i \((instruction)\)', 'instruction'),
        'h': (r'ctrl\+h\s*—\s*[^(]*\((история)\)', 'история'),
        'w': (r'(закрывают окно)', 'закрывают окно'),
        'e': (r'ctrl\+e \((edge)', 'edge'),
        'u': (r'ctrl\+u \((up)', 'up'),
        'd': (r'ctrl\+d \((down)', 'down'),
        't': (r'ctrl\+t \((theme)\)', 'theme'),
        'b': (r'ctrl\+b \((big)', 'big'),
        'm': (r'ctrl\+m \((middle)', 'middle'),
        'l': (r'ctrl\+l \((little)', 'little'),
        'f': (r'ctrl\+f (сортирует)', 'сортирует'),
        's': (r'ctrl\+s.*?(в историю)', 'в историю'),
        'z': (r'ctrl\+z перемещает на 1 действие (назад)', 'назад'),
        'y': (r'ctrl\+y\s*—\s*(вперёд)', 'вперёд'),
    },
}


def load_help_text(help_text=None):
    if help_text:
        return help_text
    try:
        from info import help_text as info_help_text
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


# ==============================================================================
# КЛАВИАТУРА
# ==============================================================================
class VirtualKeyboard:
    ROWS = ('qwertyuiop', 'asdfghjkl', 'zxcvbnm')
    ROW_OFFSETS = (0.0, 0.25, 0.75)
    KEY_ASPECT = 1.6
    PAD, GAP = 0.16, 0.09
    WIDTH_FRACTION = 0.62
    HEIGHT_FRACTION = 0.34
    FONT_FAMILY = 'Arial'
    COLOR_KEY = '#ff00ff'
    TICK_MS = 40
    BIG_SCALE = 1.3
    NOTES = {('normal', 'p'): ' π', ('normal', 'i'): ' φ',
             ('shift', 'p'): ' φ', ('shift', 'f'): ' φ'}

    VK_SHIFT, VK_CONTROL, VK_MENU = 0x10, 0x11, 0x12

    def __init__(self, master=None, help_text=None, theme='auto', alpha=0.35, anchor='bottom',
                 margin=0.06, click_through=True, close_hotkey=False,
                 hold_toggle_seconds=None, hold_requires_focus=True):
        self.own_root = master is None
        self.master = Tk() if self.own_root else master
        self.win = self.master if self.own_root else Toplevel(self.master)
        self.win.withdraw()
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', 1)
        self.win.attributes('-alpha', alpha)

        self.theme_arg, self.anchor, self.margin = theme, anchor, margin
        self.click_through, self.close_hotkey = click_through, close_hotkey
        self.hold_seconds, self.hold_requires_focus = hold_toggle_seconds, hold_requires_focus
        self.hold_start, self.hold_fired = None, False
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
        self.theme_name, self.screen_sig = self._current_theme(), None
        self.rebuild()
        self._apply_window_styles()
        self.job = self.win.after(self.TICK_MS, self._tick)

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
            if self.click_through:
                style |= 0x00000020
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
        panel_w = 2 * pad + cols * key_w + (cols - 1) * gap
        panel_h = 2 * pad + rows * key_h + (rows - 1) * gap
        free = round(area_h * self.margin)
        y = {'top': top + free, 'center': top + (area_h - panel_h) // 2}.get(self.anchor, bottom - panel_h - free)
        return {'key_w': key_w, 'key_h': key_h, 'gap': gap, 'pad': pad, 'key_r': key_r,
                'panel_r': key_r + pad,
                'key_line': max(1, round(key_h / 28)),
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

        self.win.geometry(f"{m['w']}x{m['h']}+{m['x']}+{m['y']}")
        self.canvas.config(width=m['w'], height=m['h'], bg=self.COLOR_KEY if self.has_colorkey else pal['win_bg'])
        self.canvas.delete('all')
        self.key_ids.clear()

        rounded_rect(self.canvas, 0, 0, m['w'], m['h'], m['panel_r'], fill=pal['panel_bg'], outline='')
        for row, (letters, offset) in enumerate(zip(self.ROWS, self.ROW_OFFSETS)):
            y1 = m['pad'] + row * (m['key_h'] + m['gap'])
            for col, letter in enumerate(letters):
                x1 = m['pad'] + (col + offset) * (m['key_w'] + m['gap'])
                self.key_ids[letter] = (rounded_rect(self.canvas, x1, y1, x1 + m['key_w'], y1 + m['key_h'], m['key_r'],
                                                     width=m['key_line']), (x1, y1, x1 + m['key_w'], y1 + m['key_h']))
        self._draw_labels()

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

    def _fit(self, options, max_w, max_h, caption, scale):
        """Подбирает оптимальный размер шрифта, отдавая предпочтение многострочным вариантам."""
        def best_px(opt_lines):
            px = self.m['font_px']
            while px > self.m['font_min']:
                font, big = self._font(px), self._font(round(px * scale), True)
                width = max(font.measure(line) for line in opt_lines)
                if caption:
                    width += big.measure(caption) + px * 0.35
                elif len(opt_lines) == 1 and scale > 1:
                    width += (scale - 1) * px * 0.7
                height = font.metrics('linespace') * len(opt_lines)
                if width <= max_w and height <= max_h:
                    break
                px -= 1
            return px

        best_opt = options[0]
        best_px_val = best_px(options[0])

        for opt in options[1:]:
            p = best_px(opt)
            if p >= best_px_val * 1.15:  # если перенос позволяет сделать шрифт крупнее — выбираем его
                best_opt, best_px_val = opt, p
        return best_opt, best_px_val

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
        note = self.NOTES.get((self.layer, letter), '')
        caption = None if idx is not None else (letter.upper() if shift else letter)

        # Варианты отображения: одна строка или с переносом на вторую строку
        options = [[base + note]]
        has_multi = False
        
        if not note and idx is not None and ' - ' in base:
            parts = base.split(' - ', 1)
            if idx < len(parts[0]):
                options.append([parts[0], '- ' + parts[1]])
                has_multi = True
        elif not note and idx is None:
            if ' ' in base:
                parts = base.split(' ')
                cut = min(range(1, len(parts)), key=lambda n: abs(len(' '.join(parts[:n])) - len(' '.join(parts[n:]))))
                options.append([' '.join(parts[:cut]), ' '.join(parts[cut:])])

        lines, px = self._fit(options, (x2 - x1) * 0.93, (y2 - y1) * 0.8, caption, scale)
        font, big = self._font(px), self._font(round(px * scale), True)
        
        put = lambda x, y, s, f, fill, anchor: self.canvas.create_text(x, y, text=s, font=f, fill=fill,
                                                                        anchor=anchor, tags='label')
        
        if caption is not None:
            gap, cap_w = px * 0.35, big.measure(caption)
            block_w, line_h = max(font.measure(line) for line in lines), font.metrics('linespace')
            x = cx - (cap_w + gap + block_w) / 2
            put(x, cy, caption, big, accent, 'w')
            for n, line in enumerate(lines):
                put(x + cap_w + gap + block_w / 2, cy + (n - (len(lines) - 1) / 2) * line_h, line, font, color, 'center')
        elif len(lines) == 2 and has_multi:
            line_h = font.metrics('linespace')
            for n, line in enumerate(lines):
                y = cy + (n - 0.5) * line_h
                if n == 0:
                    term = line
                    pre, ch, suf = term[:idx], term[idx], term[idx + 1:] + note
                    w_pre, w_ch, w_suf = font.measure(pre), big.measure(ch), font.measure(suf)
                    x = cx - (w_pre + w_ch + w_suf) / 2
                    if pre:
                        put(x, y, pre, font, color, 'w')
                    put(x + w_pre, y, ch, big, accent, 'w')
                    if suf:
                        put(x + w_pre + w_ch, y, suf, font, color, 'w')
                else:
                    w_line = font.measure(line)
                    put(cx - w_line / 2, y, line, font, color, 'w')
        elif len(lines) > 1 and idx is None:
            line_h = font.metrics('linespace')
            for n, line in enumerate(lines):
                w_line = font.measure(line)
                put(cx - w_line / 2, cy + (n - (len(lines) - 1) / 2) * line_h, line, font, color, 'w')
        else:
            pre, ch, suf = base[:idx], base[idx], base[idx + 1:] + note
            w_pre, w_ch, w_suf = font.measure(pre), big.measure(ch), font.measure(suf)
            x = cx - (w_pre + w_ch + w_suf) / 2
            if pre:
                put(x, cy, pre, font, color, 'w')
            put(x + w_pre, cy, ch, big, accent, 'w')
            if suf:
                put(x + w_pre + w_ch, cy, suf, font, color, 'w')

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
        
        if self._down(0x1B):  # Закрыть / скрыть по Esc
            self.hide()
            return

        if self.close_hotkey and self._down(self.VK_CONTROL) and self._down(self.VK_MENU) and self._down(ord('Q')):
            self.destroy()
            return
            
        self.set_layer('ctrl' if self._down(self.VK_CONTROL) else 'shift' if self._down(self.VK_SHIFT) else 'normal')
        self.set_pressed({ch for ch in self.key_ids if self._down(ord(ch.upper()))})

    def _check_hold(self):
        if not self.hold_seconds or not self.u32:
            return
        held = self._down(self.VK_SHIFT) or self._down(self.VK_CONTROL)
        if held and self.hold_requires_focus and self.master.focus_displayof() is None:
            held = False
        if not held:
            self.hold_start, self.hold_fired = None, False
        elif self.hold_start is None:
            self.hold_start = time.monotonic()
        elif not self.hold_fired and time.monotonic() - self.hold_start >= self.hold_seconds:
            self.hold_fired = True
            self.toggle()

    def _tick(self):
        if self.destroyed:
            return
        try:
            self._check_hold()
            if self.visible:
                self._sync()
            if not self.destroyed:
                self.job = self.win.after(self.TICK_MS, self._tick)
        except TclError:
            self.destroyed = True
        except Exception:
            traceback.print_exc()
            self.job = self.win.after(self.TICK_MS, self._tick)

    def show(self):
        if self.destroyed or self.visible:
            return
        self.visible = True
        self.win.deiconify()
        self.win.attributes('-topmost', 1)
        self._apply_window_styles()

    def hide(self):
        if self.destroyed or not self.visible:
            return
        self.visible = False
        self.win.withdraw()
        self.set_pressed(set())
        self.set_layer('normal')

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
            if self.job:
                self.win.after_cancel(self.job)
            self.win.destroy()
        except TclError:
            pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Прозрачная клавиатура-шпаргалка калькулятора')
    parser.add_argument('--theme', choices=('auto', 'dark', 'light'), default='auto')
    parser.add_argument('--alpha', type=float, default=0.35, help='0.0 (невидимо) ... 1.0 (непрозрачно)')
    parser.add_argument('--anchor', choices=('bottom', 'center', 'top'), default='bottom')
    parser.add_argument('--help-file', help='путь к help.txt (по умолчанию info.help_text или help.txt рядом)')
    args = parser.parse_args()
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass
    text = Path(args.help_file).read_text(encoding='utf-8-sig') if args.help_file else None
    keyboard_overlay = VirtualKeyboard(None, help_text=text, theme=args.theme, alpha=args.alpha,
                                       anchor=args.anchor, close_hotkey=True)
    keyboard_overlay.show()
    print('Клавиатура показана. Shift / Ctrl — другие слои, Esc — скрыть, Ctrl+Alt+Q — закрыть')
    keyboard_overlay.master.mainloop()


if __name__ == '__main__':
    main()