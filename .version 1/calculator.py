from tkinter import *
from tkinter import font, messagebox, ttk
import math
from decimal import *
import json
import datetime
import pyautogui
pyautogui.FAILSAFE = False


global settings_of_calculator, the_entry_for_example, date_time_calc, verify_but_getto_calc
global max_amount_of_examples_in_history_of_calculations

with open('calc history.json', 'r') as file_history_calc:
    try:
        history_of_calculations = json.load(file_history_calc)
    except json.decoder.JSONDecodeError:
        history_of_calculations = '0\n0\nПервое использование программмы: ' + str(datetime.datetime.today())[:-7]
with open('calc settings.json', 'r') as file_settings_calc:
    try:
        settings_of_calculator = json.load(file_settings_calc)
    except json.decoder.JSONDecodeError:
        settings_of_calculator = {
            "messagebox": True,
            "color": "standard",
            "geometry": ["300", "225"],
            "history length": "1000"}
max_amount_of_examples_in_history_of_calculations = int(settings_of_calculator["history length"])

wodden_calc = 0
flag_wodden_calc = 1
light_gamma_calc = []
for swits_calc in range(20):
    light_gamma_calc.append('black')
for swits_calc in range(40):
    light_gamma_calc.append('white')
walmart_calc = cornalt_calc = tallnut_calc = flag_exist_universe_calc = flag_smart_focus_calc = False
switch_astro_calc = True
switch_star_calc = False
switch_meteor_calc = False
getcontext().prec = 1402
astro_calc = Tk()
astro_calc.title('Калькулятор.')

astro_calc.iconbitmap('calc imgs/calculator_icon.ico')

emoji_bg_image_calc = PhotoImage(file='calc imgs/btn_emoji_history_calculator.png')
silver_bg_image_calc = PhotoImage(file='calc imgs/background_silver_calculator_style.png')
red_bg_image_calc = PhotoImage(file='calc imgs/background_red_calculator_style.png')
green_bg_image_calc = PhotoImage(file='calc imgs/background_green_calculator_style.png')
blue_bg_image_calc = PhotoImage(file='calc imgs/background_blue_calculator_style.png')
yellow_bg_image_calc = PhotoImage(file='calc imgs/background_yellow_calculator_style.png')
magenta_bg_image_calc = PhotoImage(file='calc imgs/background_magenta_calculator_style.png')
cyan_bg_image_calc = PhotoImage(file='calc imgs/background_cyan_calculator_style.png')
purple_bg_image_calc = PhotoImage(file='calc imgs/background_purple_calculator_style.png')
violet_bg_image_calc = PhotoImage(file='calc imgs/background_violet_calculator_style.png')
pink_bg_image_calc = PhotoImage(file='calc imgs/background_pink_calculator_style.png')
orange_bg_image_calc = PhotoImage(file='calc imgs/background_orange_calculator_style.png')
lime_bg_image_calc = PhotoImage(file='calc imgs/background_lime_calculator_style.png')
skyblue_bg_image_calc = PhotoImage(file='calc imgs/background_skyblue_calculator_style.png')
gold_bg_image_calc = PhotoImage(file='calc imgs/background_gold_calculator_style.png')
emerald_bg_image_calc = PhotoImage(file='calc imgs/background_emerald_calculator_style.png')
standard_bg_image_calc = PhotoImage(file='calc imgs/background_standard_calculator_style.png')
ruby_bg_image_calc = PhotoImage(file='calc imgs/background_ruby_calculator_style.png')
sapphire_bg_image_calc = PhotoImage(file='calc imgs/background_sapphire_calculator_style.png')
group_bg_image_calc = PhotoImage(file='calc imgs/background_group_calculator_style.png')
rainbow_bg_image_calc = PhotoImage(file='calc imgs/background_rainbow_calculator_style.png')
ruby_bt_image_calc = PhotoImage(file='calc imgs/button_ruby_calculator_style.png')
sapphire_bt_image_calc = PhotoImage(file='calc imgs/button_sapphire_calculator_style.png')
rainbow_bt_image_calc = PhotoImage(file='calc imgs/button_rainbow_calculator_style.png')
group_bt_image_calc = PhotoImage(file='calc imgs/button_group_calculator_style.png')


