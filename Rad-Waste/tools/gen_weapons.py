# -*- coding: utf-8 -*-
"""Генератор v2: детализированные пиксель-арт спрайты оружия (толстый контур,
трёхтоновая штриховка, вид сбоку, дуло вправо) для waste2.html. Стиль — оружейный лист."""
import os
from PIL import Image, ImageDraw

OUT = r"E:\Rad-Waste\Weapons"
SCALE = 4

# (R,G,B,A): K контур; металлы D<d<g<L<n; дерево B<b<w<v; жёлтый Y<y<v;
# оранжевый O<o<q; красный R<r<x; циан C<c<z; синий E<e<f
PAL = {
    'K': (20, 18, 24, 255),
    'D': (40, 46, 54, 255), 'd': (92, 100, 112, 255), 'g': (152, 160, 170, 255),
    'L': (212, 218, 224, 255), 'n': (236, 240, 244, 255), 's': (186, 194, 202, 255),
    'B': (84, 48, 26, 255), 'b': (134, 84, 46, 255), 'w': (180, 128, 76, 255), 'v': (208, 162, 108, 255),
    'Y': (188, 142, 26, 255), 'y': (242, 202, 64, 255),
    'O': (172, 76, 16, 255), 'o': (238, 122, 32, 255), 'q': (250, 170, 90, 255),
    'R': (124, 32, 22, 255), 'r': (198, 56, 38, 255), 'x': (234, 110, 88, 255),
    'C': (38, 130, 166, 255), 'c': (94, 208, 230, 255), 'z': (184, 242, 250, 255),
    'E': (50, 86, 178, 255), 'e': (106, 152, 236, 255), 'f': (170, 200, 250, 255),
}
# средний тон -> (светлый, тёмный): авто-штриховка каждой детали
LADDER = {'d': ('g', 'D'), 'g': ('L', 'd'), 's': ('n', 'g'), 'b': ('w', 'B'),
          'w': ('v', 'b'), 'y': ('v', 'Y'), 'o': ('q', 'O'), 'r': ('x', 'R'),
          'c': ('z', 'C'), 'e': ('f', 'E')}


class S:
    def __init__(self, w=52, h=20):
        self.w, self.h = w, h
        self.g = [[' '] * w for _ in range(h)]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.px(x, y, c)

    def bar(self, x0, y0, x1, y1, c):
        """Прямоугольник со штриховкой: верх светлее, низ темнее."""
        light, dark = LADDER.get(c, (c, c))
        h = max(y0, y1) - min(y0, y1) + 1
        for y in range(min(y0, y1), max(y0, y1) + 1):
            if h >= 3:
                col = light if y == y0 else (dark if y == y1 else c)
            else:
                col = c if y == y0 else dark
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.px(x, y, col)

    def ln(self, x0, y0, x1, y1, c, t=1):
        """Линия со штриховкой поперёк: верх/лево светлее, низ/право темнее."""
        light, dark = LADDER.get(c, (c, c))
        pts = []
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            pts.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy
        pixels = []
        for (px, py) in pts:
            for oy in range(t):
                for ox in range(t):
                    pixels.append((px + ox, py + oy))
        horizontal = abs(x1 - x0) >= abs(y1 - y0)
        groups = {}
        for (px, py) in pixels:
            key = px if horizontal else py
            groups.setdefault(key, []).append((px, py))
        for g in groups.values():
            g.sort(key=lambda p: p[1] if horizontal else p[0])
            m = len(g)
            for i, (px, py) in enumerate(g):
                if m >= 3:
                    col = light if i == 0 else (dark if i == m - 1 else c)
                else:
                    col = c if i == 0 else dark
                self.px(px, py, col)

    def outline(self):
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] != ' ':
                    continue
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.h and 0 <= nx < self.w and self.g[ny][nx] != ' ':
                            add.append((x, y))
        for x, y in add:
            self.g[y][x] = 'K'

    def render(self):
        im = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0))
        for y in range(self.h):
            for x in range(self.w):
                ch = self.g[y][x]
                if ch != ' ':
                    im.putpixel((x, y), PAL[ch])
        return im

    def save(self, name):
        im = self.render()
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
        w, h = im.size
        pad = 2
        out = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
        out.paste(im, (pad, pad))
        out = out.resize((out.width * SCALE, out.height * SCALE), Image.NEAREST)
        out.save(os.path.join(OUT, name + '.png'))


# ================= 20 ОРУЖИЙ (дуло вправо) =================

