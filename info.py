import winreg
import pyautogui
import ctypes
import re

from collections import Counter
from decimal import *

FILES = 'data'
DAY = 60 * 60 * 24

getcontext().prec = 1402
def zeros(x):
    return Decimal('.' + x * '0') if x > 0 else Decimal(f'1e{abs(x)}')

def rond(num, rounding_accuracy):
    return num.quantize(rounds[rounding_accuracy], ROUND_HALF_UP)

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
united_symbols_with_scopes = (tuple(f'{i}{j}' for j in ('|', '(') for i in darc_generator)
     + ('log(', 'sin(', 'cos(', 'ctg(', ')by(') + ('log|', 'sin|', 'cos|', 'ctg|', '|by|', '|by(', ')by|') + ('ln|', 'lg|', 'tg|') + ('ln(', 'lg(', 'tg('))
united_symbols_without_scopes = darc_generator + ('sin', 'cos', 'ctg', 'tg', 'ln', 'lg')  # порядок важен, сначала котангенс а лишь потом тангенс, чтобы удалялся ctg а не c tg
full_funcs_with_Uu = tuple((f'{i}{j}' for i in ('sin', 'cos', 'tg', 'ctg', 'lg', 'ln') for j in ('()', 'Uu'))) + tuple((f'log{i}by{j}' for i in ('()', 'Uu') for j in ('()', 'Uu')))

special_keys = ('Up', 'Down', 'Left', 'Right', 'Control_L', 'Return', 'grave', 'Tab', 'changed text', 'Win_L'
                'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Escape', 'Caps_Lock', 'apostrophe', 'quotedbl', 'braceleft', 'braceright')
ghost_keys = ('Up', 'Down', 'Left', 'Right', 'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Caps_Lock')
keys_after_dot = ('minus', 'equal', 'slash', 'semicolon', 'backslash', 'bracketleft', 'bracketright')
last_keys = ['' for _ in range(20)]

rounds = [zeros(_) for _ in (400, 380, 360, 305, 100)]
ending_symbols = list('+-•:^,%@k.') + list(united_symbols)
correct_answer_num_symbols = '0123456789Ee-+.•^() '
letters_and_inwords, letters_and_not_example_like_inwords, syntax = r'[а-яА-ЯЁё"\'«»“”()-]', r'[а-яА-ЯЁё"\'«»“”]', r'(?:[.,!?;:/—–]|\s[—–]|\s-\s(?=\w|\d+-\w))'
last_time_main_win_geometry_change = 0
last_val_before_geometry_change = 'если это вставится, значение использовали до его определения !!!техническая ошибка разработчиков!!!'
last_time_round_change = 0
num_construct = r'((?:\d+[.,]?\d*|\.\d+)(?:[eE]-?\d*[.,]?\d*)?|[φπeE])'
word_construct = '[а-яА-ЯЁё]+'
tokenator = r'(d?(?:arc)?(?:sin|cos|c?tg)|d?arc|ln|lg|√|log|by|(?<![\d.])e(?![\d.])|d(?!iv)|\+|=|!|div|mod|\||•|/|:|\^|(?:(?<!\()(?<![\d.]e))\-|\(|\))'
super_tokenator = r'(sin|cos|c?tg|arc|ln|lg|√|log|by|(?<![\d.])e(?![\d.])|d(?!iv)|\+|=|!|div|mod|\||•|/|:|\^|(?:(?<!\()(?<![\d.]e))\-|\(|\)|[\dφπeE.])'
ultra_tokenator = fr'([а-яА-ЯЁё]|\d|{super_tokenator})'

max_denominator = 10000

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

with open('help.txt', 'r', encoding='utf-8') as help_file:
    help_text = help_file.read()


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

# --------------------
screen_width, screen_height = pyautogui.size()

# Получить высоту панели задач
def get_taskbar_height():
    SPI_GETWORKAREA = 48
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    taskbar_height = screen_height - (rect.bottom - rect.top)
    return taskbar_height


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


def is_russian_layout() -> bool:
    """
    Проверяет, активна ли русская раскладка клавиатуры в текущем окне.
    Возвращает True для русской раскладки, False для остальных случаев.
    """
    user32 = ctypes.windll.user32
    
    # Получаем дескриптор активного окна и его поток
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    
    # Получаем идентификатор раскладки клавиатуры
    keyboard_layout = user32.GetKeyboardLayout(thread_id)
    language_id = keyboard_layout & 0xFFFF  # Извлекаем младшие 16 бит
    
    # Русская раскладка имеет код 0x0419
    return language_id == 0x0419


keyboard_layout_memory = ('en', 'ru')[is_russian_layout()]