def solver_of_the_example():
    global example, entry_that_get_information_of_rounding, the_entry_for_example, beluga_calc
    global max_amount_of_examples_in_history_of_calculations, verify_but_getto_calc
    example = the_entry_for_example.get()
    words_that_can_open_windows = ['история', 'history', 'examples', 'примеры', 'recent', 'недавнее'] + \
                                  ['design', 'дизайн', 'style', 'стиль', 'display', 'дисплей'] + \
                                  ['help', 'помощь', 'помогите', 'hint', 'совет']
    pi_calc = Decimal('3.1415926535897932384626433832795028841971693993'
                      '7510582097494459230781640628620899862803482534211'
                      '7067982148086513282306647093844609550582231725359'
                      '4081284811174502841027019385211055596446229489'
                      '54930381964428810975665933446128475648233786783165'
                      '271201909145648566923460348610454326648213393')

    e_calc = Decimal('2.71828182845904523536028747135266249775724709'
                     '3699959574966967627724076630353547594571382178525'
                     '16642742746639193200305992181741359662904357290033'
                     '42952605956307381323286279434907632338298807531952510'
                     '19011573834187930702154089149934884167509244761460668'
                     '0822648001684774118537423454424371075390777449920')

    BB_calc = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-', 'E', '+']
    CC_calc = '0123456789,'
    santa1_calc = Decimal('.' + 400 * '0')
    santa2_calc = Decimal('.' + 380 * '0')
    santa3_calc = Decimal('.' + 360 * '0')
    santa4_calc = Decimal('.' + 300 * '0')
    santa5_calc = Decimal('.' + 7 * '0')
    symbols_that_can_be_in_replaced_example = '0123456789+-*:^,%@!()Uu'

    words_that_can_change_design = ['silver', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'purple', 'violet',
                                    'pink', 'gold', 'classic', 'lime', 'sky', 'sapphire', 'emerald', 'standard',
                                    'ruby', 'group', 'rainbow', 'normal', 'orange', 'обычный', 'стандарт', 'радуга',
                                    'радужный', 'группа', 'рубин', 'розовый', 'желтый', 'классика', 'изумрудный',
                                    'золотой', 'голубой', 'лайм', 'салатовый', 'циан', 'магента', 'синий', 'оранжевый',
                                    'фиолетовый', 'пурпур', 'маджента', 'зеленый', 'серебряный', 'красный', 'сапфир',
                                    'жёлтый', 'зелёный']
    if len(entry_that_get_information_of_rounding.get()) > 3:
        information_of_rounding_number = entry_that_get_information_of_rounding.get()[:3]
    else:
        information_of_rounding_number = entry_that_get_information_of_rounding.get()
    for destroy_smartphone_calc in information_of_rounding_number:
        if destroy_smartphone_calc not in '0123456789':
            information_of_rounding_number = information_of_rounding_number.replace(destroy_smartphone_calc, '?')
    information_of_rounding_number = information_of_rounding_number.replace('?', '')
    entry_that_get_information_of_rounding.delete(0, END)
    entry_that_get_information_of_rounding.insert(END, information_of_rounding_number)
    if example in words_that_can_change_design:
        return 'Стиль "' + example + '" установлен.'
    if example in words_that_can_open_windows:
        return 'Открыт раздел "' + example + '".'
    if len(entry_that_get_information_of_rounding.get()) == 0:
        miss_you_calc = 10
    else:
        merlin_monro_calc = True
        for trink_trank_calc in entry_that_get_information_of_rounding.get():
            if trink_trank_calc not in '0123456789':
                merlin_monro_calc = False
                break
        if len(entry_that_get_information_of_rounding.get()) > 1 and \
                entry_that_get_information_of_rounding.get()[0] == '0':
            return 'Неверно установлено округление!'
        elif merlin_monro_calc:
            if int(entry_that_get_information_of_rounding.get()) <= 100:
                miss_you_calc = int(entry_that_get_information_of_rounding.get())
            else:
                return 'Округление должно быть не более ста знаков после запятой!'
        else:
            return 'Неверно установлено округление!'
    if example == '':
        return 'Введите пример!'
    else:
        if ' ' in example and len(set(example)) == 1:
            return 'Зачем Вам пробелы?'
    example = str.lower(example)
    if len(example) != 0 and example[0] == '#' and example[-1] == '#' and example.count('#') == 2:
        if example == '#true#':
            settings_of_calculator["messagebox"] = True
            return 'Теперь калькулятор застрахует от случайного выхода.'
        elif example == '#false#':
            settings_of_calculator["messagebox"] = False
            return 'Калькулятор больше не застрахует от случайного выхода.'
        elif example.count(';') == 1:
            simpai_calc = example.split(';')
            try:
                if 0 <= int(simpai_calc[0][1:]) <= 360 and 0 <= int(simpai_calc[1][:-1]) <= 520:
                    settings_of_calculator['geometry'] = [simpai_calc[0][1:], simpai_calc[1][:-1]]
                    verify_but_getto_calc = '600x450+' + settings_of_calculator['geometry'][0] + '+' + \
                                            settings_of_calculator['geometry'][1]
                    astro_calc.geometry(verify_but_getto_calc)
                    return 'Место появления калькулятора настроено!'
                else:
                    if int(simpai_calc[0][1:]) > 360 or int(simpai_calc[0][1:]) < 0:
                        return 'Координата по иксу больше 360-ти или меньше нуля!'
                    else:
                        return 'Координата по игреку больше 520-ти или меньше нуля!'
            except ValueError:
                return 'Координата по иксу или игреку должна быть числом!'
        elif example.count(';') == 0 and len(example) >= 4 and example[:4] == '#his':
            try:
                if example == '#his':
                    return 'Настройки размера памяти истории вычислений активированы.'
                elif 10 <= int(example[4:-1]) <= 10000:
                    his_step_calc = int(example[4:-1])
                    settings_of_calculator["history length"] = str(his_step_calc * 4)
                    max_amount_of_examples_in_history_of_calculations = int(settings_of_calculator["history length"])
                    return 'Теперь длина истории вычислений — ' + example[4:-1] + ' примеров.'
                else:
                    return 'Нельзя писать число больше 10000 или меньше 100!'
            except ValueError:
                return 'Ошибка! Длина истории вычислений должна быть числом!'
        else:
            do_nothing_calc = 0
            do_nothing_calc += 1
    elif len(example) != 0 and example[0] == '#' and example.count('#') == 1:
        if len(example) >= 4 and example[:4] == '#cpu':
            return 'Настройки частоты проверки примера активированы.'
        elif len(example) >= 4 and example[:4] == '#his':
            return 'Настройки размера памяти истории вычислений активированы.'
        else:
            return 'Настройки калькулятора активированы.'
    else:
        do_nothing_calc = 0
        do_nothing_calc += 1
    if '$' in example:
        return 'Почему символ "$" есть в примере?'
    pi_replace_calc = ('(' + str(pi_calc) + '*' + '1)')
    e_replace_calc = ('(' + str(e_calc) + '*' + '1)')
    example = example.replace('pip', '(180+0)').replace('пип', '(180+0)').replace('base', '_')
    example = example.replace('x', '*').replace('х', '*').replace('•', '*')
    example = example.replace('лг', 'lg').replace('лн', 'ln')
    example = example.replace('mod', '%').replace('мод', '%').replace('ost', '%').replace('ост', '%')
    example = example.replace('m', '|').replace('м', '|')
    example = example.replace('pi', 'π').replace('пи', 'π').replace('π', pi_replace_calc).replace('div', '@')
    example = example.replace('::', '@').replace('//', '@').replace('cel', '@').replace('цел', '@')
    example = example.replace('**', '^').replace('/', ':').replace('.', ',').replace(' ', '')
    example = example.replace('fact', 'f').replace('fa', 'f').replace('факт', 'f')
    example = example.replace('cotan', 'ct').replace('котан', 'ct')
    example = example.replace('sin', 'sn').replace('син', 'sn')
    example = example.replace('cos', 'cs').replace('кос', 'cs').replace('лог', 'log')
    example = example.replace('tan', 'tg').replace('тан', 'tg').replace('tn', 'tg')
    example = example.replace('ctg', 'ct').replace('ctn', 'ct').replace('ктн', 'ct')
    example = example.replace('e', 'е').replace('е', e_replace_calc)
    example = example.replace('√', '$').replace('к', '$').replace('k', '$').replace('r', '$')
    example = example.replace('по', '_').replace('to', '_').replace('po', '_')
    example = example.replace('_', ')_').replace('log', 'log(')
    if len(example) != 0 and example[0] == '|':
        example = 'U' + example[1:]
    while '|' in example:
        for nightmared_calc in range(len(example) - 1):
            if example[nightmared_calc + 1] == '|':
                if example[nightmared_calc] in '0123456789!)u':
                    example = example[:nightmared_calc + 1] + 'u' + example[nightmared_calc + 2:]
                else:
                    example = example[:nightmared_calc + 1] + 'U' + example[nightmared_calc + 2:]
    for chok_calc in '+-*:@%^':
        for talk_calc in '+-*:@%^':
            for smoke_calc in '+-*:@%^':
                if (chok_calc + talk_calc + smoke_calc) in example:
                    return 'Ошибка: какие-то из двух-трёх символов не должны быть соседними!'
    moskitos_calc = example.replace('log', '<').replace('_', '>')
    if len(example) != 0 and example[0] == '$':
        example = '2k' + example[1:]
    while '$' in example:
        for string_calc in range(len(example) - 1):
            if example[string_calc + 1] == '$':
                if example[string_calc] not in '0123456789,)u!':
                    example = example[:string_calc + 1] + '2k' + example[string_calc + 2:]
                else:
                    example = example[:string_calc + 1] + 'k' + example[string_calc + 2:]
    if len(example) != 0 and example[0] == '-':
        example = '(0-1)*' + example[1:]
    example = example.replace('+-', '-').replace('--', '+')
    example = example.replace('*-', '*(0-1)*').replace(':-', ':(0-1):')
    nintendo_calc = example
    example = example.replace('sn', '1+1-').replace('cs', '1+1-')
    example = example.replace('ct', '1+1-').replace('tg', '1+1-')
    example = example.replace('lg', '1+1-').replace('ln', '1+1-').replace('_', '+')
    example = example.replace('f', '1+1-').replace('k', '+1-').replace('log', '1+1-')
    example = example.replace('2.718281828459045', '1+1')
    example = example.replace('^-', '+')
    example = example.replace('+-', '-').replace('--', '+')
    triumth_calc = ['sn', 'cs', 'tg', 'ct', 'k']
    for egg_calc in '+*:^,)%@!u':
        for bird_calc in triumth_calc:
            if (bird_calc + egg_calc) in nintendo_calc:
                return 'В примере после одной из функций стоит не тот символ!'
    tragedy_calc = ['lg', 'ln', 'f', 'log']
    for bear_calc in '+*:^,)%@-0!u':
        for fox_calc in tragedy_calc:
            if fox_calc + '-' in nintendo_calc:
                return 'Число, находящееся после функции, со знаком минус берётся в скобки!'
            if ((fox_calc + bear_calc) in nintendo_calc) and ((fox_calc + '0,') not in nintendo_calc) \
                    and ('f0' not in nintendo_calc):
                return 'В примере после одной из функций ошибка!'
    triplex_calc = ['sn', 'cs', 'tg', 'ct', 'f', 'lg', 'ln', 'log']
    for devil_calc in '0123456789,.':
        for birthday_calc in triplex_calc:
            if (devil_calc + birthday_calc) in nintendo_calc:
                return 'В примере перед одной из функций стоит не тот символ!'
    for item_calculator in example:
        if item_calculator not in symbols_that_can_be_in_replaced_example:
            return 'Почему символ  "' + item_calculator + '" есть в примере?'
    for iti_calc in symbols_that_can_be_in_replaced_example:
        for jtj_calc in symbols_that_can_be_in_replaced_example:
            taraban_calc = iti_calc + jtj_calc
            if iti_calc in '(U' and jtj_calc in '+*:^),@%u' or jtj_calc in 'u)!' and iti_calc in '+-*:^(,@%U':
                if taraban_calc in example:
                    return 'Около скобки, модуля или факториала или числа e, pi, pip ошибка!'
            if jtj_calc in '(U' and iti_calc in CC_calc or iti_calc in 'u)!' and jtj_calc in CC_calc:
                if taraban_calc in example:
                    return 'Около скобки, модуля или факториала или числа e, pi, pip ошибка!'
    for ktk_calc in symbols_that_can_be_in_replaced_example[10:18]:
        for mtm_calc in symbols_that_can_be_in_replaced_example[10:18]:
            if (ktk_calc + mtm_calc) in example:
                return 'Ошибка! Два элемента в примере, которые не могут стоять рядом!'
    chosen_calc = example
    if ',' in chosen_calc:
        chosen_calc = chosen_calc.replace(',', '#')
        mog_calc = chosen_calc.split('#')
        mog_calc = mog_calc[1:-1]
        if len(mog_calc) != 0:
            for pink_calc in mog_calc:
                mukad_calc = True
                for red_calc in pink_calc:
                    if red_calc in '+-*:^%@':
                        mukad_calc = False
                        break
                if mukad_calc:
                    return 'Почему в одном числе две запятые или точки?'
    truck_calc = '+-*:^,%@!'
    syren_calc = '0123456789'
    if len(example) >= 2 and example[0] == '0' and example[1] not in truck_calc:
        return 'Почему в примере введено"' + example[0] + example[1] + '" ?'
    else:
        if len(example) >= 3:
            for fim_calc in range(len(example) - 2):
                if (example[fim_calc] in '+-*:^@%') and (example[fim_calc + 1] == '0'):
                    if example[fim_calc + 2] in syren_calc:
                        meow2_calc = example[fim_calc + 1]
                        meow3_calc = example[fim_calc + 2]
                        return 'Почему в примере введено"' + meow2_calc + meow3_calc + '" ?'
    if len(example) != 0 and example[0] in '+*:^,%@!':
        return 'Ошибка в начале примера!'
    if len(example) != 0 and example[-1] in '+-*:^,%@k':
        return 'Ошибка в конце примера!'
    sword_calc = []
    for status_calc in range(len(moskitos_calc)):
        if moskitos_calc[status_calc] in '()Uu<>':
            sword_calc.append(moskitos_calc[status_calc])
    for sport_calc in range(500):
        for ghost_calc in range(len(sword_calc) - 1):
            if sword_calc[ghost_calc] == '(' and sword_calc[ghost_calc + 1] == ')':
                sword_calc[ghost_calc] = 's'
                sword_calc[ghost_calc + 1] = 's'
            elif sword_calc[ghost_calc] == 'U' and sword_calc[ghost_calc + 1] == 'u':
                sword_calc[ghost_calc] = 's'
                sword_calc[ghost_calc + 1] = 's'
            elif sword_calc[ghost_calc] == '<' and sword_calc[ghost_calc + 1] == '>':
                sword_calc[ghost_calc] = 's'
                sword_calc[ghost_calc + 1] = 's'
        while 's' in sword_calc:
            sword_calc.remove('s')
    if len(sword_calc) != 0:
        return 'Что-то не так со скобками, модулем или логарифмом!'
    example = nintendo_calc
    try:
        for check_minus_not_calc in ['k-', 'sn-', 'cs-', 'tg-', 'ct-', '_-']:
            if check_minus_not_calc in example:
                return 'Нельзя число или выражение со знаком минус брать без скобок!'
        calcuso = example.replace('^-', '&')
        calcuso = calcuso.replace(',', '.').replace('+', ' + ').replace('!', ' ! ')
        calcuso = calcuso.replace('@', ' @ ').replace('%', ' % ').replace('(-', '((0-1)*')
        calcuso = calcuso.replace('U-', 'U(0-1)*').replace('U', ' U ').replace('u', ' u ')
        calcuso = calcuso.replace('*', ' * ').replace(':', ' : ').replace('^', ' ^ ')
        calcuso = calcuso.replace('-', ' - ').replace('(', ' ( ').replace(')', ' ) ').replace('&', ' ^- ')
        calcuso = calcuso.replace('sn', ' sn ').replace('cs', ' cs ')
        calcuso = calcuso.replace('tg', ' tg ').replace('ct', ' ct ')
        calcuso = calcuso.replace('ln', ' ln ').replace('lg', ' lg ')
        calcuso = calcuso.replace('f', ' f ').replace('k', ' k ').replace('log', ' log ').replace('_', ' _ ')
        tota_calc = calcuso.split(' ')
        while '' in tota_calc:
            tota_calc.remove('')
        calcor_stop = 0
        calcor_start = -1
        while '(' in tota_calc or 'U' in tota_calc:
            for calcor in range(len(tota_calc)):
                if tota_calc[calcor] == '(':
                    calcor_start = calcor
                if tota_calc[calcor] == 'U':
                    calcor_start = calcor
                if tota_calc[calcor] == ')' and tota_calc[calcor_start] == '(':
                    calcor_stop = calcor
                    break
                if tota_calc[calcor] == 'u' and tota_calc[calcor_start] == 'U':
                    calcor_stop = calcor
                    break
            tane_calc = tota_calc[calcor_start:calcor_stop + 1]
            tune_calc = tane_calc[1:-1]
            twix_calc = ('sn' in tune_calc or 'cs' in tune_calc or 'tg' in tune_calc)
            tromb_calc = ('ct' in tune_calc or 'ln' in tune_calc or 'lg' in tune_calc)
            goose_calc = ('k' in tune_calc or '!' in tune_calc or 'f' in tune_calc or 'log' in tune_calc)
            while twix_calc or tromb_calc or goose_calc:
                for lila_calc in range(len(tune_calc) - 1):
                    treider_calc = len([ti_calc for ti_calc in tune_calc[lila_calc]])
                    tryider_calc = len([ri_calc for ri_calc in tune_calc[lila_calc] if ri_calc in BB_calc])
                    if tune_calc[lila_calc + 1] == '!' and tryider_calc == treider_calc:
                        if Decimal(tune_calc[lila_calc]).quantize(santa4_calc, ROUND_HALF_UP) < 0:
                            return 'Факториала неположительного числа не существует!'
                        elif Decimal(tune_calc[lila_calc]).quantize(santa2_calc, ROUND_HALF_UP) % 1 == 0:
                            wild_calc = math.factorial(int(Decimal(tune_calc[lila_calc])))
                            tune_calc[lila_calc + 1] = str(wild_calc)
                        else:
                            return 'Факториал только натурального числа!'
                        tune_calc[lila_calc] = 'R'
                while 'R' in tune_calc:
                    tune_calc.remove('R')
                for lila_calc in range(len(tune_calc) - 2, -1, -1):
                    treider_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 1]])
                    tryider_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 1] if ri_calc in BB_calc])
                    if tune_calc[lila_calc] == 'f' and tryider_calc == treider_calc:
                        if Decimal(tune_calc[lila_calc + 1]).quantize(santa4_calc, ROUND_HALF_UP) < 0:
                            return 'Факториала неположительного числа не существует!'
                        elif Decimal(tune_calc[lila_calc + 1]).quantize(santa2_calc, ROUND_HALF_UP) % 1 == 0:
                            wild_calc = math.factorial(int(Decimal(tune_calc[lila_calc + 1])))
                            tune_calc[lila_calc] = str(wild_calc)
                        else:
                            return 'Факториал только натурального числа!'
                        tune_calc[lila_calc + 1] = 'R'
                while 'R' in tune_calc:
                    tune_calc.remove('R')
                for lila_calc in range(len(tune_calc) - 3, -1, -1):
                    lord_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 2]])
                    blurple_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 2] if ri_calc in BB_calc])
                    if tune_calc[lila_calc + 1] == 'k' and blurple_calc == lord_calc:
                        zombie_comes_calc = abs(Decimal(tune_calc[lila_calc]))
                        zombies_are_coming_calc = (zombie_comes_calc.quantize(santa2_calc, ROUND_HALF_UP) % 2)
                        if zombies_are_coming_calc == 1 and Decimal(tune_calc[lila_calc + 2]) < 0:
                            witches_calc = (1 / Decimal(tune_calc[lila_calc]))
                            homeless_calc = (abs(Decimal(tune_calc[lila_calc + 2])) ** witches_calc)
                            homeless_calc = -homeless_calc
                            homeless_calc = homeless_calc.quantize(santa1_calc, ROUND_HALF_UP)
                            tune_calc[lila_calc] = str(homeless_calc)
                            tune_calc[lila_calc + 1] = 'R'
                            tune_calc[lila_calc + 2] = 'R'
                        elif Decimal(tune_calc[lila_calc + 2]) >= 0:
                            witches_calc = (1 / Decimal(tune_calc[lila_calc]))
                            homeless_calc = (Decimal(tune_calc[lila_calc + 2])) ** witches_calc
                            homeless_calc = homeless_calc.quantize(santa1_calc, ROUND_HALF_UP)
                            tune_calc[lila_calc] = str(homeless_calc)
                            tune_calc[lila_calc + 1] = 'R'
                            tune_calc[lila_calc + 2] = 'R'
                        else:
                            return 'Нет решения среди действительных чисел! Ошибка у корня!'
                while 'R' in tune_calc:
                    tune_calc.remove('R')
                for lila_calc in range(len(tune_calc) - 4, -1, -1):
                    lord_calc = len([di_calc for di_calc in tune_calc[lila_calc + 1]])
                    blurple_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 1] if ri_calc in BB_calc])
                    coffee_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 3]])
                    cherry_calc = len([vi_calc for vi_calc in tune_calc[lila_calc + 3] if vi_calc in BB_calc])
                    n1_calc = (lord_calc == blurple_calc)
                    n2_calc = (coffee_calc == cherry_calc)
                    if tune_calc[lila_calc] == 'log' and tune_calc[lila_calc + 2] == '_' and n1_calc and n2_calc:
                        if Decimal(tune_calc[lila_calc + 3]) == 1 or Decimal(tune_calc[lila_calc + 3]) <= 0:
                            return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                        elif Decimal(tune_calc[lila_calc + 1]) <= 0:
                            return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                        else:
                            mega_big_log_calc = 0
                            junior_log_calc = Decimal(tune_calc[lila_calc + 1])
                            senior_log_calc = Decimal(tune_calc[lila_calc + 3])
                            if senior_log_calc > 10 ** 301 or senior_log_calc < 10 ** -301:
                                return 'Слишком длинное основание логарифма!'
                            if junior_log_calc > 10 ** 1001:
                                return 'Слишком длинное логарифмируемое число логарифма!'
                            hey_jude_yo_calc = 1
                            if junior_log_calc < 1:
                                junior_log_calc = (1 / junior_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                hey_jude_yo_calc *= (-1)
                            if senior_log_calc < 1:
                                senior_log_calc = (1 / senior_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                tune_calc[lila_calc + 3] = str(senior_log_calc)
                                hey_jude_yo_calc *= (-1)
                            if junior_log_calc > 10 ** 300:
                                if (Decimal(tune_calc[lila_calc + 3]) ** 100) <= 10 ** 300:
                                    while junior_log_calc > 10 ** 300:
                                        junior_log_calc /= (Decimal(tune_calc[lila_calc + 3]) ** 100)
                                        mega_big_log_calc += 100
                                elif (Decimal(tune_calc[lila_calc + 3]) ** 10) <= 10 ** 300:
                                    while junior_log_calc > 10 ** 300:
                                        junior_log_calc /= (Decimal(tune_calc[lila_calc + 3]) ** 10)
                                        mega_big_log_calc += 10
                                elif Decimal(tune_calc[lila_calc + 3]) <= 10 ** 300:
                                    while junior_log_calc > 10 ** 300:
                                        junior_log_calc /= Decimal(tune_calc[lila_calc + 3])
                                        mega_big_log_calc += 1
                                else:
                                    return 'Слишком длинное основание логарифма!'
                            eler_calc = math.log(junior_log_calc, senior_log_calc)
                            eler_calc = Decimal(eler_calc).quantize(santa5_calc, ROUND_HALF_UP)
                            tune_calc[lila_calc] = str((eler_calc + mega_big_log_calc) * hey_jude_yo_calc)
                            tune_calc[lila_calc + 1] = 'R'
                            tune_calc[lila_calc + 2] = 'R'
                            tune_calc[lila_calc + 3] = 'R'
                while 'R' in tune_calc:
                    tune_calc.remove('R')
                for lila_calc in range(len(tune_calc) - 1):
                    traider_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 1]])
                    troider_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 1] if ri_calc in BB_calc])
                    weird_calc = ['sn', 'cs', 'tg', 'ct', 'ln', 'lg', 'f']
                    task_calc = (tune_calc[lila_calc] in weird_calc)
                    if task_calc and traider_calc == troider_calc:
                        try_calc = tune_calc[lila_calc]
                        mir_calc = Decimal(tune_calc[lila_calc + 1]) % 360
                        if mir_calc < 0:
                            mir_calc += 360
                        if try_calc == 'tg' and mir_calc % 180 == 90 or try_calc == 'ct' and mir_calc % 180 == 0:
                            return 'Бесконечность! Тангенс или котангенс такого угла смысла не имеет!'
                        wild_calc = Decimal(str(mir_calc)) / Decimal('180') * pi_calc
                        if wild_calc == 0:
                            wild_calc = 0
                        t1s_calc = t1c_calc = Decimal('0')
                        if tune_calc[lila_calc] == 'sn':
                            for w1_calc in range(1, 100):
                                w2s_calc = math.factorial(2 * w1_calc - 1)
                                t1s_calc += Decimal(((-1) ** (w1_calc + 1) * wild_calc ** (2 * w1_calc - 1) / w2s_calc))
                            tune_calc[lila_calc] = str(t1s_calc)
                        elif tune_calc[lila_calc] == 'cs':
                            for w1_calc in range(100):
                                w2c_calc = math.factorial(2 * w1_calc)
                                t1c_calc += Decimal((-1) ** w1_calc * wild_calc ** (2 * w1_calc) / w2c_calc)
                            tune_calc[lila_calc] = str(t1c_calc)
                        elif tune_calc[lila_calc] == 'tg':
                            for w1_calc in range(1, 100):
                                w2s_calc = math.factorial(2 * w1_calc - 1)
                                t1s_calc += Decimal(((-1) ** (w1_calc + 1) * wild_calc ** (2 * w1_calc - 1) / w2s_calc))
                            for w1_calc in range(100):
                                w2c_calc = math.factorial(2 * w1_calc)
                                t1c_calc += Decimal((-1) ** w1_calc * wild_calc ** (2 * w1_calc) / w2c_calc)
                            tune_calc[lila_calc] = str(t1s_calc / t1c_calc)
                        elif tune_calc[lila_calc] == 'ct':
                            for w1_calc in range(1, 100):
                                w2s_calc = math.factorial(2 * w1_calc - 1)
                                t1s_calc += Decimal(((-1) ** (w1_calc + 1) * wild_calc ** (2 * w1_calc - 1) / w2s_calc))
                            for w1_calc in range(100):
                                w2c_calc = math.factorial(2 * w1_calc)
                                t1c_calc += Decimal((-1) ** w1_calc * wild_calc ** (2 * w1_calc) / w2c_calc)
                            tune_calc[lila_calc] = str(t1c_calc / t1s_calc)
                        elif tune_calc[lila_calc] == 'ln':
                            rayo_calc = Decimal(tune_calc[lila_calc + 1]).quantize(santa1_calc, ROUND_HALF_UP)
                            if rayo_calc <= 0:
                                return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                            else:
                                mega_big_log_calc = 0
                                middle_log_calc = Decimal(tune_calc[lila_calc + 1])
                                if middle_log_calc > 10 ** 1001:
                                    return 'Слишком длинное логарифмируемое число логарифма!'
                                hey_jude_yo_calc = 1
                                if middle_log_calc < 1:
                                    middle_log_calc = (1 / middle_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                    hey_jude_yo_calc *= (-1)
                                if middle_log_calc > 10 ** 300:
                                    while middle_log_calc > 10 ** 300:
                                        middle_log_calc /= (e_calc ** 600)
                                        mega_big_log_calc += 600
                                smirno_calc = Decimal(math.log(Decimal(middle_log_calc)))
                                wild_calc = Decimal((smirno_calc + mega_big_log_calc) * hey_jude_yo_calc)
                                wild_calc = wild_calc.quantize(santa5_calc, ROUND_HALF_UP)
                                tune_calc[lila_calc] = str(wild_calc)
                        elif tune_calc[lila_calc] == 'lg':
                            rayo_calc = Decimal(tune_calc[lila_calc + 1]).quantize(santa1_calc, ROUND_HALF_UP)
                            if rayo_calc <= 0:
                                return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                            else:
                                mega_big_log_calc = 0
                                middle_log_calc = Decimal(tune_calc[lila_calc + 1])
                                if middle_log_calc > 10 ** 1001:
                                    return 'Слишком длинное логарифмируемое число логарифма!'
                                hey_jude_yo_calc = 1
                                if middle_log_calc < 1:
                                    middle_log_calc = (1 / middle_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                    hey_jude_yo_calc *= (-1)
                                if middle_log_calc > 10 ** 300:
                                    while middle_log_calc > 10 ** 300:
                                        middle_log_calc /= (10 ** 200)
                                        mega_big_log_calc += 200
                                smirno_calc = Decimal(math.log(Decimal(middle_log_calc), 10))
                                wild_calc = Decimal((smirno_calc + mega_big_log_calc) * hey_jude_yo_calc)
                                wild_calc = wild_calc.quantize(santa5_calc, ROUND_HALF_UP)
                                tune_calc[lila_calc] = str(wild_calc)
                        tune_calc[lila_calc + 1] = 'R'
                twix_calc = ('sn' in tune_calc or 'cs' in tune_calc or 'tg' in tune_calc)
                tromb_calc = ('ct' in tune_calc or 'ln' in tune_calc or 'lg' in tune_calc)
                goose_calc = ('k' in tune_calc or '!' in tune_calc or 'f' in tune_calc or 'log' in tune_calc)
                while 'R' in tune_calc:
                    tune_calc.remove('R')
            while '^' in tune_calc or '^-' in tune_calc:
                for type_calc in range(len(tune_calc) - 3, -1, -1):
                    winter_calc = len([vid_calc for vid_calc in tune_calc[type_calc]])
                    spring_calc = len([vid_calc for vid_calc in tune_calc[type_calc] if vid_calc in BB_calc])
                    summer_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2]])
                    autumn_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2] if vid_calc in BB_calc])
                    if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] == '^-':
                        tht_calc = Decimal(1 / Decimal(tune_calc[type_calc])).quantize(santa3_calc, ROUND_HALF_UP)
                        tune_calc[type_calc] = str(tht_calc)
                        tune_calc[type_calc + 1] = '^'
                    if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] == '^':
                        trip_calc = Decimal(tune_calc[type_calc])
                        lolipop_calc = Decimal(tune_calc[type_calc + 2])
                        if trip_calc >= 0:
                            tune_calc[type_calc] = str((trip_calc ** lolipop_calc.quantize(santa1_calc, ROUND_HALF_UP)))
                            tune_calc[type_calc + 2] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                        elif trip_calc < 0 and lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) % 1 == 0:
                            tune_calc[type_calc] = str((trip_calc ** lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP)))
                            tune_calc[type_calc + 2] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                        else:
                            for matante_calc in range(3, 100, 2):
                                mem1_calc = Decimal(1 / Decimal(str(matante_calc)))
                                mem3_calc = mem1_calc.quantize(santa2_calc, ROUND_HALF_UP)
                                stanford_calc = (lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) % mem3_calc)
                                if stanford_calc.quantize(santa3_calc, ROUND_HALF_UP) == 0:
                                    pow_calc = Decimal(-(abs(trip_calc) ** mem1_calc))
                                    mast_calc = pow_calc.quantize(santa2_calc, ROUND_HALF_UP)
                                    yahoo_calc = (lolipop_calc / mem3_calc).quantize(Decimal('0'), ROUND_HALF_UP)
                                    tune_calc[type_calc] = str(mast_calc ** yahoo_calc)
                                    tune_calc[type_calc + 2] = 'R'
                                    tune_calc[type_calc + 1] = 'R'
                            else:
                                return 'Чётный или слишком большой знаменатель у степени числа!'
                while 'R' in tune_calc:
                    tune_calc.remove('R')
            while '*' in tune_calc or ':' in tune_calc or '%' in tune_calc or '@' in tune_calc:
                for type_calc in range(len(tune_calc) - 2):
                    winter_calc = len([vid_calc for vid_calc in tune_calc[type_calc]])
                    spring_calc = len([vid_calc for vid_calc in tune_calc[type_calc] if vid_calc in BB_calc])
                    summer_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2]])
                    autumn_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2] if vid_calc in BB_calc])
                    calcus = ['*', ':', '%', '@']
                    if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] in calcus:
                        trip_calc = Decimal(tune_calc[type_calc])
                        lolipop_calc = Decimal(tune_calc[type_calc + 2])
                        if tune_calc[type_calc + 1] == '*':
                            multiply_calc = (trip_calc * lolipop_calc)
                            tune_calc[type_calc + 2] = str(multiply_calc.quantize(santa1_calc, ROUND_HALF_UP))
                            tune_calc[type_calc] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                        if tune_calc[type_calc + 1] == ':':
                            divide_calc = (trip_calc / lolipop_calc)
                            tune_calc[type_calc + 2] = str(divide_calc.quantize(santa1_calc, ROUND_HALF_UP))
                            tune_calc[type_calc] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                        if tune_calc[type_calc + 1] == '%':
                            if lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) > 0:
                                lolipop_calc = Decimal(str(lolipop_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                                trip_calc = Decimal(str(trip_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                                ovocado_calc = (trip_calc % lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                if ovocado_calc < 0:
                                    ovocado_calc = (ovocado_calc + lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                else:
                                    ovocado_calc = ovocado_calc
                                tune_calc[type_calc + 2] = str(ovocado_calc)
                                tune_calc[type_calc] = 'R'
                                tune_calc[type_calc + 1] = 'R'
                            else:
                                return 'Нельзя делить нацело и/или с остатком на отрицательное число!'
                        if tune_calc[type_calc + 1] == '@':
                            if lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) > 0:
                                lolipop_calc = Decimal(str(lolipop_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                                trip_calc = Decimal(str(trip_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                                ovocado_calc = (trip_calc // lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                novocado_calc = (trip_calc % lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                if novocado_calc < 0:
                                    ovocado_calc = (ovocado_calc - 1).quantize(santa4_calc, ROUND_HALF_UP)
                                else:
                                    ovocado_calc = ovocado_calc
                                tune_calc[type_calc + 2] = str(ovocado_calc)
                                tune_calc[type_calc] = 'R'
                                tune_calc[type_calc + 1] = 'R'
                            else:
                                return 'Нельзя делить нацело и/или с остатком на отрицательное число!'
                while 'R' in tune_calc:
                    tune_calc.remove('R')
            while '+' in tune_calc or '-' in tune_calc:
                for type_calc in range(len(tune_calc) - 2):
                    winter_calc = len([vid_calc for vid_calc in tune_calc[type_calc]])
                    spring_calc = len([vid_calc for vid_calc in tune_calc[type_calc] if vid_calc in BB_calc])
                    summer_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2]])
                    autumn_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2] if vid_calc in BB_calc])
                    calcus = ['+', '-']
                    if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] in calcus:
                        trip_calc = Decimal(tune_calc[type_calc])
                        lolipop_calc = Decimal(tune_calc[type_calc + 2])
                        if tune_calc[type_calc + 1] == '+':
                            summary_calc = (trip_calc + lolipop_calc)
                            tune_calc[type_calc + 2] = str(summary_calc.quantize(santa1_calc, ROUND_HALF_UP))
                            tune_calc[type_calc] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                        if tune_calc[type_calc + 1] == '-':
                            difference_calc = (trip_calc - lolipop_calc)
                            tune_calc[type_calc + 2] = str(difference_calc.quantize(santa1_calc, ROUND_HALF_UP))
                            tune_calc[type_calc] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                while 'R' in tune_calc:
                    tune_calc.remove('R')
            if tota_calc[calcor_start] == 'U':
                tune_calc = str(abs(Decimal(tune_calc[0])))
            else:
                tune_calc = tune_calc[0]
            tota_calc[calcor_start] = tune_calc
            tota_calc[calcor_start + 1:calcor_stop + 1] = 'М'
            while 'М' in tota_calc:
                tota_calc.remove('М')
        tune_calc = tota_calc
        twix_calc = ('sn' in tune_calc or 'cs' in tune_calc or 'tg' in tune_calc)
        tromb_calc = ('ct' in tune_calc or 'ln' in tune_calc or 'lg' in tune_calc)
        goose_calc = ('k' in tune_calc or '!' in tune_calc or 'f' in tune_calc or 'log' in tune_calc)
        while twix_calc or tromb_calc or goose_calc:
            for lila_calc in range(len(tune_calc) - 1):
                treider_calc = len([ti_calc for ti_calc in tune_calc[lila_calc]])
                tryider_calc = len([ri_calc for ri_calc in tune_calc[lila_calc] if ri_calc in BB_calc])
                if tune_calc[lila_calc + 1] == '!' and tryider_calc == treider_calc:
                    if Decimal(tune_calc[lila_calc]).quantize(santa4_calc, ROUND_HALF_UP) < 0:
                        return 'Факториала неположительного числа не существует!'
                    elif Decimal(tune_calc[lila_calc]).quantize(santa2_calc, ROUND_HALF_UP) % 1 == 0:
                        wild_calc = math.factorial(int(Decimal(tune_calc[lila_calc])))
                        tune_calc[lila_calc + 1] = str(wild_calc)
                    else:
                        return 'Факториал только натурального числа!'
                    tune_calc[lila_calc] = 'R'
            while 'R' in tune_calc:
                tune_calc.remove('R')
            for lila_calc in range(len(tune_calc) - 2, -1, -1):
                treider_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 1]])
                tryider_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 1] if ri_calc in BB_calc])
                if tune_calc[lila_calc] == 'f' and tryider_calc == treider_calc:
                    if Decimal(tune_calc[lila_calc + 1]).quantize(santa4_calc, ROUND_HALF_UP) < 0:
                        return 'Факториала неположительного числа не существует!'
                    elif Decimal(tune_calc[lila_calc + 1]).quantize(santa2_calc, ROUND_HALF_UP) % 1 == 0:
                        wild_calc = math.factorial(int(Decimal(tune_calc[lila_calc + 1])))
                        tune_calc[lila_calc] = str(wild_calc)
                    else:
                        return 'Факториал только натурального числа!'
                    tune_calc[lila_calc + 1] = 'R'
            while 'R' in tune_calc:
                tune_calc.remove('R')
            for lila_calc in range(len(tune_calc) - 3, -1, -1):
                lord_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 2]])
                blurple_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 2] if ri_calc in BB_calc])
                if tune_calc[lila_calc + 1] == 'k' and blurple_calc == lord_calc:
                    zombie_comes_calc = abs(Decimal(tune_calc[lila_calc]))
                    zombies_are_coming_calc = (zombie_comes_calc.quantize(santa2_calc, ROUND_HALF_UP) % 2)
                    if zombies_are_coming_calc == 1 and Decimal(tune_calc[lila_calc + 2]) < 0:
                        witches_calc = (1 / Decimal(tune_calc[lila_calc]))
                        homeless_calc = (abs(Decimal(tune_calc[lila_calc + 2])) ** witches_calc)
                        homeless_calc = -homeless_calc
                        homeless_calc = homeless_calc.quantize(santa1_calc, ROUND_HALF_UP)
                        tune_calc[lila_calc] = str(homeless_calc)
                        tune_calc[lila_calc + 1] = 'R'
                        tune_calc[lila_calc + 2] = 'R'
                    elif Decimal(tune_calc[lila_calc + 2]) >= 0:
                        witches_calc = (1 / Decimal(tune_calc[lila_calc]))
                        homeless_calc = (Decimal(tune_calc[lila_calc + 2])) ** witches_calc
                        homeless_calc = homeless_calc.quantize(santa1_calc, ROUND_HALF_UP)
                        tune_calc[lila_calc] = str(homeless_calc)
                        tune_calc[lila_calc + 1] = 'R'
                        tune_calc[lila_calc + 2] = 'R'
                    else:
                        return 'Нет решения среди действительных чисел! Ошибка у корня!'
            while 'R' in tune_calc:
                tune_calc.remove('R')
            for lila_calc in range(len(tune_calc) - 4, -1, -1):
                lord_calc = len([di_calc for di_calc in tune_calc[lila_calc + 1]])
                blurple_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 1] if ri_calc in BB_calc])
                coffee_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 3]])
                cherry_calc = len([vi_calc for vi_calc in tune_calc[lila_calc + 3] if vi_calc in BB_calc])
                n1_calc = (lord_calc == blurple_calc)
                n2_calc = (coffee_calc == cherry_calc)
                if tune_calc[lila_calc] == 'log' and tune_calc[lila_calc + 2] == '_' and n1_calc and n2_calc:
                    if Decimal(tune_calc[lila_calc + 3]) == 1 or Decimal(tune_calc[lila_calc + 3]) <= 0:
                        return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                    elif Decimal(tune_calc[lila_calc + 1]) <= 0:
                        return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                    else:
                        mega_big_log_calc = 0
                        junior_log_calc = Decimal(tune_calc[lila_calc + 1])
                        senior_log_calc = Decimal(tune_calc[lila_calc + 3])
                        if senior_log_calc > 10 ** 301 or senior_log_calc < 10 ** -301:
                            return 'Слишком длинное основание логарифма!'
                        if junior_log_calc > 10 ** 1001:
                            return 'Слишком длинное логарифмируемое число логарифма!'
                        hey_jude_yo_calc = 1
                        if junior_log_calc < 1:
                            junior_log_calc = (1 / junior_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                            hey_jude_yo_calc *= (-1)
                        if senior_log_calc < 1:
                            senior_log_calc = (1 / senior_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                            tune_calc[lila_calc + 3] = str(senior_log_calc)
                            hey_jude_yo_calc *= (-1)
                        if junior_log_calc > 10 ** 300:
                            if (Decimal(tune_calc[lila_calc + 3]) ** 100) <= 10 ** 300:
                                while junior_log_calc > 10 ** 300:
                                    junior_log_calc /= (Decimal(tune_calc[lila_calc + 3]) ** 100)
                                    mega_big_log_calc += 100
                            elif (Decimal(tune_calc[lila_calc + 3]) ** 10) <= 10 ** 300:
                                while junior_log_calc > 10 ** 300:
                                    junior_log_calc /= (Decimal(tune_calc[lila_calc + 3]) ** 10)
                                    mega_big_log_calc += 10
                            elif Decimal(tune_calc[lila_calc + 3]) <= 10 ** 300:
                                while junior_log_calc > 10 ** 300:
                                    junior_log_calc /= Decimal(tune_calc[lila_calc + 3])
                                    mega_big_log_calc += 1
                            else:
                                return 'Слишком длинное основание логарифма!'
                        eler_calc = math.log(junior_log_calc, senior_log_calc)
                        eler_calc = Decimal(eler_calc).quantize(santa5_calc, ROUND_HALF_UP)
                        tune_calc[lila_calc] = str((eler_calc + mega_big_log_calc) * hey_jude_yo_calc)
                        tune_calc[lila_calc + 1] = 'R'
                        tune_calc[lila_calc + 2] = 'R'
                        tune_calc[lila_calc + 3] = 'R'
            while 'R' in tune_calc:
                tune_calc.remove('R')
            for lila_calc in range(len(tune_calc) - 1):
                traider_calc = len([ti_calc for ti_calc in tune_calc[lila_calc + 1]])
                troider_calc = len([ri_calc for ri_calc in tune_calc[lila_calc + 1] if ri_calc in BB_calc])
                weird_calc = ['sn', 'cs', 'tg', 'ct', 'ln', 'lg', 'f']
                task_calc = (tune_calc[lila_calc] in weird_calc)
                if task_calc and traider_calc == troider_calc:
                    try_calc = tune_calc[lila_calc]
                    mir_calc = Decimal(tune_calc[lila_calc + 1]) % 360
                    if mir_calc < 0:
                        mir_calc += 360
                    if try_calc == 'tg' and mir_calc % 180 == 90 or try_calc == 'ct' and mir_calc % 180 == 0:
                        return 'Бесконечность! Тангенс или котангенс такого угла смысла не имеет!'
                    wild_calc = Decimal(str(mir_calc)) / Decimal('180') * pi_calc
                    if wild_calc == 0:
                        wild_calc = 0
                    t1s_calc = t1c_calc = Decimal('0')
                    if tune_calc[lila_calc] == 'sn':
                        for w1_calc in range(1, 100):
                            w2s_calc = math.factorial(2 * w1_calc - 1)
                            t1s_calc += Decimal((-1) ** (w1_calc + 1) * wild_calc ** (2 * w1_calc - 1) / w2s_calc)
                        tune_calc[lila_calc] = str(t1s_calc)
                    elif tune_calc[lila_calc] == 'cs':
                        for w1_calc in range(100):
                            w2c_calc = math.factorial(2 * w1_calc)
                            t1c_calc += Decimal((-1) ** w1_calc * wild_calc ** (2 * w1_calc) / w2c_calc)
                        tune_calc[lila_calc] = str(t1c_calc)
                    elif tune_calc[lila_calc] == 'tg':
                        for w1_calc in range(1, 100):
                            w2s_calc = math.factorial(2 * w1_calc - 1)
                            t1s_calc += Decimal(((-1) ** (w1_calc + 1) * wild_calc ** (2 * w1_calc - 1) / w2s_calc))
                        for w1_calc in range(100):
                            w2c_calc = math.factorial(2 * w1_calc)
                            t1c_calc += Decimal((-1) ** w1_calc * wild_calc ** (2 * w1_calc) / w2c_calc)
                        tune_calc[lila_calc] = str(t1s_calc / t1c_calc)
                    elif tune_calc[lila_calc] == 'ct':
                        for w1_calc in range(1, 100):
                            w2s_calc = math.factorial(2 * w1_calc - 1)
                            t1s_calc += Decimal(((-1) ** (w1_calc + 1) * wild_calc ** (2 * w1_calc - 1) / w2s_calc))
                        for w1_calc in range(100):
                            w2c_calc = math.factorial(2 * w1_calc)
                            t1c_calc += Decimal((-1) ** w1_calc * wild_calc ** (2 * w1_calc) / w2c_calc)
                        tune_calc[lila_calc] = str(t1c_calc / t1s_calc)
                    elif tune_calc[lila_calc] == 'ln':
                        rayo_calc = Decimal(tune_calc[lila_calc + 1]).quantize(santa1_calc, ROUND_HALF_UP)
                        if rayo_calc <= 0:
                            return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                        else:
                            mega_big_log_calc = 0
                            middle_log_calc = Decimal(tune_calc[lila_calc + 1])
                            if middle_log_calc > 10 ** 1001:
                                return 'Слишком длинное логарифмируемое число логарифма!'
                            hey_jude_yo_calc = 1
                            if middle_log_calc < 1:
                                middle_log_calc = (1 / middle_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                hey_jude_yo_calc *= (-1)
                            if middle_log_calc > 10 ** 300:
                                while middle_log_calc > 10 ** 300:
                                    middle_log_calc /= (e_calc ** 600)
                                    mega_big_log_calc += 600
                            smirno_calc = Decimal(math.log(Decimal(middle_log_calc)))
                            wild_calc = Decimal((smirno_calc + mega_big_log_calc) * hey_jude_yo_calc)
                            wild_calc = wild_calc.quantize(santa5_calc, ROUND_HALF_UP)
                            tune_calc[lila_calc] = str(wild_calc)
                    elif tune_calc[lila_calc] == 'lg':
                        rayo_calc = Decimal(tune_calc[lila_calc + 1]).quantize(santa1_calc, ROUND_HALF_UP)
                        if rayo_calc <= 0:
                            return 'Выражение не имеет смысла! (Ошибка у логарифма)'
                        else:
                            mega_big_log_calc = 0
                            middle_log_calc = Decimal(tune_calc[lila_calc + 1])
                            if middle_log_calc > 10 ** 1001:
                                return 'Слишком длинное логарифмируемое число логарифма!'
                            hey_jude_yo_calc = 1
                            if middle_log_calc < 1:
                                middle_log_calc = (1 / middle_log_calc).quantize(santa4_calc, ROUND_HALF_UP)
                                hey_jude_yo_calc *= (-1)
                            if middle_log_calc > 10 ** 300:
                                while middle_log_calc > 10 ** 300:
                                    middle_log_calc /= (10 ** 200)
                                    mega_big_log_calc += 200
                            smirno_calc = Decimal(math.log(Decimal(middle_log_calc), 10))
                            wild_calc = Decimal((smirno_calc + mega_big_log_calc) * hey_jude_yo_calc)
                            wild_calc = wild_calc.quantize(santa5_calc, ROUND_HALF_UP)
                            tune_calc[lila_calc] = str(wild_calc)
                    tune_calc[lila_calc + 1] = 'R'
            twix_calc = ('sn' in tune_calc or 'cs' in tune_calc or 'tg' in tune_calc)
            tromb_calc = ('ct' in tune_calc or 'ln' in tune_calc or 'lg' in tune_calc)
            goose_calc = ('k' in tune_calc or '!' in tune_calc or 'f' in tune_calc or 'log' in tune_calc)
            while 'R' in tune_calc:
                tune_calc.remove('R')
        while '^' in tune_calc or '^-' in tune_calc:
            for type_calc in range(len(tune_calc) - 3, -1, -1):
                winter_calc = len([vid_calc for vid_calc in tune_calc[type_calc]])
                spring_calc = len([vid_calc for vid_calc in tune_calc[type_calc] if vid_calc in BB_calc])
                summer_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2]])
                autumn_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2] if vid_calc in BB_calc])
                if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] == '^-':
                    tht_calc = Decimal(1 / Decimal(tune_calc[type_calc])).quantize(santa3_calc, ROUND_HALF_UP)
                    tune_calc[type_calc] = str(tht_calc)
                    tune_calc[type_calc + 1] = '^'
                if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] == '^':
                    trip_calc = Decimal(tune_calc[type_calc])
                    lolipop_calc = Decimal(tune_calc[type_calc + 2])
                    if trip_calc >= 0:
                        tune_calc[type_calc] = str(trip_calc ** lolipop_calc.quantize(santa1_calc, ROUND_HALF_UP))
                        tune_calc[type_calc + 2] = 'R'
                        tune_calc[type_calc + 1] = 'R'
                    elif trip_calc < 0 and lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) % 1 == 0:
                        tune_calc[type_calc] = str(trip_calc ** lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP))
                        tune_calc[type_calc + 2] = 'R'
                        tune_calc[type_calc + 1] = 'R'
                    else:
                        for matante_calc in range(3, 100, 2):
                            mem1_calc = Decimal(1 / Decimal(str(matante_calc)))
                            mem3_calc = mem1_calc.quantize(santa2_calc, ROUND_HALF_UP)
                            stanford_calc = (lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) % mem3_calc)
                            if stanford_calc.quantize(santa3_calc, ROUND_HALF_UP) == 0:
                                mast_calc = Decimal(-(abs(trip_calc) ** mem1_calc)).quantize(santa2_calc, ROUND_HALF_UP)
                                yahoo_calc = (lolipop_calc / mem3_calc).quantize(Decimal('0'), ROUND_HALF_UP)
                                tune_calc[type_calc] = str(mast_calc ** yahoo_calc)
                                tune_calc[type_calc + 2] = 'R'
                                tune_calc[type_calc + 1] = 'R'
                        else:
                            return 'Чётный или слишком большой знаменатель у степени числа!'
            while 'R' in tune_calc:
                tune_calc.remove('R')
        while '*' in tune_calc or ':' in tune_calc or '%' in tune_calc or '@' in tune_calc:
            for type_calc in range(len(tune_calc) - 2):
                winter_calc = len([vid_calc for vid_calc in tune_calc[type_calc]])
                spring_calc = len([vid_calc for vid_calc in tune_calc[type_calc] if vid_calc in BB_calc])
                summer_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2]])
                autumn_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2] if vid_calc in BB_calc])
                calcus = ['*', ':', '%', '@']
                if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] in calcus:
                    trip_calc = Decimal(tune_calc[type_calc])
                    lolipop_calc = Decimal(tune_calc[type_calc + 2])
                    if tune_calc[type_calc + 1] == '*':
                        tune_calc[type_calc + 2] = str((trip_calc * lolipop_calc).quantize(santa1_calc, ROUND_HALF_UP))
                        tune_calc[type_calc] = 'R'
                        tune_calc[type_calc + 1] = 'R'
                    if tune_calc[type_calc + 1] == ':':
                        tune_calc[type_calc + 2] = str((trip_calc / lolipop_calc).quantize(santa1_calc, ROUND_HALF_UP))
                        tune_calc[type_calc] = 'R'
                        tune_calc[type_calc + 1] = 'R'
                    if tune_calc[type_calc + 1] == '%':
                        if lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) > 0:
                            lolipop_calc = Decimal(str(lolipop_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                            trip_calc = Decimal(str(trip_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                            ovocado_calc = (trip_calc % lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                            if ovocado_calc < 0:
                                ovocado_calc = (ovocado_calc + lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                            else:
                                ovocado_calc = ovocado_calc
                            tune_calc[type_calc + 2] = str(ovocado_calc)
                            tune_calc[type_calc] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                        else:
                            return 'Нельзя делить нацело и/или с остатком на отрицательное число!'
                    if tune_calc[type_calc + 1] == '@':
                        if lolipop_calc.quantize(santa2_calc, ROUND_HALF_UP) > 0:
                            lolipop_calc = Decimal(str(lolipop_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                            trip_calc = Decimal(str(trip_calc)).quantize(santa3_calc, ROUND_HALF_UP)
                            ovocado_calc = (trip_calc // lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                            novocado_calc = (trip_calc % lolipop_calc).quantize(santa4_calc, ROUND_HALF_UP)
                            if novocado_calc < 0:
                                ovocado_calc = (ovocado_calc - 1).quantize(santa4_calc, ROUND_HALF_UP)
                            else:
                                ovocado_calc = ovocado_calc
                            tune_calc[type_calc + 2] = str(ovocado_calc)
                            tune_calc[type_calc] = 'R'
                            tune_calc[type_calc + 1] = 'R'
                        else:
                            return 'Нельзя делить нацело и/или с остатком на отрицательное число!'
            while 'R' in tune_calc:
                tune_calc.remove('R')
        while '+' in tune_calc or '-' in tune_calc:
            for type_calc in range(len(tune_calc) - 2):
                winter_calc = len([vid_calc for vid_calc in tune_calc[type_calc]])
                spring_calc = len([vid_calc for vid_calc in tune_calc[type_calc] if vid_calc in BB_calc])
                summer_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2]])
                autumn_calc = len([vid_calc for vid_calc in tune_calc[type_calc + 2] if vid_calc in BB_calc])
                calcus = ['+', '-']
                if winter_calc == spring_calc and summer_calc == autumn_calc and tune_calc[type_calc + 1] in calcus:
                    trip_calc = Decimal(tune_calc[type_calc])
                    lolipop_calc = Decimal(tune_calc[type_calc + 2])
                    if tune_calc[type_calc + 1] == '+':
                        tune_calc[type_calc + 2] = str((trip_calc + lolipop_calc).quantize(santa1_calc, ROUND_HALF_UP))
                        tune_calc[type_calc] = 'R'
                        tune_calc[type_calc + 1] = 'R'
                    if tune_calc[type_calc + 1] == '-':
                        tune_calc[type_calc + 2] = str((trip_calc - lolipop_calc).quantize(santa1_calc, ROUND_HALF_UP))
                        tune_calc[type_calc] = 'R'
                        tune_calc[type_calc + 1] = 'R'
            while 'R' in tune_calc:
                tune_calc.remove('R')
        while '' in tune_calc:
            tune_calc.remove('')
        if len(tune_calc) == 1:
            tune_calc = Decimal(tune_calc[0]).quantize(Decimal('.' + 110 * '0'))
            if miss_you_calc != 0:
                tune_calc = tune_calc.quantize(Decimal('.' + miss_you_calc * '0'), ROUND_HALF_UP)
            else:
                tune_calc = tune_calc.quantize(Decimal('0'), ROUND_HALF_UP)
            if tune_calc == 0:
                return '0'
            elif tune_calc % 1 == 0:
                raw_res_calc = str(tune_calc.quantize(Decimal('.0'), ROUND_HALF_UP))[:-2]
            else:
                raw_res_calc = str(tune_calc)
            if Decimal(raw_res_calc) > 10 ** 24 or 0 < Decimal(raw_res_calc) < 10 ** (-6):
                fly_exp_calc = 0
                while Decimal(raw_res_calc) > 10 ** 300:
                    raw_res_calc = str(Decimal(raw_res_calc) / 10 ** 200)
                    fly_exp_calc += 200
                raw_res_exp1_calc = Decimal(math.log(Decimal(raw_res_calc), 10))
                raw_res_exp1_calc = raw_res_exp1_calc.quantize(Decimal('.' + 5 * '0'), ROUND_HALF_UP)
                raw_res_exp1_calc = raw_res_exp1_calc.quantize(Decimal('0'), ROUND_FLOOR)
                raw_res_exp2_calc = Decimal(Decimal(raw_res_calc) / Decimal(10 ** raw_res_exp1_calc))
                if -15 <= raw_res_exp1_calc <= 0:
                    raw_res_exp2_calc = raw_res_exp2_calc.quantize(Decimal('.' + '0' * 102), ROUND_HALF_UP)
                else:
                    raw_res_exp2_calc = raw_res_exp2_calc.quantize(Decimal('.' + '0' * 15), ROUND_HALF_UP)
                if 0 < Decimal(raw_res_calc) < 10 ** (-6):
                    raw_res_calc = str(raw_res_exp2_calc) + 'E' + str(raw_res_exp1_calc + fly_exp_calc)
                else:
                    raw_res_calc = str(raw_res_exp2_calc) + 'E+' + str(raw_res_exp1_calc + fly_exp_calc)
            if Decimal(raw_res_calc) < -10 ** 24 or 0 > Decimal(raw_res_calc) > -10 ** (-6):
                fly_exp_calc = 0
                while Decimal(raw_res_calc) < -10 ** 300:
                    raw_res_calc = str(Decimal(raw_res_calc) / 10 ** 200)
                    fly_exp_calc += 200
                raw_res_exp1_calc = Decimal(math.log(-Decimal(raw_res_calc), 10))
                raw_res_exp1_calc = raw_res_exp1_calc.quantize(Decimal('.' + 5 * '0'), ROUND_HALF_UP)
                raw_res_exp1_calc = raw_res_exp1_calc.quantize(Decimal('0'), ROUND_FLOOR)
                raw_res_exp2_calc = Decimal(Decimal(raw_res_calc) / Decimal(10 ** raw_res_exp1_calc))
                if -15 <= raw_res_exp1_calc <= 0:
                    raw_res_exp2_calc = raw_res_exp2_calc.quantize(Decimal('.' + '0' * 102), ROUND_HALF_UP)
                else:
                    raw_res_exp2_calc = raw_res_exp2_calc.quantize(Decimal('.' + '0' * 15), ROUND_HALF_UP)
                if 0 > Decimal(raw_res_calc) > -10 ** (-6):
                    raw_res_calc = str(raw_res_exp2_calc) + 'E' + str(raw_res_exp1_calc + fly_exp_calc)
                else:
                    raw_res_calc = str(raw_res_exp2_calc) + 'E+' + str(raw_res_exp1_calc + fly_exp_calc)
            if ('E' in raw_res_calc or 'e' in raw_res_calc) and '.' in raw_res_calc:
                while '0e' in raw_res_calc or '0E' in raw_res_calc:
                    raw_res_calc = raw_res_calc.replace('0E', 'E').replace('0e', 'e')
                while '.e' in raw_res_calc or '.E' in raw_res_calc:
                    raw_res_calc = raw_res_calc.replace('.E', 'E').replace('.e', 'e')
            else:
                while (raw_res_calc[-1] == '0' or raw_res_calc[-1] == '.') and '.' in raw_res_calc:
                    raw_res_calc = raw_res_calc[:-1]
            if raw_res_calc.count('e') == 1 or raw_res_calc.count('E') == 1:
                if 'e+' in raw_res_calc or 'E+' in raw_res_calc or 'e' in raw_res_calc or 'E' in raw_res_calc:
                    raw_res_calc = raw_res_calc.replace('e+', '*10^').replace('E+', '*10^')
                if 'e-' in raw_res_calc or 'E-' in raw_res_calc:
                    raw_res_calc = raw_res_calc.replace('e-', '*10^(-').replace('E-', '*10^(-') + ')'
                if '^(-' in raw_res_calc and raw_res_calc[-4] == '-' and int(raw_res_calc[-3:-1]) in range(7, 16):
                    step_by_step_calc = (int(raw_res_calc[-3:-1]) - 1) * '0'
                    if raw_res_calc[0] == '-':
                        raw_res_calc = '-0.' + step_by_step_calc + raw_res_calc[:-9].replace('.', '').replace('-', '')
                    else:
                        raw_res_calc = '0.' + step_by_step_calc + raw_res_calc[:-9].replace('.', '')
                if raw_res_calc[:2] == '1*':
                    raw_res_calc = raw_res_calc[2:]
                if raw_res_calc[:3] == '-1*':
                    raw_res_calc = '-' + raw_res_calc[3:]
            if '10^' not in raw_res_calc:
                if '.' not in raw_res_calc:
                    lenta_split0_calc = ''
                    for comfort_class_result_calc in range(len(raw_res_calc) - 1, -1, -1):
                        lenta_split0_calc = raw_res_calc[comfort_class_result_calc] + lenta_split0_calc
                        if len(lenta_split0_calc.replace(' ', '')) % 3 == 0 and len(lenta_split0_calc) >= 3:
                            lenta_split0_calc = ' ' + lenta_split0_calc
                    if lenta_split0_calc[0] == ' ':
                        lenta_split0_calc = lenta_split0_calc[1:]
                    if lenta_split0_calc[:2] == '- ':
                        lenta_split0_calc = '-' + lenta_split0_calc[2:]
                    raw_res_calc = lenta_split0_calc
                else:
                    lenta_split1_calc = ''
                    lenta_split2_calc = ''
                    splitted_raw_res_calc = raw_res_calc.split('.')
                    for comfort_class_result_calc in range(len(splitted_raw_res_calc[0]) - 1, -1, -1):
                        lenta_split1_calc = splitted_raw_res_calc[0][comfort_class_result_calc] + lenta_split1_calc
                        if len(lenta_split1_calc.replace(' ', '')) % 3 == 0 and len(lenta_split1_calc) >= 3:
                            lenta_split1_calc = ' ' + lenta_split1_calc
                    if lenta_split1_calc[0] == ' ':
                        lenta_split1_calc = lenta_split1_calc[1:]
                    if lenta_split1_calc[:2] == '- ':
                        lenta_split1_calc = '-' + lenta_split1_calc[2:]
                    for comfort_class_result_calc in range(len(splitted_raw_res_calc[1])):
                        lenta_split2_calc += splitted_raw_res_calc[1][comfort_class_result_calc]
                        if len(lenta_split2_calc.replace(' ', '')) % 3 == 0 and len(lenta_split2_calc) >= 3:
                            lenta_split2_calc += ' '
                    if lenta_split2_calc[-1] == ' ':
                        lenta_split2_calc = lenta_split2_calc[:-1]
                    raw_res_calc = lenta_split1_calc + '.' + lenta_split2_calc
            return raw_res_calc
        else:
            return 'Где-то ошибка!'
    except ZeroDivisionError:
        return 'Бесконечность! (На ноль делить нельзя)'
    except (OverflowError, Overflow, InvalidOperation):
        return 'Слишком длинные числа! Или возможно где-то ошибка!'
    except ValueError:
        return 'Где-то ошибка!'


def configure_size_of_example_calc():
    global the_entry_for_example, beluga_calc
    if len(the_entry_for_example.get()) < 32:
        the_entry_for_example.configure(font=('Arial', 20, 'bold'))
    elif 32 <= len(the_entry_for_example.get()) < 37:
        the_entry_for_example.configure(font=('Arial', 18, 'bold'))
    elif 37 <= len(the_entry_for_example.get()) < 41:
        the_entry_for_example.configure(font=('Arial', 16, 'bold'))
    else:
        the_entry_for_example.configure(font=('Arial', 14, 'bold'))
    if len(beluga_calc.get()) < 41:
        beluga_calc.configure(font=('Arial', 16, 'bold'))
    elif 41 <= len(beluga_calc.get()) < 45:
        beluga_calc.configure(font=('Arial', 14, 'bold'))
    elif 45 <= len(beluga_calc.get()) < 54:
        beluga_calc.configure(font=('Arial', 12, 'bold'))
    elif 54 <= len(beluga_calc.get()) < 70:
        beluga_calc.configure(font=('Arial', 10, 'bold'))
    elif 70 <= len(beluga_calc.get()) < 80:
        beluga_calc.configure(font=('Arial', 8, 'bold'))
    else:
        beluga_calc.configure(font=('Arial', 6, 'bold'))


def clicki_silver_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=silver_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(180, 240):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        light_gamma_calc.append('#' + 3 * norman_color_calc)
    configure_color1_calc()


def clicki_red_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=red_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        light_gamma_calc.append('#' + 'ff' + 2 * norman_color_calc)
    settings_of_calculator['color'] = 'red'
    configure_color1_calc()


def clicki_green_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=green_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        light_gamma_calc.append('#' + norman_color_calc + 'ff' + norman_color_calc)
    settings_of_calculator['color'] = 'green'
    configure_color1_calc()


def clicki_blue_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=blue_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        light_gamma_calc.append('#' + 2 * norman_color_calc + 'ff')
    settings_of_calculator['color'] = 'blue'
    configure_color1_calc()


def clicki_yellow_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=yellow_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        light_gamma_calc.append('#' + 'ff' + 'ff' + norman_color_calc)
    settings_of_calculator['color'] = 'yellow'
    configure_color1_calc()


def clicki_magenta_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=magenta_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        light_gamma_calc.append('#' + 'ff' + norman_color_calc + 'ff')
    settings_of_calculator['color'] = 'magenta'
    configure_color1_calc()


def clicki_cyan_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=cyan_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        light_gamma_calc.append('#' + norman_color_calc + 'ff' + 'ff')
    settings_of_calculator['color'] = 'cyan'
    configure_color1_calc()


def clicki_purple_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=purple_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        norman0_calc = str('0' * (2 - len(hex(120 + int(swits_calc / 2))[2:])) + hex(120 + int(swits_calc / 2))[2:])
        light_gamma_calc.append('#' + norman0_calc + norman_color_calc + norman0_calc)
        settings_of_calculator['color'] = 'purple'
    configure_color1_calc()


def clicki_violet_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=violet_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        norman0_calc = str('0' * (2 - len(hex(120 + int(swits_calc / 2))[2:])) + hex(120 + int(swits_calc / 2))[2:])
        light_gamma_calc.append('#' + norman0_calc + norman_color_calc + 'ff')
    settings_of_calculator['color'] = 'violet'
    configure_color1_calc()


def clicki_pink_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=pink_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        lilami1_calc = hex(159 + int(6 * swits_calc / 16))[2:]
        lilami2_calc = hex(int(47 + int(13 * swits_calc / 16)))[2:]
        norman0_calc = str('0' * (2 - len(lilami1_calc)) + lilami1_calc)
        norman1_calc = str('0' * (2 - len(lilami2_calc)) + lilami2_calc)
        light_gamma_calc.append('#' + 'ff' + norman1_calc + norman0_calc)
    settings_of_calculator['color'] = 'pink'
    configure_color1_calc()


def clicki_orange_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=orange_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        lilami1_calc = hex(159 + int(6 * swits_calc / 16))[2:]
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        norman0_calc = str('0' * (2 - len(lilami1_calc)) + lilami1_calc)
        light_gamma_calc.append('#' + 'ff' + norman0_calc + norman_color_calc)
    settings_of_calculator['color'] = 'orange'
    configure_color1_calc()


def clicki_lime_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=lime_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        norman0_calc = str('0' * (2 - len(hex(120 + int(swits_calc / 2))[2:])) + hex(120 + int(swits_calc / 2))[2:])
        light_gamma_calc.append('#' + norman0_calc + 'ff' + norman_color_calc)
    settings_of_calculator['color'] = 'lime'
    configure_color1_calc()


def clicki_skyblue_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=skyblue_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        lilami1_calc = hex(210 + int(1 * swits_calc / 8))[2:]
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        norman0_calc = str('0' * (2 - len(lilami1_calc)) + lilami1_calc)
        light_gamma_calc.append('#' + norman_color_calc + norman0_calc + 'ff')
    settings_of_calculator['color'] = 'sky'
    configure_color1_calc()


def clicki_gold_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=gold_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        lilami1_calc = hex(210 + int(1 * swits_calc / 8))[2:]
        lilami2_calc = hex(180 + int(1 * swits_calc / 4))[2:]
        lilami3_calc = hex(60 + int(3 * swits_calc / 4))[2:]
        norman0_calc = str('0' * (2 - len(lilami1_calc)) + lilami1_calc)
        norman1_calc = str('0' * (2 - len(lilami2_calc)) + lilami2_calc)
        norman2_calc = str('0' * (2 - len(lilami3_calc)) + lilami3_calc)
        light_gamma_calc.append('#' + norman0_calc + norman1_calc + norman2_calc)
    settings_of_calculator['color'] = 'gold'
    configure_color1_calc()


def clicki_emerald_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=emerald_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(0, 240, 4):
        lilami1_calc = hex(150 + int(3 * swits_calc / 8))[2:]
        lilami2_calc = hex(180 + int(1 * swits_calc / 4))[2:]
        norman_color_calc = ('0' * (2 - len(hex(swits_calc)[2:])) + hex(swits_calc)[2:])
        norman0_calc = str('0' * (2 - len(lilami1_calc)) + lilami1_calc)
        norman1_calc = str('0' * (2 - len(lilami2_calc)) + lilami2_calc)
        light_gamma_calc.append('#' + norman_color_calc + norman1_calc + norman0_calc)
    settings_of_calculator['color'] = 'emerald'
    configure_color1_calc()


def clicki_standard_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=standard_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(20):
        light_gamma_calc.append('black')
    for swits_calc in range(40):
        light_gamma_calc.append('white')
    settings_of_calculator['color'] = 'standard'
    configure_color4_calc()


def clicki_ruby_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=ruby_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(20):
        light_gamma_calc.append('#aaa9ad')
    for swits_calc in range(40):
        light_gamma_calc.append('#d4af37')
    settings_of_calculator['color'] = 'ruby'
    configure_color2_calc()


def clicki_sapphire_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=sapphire_bg_image_calc)
    light_gamma_calc = []
    for swits_calc in range(20):
        light_gamma_calc.append('#aaa9ad')
    for swits_calc in range(40):
        light_gamma_calc.append('#d4af37')
    settings_of_calculator['color'] = 'sapphire'
    configure_color3_calc()


def clicki_rainbow_configure_calc():
    global light_gamma_calc, general_background_label_calc
    general_background_label_calc.configure(image=rainbow_bg_image_calc)
    light_gamma_calc = []
    settings_of_calculator['color'] = 'rainbow'
    light_gamma_calc.append('red')
    light_gamma_calc.append('orange')
    light_gamma_calc.append('yellow')
    light_gamma_calc.append('green')
    light_gamma_calc.append('skyblue')
    light_gamma_calc.append('blue')
    light_gamma_calc.append('violet')
    light_gamma_calc.append('pink')
    the_entry_for_example.configure(bg='pink', fg='black')
    beluga_calc.configure(bg='pink', fg='black')
    buttonp_calc.configure(bg=light_gamma_calc[0], fg='black', activebackground=light_gamma_calc[0],
                           activeforeground='black')
    buttonu_calc.configure(bg=light_gamma_calc[1], fg='black', activebackground=light_gamma_calc[1],
                           activeforeground='black')
    buttono_calc.configure(bg=light_gamma_calc[2], fg='black', activebackground=light_gamma_calc[2],
                           activeforeground='black')
    buttong_calc.configure(bg=light_gamma_calc[3], fg='black', activebackground=light_gamma_calc[3],
                           activeforeground='black')
    buttonh_calc.configure(bg=light_gamma_calc[4], fg='black', activebackground=light_gamma_calc[4],
                           activeforeground='black')
    buttoni_calc.configure(bg=light_gamma_calc[5], fg='black', activebackground=light_gamma_calc[5],
                           activeforeground='black')
    buttonj_calc.configure(bg=light_gamma_calc[6], fg='black', activebackground=light_gamma_calc[6],
                           activeforeground='black')
    button03_calc.configure(bg=light_gamma_calc[7], fg='black', activebackground=light_gamma_calc[7],
                            activeforeground='black')
    buttonq_calc.configure(bg=light_gamma_calc[0], fg='black', activebackground=light_gamma_calc[0],
                           activeforeground='black')
    buttonv_calc.configure(bg=light_gamma_calc[1], fg='black', activebackground=light_gamma_calc[1],
                           activeforeground='black')
    buttonn_calc.configure(bg=light_gamma_calc[2], fg='black', activebackground=light_gamma_calc[2],
                           activeforeground='black')
    button7_calc.configure(bg=light_gamma_calc[3], fg='black', activebackground=light_gamma_calc[3],
                           activeforeground='black')
    button8_calc.configure(bg=light_gamma_calc[4], fg='black', activebackground=light_gamma_calc[4],
                           activeforeground='black')
    button9_calc.configure(bg=light_gamma_calc[5], fg='black', activebackground=light_gamma_calc[5],
                           activeforeground='black')
    buttonf_calc.configure(bg=light_gamma_calc[6], fg='black', activebackground=light_gamma_calc[6],
                           activeforeground='black')
    button02_calc.configure(bg=light_gamma_calc[7], fg='black', activebackground=light_gamma_calc[7],
                            activeforeground='black')
    buttonr_calc.configure(bg=light_gamma_calc[0], fg='black', activebackground=light_gamma_calc[0],
                           activeforeground='black')
    buttonw_calc.configure(bg=light_gamma_calc[1], fg='black', activebackground=light_gamma_calc[1],
                           activeforeground='black')
    buttonm_calc.configure(bg=light_gamma_calc[2], fg='black', activebackground=light_gamma_calc[2],
                           activeforeground='black')
    button4_calc.configure(bg=light_gamma_calc[3], fg='black', activebackground=light_gamma_calc[3],
                           activeforeground='black')
    button5_calc.configure(bg=light_gamma_calc[4], fg='black', activebackground=light_gamma_calc[4],
                           activeforeground='black')
    button6_calc.configure(bg=light_gamma_calc[5], fg='black', activebackground=light_gamma_calc[5],
                           activeforeground='black')
    buttone_calc.configure(bg=light_gamma_calc[6], fg='black', activebackground=light_gamma_calc[6],
                           activeforeground='black')
    entry_that_get_information_of_rounding.configure(bg=light_gamma_calc[7], fg='black')
    buttons_calc.configure(bg=light_gamma_calc[0], fg='black', activebackground=light_gamma_calc[0],
                           activeforeground='black')
    buttonx_calc.configure(bg=light_gamma_calc[1], fg='black', activebackground=light_gamma_calc[1],
                           activeforeground='black')
    buttonl_calc.configure(bg=light_gamma_calc[2], fg='black', activebackground=light_gamma_calc[2],
                           activeforeground='black')
    button1_calc.configure(bg=light_gamma_calc[3], fg='black', activebackground=light_gamma_calc[3],
                           activeforeground='black')
    button2_calc.configure(bg=light_gamma_calc[4], fg='black', activebackground=light_gamma_calc[4],
                           activeforeground='black')
    button3_calc.configure(bg=light_gamma_calc[5], fg='black', activebackground=light_gamma_calc[5],
                           activeforeground='black')
    buttond_calc.configure(bg=light_gamma_calc[6], fg='black', activebackground=light_gamma_calc[6],
                           activeforeground='black')
    buttonb_calc.configure(bg=light_gamma_calc[7], fg='black', activebackground=light_gamma_calc[7],
                           activeforeground='black')
    buttont_calc.configure(bg=light_gamma_calc[0], fg='black', activebackground=light_gamma_calc[0],
                           activeforeground='black')
    buttony_calc.configure(bg=light_gamma_calc[1], fg='black', activebackground=light_gamma_calc[1],
                           activeforeground='black')
    buttonk_calc.configure(bg=light_gamma_calc[2], fg='black', activebackground=light_gamma_calc[2],
                           activeforeground='black')
    button0_calc.configure(bg=light_gamma_calc[3], fg='black', activebackground=light_gamma_calc[3],
                           activeforeground='black')
    buttona_calc.configure(bg=light_gamma_calc[4], fg='black', activebackground=light_gamma_calc[4],
                           activeforeground='black')
    button01_calc.configure(bg=light_gamma_calc[5], fg='black', activebackground=light_gamma_calc[5],
                            activeforeground='black')
    buttonc_calc.configure(bg=light_gamma_calc[6], fg='black', activebackground=light_gamma_calc[6],
                           activeforeground='black')
    button00_calc.configure(bg=light_gamma_calc[7], fg='black', activebackground=light_gamma_calc[7],
                            activeforeground='black')


def configure_color1_calc():
    global general_background_label_calc
    the_entry_for_example.configure(bg=light_gamma_calc[40], fg='black')
    beluga_calc.configure(bg=light_gamma_calc[19], fg='black')
    buttonp_calc.configure(bg=light_gamma_calc[20], fg='black', activebackground=light_gamma_calc[20],
                           activeforeground='black')
    buttonu_calc.configure(bg=light_gamma_calc[21], fg='black', activebackground=light_gamma_calc[21],
                           activeforeground='black')
    buttono_calc.configure(bg=light_gamma_calc[22], fg='black', activebackground=light_gamma_calc[22],
                           activeforeground='black')
    buttong_calc.configure(bg=light_gamma_calc[23], fg='black', activebackground=light_gamma_calc[23],
                           activeforeground='black')
    buttonh_calc.configure(bg=light_gamma_calc[24], fg='black', activebackground=light_gamma_calc[24],
                           activeforeground='black')
    buttoni_calc.configure(bg=light_gamma_calc[25], fg='black', activebackground=light_gamma_calc[25],
                           activeforeground='black')
    buttonj_calc.configure(bg=light_gamma_calc[26], fg='black', activebackground=light_gamma_calc[26],
                           activeforeground='black')
    button03_calc.configure(bg=light_gamma_calc[27], fg='black', activebackground=light_gamma_calc[27],
                            activeforeground='black')
    buttonq_calc.configure(bg=light_gamma_calc[28], fg='black', activebackground=light_gamma_calc[28],
                           activeforeground='black')
    buttonv_calc.configure(bg=light_gamma_calc[29], fg='black', activebackground=light_gamma_calc[29],
                           activeforeground='black')
    buttonn_calc.configure(bg=light_gamma_calc[30], fg='black', activebackground=light_gamma_calc[30],
                           activeforeground='black')
    button7_calc.configure(bg=light_gamma_calc[31], fg='black', activebackground=light_gamma_calc[31],
                           activeforeground='black')
    button8_calc.configure(bg=light_gamma_calc[32], fg='black', activebackground=light_gamma_calc[32],
                           activeforeground='black')
    button9_calc.configure(bg=light_gamma_calc[33], fg='black', activebackground=light_gamma_calc[33],
                           activeforeground='black')
    buttonf_calc.configure(bg=light_gamma_calc[34], fg='black', activebackground=light_gamma_calc[34],
                           activeforeground='black')
    button02_calc.configure(bg=light_gamma_calc[35], fg='black', activebackground=light_gamma_calc[35],
                            activeforeground='black')
    buttonr_calc.configure(bg=light_gamma_calc[36], fg='black', activebackground=light_gamma_calc[36],
                           activeforeground='black')
    buttonw_calc.configure(bg=light_gamma_calc[37], fg='black', activebackground=light_gamma_calc[37],
                           activeforeground='black')
    buttonm_calc.configure(bg=light_gamma_calc[38], fg='black', activebackground=light_gamma_calc[38],
                           activeforeground='black')
    button4_calc.configure(bg=light_gamma_calc[39], fg='black', activebackground=light_gamma_calc[39],
                           activeforeground='black')
    button5_calc.configure(bg=light_gamma_calc[40], fg='black', activebackground=light_gamma_calc[40],
                           activeforeground='black')
    button6_calc.configure(bg=light_gamma_calc[41], fg='black', activebackground=light_gamma_calc[41],
                           activeforeground='black')
    buttone_calc.configure(bg=light_gamma_calc[42], fg='black', activebackground=light_gamma_calc[42],
                           activeforeground='black')
    entry_that_get_information_of_rounding.configure(bg=light_gamma_calc[43], fg='black')
    buttons_calc.configure(bg=light_gamma_calc[44], fg='black', activebackground=light_gamma_calc[44],
                           activeforeground='black')
    buttonx_calc.configure(bg=light_gamma_calc[45], fg='black', activebackground=light_gamma_calc[45],
                           activeforeground='black')
    buttonl_calc.configure(bg=light_gamma_calc[46], fg='black', activebackground=light_gamma_calc[46],
                           activeforeground='black')
    button1_calc.configure(bg=light_gamma_calc[47], fg='black', activebackground=light_gamma_calc[47],
                           activeforeground='black')
    button2_calc.configure(bg=light_gamma_calc[48], fg='black', activebackground=light_gamma_calc[48],
                           activeforeground='black')
    button3_calc.configure(bg=light_gamma_calc[49], fg='black', activebackground=light_gamma_calc[49],
                           activeforeground='black')
    buttond_calc.configure(bg=light_gamma_calc[50], fg='black', activebackground=light_gamma_calc[50],
                           activeforeground='black')
    buttonb_calc.configure(bg=light_gamma_calc[51], fg='black', activebackground=light_gamma_calc[51],
                           activeforeground='black')
    buttont_calc.configure(bg=light_gamma_calc[52], fg='black', activebackground=light_gamma_calc[52],
                           activeforeground='black')
    buttony_calc.configure(bg=light_gamma_calc[53], fg='black', activebackground=light_gamma_calc[53],
                           activeforeground='black')
    buttonk_calc.configure(bg=light_gamma_calc[54], fg='black', activebackground=light_gamma_calc[54],
                           activeforeground='black')
    button0_calc.configure(bg=light_gamma_calc[55], fg='black', activebackground=light_gamma_calc[55],
                           activeforeground='black')
    buttona_calc.configure(bg=light_gamma_calc[56], fg='black', activebackground=light_gamma_calc[56],
                           activeforeground='black')
    button01_calc.configure(bg=light_gamma_calc[57], fg='black', activebackground=light_gamma_calc[57],
                            activeforeground='black')
    buttonc_calc.configure(bg=light_gamma_calc[58], fg='black', activebackground=light_gamma_calc[58],
                           activeforeground='black')
    button00_calc.configure(bg=light_gamma_calc[59], fg='black', activebackground=light_gamma_calc[59],
                            activeforeground='black')


def configure_color2_calc():
    global general_background_label_calc
    the_entry_for_example.configure(bg=light_gamma_calc[40], fg='#9f003d')
    beluga_calc.configure(bg=light_gamma_calc[19], fg='#9f003d')
    buttonp_calc.configure(bg=light_gamma_calc[20], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[20])
    buttonu_calc.configure(bg=light_gamma_calc[21], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[21])
    buttono_calc.configure(bg=light_gamma_calc[22], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[22])
    buttong_calc.configure(bg=light_gamma_calc[23], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[23])
    buttonh_calc.configure(bg=light_gamma_calc[24], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[24])
    buttoni_calc.configure(bg=light_gamma_calc[25], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[25])
    buttonj_calc.configure(bg=light_gamma_calc[26], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[26])
    button03_calc.configure(bg=light_gamma_calc[27], fg='#9f003d', activeforeground='#9f003d',
                            activebackground=light_gamma_calc[27])
    buttonq_calc.configure(bg=light_gamma_calc[28], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[28])
    buttonv_calc.configure(bg=light_gamma_calc[29], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[29])
    buttonn_calc.configure(bg=light_gamma_calc[30], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[30])
    button7_calc.configure(bg=light_gamma_calc[31], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[31])
    button8_calc.configure(bg=light_gamma_calc[32], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[32])
    button9_calc.configure(bg=light_gamma_calc[33], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[33])
    buttonf_calc.configure(bg=light_gamma_calc[34], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[34])
    button02_calc.configure(bg=light_gamma_calc[35], fg='#9f003d', activeforeground='#9f003d',
                            activebackground=light_gamma_calc[35])
    buttonr_calc.configure(bg=light_gamma_calc[36], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[36])
    buttonw_calc.configure(bg=light_gamma_calc[37], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[37])
    buttonm_calc.configure(bg=light_gamma_calc[38], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[38])
    button4_calc.configure(bg=light_gamma_calc[39], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[39])
    button5_calc.configure(bg=light_gamma_calc[40], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[40])
    button6_calc.configure(bg=light_gamma_calc[41], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[41])
    buttone_calc.configure(bg=light_gamma_calc[42], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[42])
    entry_that_get_information_of_rounding.configure(bg=light_gamma_calc[43], fg='#9f003d')
    buttons_calc.configure(bg=light_gamma_calc[44], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[44])
    buttonx_calc.configure(bg=light_gamma_calc[45], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[45])
    buttonl_calc.configure(bg=light_gamma_calc[46], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[46])
    button1_calc.configure(bg=light_gamma_calc[47], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[47])
    button2_calc.configure(bg=light_gamma_calc[48], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[48])
    button3_calc.configure(bg=light_gamma_calc[49], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[49])
    buttond_calc.configure(bg=light_gamma_calc[50], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[50])
    buttonb_calc.configure(bg=light_gamma_calc[51], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[51])
    buttont_calc.configure(bg=light_gamma_calc[52], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[52])
    buttony_calc.configure(bg=light_gamma_calc[53], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[53])
    buttonk_calc.configure(bg=light_gamma_calc[54], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[54])
    button0_calc.configure(bg=light_gamma_calc[55], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[55])
    buttona_calc.configure(bg=light_gamma_calc[56], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[56])
    button01_calc.configure(bg=light_gamma_calc[57], fg='#9f003d', activeforeground='#9f003d',
                            activebackground=light_gamma_calc[57])
    buttonc_calc.configure(bg=light_gamma_calc[58], fg='#9f003d', activeforeground='#9f003d',
                           activebackground=light_gamma_calc[58])
    button00_calc.configure(bg=light_gamma_calc[59], fg='#9f003d', activeforeground='#9f003d',
                            activebackground=light_gamma_calc[59])


def configure_color3_calc():
    global general_background_label_calc
    the_entry_for_example.configure(bg=light_gamma_calc[40], fg='#082567')
    beluga_calc.configure(bg=light_gamma_calc[19], fg='#082567')
    buttonp_calc.configure(bg=light_gamma_calc[20], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[20])
    buttonu_calc.configure(bg=light_gamma_calc[21], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[21])
    buttono_calc.configure(bg=light_gamma_calc[22], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[22])
    buttong_calc.configure(bg=light_gamma_calc[23], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[23])
    buttonh_calc.configure(bg=light_gamma_calc[24], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[24])
    buttoni_calc.configure(bg=light_gamma_calc[25], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[25])
    buttonj_calc.configure(bg=light_gamma_calc[26], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[26])
    button03_calc.configure(bg=light_gamma_calc[27], fg='#082567', activeforeground='#082567',
                            activebackground=light_gamma_calc[27])
    buttonq_calc.configure(bg=light_gamma_calc[28], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[28])
    buttonv_calc.configure(bg=light_gamma_calc[29], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[29])
    buttonn_calc.configure(bg=light_gamma_calc[30], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[30])
    button7_calc.configure(bg=light_gamma_calc[31], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[31])
    button8_calc.configure(bg=light_gamma_calc[32], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[32])
    button9_calc.configure(bg=light_gamma_calc[33], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[33])
    buttonf_calc.configure(bg=light_gamma_calc[34], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[34])
    button02_calc.configure(bg=light_gamma_calc[35], fg='#082567', activeforeground='#082567',
                            activebackground=light_gamma_calc[35])
    buttonr_calc.configure(bg=light_gamma_calc[36], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[36])
    buttonw_calc.configure(bg=light_gamma_calc[37], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[37])
    buttonm_calc.configure(bg=light_gamma_calc[38], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[38])
    button4_calc.configure(bg=light_gamma_calc[39], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[39])
    button5_calc.configure(bg=light_gamma_calc[40], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[40])
    button6_calc.configure(bg=light_gamma_calc[41], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[41])
    buttone_calc.configure(bg=light_gamma_calc[42], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[42])
    entry_that_get_information_of_rounding.configure(bg=light_gamma_calc[43], fg='#082567')
    buttons_calc.configure(bg=light_gamma_calc[44], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[44])
    buttonx_calc.configure(bg=light_gamma_calc[45], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[45])
    buttonl_calc.configure(bg=light_gamma_calc[46], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[46])
    button1_calc.configure(bg=light_gamma_calc[47], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[47])
    button2_calc.configure(bg=light_gamma_calc[48], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[48])
    button3_calc.configure(bg=light_gamma_calc[49], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[49])
    buttond_calc.configure(bg=light_gamma_calc[50], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[50])
    buttonb_calc.configure(bg=light_gamma_calc[51], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[51])
    buttont_calc.configure(bg=light_gamma_calc[52], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[52])
    buttony_calc.configure(bg=light_gamma_calc[53], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[53])
    buttonk_calc.configure(bg=light_gamma_calc[54], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[54])
    button0_calc.configure(bg=light_gamma_calc[55], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[55])
    buttona_calc.configure(bg=light_gamma_calc[56], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[56])
    button01_calc.configure(bg=light_gamma_calc[57], fg='#082567', activeforeground='#082567',
                            activebackground=light_gamma_calc[57])
    buttonc_calc.configure(bg=light_gamma_calc[58], fg='#082567', activeforeground='#082567',
                           activebackground=light_gamma_calc[58])
    button00_calc.configure(bg=light_gamma_calc[59], fg='#082567', activeforeground='#082567',
                            activebackground=light_gamma_calc[59])


def configure_color4_calc():
    global general_background_label_calc
    the_entry_for_example.configure(bg=light_gamma_calc[40], fg='black')
    beluga_calc.configure(bg=light_gamma_calc[19], fg='white')
    buttonp_calc.configure(bg=light_gamma_calc[20], fg='black', activebackground='white', activeforeground='black')
    buttonu_calc.configure(bg=light_gamma_calc[21], fg='black', activebackground='white', activeforeground='black')
    buttono_calc.configure(bg=light_gamma_calc[22], fg='black', activebackground='white', activeforeground='black')
    buttong_calc.configure(bg=light_gamma_calc[23], fg='black', activebackground='white', activeforeground='black')
    buttonh_calc.configure(bg=light_gamma_calc[24], fg='black', activebackground='white', activeforeground='black')
    buttoni_calc.configure(bg=light_gamma_calc[25], fg='black', activebackground='white', activeforeground='black')
    buttonj_calc.configure(bg=light_gamma_calc[26], fg='black', activebackground='white', activeforeground='black')
    button03_calc.configure(bg=light_gamma_calc[27], fg='black', activebackground='white', activeforeground='black')
    buttonq_calc.configure(bg=light_gamma_calc[28], fg='black', activebackground='white', activeforeground='black')
    buttonv_calc.configure(bg=light_gamma_calc[29], fg='black', activebackground='white', activeforeground='black')
    buttonn_calc.configure(bg=light_gamma_calc[30], fg='black', activebackground='white', activeforeground='black')
    button7_calc.configure(bg=light_gamma_calc[31], fg='black', activebackground='white', activeforeground='black')
    button8_calc.configure(bg=light_gamma_calc[32], fg='black', activebackground='white', activeforeground='black')
    button9_calc.configure(bg=light_gamma_calc[33], fg='black', activebackground='white', activeforeground='black')
    buttonf_calc.configure(bg=light_gamma_calc[34], fg='black', activebackground='white', activeforeground='black')
    button02_calc.configure(bg=light_gamma_calc[35], fg='black', activebackground='white', activeforeground='black')
    buttonr_calc.configure(bg=light_gamma_calc[36], fg='black', activebackground='white', activeforeground='black')
    buttonw_calc.configure(bg=light_gamma_calc[37], fg='black', activebackground='white', activeforeground='black')
    buttonm_calc.configure(bg=light_gamma_calc[38], fg='black', activebackground='white', activeforeground='black')
    button4_calc.configure(bg=light_gamma_calc[39], fg='black', activebackground='white', activeforeground='black')
    button5_calc.configure(bg=light_gamma_calc[40], fg='black', activebackground='white', activeforeground='black')
    button6_calc.configure(bg=light_gamma_calc[41], fg='black', activebackground='white', activeforeground='black')
    buttone_calc.configure(bg=light_gamma_calc[42], fg='black', activebackground='white', activeforeground='black')
    entry_that_get_information_of_rounding.configure(bg=light_gamma_calc[43], fg='black')
    buttons_calc.configure(bg=light_gamma_calc[44], fg='black', activebackground='white', activeforeground='black')
    buttonx_calc.configure(bg=light_gamma_calc[45], fg='black', activebackground='white', activeforeground='black')
    buttonl_calc.configure(bg=light_gamma_calc[46], fg='black', activebackground='white', activeforeground='black')
    button1_calc.configure(bg=light_gamma_calc[47], fg='black', activebackground='white', activeforeground='black')
    button2_calc.configure(bg=light_gamma_calc[48], fg='black', activebackground='white', activeforeground='black')
    button3_calc.configure(bg=light_gamma_calc[49], fg='black', activebackground='white', activeforeground='black')
    buttond_calc.configure(bg=light_gamma_calc[50], fg='black', activebackground='white', activeforeground='black')
    buttonb_calc.configure(bg=light_gamma_calc[51], fg='black', activebackground='white', activeforeground='black')
    buttont_calc.configure(bg=light_gamma_calc[52], fg='black', activebackground='white', activeforeground='black')
    buttony_calc.configure(bg=light_gamma_calc[53], fg='black', activebackground='white', activeforeground='black')
    buttonk_calc.configure(bg=light_gamma_calc[54], fg='black', activebackground='white', activeforeground='black')
    button0_calc.configure(bg=light_gamma_calc[55], fg='black', activebackground='white', activeforeground='black')
    buttona_calc.configure(bg=light_gamma_calc[56], fg='black', activebackground='white', activeforeground='black')
    button01_calc.configure(bg=light_gamma_calc[57], fg='black', activebackground='white', activeforeground='black')
    buttonc_calc.configure(bg=light_gamma_calc[58], fg='black', activebackground='white', activeforeground='black')
    button00_calc.configure(bg=light_gamma_calc[59], fg='black', activebackground='white', activeforeground='black')


def clicki_group_calc():
    global general_background_label_calc
    general_background_label_calc.configure(image=group_bg_image_calc)
    settings_of_calculator['color'] = 'group'
    the_entry_for_example.configure(bg='white', fg='black')
    beluga_calc.configure(bg='black', fg='white')
    buttonp_calc.configure(fg='black', bg='SkyBlue3', activebackground='Skyblue3', activeforeground='black')
    buttonu_calc.configure(fg='black', bg='SkyBlue3', activebackground='Skyblue3', activeforeground='black')
    buttono_calc.configure(fg='black', bg='yellow', activebackground='yellow', activeforeground='black')
    buttong_calc.configure(fg='black', bg='orange', activebackground='orange', activeforeground='black')
    buttonh_calc.configure(fg='black', bg='orange', activebackground='orange', activeforeground='black')
    buttoni_calc.configure(fg='black', bg='orange', activebackground='orange', activeforeground='black')
    buttonj_calc.configure(fg='black', bg='yellow', activebackground='yellow', activeforeground='black')
    button03_calc.configure(fg='black', bg='mistyrose', activebackground='mistyrose', activeforeground='black')
    buttonq_calc.configure(fg='black', bg='coral2', activebackground='coral2', activeforeground='black')
    buttonv_calc.configure(fg='black', bg='SkyBlue3', activebackground='Skyblue3', activeforeground='black')
    buttonn_calc.configure(fg='black', bg='purple', activebackground='purple', activeforeground='black')
    button7_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    button8_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    button9_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    buttonf_calc.configure(fg='black', bg='yellow', activebackground='yellow', activeforeground='black')
    button02_calc.configure(fg='black', bg='mistyrose', activebackground='mistyrose', activeforeground='black')
    buttonr_calc.configure(fg='black', bg='coral2', activebackground='coral2', activeforeground='black')
    buttonw_calc.configure(fg='black', bg='purple', activebackground='purple', activeforeground='black')
    buttonm_calc.configure(fg='black', bg='purple', activebackground='purple', activeforeground='black')
    button4_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    button5_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    button6_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    buttone_calc.configure(fg='black', bg='yellow', activebackground='yellow', activeforeground='black')
    entry_that_get_information_of_rounding.configure(fg='black', bg='mistyrose')
    buttons_calc.configure(fg='black', bg='coral2', activebackground='coral2', activeforeground='black')
    buttonx_calc.configure(fg='black', bg='purple', activebackground='purple', activeforeground='black')
    buttonl_calc.configure(fg='black', bg='pale green', activebackground='pale green', activeforeground='black')
    button1_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    button2_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    button3_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    buttond_calc.configure(fg='black', bg='yellow', activebackground='yellow', activeforeground='black')
    buttonb_calc.configure(fg='black', bg='gray', activebackground='gray', activeforeground='black')
    buttont_calc.configure(fg='black', bg='coral2', activebackground='coral2', activeforeground='black')
    buttony_calc.configure(fg='black', bg='pale green', activebackground='pale green', activeforeground='black')
    buttonk_calc.configure(fg='black', bg='pale green', activebackground='pale green', activeforeground='black')
    button0_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    buttona_calc.configure(fg='black', bg='light yellow', activebackground='light yellow', activeforeground='black')
    button01_calc.configure(fg='white', bg='dark blue', activeforeground='white', activebackground='dark blue')
    buttonc_calc.configure(fg='black', bg='yellow', activebackground='yellow', activeforeground='black')
    button00_calc.configure(fg='black', bg='gray', activebackground='gray', activeforeground='black')


def clicki0_calc():
    global the_entry_for_example, beluga_calc, example, walmart_calc, cornalt_calc, tallnut_calc, flag_smart_focus_calc
    global flag_of_window_exist
    beluga_calc.delete(0, END)
    if len(the_entry_for_example.get()) > 168:
        the_entry_for_example.delete(168, END)
    example = the_entry_for_example.get()
    awesome_solo1_calc = (example == 'help' or example == 'помощь' or example == 'помогите')
    awesome_solo2_calc = (example == 'hint' or example == 'совет')
    awesome_solo3_calc = (example == 'design' or example == 'дизайн' or example == 'style')
    awesome_solo4_calc = (example == 'стиль' or example == 'display' or example == 'дисплей')
    awesome_solo5_calc = (example == 'история' or example == 'history' or example == 'examples')
    awesome_solo6_calc = (example == 'примеры' or example == 'recent' or example == 'недавнее')
    if (awesome_solo1_calc or awesome_solo2_calc) and not walmart_calc:
        walmart_calc = True
        clickbeit02_calc()
    elif (awesome_solo1_calc or awesome_solo2_calc) and walmart_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        walmart_calc = False
    if (awesome_solo3_calc or awesome_solo4_calc) and not cornalt_calc:
        cornalt_calc = True
        clickbeit03_calc()
    elif (awesome_solo3_calc or awesome_solo4_calc) and cornalt_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        cornalt_calc = False
    if (awesome_solo5_calc or awesome_solo6_calc) and not tallnut_calc:
        tallnut_calc = True
        clickbeit04_calc()
    elif (awesome_solo5_calc or awesome_solo6_calc) and tallnut_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        tallnut_calc = False
    normy_calc = (example == 'standard' or example == 'стандарт' or example == 'normal')
    if example == 'silver' or example == 'серебряный':
        clicki_silver_calc()
    elif example == 'red' or example == 'красный':
        clicki_red_calc()
    elif example == 'green' or example == 'зеленый' or example == 'зелёный':
        clicki_green_calc()
    elif example == 'blue' or example == 'синий':
        clicki_blue_calc()
    elif example == 'yellow' or example == 'желтый' or example == 'жёлтый':
        clicki_yellow_calc()
    elif example == 'magenta' or example == 'маджента' or example == 'магента':
        clicki_magenta_calc()
    elif example == 'cyan' or example == 'циан':
        clicki_cyan_calc()
    elif example == 'purple' or example == 'пурпур':
        clicki_purple_calc()
    elif example == 'violet' or example == 'фиолетовый':
        clicki_violet_calc()
    elif example == 'pink' or example == 'розовый':
        clicki_pink_calc()
    elif example == 'orange' or example == 'оранжевый':
        clicki_orange_calc()
    elif example == 'lime' or example == 'салатовый' or example == 'лайм':
        clicki_lime_calc()
    elif example == 'sky' or example == 'голубой':
        clicki_skyblue_calc()
    elif example == 'gold' or example == 'золотой':
        clicki_gold_calc()
    elif example == 'emerald' or example == 'изумрудный':
        clicki_emerald_calc()
    elif normy_calc or example == 'классика' or example == 'classic' or example == 'обычный':
        clicki_standard_calc()
    elif example == 'sapphire' or example == 'сапфир':
        clicki_sapphire_calc()
    elif example == 'ruby' or example == 'рубин':
        clicki_ruby_calc()
    elif example == 'group' or example == 'группа':
        clicki_group_calc()
    elif example == 'rainbow' or example == 'радужный' or example == 'радуга':
        clicki_rainbow_configure_calc()
    else:
        do_nothing_calc = 0
        do_nothing_calc += 1
    beluga_calc.insert(END, str(solver_of_the_example()))
    configure_size_of_example_calc()


def clicki0_equal_calc():
    global the_entry_for_example, beluga_calc, walmart_calc, cornalt_calc, tallnut_calc, history_of_calculations, example
    beluga_calc.delete(0, END)
    if len(the_entry_for_example.get()) > 168:
        the_entry_for_example.delete(168, END)

    if len(the_entry_for_example.get()) != 0 and the_entry_for_example.get()[-1] == '=':
        example = the_entry_for_example.get()[:-1].lower()
    else:
        example = the_entry_for_example.get().lower()
    the_entry_for_example.delete(0, END)
    the_entry_for_example.insert(END, example)
    awesome_solo1_calc = (example == 'help' or example == 'помощь' or example == 'помогите')
    awesome_solo2_calc = (example == 'hint' or example == 'совет')
    awesome_solo3_calc = (example == 'design' or example == 'дизайн' or example == 'style')
    awesome_solo4_calc = (example == 'стиль' or example == 'display' or example == 'дисплей')
    awesome_solo5_calc = (example == 'история' or example == 'history' or example == 'examples')
    awesome_solo6_calc = (example == 'примеры' or example == 'recent' or example == 'недавнее')
    if (awesome_solo1_calc or awesome_solo2_calc) and not walmart_calc:
        walmart_calc = True
        clickbeit02_calc()
    elif (awesome_solo1_calc or awesome_solo2_calc) and walmart_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        walmart_calc = False
    if (awesome_solo3_calc or awesome_solo4_calc) and not cornalt_calc:
        cornalt_calc = True
        clickbeit03_calc()
    elif (awesome_solo3_calc or awesome_solo4_calc) and cornalt_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        cornalt_calc = False
    if (awesome_solo5_calc or awesome_solo6_calc) and not tallnut_calc:
        tallnut_calc = True
        clickbeit04_calc()
    elif (awesome_solo5_calc or awesome_solo6_calc) and tallnut_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        tallnut_calc = False
    normy_calc = (example == 'standard' or example == 'стандарт' or example == 'normal')
    if example == 'silver' or example == 'серебряный':
        clicki_silver_calc()
    elif example == 'red' or example == 'красный':
        clicki_red_calc()
    elif example == 'green' or example == 'зеленый':
        clicki_green_calc()
    elif example == 'blue' or example == 'синий':
        clicki_blue_calc()
    elif example == 'yellow' or example == 'желтый':
        clicki_yellow_calc()
    elif example == 'magenta' or example == 'маджента' or example == 'магента':
        clicki_magenta_calc()
    elif example == 'cyan' or example == 'циан':
        clicki_cyan_calc()
    elif example == 'purple' or example == 'пурпур':
        clicki_purple_calc()
    elif example == 'violet' or example == 'фиолетовый':
        clicki_violet_calc()
    elif example == 'pink' or example == 'розовый':
        clicki_pink_calc()
    elif example == 'orange' or example == 'оранжевый':
        clicki_orange_calc()
    elif example == 'lime' or example == 'салатовый' or example == 'лайм':
        clicki_lime_calc()
    elif example == 'sky' or example == 'голубой':
        clicki_skyblue_calc()
    elif example == 'gold' or example == 'золотой':
        clicki_gold_calc()
    elif example == 'emerald' or example == 'изумрудный':
        clicki_emerald_calc()
    elif normy_calc or example == 'классика' or example == 'classic' or example == 'обычный':
        clicki_standard_calc()
    elif example == 'sapphire' or example == 'сапфир':
        clicki_sapphire_calc()
    elif example == 'ruby' or example == 'рубин':
        clicki_ruby_calc()
    elif example == 'group' or example == 'группа':
        clicki_group_calc()
    elif example == 'rainbow' or example == 'радужный' or example == 'радуга':
        clicki_rainbow_configure_calc()
    beluga_calc.insert(END, str(solver_of_the_example()))
    configure_size_of_example_calc()


def clickbeit1_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '1')
    else:
        entry_that_get_information_of_rounding.insert('insert', '1')
    clicki0_calc()


def clickbeit2_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '2')
    else:
        entry_that_get_information_of_rounding.insert('insert', '2')
    clicki0_calc()


def clickbeit3_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '3')
    else:
        entry_that_get_information_of_rounding.insert('insert', '3')
    clicki0_calc()


def clickbeit4_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '4')
    else:
        entry_that_get_information_of_rounding.insert('insert', '4')
    clicki0_calc()


def clickbeit5_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '5')
    else:
        entry_that_get_information_of_rounding.insert('insert', '5')
    clicki0_calc()