def s_pipe():
    s = S(50, 20)
    s.bar(3, 8, 42, 12, 'd')                        # труба: 5 рядов g/d/D
    for x in (5, 6, 30, 31):
        s.px(x, 8, 'L')                              # блики
    for x, y in [(8, 10), (9, 11), (15, 9), (25, 11), (33, 10), (38, 9)]:
        s.px(x, y, 'Y')                              # ржавчина
    for x, y in [(16, 10), (26, 10), (36, 11)]:
        s.px(x, y, 'O')
    s.bar(6, 7, 9, 13, 'b')                          # изолента у основания
    s.bar(20, 7, 24, 13, 'g')                        # муфта
    s.rect(24, 7, 24, 13, 'd')
    s.bar(42, 7, 44, 13, 'd')                        # раструб
    s.rect(45, 8, 45, 12, 'K')                       # дыра
    return s

def s_obrez():
    s = S(46, 19)
    s.bar(14, 5, 40, 7, 's')                         # верхний ствол: n/s/g
    s.bar(14, 8, 40, 10, 'd')                        # нижний ствол: g/d/D
    s.rect(24, 5, 24, 10, 'D'); s.rect(32, 5, 32, 10, 'D')   # кольца
    s.rect(39, 5, 40, 10, 'D')                       # казённый срез
    s.px(41, 6, 'n'); s.px(41, 9, 'n')               # блики среза
    s.bar(10, 5, 14, 10, 'd')                        # коробка
    s.px(11, 3, 'd'); s.px(12, 4, 'd')               # курок
    s.ln(12, 11, 7, 17, 'b', 3)                      # рукоять
    for x, y in [(15, 11), (16, 12), (17, 12), (18, 11)]:
        s.px(x, y, 'D')                              # спусковая скоба
    s.px(16, 11, 'K')                                # крючок
    return s

def s_bat():
    s = S(48, 20)
    s.ln(4, 16, 13, 11, 'b', 3)                      # ручка
    s.rect(4, 15, 6, 16, 'B')                        # обмотка
    s.ln(13, 11, 34, 5, 'w', 5)                      # тело биты v/w/w/w/B
    s.rect(33, 3, 36, 7, 'w')                        # толстый конец
    s.ln(33, 3, 36, 3, 'v', 1); s.ln(33, 7, 36, 7, 'B', 1)
    for x, y in [(18, 7), (23, 6), (28, 5)]:          # гвозди сверху
        s.px(x, y - 1, 'n'); s.px(x, y - 2, 's')
    for x, y in [(16, 13), (21, 12), (26, 10)]:       # гвозди снизу
        s.px(x, y + 1, 'n'); s.px(x, y + 2, 's')
    return s

def s_laserp():
    s = S(48, 19)
    s.bar(14, 7, 30, 11, 'y')                        # корпус: v/y/Y
    s.bar(18, 5, 24, 6, 'Y')                         # верхний гребень
    s.px(18, 7, 'r')                                 # индикатор
    s.bar(30, 8, 38, 10, 'g')                        # ствол
    s.rect(34, 7, 35, 7, 'd')                        # ребра
    s.rect(38, 8, 39, 10, 'c')                       # излучатель
    s.px(40, 9, 'z')                                 # свечение
    s.ln(20, 12, 16, 17, 'Y', 3)                     # рукоять
    s.px(21, 12, 'K')                                # крючок
    s.rect(24, 8, 27, 10, 'c')                       # окно энергоячейки
    s.px(25, 9, 'z')
    return s

def s_chainsaw():
    s = S(52, 19)
    s.ln(6, 4, 12, 3, 'd', 2)                        # верхняя ручка
    s.bar(4, 6, 16, 12, 'o')                         # корпус: q/o/O
    s.rect(7, 8, 13, 8, 'O')                         # щель вентиляции
    s.px(9, 6, 'Y'); s.px(10, 6, 'y')                # крышка бака
    s.bar(16, 8, 42, 10, 'g')                        # шина: L/g/d
    for x in range(17, 42, 2):                        # зубья
        s.px(x, 7, 'n'); s.px(x + 1, 11, 'n')
    s.px(43, 9, 'g')                                 # носок
    s.px(4, 11, 'D')                                 # стартер
    s.ln(6, 13, 4, 16, 'B', 2)                       # задняя рукоять
    return s

