"""
virtual_keyboard.py — экранная клавиатура-шпаргалка для строки-калькулятора.

Вместо букв на клавишах — слова-подсказки, которые берутся из help_text (info.help_text
или help.txt рядом со скриптом). Буква клавиши в слове выделена жирным; если её в слове
нет (x^2, умножение, история ...), подпись клавиши стоит слева от слова.

• Цвета — серые тона, подсказки яркие, фон плотный (alpha по умолчанию 0.85).
• Скруглены рамки клавиш; окно пропускает клики мыши.
• Размеры считаются от рабочей области экрана.
• Перенос слов: если подсказка не влезает в клавишу, она переносится на 2-3 строки,
  шрифт уменьшается только когда ни один вариант переноса не помог.
• Слои: зажми Shift — подсказки больших букв, зажми Ctrl — подсказки ctrl+клавиша.
  Нажатая клавиша подсвечивается.

Привязка в calculator.py (ты привязываешь сам):

    from virtual_keyboard import create_keyboard, delete_keyboard, toggle_keyboard

    toggle = lambda e: toggle_keyboard(main_win, help_text=help_text,
                                       theme=lambda: settings['theme'])
    main_win.bind('<Control-k>', toggle)
    entry.bind('<Control-k>', toggle)   # у Entry/Text своя реакция на Ctrl+K — перебиваем её

Функции:
    create_keyboard(master, help_text=None, **kwargs)  — создать и показать
    delete_keyboard()                                  — удалить
    toggle_keyboard(master, help_text=None, **kwargs)  — чередует создание/удаление

Отдельный запуск (Ctrl+K — показать/скрыть, Ctrl+Alt+Q — закрыть):
    python virtual_keyboard.py [--theme dark|light] [--alpha 0.85]
"""
import itertools
import re
import sys
import ctypes
import traceback
from pathlib import Path
from tkinter import Tk, Toplevel, Canvas, TclError, font as tkfont