def clickbeit6_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '6')
    else:
        entry_that_get_information_of_rounding.insert('insert', '6')
    clicki0_calc()


def clickbeit7_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '7')
    else:
        entry_that_get_information_of_rounding.insert('insert', '7')
    clicki0_calc()


def clickbeit8_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '8')
    else:
        entry_that_get_information_of_rounding.insert('insert', '8')
    clicki0_calc()


def clickbeit9_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '9')
    else:
        entry_that_get_information_of_rounding.insert('insert', '9')
    clicki0_calc()


def clickbeit0_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '0')
    else:
        entry_that_get_information_of_rounding.insert('insert', '0')
    clicki0_calc()


def clickbeit00_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global history_of_calculations, beluga_calc
    global flag_exist_universe_calc, text_history_area_calc, universe_calc
    global max_amount_of_examples_in_history_of_calculations
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()) > 0 and the_entry_for_example.get()[-1] == '=':
            simply_the_best_calc = the_entry_for_example.get()[:-1]
        else:
            simply_the_best_calc = the_entry_for_example.get()
        clicki0_equal_calc()
        check_the_equal = True
        for equality_cheking_calc in beluga_calc.get():
            if equality_cheking_calc not in '0123456789Ee-+.*^() ':
                check_the_equal = False
                break
        if check_the_equal and len(the_entry_for_example.get()) != 0:
            date_time_calc = str(datetime.datetime.today())[:-7]
            text_history_calculat0_calc = simply_the_best_calc + '\n' + beluga_calc.get() + '\n'
            text_history_calculat0_calc = text_history_calculat0_calc + date_time_calc + '\n' + '\n'
            splitstephistory_of_calculations = text_history_calculat0_calc + history_of_calculations
            split0_history_of_calculations = splitstephistory_of_calculations.split('\n')
            if len(split0_history_of_calculations) <= max_amount_of_examples_in_history_of_calculations:
                history_of_calculations = '\n'.join(split0_history_of_calculations)
                if flag_exist_universe_calc:
                    date_time_calc = str(datetime.datetime.today())[:-7]
                    text_history_area_calc['state'] = NORMAL
                    text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                    text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                    text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                    text_history_area_calc['state'] = DISABLED
                else:
                    do_not_anithing_calc = 0
                    do_not_anithing_calc += 1
            else:
                history_of_calculations = '\n'.join(split0_history_of_calculations[:max_amount_of_examples_in_history_of_calculations])
                if flag_exist_universe_calc:
                    date_time_calc = str(datetime.datetime.today())[:-7]
                    text_history_area_calc['state'] = NORMAL
                    text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                    text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                    text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                    text_history_area_calc.delete(1.0, END)
                    split_history_of_calculations = history_of_calculations.split('\n')
                    lindow_tag_calc = 0
                    for changable_color_text_calc in split_history_of_calculations:
                        lindow_tag_calc += 1
                        if lindow_tag_calc % 4 == 1:
                            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_maroon_text_calc')
                        elif lindow_tag_calc % 4 == 2:
                            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_green_text_calc')
                        elif lindow_tag_calc % 4 == 3:
                            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_blue_text_calc')
                        else:
                            text_history_area_calc.insert(END, '\n')
                    text_history_area_calc['state'] = DISABLED
                else:
                    do_not_anithing_calc = 0
                    do_not_anithing_calc += 1
        the_entry_for_example.delete(0, END)
    else:
        entry_that_get_information_of_rounding.delete(0, END)
    clicki0_calc()