def s_crossbow():
    s = S(50, 20)
    s.bar(6, 10, 28, 12, 'b')                        # ложе: w/b/B
    s.ln(12, 13, 10, 17, 'B', 2)                     # рукоять
    s.px(14, 13, 'K')                                # крючок
    s.ln(28, 11, 35, 4, 'D', 2)                      # плечо верх
    s.ln(28, 11, 35, 17, 'D', 2)                     # плечо низ
    s.ln(35, 4, 27, 10, 's', 1)                      # тетива
    s.ln(35, 17, 27, 10, 's', 1)
    s.ln(10, 9, 30, 9, 'w', 1)                       # болт
    s.px(31, 9, 's'); s.px(32, 9, 'n')               # наконечник
    s.px(11, 8, 'r'); s.px(12, 8, 'r'); s.px(11, 10, 'r'); s.px(12, 10, 'r')  # оперение
    return s

def s_rifle():
    s = S(52, 19)
    s.ln(2, 9, 13, 9, 'b', 4)                        # приклад: w/b/b/B
    s.bar(13, 7, 28, 10, 'd')                        # ствольная коробка
    s.bar(28, 6, 38, 7, 'g')                         # газовая трубка
    s.bar(28, 8, 44, 9, 'd')                         # ствол
    s.bar(29, 8, 35, 10, 'b')                        # цевьё
    s.rect(42, 5, 43, 7, 'd')                        # мушка
    s.rect(44, 8, 45, 9, 'D')                        # компенсатор
    s.rect(20, 11, 24, 13, 'D')                      # магазин (изогнутый)
    s.rect(19, 13, 23, 15, 'D')
    s.rect(18, 15, 22, 16, 'D')
    s.px(20, 11, 'd')
    s.ln(17, 11, 14, 16, 'B', 3)                     # рукоять
    s.px(18, 11, 'K')                                # крючок
    return s

def s_flamethrower():
    s = S(52, 20)
    s.bar(6, 4, 13, 8, 'r')                          # баллон: x/r/R
    s.px(9, 3, 'D')                                  # вентиль
    s.ln(13, 6, 17, 9, 'D', 1)                       # шланг
    s.bar(5, 9, 20, 13, 'r')                         # корпус
    s.bar(20, 10, 30, 11, 'd')                       # ствол
    s.rect(30, 9, 32, 12, 'D')                       # сопло
    s.px(31, 8, 'o')                                 # запальник
    s.rect(33, 9, 35, 12, 'O')                       # пламя: ядро
    s.rect(34, 8, 37, 13, 'o')
    s.rect(35, 9, 39, 12, 'y')
    s.rect(37, 10, 40, 11, 'v')
    s.px(41, 10, 'v'); s.px(38, 8, 'y'); s.px(38, 13, 'y')
    s.ln(10, 14, 7, 18, 'B', 2)                      # задняя рукоять
    s.ln(24, 12, 22, 16, 'B', 2)                     # передняя рукоять
    return s

def s_machete():
    s = S(48, 18)
    s.ln(16, 11, 40, 5, 's', 4)                      # клинок: n/s/g
    s.px(41, 4, 's'); s.px(42, 4, 'n')               # кончик
    s.rect(14, 9, 15, 14, 'D')                       # гарда
    s.ln(8, 13, 14, 12, 'B', 3)                      # рукоять
    s.px(10, 12, 'w'); s.px(12, 12, 'w')             # обмотка
    s.px(7, 14, 'r')                                 # темляк
    return s

def s_kuvarda():
    s = S(50, 18)
    s.ln(4, 14, 28, 7, 'b', 3)                       # черенок
    s.bar(28, 3, 40, 10, 'g')                        # голова: L/g/d
    s.rect(33, 3, 35, 10, 'D')                       # обжим
    s.px(30, 8, 'L'); s.px(38, 4, 'L')               # блики
    return s

def s_sniper():
    s = S(54, 20)
    s.ln(2, 10, 14, 10, 'b', 4)                      # приклад
    s.bar(4, 8, 10, 9, 'b')                          # щека
    s.bar(14, 8, 30, 11, 'd')                        # коробка
    s.bar(30, 9, 48, 10, 'd')                        # ствол
    s.rect(48, 8, 50, 11, 'D')                       # дульный тормоз
    s.px(49, 8, 'K'); s.px(49, 11, 'K')              # прорези
    s.bar(18, 4, 27, 6, 'D')                         # прицел
    s.rect(28, 4, 28, 6, 'c'); s.px(28, 5, 'z')      # линза
    s.rect(19, 7, 20, 7, 'D'); s.rect(26, 7, 27, 7, 'D')   # кронштейны
    s.px(24, 11, 'D'); s.px(25, 12, 'd')             # рукоять затвора
    s.rect(24, 12, 27, 13, 'D')                      # магазин
    s.ln(18, 12, 15, 17, 'B', 3)                     # рукоять
    return s

