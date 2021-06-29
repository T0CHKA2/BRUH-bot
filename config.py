from itertools import cycle
import ctypes

FuncA = {
    'PREFIX': '!',
    'TOKEN': 'ODExNjc4NzgxMDIyNTM1NzAw.YC1sxQ.ZVdfXP0c19MzT7pG9X7YI3KFL44',
    'ID': '811678781022535700',
}
color = (0xFFFFFF, 0x00FFFF, 0x0080FF, 0xFF00FF, 0x0000FF, 0xFFFF00, 0xFF8000, 0xFF0000, 0x00FF00)
status = cycle(['Используйте "!help" для помощи', "Если вы нашли баг сообщите его T0CHKA#2838"])

kernel32 = ctypes.windll.kernel32