def clickbeita_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if the_entry_for_example.index('insert') == 0:
            the_entry_for_example.insert('insert', '0.')
        elif the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] not in list('0123456789'):
            the_entry_for_example.insert('insert', '0.')
        else:
            the_entry_for_example.insert('insert', '.')
    clicki0_calc()


def clickbeitb_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
    else:
        entry_that_get_information_of_rounding.delete(entry_that_get_information_of_rounding.index('insert') - 1)
    clicki0_calc()


def clickbeitc_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '+')
    clicki0_calc()


def clickbeitd_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '-')
    clicki0_calc()


def clickbeite_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '•')
    clicki0_calc()


def clickbeitf_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '/')
    clicki0_calc()


def clickbeitg_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•(')
        else:
            the_entry_for_example.insert('insert', '(')
    clicki0_calc()


def clickbeith_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', ')')
    clicki0_calc()


def clickbeiti_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '|')
    clicki0_calc()


def clickbeitj_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '^')
    clicki0_calc()


def clickbeitk_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', 'mod')
    clicki0_calc()


def clickbeitl_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', 'div')
    clicki0_calc()


def clickbeitm_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', 'base')
    clicki0_calc()


def clickbeitn_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•log')
        else:
            the_entry_for_example.insert('insert', 'log')
    clicki0_calc()