def s_grenade():
    s = S(50, 20)
    s.bar(12, 6, 40, 11, 'd')                        # толстый ствол
    s.rect(40, 5, 42, 12, 'D')                       # дуло
    s.rect(41, 6, 41, 11, 'K')                       # отверстие
    s.rect(14, 4, 15, 5, 'd')                        # прицел
    s.ln(3, 9, 12, 8, 'b', 4)                        # приклад
    s.rect(16, 12, 24, 15, 'D')                      # барабан
    s.px(18, 13, 'd'); s.px(21, 14, 'd')             # гнезда
    s.ln(28, 12, 26, 17, 'B', 3)                     # рукоять
    s.px(27, 12, 'K')
    return s

def s_taser():
    s = S(42, 20)
    s.bar(10, 7, 22, 12, 'y')                        # корпус
    s.rect(13, 10, 19, 11, 'Y')                      # полоса-надпись
    s.px(14, 8, 'r')                                 # кнопка
    s.ln(22, 7, 30, 3, 's', 1)                       # штырь 1
    s.ln(22, 12, 30, 16, 's', 1)                     # штырь 2
    s.px(31, 3, 'n'); s.px(31, 16, 'n')
    for x, y, c in [(27, 9, 'c'), (26, 10, 'z'), (28, 10, 'e'), (27, 11, 'c')]:
        s.px(x, y, c)                                # дуга
    s.ln(14, 13, 11, 18, 'D', 3)                     # рукоять
    return s

def s_katana():
    s = S(52, 16)
    s.ln(16, 10, 44, 3, 's', 3)                      # клинок: n/s/g
    s.ln(16, 9, 45, 2, 'n', 1)                       # лезвие-кромка
    s.px(46, 2, 's'); s.px(47, 2, 'n')               # остриё
    s.rect(14, 8, 15, 13, 'D')                       # цуба
    s.ln(7, 13, 14, 11, 'B', 2)                      # рукоять
    s.px(9, 12, 'w'); s.px(11, 12, 'w'); s.px(13, 11, 'w')   # обмотка
    s.px(6, 14, 'D')                                 # навершие
    return s

def s_smg():
    s = S(46, 20)
    s.bar(8, 6, 28, 10, 'd')                         # корпус: g/d/D
    s.bar(28, 7, 36, 8, 'g')                         # ствол
    s.rect(36, 7, 37, 8, 'D')                        # дуло
    s.rect(2, 8, 4, 9, 'd')                          # плечевой упор
    s.ln(4, 8, 8, 8, 'd', 1)
    s.rect(9, 5, 9, 5, 'd'); s.rect(35, 6, 35, 6, 'd')   # прицельные
    s.rect(14, 11, 17, 17, 'D')                      # длинный магазин
    s.rect(13, 17, 18, 18, 'd')                      # пятка
    s.ln(24, 11, 21, 16, 'B', 3)                     # рукоять
    s.px(23, 11, 'K')
    return s

def s_spear():
    s = S(52, 18)
    s.ln(4, 14, 32, 6, 'b', 3)                       # древко
    s.ln(25, 9, 28, 8, 'B', 3)                       # обмотка
    s.rect(33, 4, 40, 7, 's')                        # перо наконечника
    s.ln(34, 3, 41, 4, 'n', 1)                       # светлая грань
    s.ln(34, 8, 41, 6, 'g', 1)                       # тёмная грань
    s.ln(35, 5, 42, 5, 'n', 1)                       # ребро
    s.px(42, 4, 's'); s.px(43, 4, 'n')               # остриё
    return s

def s_rocket():
    s = S(54, 20)
    s.rect(2, 5, 6, 15, 'd')                         # раструб
    s.rect(2, 8, 2, 12, 'K')                         # сопло
    s.bar(6, 7, 36, 13, 'g')                         # труба: L/g/d
    s.rect(4, 4, 7, 5, 'd'); s.rect(4, 15, 7, 16, 'd')   # стабилизаторы
    s.rect(30, 7, 31, 13, 'Y')                       # сигнальная полоса
    s.rect(12, 4, 13, 6, 'd')                        # прицел
    s.bar(36, 8, 44, 12, 'r')                        # боеголовка: x/r/R
    s.px(45, 8, 'r'); s.px(45, 12, 'r')
    s.px(46, 9, 'o'); s.px(46, 11, 'o')
    s.px(47, 10, 'y')
    s.ln(16, 14, 14, 18, 'B', 2)                     # задняя рукоять
    s.ln(26, 14, 24, 18, 'B', 2)                     # передняя рукоять
    return s