# ==============================================================================
# ПАЛИТРА — серые тона, подсказки яркие
# ==============================================================================
def get_palette(theme_is_light):
    pick = lambda dark, light: light if theme_is_light else dark
    return {
        'panel_bg': pick('#101010', '#f2f2f2'),  # фон панели
        'win_bg': pick('#262626', '#dcdcdc'),    # фон клавиш
        'fg': pick('#ffffff', '#000000'),        # акцент (выделенная буква)
        'sel': pick('#505050', '#b0b0b0'),       # фон выделения
        'thumb': pick('#a0a0a0', '#666666'),     # рамка нажатой клавиши
        'help': {                                # оттенки серого, заметно ярче
            'black': pick('#f0f0f0', '#1f1f1f'),
            'green': pick('#e0e0e0', '#2e2e2e'),
            'blue': pick('#d2d2d2', '#3d3d3d'),
            'gray': pick('#c4c4c4', '#4c4c4c'),
            'red': pick('#b6b6b6', '#5a5a5a'),
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


# ==============================================================================
# КЛАВИАТУРА
# ==============================================================================
class VirtualKeyboard:
    ROWS = ('qwertyuiop', 'asdfghjkl', 'zxcvbnm')
    ROW_OFFSETS = (0.0, 0.25, 0.75)
    KEY_ASPECT = 1.6
    PAD, GAP = 0.16, 0.09
    WIDTH_FRACTION = 0.9
    HEIGHT_FRACTION = 0.5
    FONT_FAMILY = 'Arial'
    COLOR_KEY = '#ff00ff'
    TICK_MS = 40
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

    @staticmethod
    def _wrap_options(text, max_lines=3):
        """Все варианты переноса по пробелам (тире '- слово' не отрывается от слова).
        Вариант = список (start, end) срезов text. Сначала меньше строк, затем ровнее."""
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
        """Разбивает строку на куски (текст, выделен_ли) — выделена буква клавиши."""
        s, e = line
        if idx is not None and s <= idx < e:
            return [(t, acc) for t, acc in ((text[s:idx], False), (text[idx], True), (text[idx + 1:e], False)) if t]
        return [(text[s:e], False)]

    def _fit(self, options, text, idx, max_w, max_h, caption, scale):
        """Максимально крупный шрифт; к уменьшению шрифта переходим, только если
        не помог ни один вариант переноса."""
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
            if self.own_root and self.u32:  # отдельный запуск: ловим Ctrl+K глобально
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
            self.job = self.win.after(self.TICK_MS, self._tick)

    def show(self):
        if self.destroyed or self.visible:
            return
        try:
            prev_focus = self.master.focus_get()  # куда вернуть фокус после показа
        except (KeyError, TclError):
            prev_focus = None
        self.visible = True
        self._apply_window_styles()  # стили NOACTIVATE до показа, чтобы окно не забирало фокус
        self.win.deiconify()
        self.win.attributes('-topmost', 1)
        self._apply_window_styles()
        if prev_focus is not None and not self.own_root:
            self.master.after(10, lambda: self._restore_focus(prev_focus))

    @staticmethod
    def _restore_focus(widget):
        try:
            widget.focus_force()
        except TclError:
            pass

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


# ==============================================================================
# ФУНКЦИИ ДЛЯ ПРИВЯЗКИ К main_win
# ==============================================================================
_vkb = None  # текущая клавиатура (None, если не создана)
_vkb_args = None  # (master, help_text, kwargs) последнего создания — для пересоздания


def keyboard_exists():
    """True, если клавиатура создана и ещё не удалена (в том числе если скрыта)."""
    if _vkb is None or _vkb.destroyed:
        return False
    try:
        return bool(_vkb.win.winfo_exists())  # окно могло умереть вместе с родителем
    except TclError:
        return False


def create_keyboard(master, help_text=None, **kwargs):
    """СОЗДАТЬ и сразу показать клавиатуру. Если уже есть, ничего не делает."""
    global _vkb, _vkb_args
    if not keyboard_exists():
        _vkb_args = (master, help_text, kwargs)
        _vkb = VirtualKeyboard(master, help_text=help_text, **kwargs)
        _vkb.show()
    return _vkb


def delete_keyboard():
    """УДАЛИТЬ клавиатуру (окно уничтожается)."""
    global _vkb
    if _vkb is not None:
        _vkb.destroy()
        _vkb = None


def recreate_keyboard(theme=None):
    """РАЗРУШИТЬ и заново СОЗДАТЬ клавиатуру, ЕСЛИ она существует.
    theme: новая тема ('dark' / 'light' / 'auto' или функция без аргументов) — клавиатура
    создаётся сразу с ней и запоминает её; None — параметры прежние.
    Возвращает True, если клавиатура была и пересоздана."""
    if not keyboard_exists() or _vkb_args is None:
        return False
    master, help_text, kwargs = _vkb_args
    if theme is not None:
        kwargs = {**kwargs, 'theme': theme}
    delete_keyboard()
    create_keyboard(master, help_text=help_text, **kwargs)
    return True


refresh_keyboard = recreate_keyboard  # старое имя, на всякий случай


def toggle_keyboard(master, help_text=None, **kwargs):
    """Чередует создание и удаление: нечётное нажатие создаёт, чётное удаляет."""
    if not keyboard_exists():
        create_keyboard(master, help_text=help_text, **kwargs)
    else:
        delete_keyboard()
    return 'break'  # не даём Entry/Text выполнить свою реакцию на Ctrl+K


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Клавиатура-шпаргалка калькулятора')
    parser.add_argument('--theme', choices=('auto', 'dark', 'light'), default='auto')
    parser.add_argument('--alpha', type=float, default=0.75, help='0.0 (невидимо) ... 1.0 (непрозрачно)')
    parser.add_argument('--anchor', choices=('bottom', 'center', 'top'), default='bottom')
    parser.add_argument('--help-file', help='путь к help.txt (по умолчанию info.help_text или help.txt рядом)')
    args = parser.parse_args()
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass
    text = Path(args.help_file).read_text(encoding='utf-8-sig') if args.help_file else None
    create_keyboard()
    print('Ctrl+K — показать/скрыть клавиатуру, Shift / Ctrl — другие слои, Ctrl+Alt+Q — закрыть')
    _vkb.master.mainloop()


if __name__ == '__main__':
    main()