def clickbeito_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '√')
    clicki0_calc()


def clickbeitp_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•pip')
        else:
            the_entry_for_example.insert('insert', 'pip')
    clicki0_calc()


def clickbeitq_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•sin(')
        else:
            the_entry_for_example.insert('insert', 'sin(')
    clicki0_calc()


def clickbeitr_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•cos(')
        else:
            the_entry_for_example.insert('insert', 'cos(')
    clicki0_calc()


def clickbeits_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•tg(')
        else:
            the_entry_for_example.insert('insert', 'tg(')
    clicki0_calc()


def clickbeitt_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•ctg(')
        else:
            the_entry_for_example.insert('insert', 'ctg(')
    clicki0_calc()


def clickbeitu_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•π')
        else:
            the_entry_for_example.insert('insert', 'π')
    clicki0_calc()


def clickbeitv_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•e')
        else:
            the_entry_for_example.insert('insert', 'e')
    clicki0_calc()


def clickbeitw_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•ln(')
        else:
            the_entry_for_example.insert('insert', 'ln(')
    clicki0_calc()


def clickbeitx_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
            the_entry_for_example.insert('insert', '•lg(')
        else:
            the_entry_for_example.insert('insert', 'lg(')
    clicki0_calc()


def clickbeity_calc():
    global the_entry_for_example, entry_that_get_information_of_rounding, flag_smart_focus_calc
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    if not flag_smart_focus_calc:
        the_entry_for_example.insert('insert', '!')
    else:
        entry_that_get_information_of_rounding.insert('insert', '!')
    clicki0_calc()


def clickbeit01_calc():
    global the_entry_for_example, example, beluga_calc, history_of_calculations, walmart_calc, cornalt_calc
    global flag_exist_universe_calc, text_history_area_calc, universe_calc, tallnut_calc
    global max_amount_of_examples_in_history_of_calculations
    global wodden_calc, flag_wodden_calc
    wodden_calc = 0
    flag_wodden_calc = 1
    toto_calc = str(the_entry_for_example.get()).lower()
    the_entry_for_example.delete(0, END)
    the_entry_for_example.insert(END, toto_calc)
    if len(the_entry_for_example.get()) > 0 and the_entry_for_example.get()[-1] == '=':
        simply_the_best_calc = the_entry_for_example.get()[:-1]
    else:
        simply_the_best_calc = the_entry_for_example.get()
    clicki0_equal_calc()
    awesome_solo1_calc = (example == 'help' or example == 'помощь' or example == 'помогите')
    awesome_solo2_calc = (example == 'hint' or example == 'совет')
    awesome_solo3_calc = (example == 'design' or example == 'дизайн' or example == 'style')
    awesome_solo4_calc = (example == 'стиль' or example == 'display' or example == 'дисплей')
    awesome_solo5_calc = (example == 'история' or example == 'history' or example == 'examples')
    awesome_solo6_calc = (example == 'примеры' or example == 'recent' or example == 'недавнее')
    if (awesome_solo1_calc or awesome_solo2_calc) and not walmart_calc:
        walmart_calc = True
        clickbeit02_calc()
    elif (awesome_solo1_calc or awesome_solo2_calc) and walmart_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        walmart_calc = False
    if (awesome_solo3_calc or awesome_solo4_calc) and not cornalt_calc:
        cornalt_calc = True
        clickbeit03_calc()
    elif (awesome_solo3_calc or awesome_solo4_calc) and cornalt_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        cornalt_calc = False
    if (awesome_solo5_calc or awesome_solo6_calc) and not tallnut_calc:
        tallnut_calc = True
        clickbeit03_calc()
    elif (awesome_solo5_calc or awesome_solo6_calc) and tallnut_calc:
        does_not_do_anything_calc = 0
        does_not_do_anything_calc += 1
    else:
        tallnut_calc = False
    check_the_equal = True
    for equality_cheking_calc in beluga_calc.get():
        if equality_cheking_calc not in '0123456789Ee-+.*^() ':
            check_the_equal = False
            break
    if check_the_equal:
        example2 = str(beluga_calc.get())
        the_entry_for_example.delete(0, END)
        the_entry_for_example.insert(END, example2)
        configure_size_of_example_calc()
        if len(the_entry_for_example.get()) != 0:
            date_time_calc = str(datetime.datetime.today())[:-7]
            text_history_calculat0_calc = simply_the_best_calc + '\n' + beluga_calc.get() + '\n'
            text_history_calculat0_calc = text_history_calculat0_calc + date_time_calc + '\n' + '\n'
            splitstephistory_of_calculations = text_history_calculat0_calc + history_of_calculations
            split0_history_of_calculations = splitstephistory_of_calculations.split('\n')
            if len(split0_history_of_calculations) <= max_amount_of_examples_in_history_of_calculations:
                history_of_calculations = '\n'.join(split0_history_of_calculations)
                if flag_exist_universe_calc:
                    date_time_calc = str(datetime.datetime.today())[:-7]
                    text_history_area_calc['state'] = NORMAL
                    text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                    text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                    text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                    text_history_area_calc['state'] = DISABLED
                else:
                    do_not_anithing_calc = 0
                    do_not_anithing_calc += 1
            else:
                history_of_calculations = '\n'.join(split0_history_of_calculations[:max_amount_of_examples_in_history_of_calculations])
                if flag_exist_universe_calc:
                    date_time_calc = str(datetime.datetime.today())[:-7]
                    text_history_area_calc['state'] = NORMAL
                    text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                    text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                    text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                    text_history_area_calc.delete(1.0, END)
                    split_history_of_calculations = history_of_calculations.split('\n')
                    lindow_tag_calc = 0
                    for changable_color_text_calc in split_history_of_calculations:
                        lindow_tag_calc += 1
                        if lindow_tag_calc % 4 == 1:
                            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_maroon_text_calc')
                        elif lindow_tag_calc % 4 == 2:
                            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_green_text_calc')
                        elif lindow_tag_calc % 4 == 3:
                            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_blue_text_calc')
                        else:
                            text_history_area_calc.insert(END, '\n')
                    text_history_area_calc['state'] = DISABLED
                else:
                    do_not_anithing_calc = 0
                    do_not_anithing_calc += 1


def clickbeit02_calc():
    global button02_calc, star_calc, meteor_calc, button03_calc, button02_calc
    try:
        universe_calc.destroy()
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    try:
        star_calc.destroy()
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    try:
        meteor_calc.destroy()
        button03_calc['state'] = ACTIVE
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    button02_calc['state'] = DISABLED
    star_calc = Toplevel()
    star_calc.focus_set()
    star_calc.bind('<Escape>', close_esc_star_calc)
    star_calc.protocol('WM_DELETE_WINDOW', lambda: exist_star_calc(star_calc))
    star_calc.geometry('1270x950+0+0')
    star_calc.title('Как использовать приложение "Калькулятор".')
    star_calc.iconbitmap('calc imgs/calculator_help_icon.ico')
    star_calc.resizable(width=False, height=False)
    star_calc['bg'] = 'light yellow'
    texta_help_calc = ('Описание.\n'
                       'Калькулятор — приложение, позволяющее быстро и удобно ввести пример, вычислить его и \n'
                       'приблизительно указать почему пример введён неправильно.\n'
                       'Из всей инструкции запомните то, что вам нравится больше всего и применяйте на здоровье!\n'
                       'Как ввести пример?\n'
                       'Около каждого типа операции в скобках будут указаны символы, которые можно использовать для '
                       'ввода:\n'
                       'сложение(+)\n'
                       'вычитание(-)\n'
                       'умножение(*, •, х)\n'
                       'деление(/, :)\n'
                       'степень(••, **, ^)\n'
                       'модуль(|, m, м)\n'
                       'скобки по-обычному\n'
                       'деление с остатком(mod, мод, %, ост, ost)\n'
                       'деление нацело(//, ::, @, цел, cel, div)\n'
                       'корень(√, к, k, r)\n'
                       'десятичная дробь через запятую или точку\n'
                       'факториал от числа x (f(x), fa(x), факт(x), fact(x), x!)\n'
                       'синус(син, sin, sn)\n'
                       'косинус(кос, cos, cs),\n'
                       'тангенс(тан, tan, tn, tg)\n'
                       'котангенс(cotan, котан, ctg, cnt, ктн, ct),\n'
                       '5√32 — корень 5 степени из 32\n'
                       'константа e(e),\n'
                       'константа пи=3,14... (pi, пи, π)\n'
                       'пи радианов=180 градусов(pip, пип)\n'
                       'десятичный логарифм(лг, lg)\n'
                       'натуральный логарифм(лн, ln)\n'
                       'логарифм 25 по основанию 5 (log25po5, log25to5, лог25по5, log25base5, log25_5)\n'
                       'Поле среди кнопок нужно для ввода числа знаков после запятой, до которого будет округлён ответ.\n'
                       'Приоритетность операций.\n'
                       'Под скобкой или модулем >>> факториал >>> корень >>> логарифм >>> другие функции >>> степень >>>\n'
                       'умножение или деление или деление нацело или деление с остатком >>> cложение или вычитание.\n'
                       'Предупреждения!!!\n'
                       '❗ Пример не может быть длиннее 168 символов.\n'
                       '❗ Знак умножить писать обязательно, то есть нельзя 5sin90, можно 5*sin90.\n'
                       '❗ Не стоит использовать значения чисел, модуль которых меньше, чем 10 в степени -100 или больше,\n'
                       '   чем 10 в степени 300, из-за потери точности вычислений.\n'
                       '❗ Верно: 2^2^2^2=2^2^4=2^16=65536, 3k3k19683=3k27=3, -10^(-40)=-(10^(-40)), но неверно:\n'
                       '   2^2^2^2=4^2^2=16^2=256, 3k3k19683=1.442249k19683=949.2, -10^(-40)=(-10)^(-40).\n'
                       '❗ Нельзя использовать округление более, чем 100 знаков после запятой.\n'
                       '❗ π или e или бесконечную дробь, модуль которой меньше 10^(-6), не всегда можно округлить.\n'
                       '❗ Приложение не даст вам открыть более 1 дополнительного окна во избежание бардака.\n'
                       'Лайфхаки и преимущества!\n'
                       '★ C этим калькулятором в точности вычисления тригонометрических функций сравнится только\n'
                       '    нейросеть "WolframAlfa".\n'
                       '★ Калькулятор рассчитан на удобный, быстрый ввод примеров.\n'
                       '★ В примере минус можно использовать после символов сложения, вычитания, умножения, деления,\n'
                       '    возведения в степень.\n'
                       '★ Между log и base можно писать любой пример без скобок.\n'
                       '★ Если после функции не стоит минус разрешено не использовать скобки при функции.\n'
                       '★ Если не знаешь какое действие важнее, возьми в скобки то, что тебе приоритетнее.\n'
                       '★ Калькулятор справится с выражением (-8)^(2/3), но калькулятор в интернете выдаст ошибку.\n'
                       'Дизайн.\n'
                       'Чтобы выбрать дизайн, достаточно нажать на кнопку "дизайн".\n'
                       'История вычислений.\n'
                       'В разделе "История" по умолчанию сохраняется 1000 последних вычислений на калькуляторе.\n'
                       'Пример сохраняется в истории, если нажать одну из кнопок: "=", "AC".\n'
                       'Чтобы появилась история вычислений, нужно нажать на кнопку в нижнем правом углу.\n'
                       'Настройки.\n'
                       'Настроишь 1 раз и забудешь!\n'
                       '⚙ Размещение калькулятора. Пишем #x;y#, где x и y — координаты левого вернего угла калькулятора.\n'
                       '⚙ Чтобы калькулятор не задавал вопросы перед выходом пишем #false#, иначе #true#.\n'
                       '⚙ Чтобы настроить количество примеров в памяти истории напишите #hisx#, где x — это число примеров.'
                       '\nКлавиатура.\n'
                       'Итак, друзья, мы добрались до самого сочного, с этим навыком вы будете порхать, как бабочка,\n'
                       'летать, как ниндзя! Ну в общем вы поняли...\n'
                       '1) Чтобы открыть окно дизайна можно просто ввести одну из этих команд: design, дизайн, style,\n'
                       '    стиль, display, дисплей, чтобы помощи — одну из этих: help, помощь, помогите, hint, совет, чтобы'
                       '\n    истории — история, history, examples, примеры, recent, недавнее.\n'
                       '2) При помощи клавиш "↑","↓","Page Up","Page Down","Home","End" можно прокручивать историю.\n'
                       '3) Можно не открывать окно для дизайна, а написать одну из команд:\n    '
                       'стандарт/классика/обычный/standard/classic/normal, красный/red, синий/blue,\n'
                       '    зелёный/зеленый/green, жёлтый/желтый/yellow, маджента/магента/magenta, циан/cyan, розовый/pink,'
                       '\n    салатовый/лайм/lime, голубой/sky, оранжевый/orange, пурпур/purple, фиолетовый/violet,\n'
                       '    изумрудный/emerald, золотой/gold, серебряный/silver, радужный/радуга/rainbow, рубин/ruby,\n'
                       '    сапфир/sapphire, группа/group.\n'
                       '3) При помощи клавиш "↑", "↓" можно переключать фокус между полем ввода примера и округления.\n'
                       '4) Пример сохраняется в истории, если нажать на одну из клавиш: "Enter", "=", "`" (обратный штрих).\n'
                       '5) Клавиша "Esc" закрывает окно, находящееся во внимании приложения.\n'
                       '6) Хотите перемещаться в истории вычислений, как путешественник во времени?\n'
                       '    Тогда, если у вас в история вычислений хранит не менее 20 примеров, зажмите crtl+z, затем\n'
                       '    crtl+y. Эффект будет незабываемым! Нажатие crtl+z перемещает на пример назад, а crtl+y вперёд.\n'
                       '    Это были бабочки, теперь поучимся мастерству скорости у настоящего ниндзя.\n'
                       '7) Чтобы удалить весь пример не нужно долго нажимать на стрелку влево, нажмите "`".\n'
                       '    Теперь ваш враг повержен!\n'
                       '8) Для того, чтобы внести ответ на пример вместо примера нужно нажать клавишу "Enter" или "=".\n'
                       '9) И самое секретное оружие мастера скорости — это CapsLock. При нажатии на эту клавишу\n'
                       '    Вселенная разрывается на части, открывается 4-ое измерение пространства.\n'
                       '    Знак умножить проставляется автоматически, больше не придётся потеть над 5sin и 5*sin.\n'
                       '    Только в модуле знак умножить проставляется не всегда, ведь как прочесть это\n'
                       '    "|5+5|7+8|2+2|"? Первый вариант: |5+5|•7+8•|2+2|=102, второй вариант |5+5•|7+8|•2+2|=157.\n'
                       '    "M" превращается в "|", "R" в "√", "*" в "•", "%" в "mod", "@" в "div",\n'
                       '    "." превращается в "0." если перед "." не стоят цифры 0 — 9, "\\" превращается в " 000",\n'
                       '    "S" в "sin(", "C" в "cos(", "T" в "tg(", "K" в "ctg(", "L" в "log", "B" в "base", "N" в '
                       '"ln(",\n'
                       '    "G" в "lg(", "P" в "π", "D" в "pip". В общем, всё по красоте.\n'
                       '!!! В случае ошибки в ответе пишите жалобу мне на продукт.')

    font_gen1_calc = font.Font(family="Arial", size=20, weight="bold", slant="italic", underline=True)
    meta_help_calc = Text(star_calc, font=('Arial', 16, 'bold'), bg='light yellow')
    meta_help_calc.place(x=2, y=2, width=1246, height=916)
    scrollbar_help_calc = ttk.Scrollbar(star_calc, orient="vertical", command=meta_help_calc.yview)
    scrollbar_help_calc.pack(side=RIGHT, fill=Y)
    meta_help_calc['yscrollcommand'] = scrollbar_help_calc.set
    star_calc.bind('<Up>', scroll_esc_universe_calc)
    star_calc.bind('<Down>', scroll_esc_universe_calc)
    meta_help_calc.tag_config('help_green_20_calc', font=font_gen1_calc, foreground='green')
    meta_help_calc.tag_config('help_green_16_calc', font=('Arial', 16, 'bold'), foreground='green')
    meta_help_calc.tag_config('help_blue_20_calc', font=font_gen1_calc, foreground='blue')
    meta_help_calc.tag_config('help_blue_16_calc', font=('Arial', 16, 'bold'), foreground='blue')
    meta_help_calc.tag_config('help_violet_20_calc', font=font_gen1_calc, foreground='purple')
    meta_help_calc.tag_config('help_violet_16_calc', font=('Arial', 16, 'bold'), foreground='purple')
    meta_help_calc.tag_config('help_gray_20_calc', font=font_gen1_calc, foreground='gray')
    meta_help_calc.tag_config('help_gray_16_calc', font=('Arial', 16, 'bold'), foreground='gray')
    meta_help_calc.tag_config('help_lime_20_calc', font=font_gen1_calc, foreground='lime')
    meta_help_calc.tag_config('help_lime_16_calc', font=('Arial', 16, 'bold'), foreground='lime')
    meta_help_calc.tag_config('help_black_20_calc', font=font_gen1_calc, foreground='black')
    meta_help_calc.tag_config('help_black_16_calc', font=('Arial', 16, 'bold'), foreground='black')
    meta_help_calc.tag_config('help_red_20_calc', font=font_gen1_calc, foreground='red')
    meta_help_calc.tag_config('help_red_16_calc', font=('Arial', 16, 'bold'), foreground='red')
    texta_split_help_calc = texta_help_calc.split('\n')
    meta_help_calc.delete(1.0, END)
    for filled_color_text_calc in range(len(texta_split_help_calc)):
        if filled_color_text_calc in [0, 4, 30]:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_black_20_calc')
        elif filled_color_text_calc < 33:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_black_16_calc')
        elif filled_color_text_calc == 33:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_red_20_calc')
        elif 33 < filled_color_text_calc <= 42:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_red_16_calc')
        elif filled_color_text_calc == 43:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_green_20_calc')
        elif 43 < filled_color_text_calc <= 52:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_green_16_calc')
        elif filled_color_text_calc == 53:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_lime_20_calc')
        elif filled_color_text_calc == 54:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_lime_16_calc')
        elif filled_color_text_calc == 55:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_violet_20_calc')
        elif 55 < filled_color_text_calc <= 58:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_violet_16_calc')
        elif filled_color_text_calc == 59:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_gray_20_calc')
        elif 59 < filled_color_text_calc <= 63:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_gray_16_calc')
        elif filled_color_text_calc == 64:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_blue_20_calc')
        elif 64 < filled_color_text_calc <= 95:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_blue_16_calc')
        else:
            meta_help_calc.insert(END, texta_split_help_calc[filled_color_text_calc] + '\n', 'help_red_20_calc')
    meta_help_calc['state'] = DISABLED
    label_star_history_calc = Label(star_calc, text='Кнопка, открывающая историю вычислений:',
                                    bg='light yellow', font=('Arial', 16, 'bold'), fg='brown')
    label_star_history_calc.place(x=735, y=920, width=480, height=25)
    button_star_history_calc = Button(star_calc, image=emoji_bg_image_calc, font=('Arial', 10, 'bold'),
                                      borderwidth=0, command=clickbeit04_calc)
    button_star_history_calc.place(x=1220, y=920, width=25, height=25)


def clickbeit03_calc():
    global button03_calc, meteor_calc, star_calc, button02_calc
    try:
        universe_calc.destroy()
        button02_calc['state'] = ACTIVE
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    try:
        star_calc.destroy()
        button02_calc['state'] = ACTIVE
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    try:
        meteor_calc.destroy()
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    button03_calc['state'] = DISABLED
    meteor_calc = Toplevel()
    meteor_calc.focus_set()
    meteor_calc.bind('<Escape>', close_esc_meteor_calc)
    meteor_calc.protocol('WM_DELETE_WINDOW', lambda: exist_meteor_calc(meteor_calc))
    meteor_calc.title('Дизайн интерфейса приложения "Калькулятор".')
    meteor_calc.iconbitmap('calc imgs/calculator_desing_icon.ico')
    meteor_calc['bg'] = 'white'
    gdx_calc = str(int(verify_but_getto_calc.split('+')[1]) + 500)
    gdy_calc = str(int(verify_but_getto_calc.split('+')[2]) + 25)
    meteor_calc.geometry('400x400+' + gdx_calc + '+' + gdy_calc)
    meteor_calc.resizable(False, False)
    yellow_btn_image_calc = Button(meteor_calc, bg='#ffff00', text='жёлтый',
                                   font=('Arial', 16, 'bold'), fg='#000000', command=clicki_yellow_calc)
    yellow_btn_image_calc.place(x=0, y=0, width=100, height=80)
    red_btn_image_calc = Button(meteor_calc, bg='#ff0000', text='красный',
                                font=('Arial', 16, 'bold'), fg='#000000', command=clicki_red_calc)
    red_btn_image_calc.place(x=100, y=0, width=100, height=80)
    green_btn_image_calc = Button(meteor_calc, bg='#00ff00', text='зелёный',
                                  font=('Arial', 16, 'bold'), fg='#000000', command=clicki_green_calc)
    green_btn_image_calc.place(x=200, y=0, width=100, height=80)
    blue_btn_image_calc = Button(meteor_calc, bg='#0000ff', text='синий',
                                 font=('Arial', 16, 'bold'), fg='#000000', command=clicki_blue_calc)
    blue_btn_image_calc.place(x=300, y=0, width=100, height=80)
    pink_btn_image_calc = Button(meteor_calc, bg='#ffc0cb', text='розовый',
                                 font=('Arial', 16, 'bold'), fg='#000000', command=clicki_pink_calc)
    pink_btn_image_calc.place(x=0, y=80, width=100, height=80)
    magenta_btn_image_calc = Button(meteor_calc, bg='#ff00ff', text='маджента',
                                    font=('Arial', 14, 'bold'), fg='#000000', command=clicki_magenta_calc)
    magenta_btn_image_calc.place(x=100, y=80, width=100, height=80)
    purple_btn_image_calc = Button(meteor_calc, bg='#800080', text='пурпур',
                                   font=('Arial', 16, 'bold'), fg='#000000', command=clicki_purple_calc)
    purple_btn_image_calc.place(x=200, y=80, width=100, height=80)
    violet_btn_image_calc = Button(meteor_calc, bg='#7f00ff', text='фиолетовый',
                                   font=('Arial', 11, 'bold'), fg='#000000', command=clicki_violet_calc)
    violet_btn_image_calc.place(x=300, y=80, width=100, height=80)
    cyan_btn_image_calc = Button(meteor_calc, bg='#00ffff', text='циан',
                                 font=('Arial', 16, 'bold'), fg='#000000', command=clicki_cyan_calc)
    cyan_btn_image_calc.place(x=0, y=160, width=100, height=80)
    skyblue_btn_image_calc = Button(meteor_calc, bg='#00bfff', text='голубой',
                                    font=('Arial', 16, 'bold'), fg='#000000', command=clicki_skyblue_calc)
    skyblue_btn_image_calc.place(x=100, y=160, width=100, height=80)
    lime_btn_image_calc = Button(meteor_calc, bg='#7fff00', text='лайм',
                                 font=('Arial', 16, 'bold'), fg='#000000', command=clicki_lime_calc)
    lime_btn_image_calc.place(x=200, y=160, width=100, height=80)
    orange_btn_image_calc = Button(meteor_calc, bg='#ff8000', text='оранжевый',
                                   font=('Arial', 12, 'bold'), fg='#000000', command=clicki_orange_calc)
    orange_btn_image_calc.place(x=300, y=160, width=100, height=80)
    silver_btn_image_calc = Button(meteor_calc, bg='#c0c0c0', text='серебряный',
                                   font=('Arial', 11, 'bold'), fg='#000000', command=clicki_silver_calc)
    silver_btn_image_calc.place(x=0, y=240, width=100, height=80)
    gold_btn_image_calc = Button(meteor_calc, bg='#d4af37', text='золотой',
                                 font=('Arial', 16, 'bold'), fg='#000000', command=clicki_gold_calc)
    gold_btn_image_calc.place(x=100, y=240, width=100, height=80)
    emerald_btn_image_calc = Button(meteor_calc, bg='#04b58d', text='изумрудный',
                                    font=('Arial', 11, 'bold'), fg='#000000', command=clicki_emerald_calc)
    emerald_btn_image_calc.place(x=200, y=240, width=100, height=80)
    standard_btn_image_calc = Button(meteor_calc, bg='#000000', text='стандарт',
                                     font=('Arial', 16, 'bold'), fg='#ffffff', command=clicki_standard_calc)
    standard_btn_image_calc.place(x=300, y=240, width=100, height=80)
    ruby_btn_image_calc = Button(meteor_calc, image=ruby_bt_image_calc,
                                 fg='#9f003d', command=clicki_ruby_calc)
    ruby_btn_image_calc.place(x=0, y=320, width=100, height=80)
    sapphire_btn_image_calc = Button(meteor_calc, image=sapphire_bt_image_calc,
                                     fg='#d4af37', command=clicki_sapphire_calc)
    sapphire_btn_image_calc.place(x=100, y=320, width=100, height=80)
    rainbow_btn_image_calc = Button(meteor_calc, image=rainbow_bt_image_calc,
                                    fg='#ffffff', command=clicki_rainbow_configure_calc)
    rainbow_btn_image_calc.place(x=200, y=320, width=100, height=80)
    group_btn_image_calc = Button(meteor_calc, image=group_bt_image_calc,
                                  fg='#ffffff', command=clicki_group_calc)
    group_btn_image_calc.place(x=300, y=320, width=100, height=80)


def clickbeit04_calc():
    global universe_calc, text_history_area_calc, history_of_calculations, button03_calc, flag_exist_universe_calc
    global max_amount_of_examples_in_history_of_calculations
    try:
        universe_calc.destroy()
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    try:
        star_calc.destroy()
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    try:
        meteor_calc.destroy()
        button03_calc['state'] = ACTIVE
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    button02_calc['state'] = DISABLED
    universe_calc = Toplevel()
    flag_exist_universe_calc = True
    try:
        star_calc.destroy()
    except NameError:
        nothing_sing_calc = 0
        nothing_sing_calc += 1
    universe_calc.focus_set()
    universe_calc.bind('<Escape>', close_esc_universe_calc)
    universe_calc.bind('<Up>', scroll_esc_universe_calc)
    universe_calc.bind('<Down>', scroll_esc_universe_calc)
    universe_calc.bind('<Prior>', scroll_esc_universe_calc)
    universe_calc.bind('<Next>', scroll_esc_universe_calc)
    universe_calc.bind('<Home>', scroll_esc_universe_calc)
    universe_calc.bind('<End>', scroll_esc_universe_calc)
    universe_calc.protocol('WM_DELETE_WINDOW', lambda: exist_star_calc(universe_calc))
    universe_calc.iconbitmap('calc imgs/calculator_history_icon.ico')
    universe_calc.geometry('1270x950+0+0')
    universe_calc.resizable(width=False, height=False)
    universe_calc.title('История вычислений.')
    text_history_area_calc = Text(universe_calc, bg='light yellow', fg='maroon',
                                  font=('Comic Sans', 10, 'bold', 'italic'))
    text_history_area_calc.place(x=2, y=2, width=1266, height=946)
    text_history_area_calc.tag_config('tag_maroon_text_calc', foreground='maroon')
    text_history_area_calc.tag_config('tag_green_text_calc', foreground='green')
    text_history_area_calc.tag_config('tag_blue_text_calc', foreground='blue')
    lindow_tag_calc = 0
    split_history_of_calculations = history_of_calculations.split('\n')
    for changable_color_text_calc in split_history_of_calculations:
        lindow_tag_calc += 1
        if lindow_tag_calc % 4 == 1:
            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_maroon_text_calc')
        elif lindow_tag_calc % 4 == 2:
            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_green_text_calc')
        elif lindow_tag_calc % 4 == 3:
            text_history_area_calc.insert(END, changable_color_text_calc + '\n', 'tag_blue_text_calc')
        else:
            text_history_area_calc.insert(END, '\n')
    scrollbar_history_calc = ttk.Scrollbar(universe_calc, orient="vertical", command=text_history_area_calc.yview)
    scrollbar_history_calc.pack(side=RIGHT, fill=Y)
    text_history_area_calc['yscrollcommand'] = scrollbar_history_calc.set
    text_history_area_calc['state'] = DISABLED


def exist_meteor_calc(window_calc):
    global button03_calc, meteor_calc
    button03_calc['state'] = ACTIVE
    window_calc.destroy()


def exist_star_calc(window_calc):
    global button02_calc, star_calc, universe_calc, flag_exist_universe_calc
    button02_calc['state'] = ACTIVE
    window_calc.destroy()
    flag_exist_universe_calc = False


verify_but_getto_calc = '600x450+' + settings_of_calculator['geometry'][0] + '+' + settings_of_calculator['geometry'][1]
astro_calc.geometry(verify_but_getto_calc)
astro_calc.resizable(width=False, height=False)
general_background_label_calc = Label(astro_calc, image=standard_bg_image_calc)
general_background_label_calc.place(x='0', y='0', width='600', height='450')
the_entry_for_example = Entry(astro_calc, font=('Arial', 20, 'bold'), bg=light_gamma_calc[40], fg='black',
                              borderwidth='2')
the_entry_for_example.place(x='10', y='15', width='580', height='36')
the_entry_for_example.focus_set()
beluga_calc = Entry(astro_calc, font=('Arial', 16, 'bold'), fg='white', bg=light_gamma_calc[19])
beluga_calc.place(x='10', y='54', width='580', height='30')


def key_calc(nor_calc):
    global the_entry_for_example, flag_smart_focus_calc, history_of_calculations, flag_exist_universe_calc
    global flag_exist_universe_calc, text_history_area_calc, universe_calc, history_of_calculations
    global max_amount_of_examples_in_history_of_calculations, flag_smart_focus_calc, wodden_calc, flag_wodden_calc
    if not flag_smart_focus_calc:
        if nor_calc.keysym == 'backslash':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            the_entry_for_example.insert('insert', ' 000')
        elif nor_calc.keysym == 'period':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if the_entry_for_example.index('insert') == 0:
                the_entry_for_example.insert('insert', '0.')
            elif the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] not in list('0123456789'):
                the_entry_for_example.insert('insert', '0.')
            else:
                the_entry_for_example.insert('insert', '.')
        elif nor_calc.keysym == 'S':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'sin(')
        elif nor_calc.keysym == 'C':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'cos(')
        elif nor_calc.keysym == 'T':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'tg(')
        elif nor_calc.keysym == 'K':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'ctg(')
        elif nor_calc.keysym == 'L':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'log')
        elif nor_calc.keysym == 'B':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            the_entry_for_example.insert('insert', 'base')
        elif nor_calc.keysym == 'N':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'ln(')
        elif nor_calc.keysym == 'G':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'lg(')
        elif nor_calc.keysym == 'P':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'π')
        elif nor_calc.keysym == 'D':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'pip')
        elif nor_calc.keysym == 'R':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            the_entry_for_example.insert('insert', '√')
        elif nor_calc.keysym == 'M':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    (the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!' and
                     the_entry_for_example.get().count('|') == 0 or the_entry_for_example.get()[
                         the_entry_for_example.index('insert') - 1] == '|'):
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', '|')
        elif nor_calc.keysym == 'percent':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            the_entry_for_example.insert('insert', 'mod')
        elif nor_calc.keysym == 'at':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            the_entry_for_example.insert('insert', 'div')
        elif nor_calc.keysym == 'asterisk':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            the_entry_for_example.insert('insert', '•')
        elif nor_calc.keysym == 'slash':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            the_entry_for_example.insert('insert', ':')
        elif nor_calc.keysym == 'E':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', 'e')
        elif nor_calc.keysym == 'parenleft':
            the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
            if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                    the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in '0123456789πe)!':
                if the_entry_for_example.get()[
                        the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                    the_entry_for_example.insert('insert', '•')
            the_entry_for_example.insert('insert', '(')
        else:
            if nor_calc.keysym in 'ABCDEFGHIJKLMNOPQRSTUVWX':
                the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
                the_entry_for_example.insert('insert', nor_calc.keysym.lower())
            if nor_calc.keysym in '0123456789':
                the_entry_for_example.delete(the_entry_for_example.index('insert') - 1)
                if len(the_entry_for_example.get()[:the_entry_for_example.index('insert')]) != 0 and \
                        the_entry_for_example.get()[the_entry_for_example.index('insert') - 1] in 'πe)!':
                    if the_entry_for_example.get()[
                            the_entry_for_example.index('insert') - 4: the_entry_for_example.index('insert')] != 'base':
                        the_entry_for_example.insert('insert', '•')
                the_entry_for_example.insert('insert', nor_calc.keysym)
        if nor_calc.keysym == 'Down':
            entry_that_get_information_of_rounding.focus_set()
            flag_smart_focus_calc = True
        elif nor_calc.keysym == 'grave':
            if len(the_entry_for_example.get()) > 0 and the_entry_for_example.get()[-1] == '=':
                simply_the_best_calc = the_entry_for_example.get()[:-1]
            else:
                simply_the_best_calc = the_entry_for_example.get()
            clicki0_equal_calc()
            check_the_equal = True
            for equality_cheking_calc in beluga_calc.get():
                if equality_cheking_calc not in '0123456789Ee-+.*^() ':
                    check_the_equal = False
                    break
            if check_the_equal and len(the_entry_for_example.get()) != 0:
                date_time_calc = str(datetime.datetime.today())[:-7]
                text_history_calculat0_calc = simply_the_best_calc + '\n' + beluga_calc.get() + '\n'
                text_history_calculat0_calc = text_history_calculat0_calc + date_time_calc + '\n' + '\n'
                splitstephistory_of_calculations = text_history_calculat0_calc + history_of_calculations
                split0_history_of_calculations = splitstephistory_of_calculations.split('\n')
                if len(split0_history_of_calculations) <= max_amount_of_examples_in_history_of_calculations:
                    history_of_calculations = '\n'.join(split0_history_of_calculations)
                    if flag_exist_universe_calc:
                        date_time_calc = str(datetime.datetime.today())[:-7]
                        text_history_area_calc['state'] = NORMAL
                        text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                        text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                        text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                        text_history_area_calc['state'] = DISABLED
                    else:
                        do_not_anithing_calc = 0
                        do_not_anithing_calc += 1
                else:
                    history_of_calculations = '\n'.join(split0_history_of_calculations[:max_amount_of_examples_in_history_of_calculations])
                    if flag_exist_universe_calc:
                        date_time_calc = str(datetime.datetime.today())[:-7]
                        text_history_area_calc['state'] = NORMAL
                        text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                        text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                        text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                        text_history_area_calc.delete(1.0, END)
                        split_history_of_calculations = history_of_calculations.split('\n')
                        lindow_tag_calc = 0
                        for changable_color_text_calc in split_history_of_calculations:
                            lindow_tag_calc += 1
                            if lindow_tag_calc % 4 == 1:
                                text_history_area_calc.insert(END, changable_color_text_calc + '\n',
                                                              'tag_maroon_text_calc')
                            elif lindow_tag_calc % 4 == 2:
                                text_history_area_calc.insert(END, changable_color_text_calc + '\n',
                                                              'tag_green_text_calc')
                            elif lindow_tag_calc % 4 == 3:
                                text_history_area_calc.insert(END, changable_color_text_calc + '\n',
                                                              'tag_blue_text_calc')
                            else:
                                text_history_area_calc.insert(END, '\n')
                        text_history_area_calc['state'] = DISABLED
                    else:
                        do_not_anithing_calc = 0
                        do_not_anithing_calc += 1
            the_entry_for_example.delete(0, END)
    else:
        toto_calc = str(entry_that_get_information_of_rounding.get()).lower()
        entry_that_get_information_of_rounding.delete(0, END)
        entry_that_get_information_of_rounding.insert(END, toto_calc)
        if nor_calc.keysym == 'Up':
            the_entry_for_example.focus_set()
            flag_smart_focus_calc = False
        if nor_calc.keysym == 'grave':
            entry_that_get_information_of_rounding.delete(0, END)
    if nor_calc.keysym not in ['Control_L', 'Shift_L']:
        clicki0_calc()
    if nor_calc.keysym == 'Return' or nor_calc.keysym == 'equal' or nor_calc.keysym == 'Clear':
        if len(the_entry_for_example.get()) > 0 and the_entry_for_example.get()[-1] == '=':
            simply_the_best_calc = the_entry_for_example.get()[:-1]
        else:
            simply_the_best_calc = the_entry_for_example.get()
        clicki0_equal_calc()
        check_the_equal = True
        for equality_cheking_calc in beluga_calc.get():
            if equality_cheking_calc not in '0123456789Ee-+.*^() ':
                check_the_equal = False
                break
        if check_the_equal:
            example2 = str(beluga_calc.get())
            the_entry_for_example.delete(0, END)
            the_entry_for_example.insert(END, example2)
            configure_size_of_example_calc()
            if len(the_entry_for_example.get()) != 0:
                date_time_calc = str(datetime.datetime.today())[:-7]
                text_history_calculat0_calc = simply_the_best_calc + '\n' + beluga_calc.get() + '\n'
                text_history_calculat0_calc = text_history_calculat0_calc + date_time_calc + '\n' + '\n'
                splitstephistory_of_calculations = text_history_calculat0_calc + history_of_calculations
                split0_history_of_calculations = splitstephistory_of_calculations.split('\n')
                if len(split0_history_of_calculations) <= max_amount_of_examples_in_history_of_calculations:
                    history_of_calculations = '\n'.join(split0_history_of_calculations)
                    if flag_exist_universe_calc:
                        date_time_calc = str(datetime.datetime.today())[:-7]
                        text_history_area_calc['state'] = NORMAL
                        text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                        text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                        text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                        text_history_area_calc['state'] = DISABLED
                    else:
                        do_not_anithing_calc = 0
                        do_not_anithing_calc += 1
                else:
                    history_of_calculations = '\n'.join(split0_history_of_calculations[:max_amount_of_examples_in_history_of_calculations])
                    if flag_exist_universe_calc:
                        date_time_calc = str(datetime.datetime.today())[:-7]
                        text_history_area_calc['state'] = NORMAL
                        text_history_area_calc.insert(0.0, date_time_calc + '\n' + '\n', 'tag_blue_text_calc')
                        text_history_area_calc.insert(0.0, beluga_calc.get() + '\n', 'tag_green_text_calc')
                        text_history_area_calc.insert(0.0, simply_the_best_calc + '\n', 'tag_maroon_text_calc')
                        text_history_area_calc.delete(1.0, END)
                        split_history_of_calculations = history_of_calculations.split('\n')
                        lindow_tag_calc = 0
                        for changable_color_text_calc in split_history_of_calculations:
                            lindow_tag_calc += 1
                            if lindow_tag_calc % 4 == 1:
                                text_history_area_calc.insert(END, changable_color_text_calc + '\n',
                                                              'tag_maroon_text_calc')
                            elif lindow_tag_calc % 4 == 2:
                                text_history_area_calc.insert(END, changable_color_text_calc + '\n',
                                                              'tag_green_text_calc')
                            elif lindow_tag_calc % 4 == 3:
                                text_history_area_calc.insert(END, changable_color_text_calc + '\n',
                                                              'tag_blue_text_calc')
                            else:
                                text_history_area_calc.insert(END, '\n')
                        text_history_area_calc['state'] = DISABLED
                    else:
                        do_not_anithing_calc = 0
                        do_not_anithing_calc += 1
    if nor_calc.keysym not in ['Control_L', 'C', 'V', 'Y', 'Z', 'c', 'v', 'y', 'z']:
        wodden_calc = 0
        flag_wodden_calc = 1


def crtl_z_calc(self):
    global history_of_calculations
    global wodden_calc, flag_wodden_calc
    if flag_wodden_calc == 1:
        wodden_calc = 0
        the_entry_for_example.delete(0, END)
        the_entry_for_example.insert(END, history_of_calculations.split('\n')[wodden_calc])
        flag_wodden_calc = 0
    elif wodden_calc <= len(history_of_calculations.split('\n')) - 4:
        wodden_calc += 4
        the_entry_for_example.delete(0, END)
        the_entry_for_example.insert(END, history_of_calculations.split('\n')[wodden_calc])
    else:
        the_entry_for_example.delete(0, END)
        the_entry_for_example.insert(END, 'В этом промежутке времени история вычислений была пустой!')
        flag_wodden_calc = -1
    clicki0_calc()


def crtl_y_calc(self):
    global history_of_calculations
    global wodden_calc, flag_wodden_calc
    if flag_wodden_calc == -1:
        wodden_calc = len(history_of_calculations.split('\n')) - 3
        the_entry_for_example.delete(0, END)
        the_entry_for_example.insert(END, history_of_calculations.split('\n')[wodden_calc])
        flag_wodden_calc = 0
    elif wodden_calc > 3:
        wodden_calc -= 4
        the_entry_for_example.delete(0, END)
        the_entry_for_example.insert(END, history_of_calculations.split('\n')[wodden_calc])
    else:
        the_entry_for_example.delete(0, END)
        the_entry_for_example.insert(END, 'Пока что путешествовать в будущее невозможно! :)')
        flag_wodden_calc = 1
    clicki0_calc()


astro_calc.bind('<Key>', key_calc)
astro_calc.bind('<Control-y>', crtl_y_calc)
astro_calc.bind('<Control-z>', crtl_z_calc)
astro_calc.bind('<Control-Y>', crtl_y_calc)
astro_calc.bind('<Control-Z>', crtl_z_calc)

buttonp_calc = Button(astro_calc, text='pip', fg='black', bg=light_gamma_calc[20],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitp_calc)
buttonp_calc.place(x='26', y='150')
buttonu_calc = Button(astro_calc, text='pi', fg='black', bg=light_gamma_calc[21],
                      font=('Arial', 20, 'bold', 'italic'), width=3, height=1, command=clickbeitu_calc)
buttonu_calc.place(x='103', y='150')
buttono_calc = Button(astro_calc, text='√', fg='black', bg=light_gamma_calc[22],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeito_calc)
buttono_calc.place(x='163', y='150')
buttong_calc = Button(astro_calc, text='(', fg='black', bg=light_gamma_calc[23],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeitg_calc)
buttong_calc.place(x='240', y='150')
buttonh_calc = Button(astro_calc, text=')', fg='black', bg=light_gamma_calc[24],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeith_calc)
buttonh_calc.place(x='283', y='150')
buttoni_calc = Button(astro_calc, text='|', fg='black', bg=light_gamma_calc[25],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeiti_calc)
buttoni_calc.place(x='326', y='150')
buttonj_calc = Button(astro_calc, text='^', fg='black', bg=light_gamma_calc[26],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeitj_calc)
buttonj_calc.place(x='369', y='150')
button03_calc = Button(astro_calc, text='дизайн', fg='black', bg=light_gamma_calc[27],
                       font=('Arial', 10, 'bold', 'italic'), command=clickbeit03_calc)
button03_calc.place(x='412', y='150', width=60, height=56)
buttonq_calc = Button(astro_calc, text='sin', fg='black', bg=light_gamma_calc[28],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitq_calc)
buttonq_calc.place(x='26', y='205')
buttonv_calc = Button(astro_calc, text='e', fg='black', bg=light_gamma_calc[29],
                      font=('Arial', 20, 'bold', 'italic'), width=3, height=1, command=clickbeitv_calc)
buttonv_calc.place(x='103', y='205')
buttonn_calc = Button(astro_calc, text='log', fg='black', bg=light_gamma_calc[30],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitn_calc)
buttonn_calc.place(x='163', y='205')
button7_calc = Button(astro_calc, text='7', fg='black', bg=light_gamma_calc[31],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit7_calc)
button7_calc.place(x='240', y='205')
button8_calc = Button(astro_calc, text='8', fg='black', bg=light_gamma_calc[32],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit8_calc)
button8_calc.place(x='283', y='205')
button9_calc = Button(astro_calc, text='9', fg='black', bg=light_gamma_calc[33],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit9_calc)
button9_calc.place(x='326', y='205')
buttonf_calc = Button(astro_calc, text='÷', fg='black', bg=light_gamma_calc[34],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeitf_calc)
buttonf_calc.place(x='369', y='205')
button02_calc = Button(astro_calc, text='помощь', fg='black', bg=light_gamma_calc[35],
                       font=('Arial', 10, 'bold', 'italic'), command=clickbeit02_calc)
button02_calc.place(x='412', y='205', width=60, height=55)
buttonr_calc = Button(astro_calc, text='cos', fg='black', bg=light_gamma_calc[36],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitr_calc)
buttonr_calc.place(x='26', y='260')
buttonw_calc = Button(astro_calc, text='ln', fg='black', bg=light_gamma_calc[37],
                      font=('Arial', 20, 'bold', 'italic'), width=3, height=1, command=clickbeitw_calc)
buttonw_calc.place(x='103', y='260')
buttonm_calc = Button(astro_calc, text='base', fg='black', bg=light_gamma_calc[38],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitm_calc)
buttonm_calc.place(x='163', y='260')
button4_calc = Button(astro_calc, text='4', fg='black', bg=light_gamma_calc[39],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit4_calc)
button4_calc.place(x='240', y='260')
button5_calc = Button(astro_calc, text='5', fg='black', bg=light_gamma_calc[40],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit5_calc)
button5_calc.place(x='283', y='260')
button6_calc = Button(astro_calc, text='6', fg='black', bg=light_gamma_calc[41],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit6_calc)
button6_calc.place(x='326', y='260')
buttone_calc = Button(astro_calc, text='x', fg='black', bg=light_gamma_calc[42],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeite_calc)
buttone_calc.place(x='369', y='260')
entry_that_get_information_of_rounding = Entry(astro_calc, font=('Arial', 24, 'bold', 'italic'), fg='black',
                           bg=light_gamma_calc[43], borderwidth='2')
entry_that_get_information_of_rounding.place(x='412', y='260', width=60, height=55)
buttons_calc = Button(astro_calc, text='tg', fg='black', bg=light_gamma_calc[44],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeits_calc)
buttons_calc.place(x='26', y='315')
buttonx_calc = Button(astro_calc, text='lg', fg='black', bg=light_gamma_calc[45],
                      font=('Arial', 20, 'bold', 'italic'), width=3, height=1, command=clickbeitx_calc)
buttonx_calc.place(x='103', y='315')
buttonl_calc = Button(astro_calc, text='div', fg='black', bg=light_gamma_calc[46],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitl_calc)
buttonl_calc.place(x='163', y='315')
button1_calc = Button(astro_calc, text='1', fg='black', bg=light_gamma_calc[47],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit1_calc)
button1_calc.place(x='240', y='315')
button2_calc = Button(astro_calc, text='2', fg='black', bg=light_gamma_calc[48],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit2_calc)
button2_calc.place(x='283', y='315')
button3_calc = Button(astro_calc, text='3', fg='black', bg=light_gamma_calc[49],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit3_calc)
button3_calc.place(x='326', y='315')
buttond_calc = Button(astro_calc, text='–', fg='black', bg=light_gamma_calc[50],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeitd_calc)
buttond_calc.place(x='369', y='315')
buttonb_calc = Button(astro_calc, text='⟵', fg='black', bg=light_gamma_calc[51],
                      font=('Arial', 20, 'bold', 'italic'), width=3, height=1, command=clickbeitb_calc)
buttonb_calc.place(x='412', y='315')
buttont_calc = Button(astro_calc, text='ctg', fg='black', bg=light_gamma_calc[52],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitt_calc)
buttont_calc.place(x='26', y='370')
buttony_calc = Button(astro_calc, text='!', fg='black', bg=light_gamma_calc[53],
                      font=('Arial', 20, 'bold', 'italic'), width=3, height=1, command=clickbeity_calc)
buttony_calc.place(x='103', y='370')
buttonk_calc = Button(astro_calc, text='mod', fg='black', bg=light_gamma_calc[54],
                      font=('Arial', 20, 'bold', 'italic'), width=4, height=1, command=clickbeitk_calc)
buttonk_calc.place(x='163', y='370')
button0_calc = Button(astro_calc, text='0', fg='black', bg=light_gamma_calc[55],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit0_calc)
button0_calc.place(x='240', y='370')
buttona_calc = Button(astro_calc, text=' .', fg='black', bg=light_gamma_calc[56],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeita_calc)
buttona_calc.place(x='283', y='370')
button01_calc = Button(astro_calc, text='=', fg='black', bg=light_gamma_calc[57],
                       font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeit01_calc)
button01_calc.place(x='326', y='370')
buttonc_calc = Button(astro_calc, text='+', fg='black', bg=light_gamma_calc[58],
                      font=('Arial', 20, 'bold', 'italic'), width=2, height=1, command=clickbeitc_calc)
buttonc_calc.place(x='369', y='370')
button00_calc = Button(astro_calc, text='AC', fg='black', bg=light_gamma_calc[59],
                       font=('Arial', 20, 'bold', 'italic'), width=3, height=1, command=clickbeit00_calc)
button00_calc.place(x='412', y='370')


def flaged_focus_calc(self):
    global flag_smart_focus_calc
    flag_smart_focus_calc = True


def deflaged_focus_calc(self):
    global flag_smart_focus_calc
    flag_smart_focus_calc = False


def close_not_esc_astro_calc(winning_calc):
    global astro_calc, history_of_calculations
    if settings_of_calculator["messagebox"]:
        if messagebox.askyesno(title='Вопрос.', message='Вы уверены, что хотите закрыть калькулятор?'):
            with open('calc history.json', 'w') as file_history_calc:
                json.dump(history_of_calculations, file_history_calc)
            with open('calc settings.json', 'w') as file_settings_calc:
                json.dump(settings_of_calculator, file_settings_calc)
            winning_calc.destroy()
        else:
            pass
    else:
        with open('calc history.json', 'w') as file_history_calc:
            json.dump(history_of_calculations, file_history_calc)
        with open('calc settings.json', 'w') as file_settings_calc:
            json.dump(settings_of_calculator, file_settings_calc)
        winning_calc.destroy()


def close_esc_astro_calc(self):
    global astro_calc, history_of_calculations
    if settings_of_calculator["messagebox"]:
        if messagebox.askyesno(title='Вопрос.', message='Вы уверены, что хотите закрыть калькулятор?'):
            with open('calc history.json', 'w') as file_history_calc:
                json.dump(history_of_calculations, file_history_calc)
            with open('calc settings.json', 'w') as file_settings_calc:
                json.dump(settings_of_calculator, file_settings_calc)
            astro_calc.destroy()
        else:
            pass
    else:
        with open('calc history.json', 'w') as file_history_calc:
            json.dump(history_of_calculations, file_history_calc)
        with open('calc settings.json', 'w') as file_settings_calc:
            json.dump(settings_of_calculator, file_settings_calc)
        astro_calc.destroy()


def close_esc_meteor_calc(self):
    global meteor_calc, button03_calc
    button03_calc['state'] = ACTIVE
    meteor_calc.destroy()


def close_esc_universe_calc(self):
    global universe_calc, button02_calc, flag_exist_universe_calc
    button02_calc['state'] = ACTIVE
    universe_calc.destroy()
    flag_exist_universe_calc = False


def close_esc_star_calc(self):
    global star_calc, button02_calc
    button02_calc['state'] = ACTIVE
    star_calc.destroy()


def scroll_esc_universe_calc(kor_calc):
    global text_history_area_calc
    if kor_calc.keysym == 'Up':
        pyautogui.scroll(700)
    if kor_calc.keysym == 'Down':
        pyautogui.scroll(-700)
    if kor_calc.keysym == 'Prior':
        pyautogui.scroll(2800)
    if kor_calc.keysym == 'Next':
        pyautogui.scroll(-2800)
    if kor_calc.keysym == 'Home':
        text_history_area_calc.yview(1.0)
    if kor_calc.keysym == 'End':
        text_history_area_calc.yview(END)


astro_calc.bind('<Escape>', close_esc_astro_calc)
astro_calc.protocol('WM_DELETE_WINDOW', lambda: close_not_esc_astro_calc(astro_calc))
entry_that_get_information_of_rounding.bind('<FocusIn>', flaged_focus_calc)
the_entry_for_example.bind('<FocusIn>', deflaged_focus_calc)
the_entry_for_example.insert(END, '#' + str(settings_of_calculator["messagebox"]).lower())
clicki0_equal_calc()
the_entry_for_example.delete(0, END)
the_entry_for_example.insert(END, settings_of_calculator["color"])
clicki0_equal_calc()
the_entry_for_example.delete(0, END)
the_entry_for_example.insert(END, '#' + settings_of_calculator["geometry"][0] + ';' +
                             settings_of_calculator["geometry"][1])
clicki0_equal_calc()
the_entry_for_example.delete(0, END)
the_entry_for_example.insert(END, '#his' + str(settings_of_calculator["history length"]))
clicki0_equal_calc()
the_entry_for_example.delete(0, END)
clicki0_equal_calc()

astro_calc.mainloop()