def s_tesak():
    s = S(48, 18)
    s.bar(16, 4, 40, 11, 's')                        # полотно: n/s/g
    s.ln(17, 12, 40, 12, 'n', 1)                     # светлая кромка снизу
    s.px(19, 6, 'K')                                 # отверстие
    s.bar(7, 7, 15, 9, 'b')                          # рукоять: w/b/B
    s.rect(15, 5, 16, 11, 'D')                       # больстер
    s.px(9, 8, 'v'); s.px(12, 8, 'v')                # заклёпки
    return s

def s_drobovik():
    s = S(52, 18)
    s.ln(3, 8, 13, 9, 'w', 4)                        # приклад: v/w/b/B
    s.rect(2, 7, 3, 11, 'D')                         # затыльник
    s.bar(13, 6, 22, 9, 'd')                         # колодка
    s.bar(22, 6, 44, 7, 'g')                         # ствол
    s.bar(22, 8, 40, 9, 'd')                         # трубка магазина
    s.bar(26, 8, 34, 10, 'b')                        # цевьё
    s.px(28, 11, 'B'); s.px(31, 11, 'B')             # насечки
    s.rect(44, 6, 45, 7, 'D')                        # дуло
    s.px(17, 8, 'K')                                 # окно выброса
    for x, y in [(19, 10), (20, 11), (21, 11)]:
        s.px(x, y, 'D')                              # скоба
    s.px(20, 10, 'K')
    return s

def s_impulse():
    s = S(50, 19)
    s.bar(10, 7, 26, 12, 'e')                        # корпус: f/e/E
    s.rect(16, 4, 24, 6, 'E')                        # плавник
    s.rect(16, 4, 24, 4, 'e')
    s.px(12, 9, 'E'); s.px(14, 9, 'E')               # вентиляция
    s.bar(26, 8, 36, 10, 'c')                        # ствол: z/c/C
    for x in (28, 31, 34):                            # катушки
        s.rect(x, 7, x, 11, 'E')
    s.rect(37, 8, 38, 10, 'c'); s.px(39, 9, 'z')     # свечение дула
    s.rect(20, 9, 23, 11, 'c'); s.px(21, 10, 'z')    # энергоблок
    s.ln(18, 13, 15, 17, 'E', 3)                     # рукоять
    return s


WEAPONS = [
    ('pipe', s_pipe), ('obrez', s_obrez), ('bat', s_bat), ('laserp', s_laserp),
    ('chainsaw', s_chainsaw), ('crossbow', s_crossbow), ('rifle', s_rifle),
    ('flamethrower', s_flamethrower), ('machete', s_machete), ('kuvarda', s_kuvarda),
    ('sniper', s_sniper), ('grenade', s_grenade), ('taser', s_taser),
    ('katana', s_katana), ('smg', s_smg), ('spear', s_spear), ('rocket', s_rocket),
    ('tesak', s_tesak), ('drobovik', s_drobovik), ('impulse', s_impulse),
]


def build_all():
    os.makedirs(OUT, exist_ok=True)
    sprites = []
    for name, fn in WEAPONS:
        s = fn()
        s.outline()
        s.save(name)
        sprites.append((name, s.render()))
    cols, cell_w, cell_h, label = 5, 240, 120, 18
    rows = (len(sprites) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * cell_w, rows * (cell_h + label)), (43, 47, 54))
    dr = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(sprites):
        cx, cy = (i % cols) * cell_w, (i // cols) * (cell_h + label)
        im2 = im.resize((im.width * SCALE, im.height * SCALE), Image.NEAREST)
        if im2.width > cell_w - 10:
            r = (cell_w - 10) / im2.width
            im2 = im2.resize((int(im2.width * r), int(im2.height * r)), Image.NEAREST)
        sheet.paste(im2, (cx + (cell_w - im2.width) // 2, cy + (cell_h - im2.height) // 2), im2)
        dr.text((cx + cell_w // 2 - len(name) * 3, cy + cell_h + 3), name, fill=(220, 220, 220))
    sheet.save(r"E:\Rad-Waste\tools\contact_sheet.png")
    print("OK:", len(sprites), "sprites ->", OUT)


if __name__ == '__main__':
    build_all()
