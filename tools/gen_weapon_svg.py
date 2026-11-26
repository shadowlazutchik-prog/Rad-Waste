#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор SVG-иллюстраций оружия для папки Weapons/.

Единый визуальный язык: ржавая сталь, тёмное дерево, изолента, заклёпки.
Каждое оружие — отдельный файл 600x300, прозрачный фон, чистый силуэт
в профиль (как в инвентаре Fallout).

Запуск:  python3 tools/gen_weapon_svg.py
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "Weapons")

DEFS = """
  <defs>
    <!-- Металл -->
    <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#9a9a92"/>
      <stop offset="0.18" stop-color="#6e6f68"/>
      <stop offset="0.55" stop-color="#4a4b45"/>
      <stop offset="0.8"  stop-color="#3a3b36"/>
      <stop offset="1"   stop-color="#232420"/>
    </linearGradient>
    <linearGradient id="steelDark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#6a6b64"/>
      <stop offset="0.3" stop-color="#45463f"/>
      <stop offset="0.75" stop-color="#2c2d28"/>
      <stop offset="1"   stop-color="#171814"/>
    </linearGradient>
    <linearGradient id="steelLight" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#c9c8bd"/>
      <stop offset="0.35" stop-color="#8e8f86"/>
      <stop offset="0.7"  stop-color="#5b5c55"/>
      <stop offset="1"   stop-color="#2f302b"/>
    </linearGradient>
    <linearGradient id="rust" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#a1653a"/>
      <stop offset="0.45" stop-color="#7a4a28"/>
      <stop offset="1"   stop-color="#4a2b17"/>
    </linearGradient>
    <linearGradient id="brass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#b99a52"/>
      <stop offset="0.5" stop-color="#8d7134"/>
      <stop offset="1"   stop-color="#5a4720"/>
    </linearGradient>
    <!-- Дерево -->
    <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#8a5a34"/>
      <stop offset="0.4" stop-color="#6b4325"/>
      <stop offset="0.78" stop-color="#4a2d18"/>
      <stop offset="1"   stop-color="#2e1c0f"/>
    </linearGradient>
    <linearGradient id="woodDark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#5e3d22"/>
      <stop offset="0.5" stop-color="#432b17"/>
      <stop offset="1"   stop-color="#25160b"/>
    </linearGradient>
    <!-- Изолента / тряпьё -->
    <linearGradient id="tape" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#4a4a44"/>
      <stop offset="0.5" stop-color="#33332e"/>
      <stop offset="1"   stop-color="#1d1d19"/>
    </linearGradient>
    <linearGradient id="cloth" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#7d7357"/>
      <stop offset="0.5" stop-color="#5d5540"/>
      <stop offset="1"   stop-color="#3a3428"/>
    </linearGradient>
    <!-- Свечение -->
    <radialGradient id="glowBlue" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0"   stop-color="#bfeaff" stop-opacity="0.95"/>
      <stop offset="0.4" stop-color="#4aa8e0" stop-opacity="0.75"/>
      <stop offset="1"   stop-color="#123a55" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowCyan" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0"   stop-color="#d8fff6" stop-opacity="0.95"/>
      <stop offset="0.45" stop-color="#43d9b5" stop-opacity="0.7"/>
      <stop offset="1"   stop-color="#0d3a30" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowRed" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0"   stop-color="#ffd3c6" stop-opacity="0.95"/>
      <stop offset="0.45" stop-color="#d0432a" stop-opacity="0.7"/>
      <stop offset="1"   stop-color="#3a0d06" stop-opacity="0"/>
    </radialGradient>

    <!-- Ржавая крапинка: накладывается поверх металла -->
    <filter id="grunge" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.55 0.75" numOctaves="3" seed="7" result="noise"/>
      <feColorMatrix in="noise" type="saturate" values="0" result="gray"/>
      <feComponentTransfer in="gray" result="spots">
        <feFuncA type="table" tableValues="0 0 0 0.55 0.9"/>
      </feComponentTransfer>
      <feComposite in="spots" in2="SourceAlpha" operator="in" result="masked"/>
      <feFlood flood-color="#5b3418" result="rust"/>
      <feComposite in="rust" in2="masked" operator="in" result="rustOn"/>
      <feMerge>
        <feMergeNode in="SourceGraphic"/>
        <feMergeNode in="rustOn"/>
      </feMerge>
    </filter>

    <!-- Мягкая тень под оружием -->
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#000" flood-opacity="0.65"/>
    </filter>

    <!-- Царапины -->
    <pattern id="scratches" width="46" height="34" patternUnits="userSpaceOnUse">
      <path d="M4 8 l14 -3" stroke="#cfd0c6" stroke-opacity="0.16" stroke-width="1.2"/>
      <path d="M28 22 l11 2" stroke="#e8e9df" stroke-opacity="0.12" stroke-width="1"/>
      <path d="M12 28 l6 -9" stroke="#000" stroke-opacity="0.22" stroke-width="1.3"/>
    </pattern>

    <!-- Патина: объём по краю + ржавая крапина, без серого налёта -->
    <filter id="patina" x="-12%" y="-12%" width="124%" height="124%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="b"/>
      <feOffset in="b" dy="-2.2" result="bUp"/>
      <feComposite in="SourceAlpha" in2="bUp" operator="out" result="edgeUp"/>
      <feGaussianBlur in="edgeUp" stdDeviation="1.2" result="edgeUpS"/>
      <feFlood flood-color="#fff8e6" flood-opacity="0.62" result="lit"/>
      <feComposite in="lit" in2="edgeUpS" operator="in" result="litMasked"/>

      <feOffset in="b" dy="2.6" result="bDn"/>
      <feComposite in="SourceAlpha" in2="bDn" operator="out" result="edgeDn"/>
      <feGaussianBlur in="edgeDn" stdDeviation="1.8" result="edgeDnS"/>
      <feFlood flood-color="#060402" flood-opacity="0.78" result="dark"/>
      <feComposite in="dark" in2="edgeDnS" operator="in" result="darkMasked"/>

      <!-- ржавые вкрапления строго внутри силуэта -->
      <feTurbulence type="fractalNoise" baseFrequency="0.09 0.14" numOctaves="4" seed="11" result="noise"/>
      <feColorMatrix in="noise" type="matrix" result="noiseA"
        values="0 0 0 0 0.26  0 0 0 0 0.13  0 0 0 0 0.05  -2.6 0 0 0 1.62"/>
      <feComposite in="noiseA" in2="SourceAlpha" operator="in" result="noiseIn"/>
      <feComposite in="SourceGraphic" in2="noiseIn" operator="over" result="grained"/>

      <!-- насыщенность и контраст -->
      <feComponentTransfer in="grained" result="punchy">
        <feFuncR type="linear" slope="1.16" intercept="-0.03"/>
        <feFuncG type="linear" slope="1.12" intercept="-0.025"/>
        <feFuncB type="linear" slope="1.04" intercept="-0.01"/>
      </feComponentTransfer>

      <feMerge>
        <feMergeNode in="punchy"/>
        <feMergeNode in="darkMasked"/>
        <feMergeNode in="litMasked"/>
      </feMerge>
    </filter>
  </defs>
"""


# Кроп-окна под каждое оружие: [x, y, w, h] в координатах холста 600x300.
# Подобраны так, чтобы оружие занимало ~88-94% ширины кадра и стояло по центру —
# как у фотореалистичных рендеров в остальных карточках.
CROPS = {
    "sniper":    (28, 78, 452, 162),
    "grenade":   (63, 82, 382, 182),
    "taser":     (70, 100, 440, 92),
    "katana":    (26, 96, 436, 110),
    "smg":       (58, 82, 348, 154),
    "spear":     (34, 50, 530, 168),
    "rocket":    (42, 48, 514, 216),
    "tesak":     (50, 74, 430, 164),
    "drobovik":  (58, 88, 424, 136),
    "impulse":   (46, 72, 398, 158),
}


def svg(inner: str, key: str = "") -> str:
    """Холст 600x300; содержимое обрезается по окну CROPS и растягивается на кадр."""
    x, y, w, h = CROPS.get(key, (0, 0, 600, 300))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" '
            f'width="600" height="300" preserveAspectRatio="xMidYMid meet" role="img">\n{DEFS}\n'
            f'<g filter="url(#patina)" style="filter:url(#patina)">\n{inner}\n</g>\n</svg>\n')


def rivets(points, r=2.4, fill="#20211d"):
    out = []
    for x, y in points:
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')
        out.append(f'<circle cx="{x - 0.6}" cy="{y - 0.7}" r="{r * 0.42}" fill="#b9bab0" opacity="0.55"/>')
    return "\n".join(out)


# --------------------------------------------------------------------------
# 1. Снайперская винтовка
# --------------------------------------------------------------------------
def sniper():
    p = []
    p.append('<g filter="url(#grunge)">')
    # ствол
    p.append('<rect x="70" y="140" width="300" height="13" rx="3" fill="url(#steelDark)"/>')
    p.append('<rect x="70" y="140" width="300" height="4" rx="2" fill="#7e7f76" opacity="0.55"/>')
    # дульный тормоз
    p.append('<rect x="52" y="132" width="34" height="29" rx="4" fill="url(#steel)"/>')
    p.append('<rect x="56" y="138" width="6" height="17" rx="2" fill="#111"/>')
    p.append('<rect x="66" y="138" width="6" height="17" rx="2" fill="#111"/>')
    # цевьё деревянное
    p.append('<path d="M150 153 h130 l-12 26 h-106 z" fill="url(#wood)"/>')
    p.append('<path d="M150 153 h130 l-2 5 h-126 z" fill="#a9794b" opacity="0.35"/>')
    # ресивер
    p.append('<rect x="270" y="126" width="118" height="52" rx="6" fill="url(#steel)"/>')
    p.append('<rect x="270" y="126" width="118" height="8" rx="3" fill="#b7b8ad" opacity="0.4"/>')
    p.append('<rect x="286" y="150" width="52" height="14" rx="3" fill="#15160f" opacity="0.75"/>')
    # затворная рукоять
    p.append('<rect x="330" y="112" width="10" height="20" rx="4" fill="url(#steelLight)"/>')
    p.append('<circle cx="335" cy="110" r="7" fill="url(#steel)"/>')
    # магазин
    p.append('<path d="M300 176 h34 l6 32 h-44 z" fill="url(#steelDark)"/>')
    p.append('<path d="M300 176 h34 l1 5 h-36 z" fill="#8e8f86" opacity="0.35"/>')
    # спусковая скоба
    p.append('<path d="M352 176 q6 22 26 22" fill="none" stroke="#2a2b26" stroke-width="5" stroke-linecap="round"/>')
    p.append('<path d="M360 172 q4 16 10 18" fill="none" stroke="#4b4c45" stroke-width="3"/>')
    # рукоять
    p.append('<path d="M378 173 l30 -4 12 46 -28 8 z" fill="url(#woodDark)"/>')
    p.append('<path d="M382 182 l24 -4 M384 192 l24 -4 M386 202 l24 -4" stroke="#20140a" stroke-width="2" opacity="0.6"/>')
    # приклад
    p.append('<path d="M390 130 h74 l26 20 -14 62 -30 -6 -8 -34 -48 -6 z" fill="url(#wood)"/>')
    p.append('<path d="M464 150 l26 -20 22 6 -6 66 -30 4 -14 -52 z" fill="url(#woodDark)"/>')
    p.append('<rect x="486" y="140" width="9" height="76" rx="4" fill="#2b2c26"/>')
    # приклад-резинка
    p.append('<path d="M390 130 h74 l26 20 -6 8 -22 -16 -72 2 z" fill="#8a5a34" opacity="0.5"/>')
    # оптика
    p.append('<rect x="252" y="96" width="126" height="24" rx="11" fill="url(#steelDark)"/>')
    p.append('<rect x="252" y="96" width="126" height="7" rx="4" fill="#9a9b91" opacity="0.5"/>')
    p.append('<rect x="240" y="92" width="20" height="32" rx="7" fill="url(#steel)"/>')
    p.append('<rect x="368" y="93" width="26" height="30" rx="8" fill="url(#steel)"/>')
    p.append('<circle cx="381" cy="108" r="7" fill="#0e1a20"/>')
    p.append('<circle cx="381" cy="108" r="7" fill="url(#glowCyan)" opacity="0.55"/>')
    # кольца крепления оптики
    p.append('<rect x="272" y="112" width="14" height="18" rx="4" fill="#23241f"/>')
    p.append('<rect x="336" y="112" width="14" height="18" rx="4" fill="#23241f"/>')
    # сошки
    p.append('<path d="M196 160 l-30 84" stroke="#2b2c26" stroke-width="8" stroke-linecap="round"/>')
    p.append('<path d="M216 160 l18 84" stroke="#2b2c26" stroke-width="8" stroke-linecap="round"/>')
    p.append('<rect x="152" y="240" width="20" height="7" rx="3" fill="#45463f"/>')
    p.append('<rect x="228" y="240" width="20" height="7" rx="3" fill="#45463f"/>')
    # изолента на стыке ствола
    p.append('<rect x="236" y="136" width="18" height="21" rx="2" fill="url(#tape)"/>')
    p.append(rivets([(300, 140), (322, 140), (344, 140), (366, 140)], 2.6))
    p.append('</g>')
    p.append('<rect x="70" y="140" width="300" height="52" fill="url(#scratches)" opacity="0.5"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 2. Гранатомёт
# --------------------------------------------------------------------------
def grenade():
    p = []
    p.append('<g filter="url(#grunge)">')
    # корпус
    p.append('<rect x="196" y="118" width="188" height="74" rx="10" fill="url(#steel)"/>')
    p.append('<rect x="196" y="118" width="188" height="12" rx="6" fill="#b4b5aa" opacity="0.35"/>')
    # барабан
    p.append('<circle cx="402" cy="155" r="52" fill="url(#steelDark)"/>')
    p.append('<circle cx="402" cy="155" r="38" fill="#2a2b25"/>')
    p.append('<circle cx="402" cy="155" r="30" fill="url(#steel)"/>')
    p.append('<circle cx="402" cy="155" r="9" fill="#14150f"/>')
    for i in range(6):
        import math
        a = math.radians(i * 60 + 15)
        x = 402 + 34 * math.cos(a)
        y = 155 + 34 * math.sin(a)
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#1b1c16"/>')
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="url(#brass)"/>')
    # ствол
    p.append('<rect x="96" y="136" width="112" height="40" rx="7" fill="url(#steelDark)"/>')
    p.append('<rect x="96" y="136" width="112" height="8" rx="4" fill="#8d8e85" opacity="0.45"/>')
    p.append('<ellipse cx="98" cy="156" rx="9" ry="20" fill="#111208"/>')
    p.append('<ellipse cx="98" cy="156" rx="9" ry="20" fill="none" stroke="#6f7067" stroke-width="4"/>')
    # кожух с прорезями
    for i in range(4):
        p.append(f'<rect x="{124 + i * 20}" y="142" width="10" height="28" rx="4" fill="#16170f" opacity="0.8"/>')
    # рукоять
    p.append('<path d="M300 190 l30 4 -6 62 -30 -4 z" fill="url(#woodDark)"/>')
    p.append('<path d="M303 200 l24 3 M301 214 l24 3 M299 228 l24 3" stroke="#1c1109" stroke-width="2.4" opacity="0.65"/>')
    p.append('<rect x="296" y="188" width="36" height="9" rx="3" fill="#2c2d27"/>')
    # спуск
    p.append('<path d="M344 196 q4 26 24 24" fill="none" stroke="#2a2b26" stroke-width="5" stroke-linecap="round"/>')
    # прицел
    p.append('<rect x="236" y="100" width="52" height="20" rx="5" fill="url(#steelLight)"/>')
    p.append('<rect x="246" y="104" width="32" height="12" rx="3" fill="#0d1208"/>')
    p.append('<rect x="236" y="100" width="52" height="5" rx="2" fill="#d0d1c6" opacity="0.4"/>')
    # ремень
    p.append('<path d="M214 192 q30 66 -6 74" fill="none" stroke="url(#cloth)" stroke-width="11" stroke-linecap="round" opacity="0.9"/>')
    p.append(rivets([(214, 128), (240, 128), (266, 128), (292, 128), (318, 128), (344, 128), (370, 128)]))
    p.append('</g>')
    p.append('<rect x="196" y="118" width="188" height="74" fill="url(#scratches)" opacity="0.55"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 3. Электрошокер
# --------------------------------------------------------------------------
def taser():
    p = []
    p.append('<g filter="url(#grunge)">')
    # рукоять
    p.append('<rect x="96" y="140" width="150" height="26" rx="11" fill="url(#woodDark)"/>')
    p.append('<rect x="100" y="143" width="142" height="7" rx="4" fill="#8a5a34" opacity="0.3"/>')
    for i in range(5):
        p.append(f'<rect x="{112 + i * 26}" y="140" width="11" height="26" fill="url(#tape)" opacity="0.85"/>')
    # корпус
    p.append('<rect x="240" y="126" width="150" height="54" rx="9" fill="url(#steel)"/>')
    p.append('<rect x="240" y="126" width="150" height="10" rx="5" fill="#b6b7ac" opacity="0.35"/>')
    # катушка
    p.append('<rect x="264" y="136" width="86" height="34" rx="6" fill="url(#brass)" opacity="0.85"/>')
    for i in range(7):
        p.append(f'<rect x="{268 + i * 12}" y="136" width="5" height="34" fill="#2b2313" opacity="0.5"/>')
    # провода
    p.append('<path d="M356 132 q28 -12 40 -2" fill="none" stroke="#8e2f24" stroke-width="3.4"/>')
    p.append('<path d="M356 176 q26 12 42 2" fill="none" stroke="#2b2b28" stroke-width="3.4"/>')
    # штыри
    p.append('<rect x="388" y="136" width="74" height="8" rx="4" fill="url(#steelLight)"/>')
    p.append('<rect x="388" y="162" width="74" height="8" rx="4" fill="url(#steelLight)"/>')
    p.append('<circle cx="466" cy="140" r="6" fill="#c8b06a"/>')
    p.append('<circle cx="466" cy="166" r="6" fill="#c8b06a"/>')
    # электрическая дуга
    p.append('<path d="M468 140 q22 -22 34 -2 q-16 18 -34 2 z" fill="url(#glowBlue)"/>')
    p.append('<path d="M470 166 q20 22 34 4 q-14 -20 -34 -4 z" fill="url(#glowBlue)"/>')
    p.append('<path d="M474 142 l14 -12 4 10 12 -8" fill="none" stroke="#cdefff" stroke-width="2.6" stroke-linejoin="round" opacity="0.95"/>')
    p.append('<path d="M474 164 l12 12 5 -9 13 7" fill="none" stroke="#cdefff" stroke-width="2.6" stroke-linejoin="round" opacity="0.95"/>')
    p.append('<circle cx="500" cy="152" r="34" fill="url(#glowBlue)" opacity="0.55"/>')
    # кнопка
    p.append('<circle cx="322" cy="162" r="9" fill="#7d2118"/>')
    p.append('<circle cx="322" cy="162" r="9" fill="none" stroke="#c8c9be" stroke-width="2" opacity="0.5"/>')
    p.append(rivets([(252, 134), (252, 172), (380, 134), (380, 172)]))
    p.append('</g>')
    p.append('<rect x="240" y="126" width="150" height="54" fill="url(#scratches)" opacity="0.4"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 4. Катана
# --------------------------------------------------------------------------
def katana():
    p = []
    p.append('<g filter="url(#grunge)">')
    # клинок (с лёгкой кривизной)
    p.append('<path d="M470 118 C 380 126, 268 132, 168 138 L 160 150 C 262 146, 380 142, 472 136 Z" fill="url(#steelLight)"/>')
    p.append('<path d="M470 118 C 380 126, 268 132, 168 138 L 166 142 C 266 136, 380 130, 471 124 Z" fill="#ffffff" opacity="0.35"/>')
    # хамон (линия закалки)
    p.append('<path d="M466 126 C 380 134, 270 140, 176 146" fill="none" stroke="#dfe2d6" stroke-width="2.2" opacity="0.5"/>')
    # гарда
    p.append('<ellipse cx="152" cy="146" rx="10" ry="26" fill="url(#steelDark)"/>')
    p.append('<ellipse cx="152" cy="146" rx="6" ry="19" fill="#14150f" opacity="0.6"/>')
    # рукоять
    p.append('<path d="M142 130 L66 138 L64 162 L142 154 Z" fill="url(#cloth)"/>')
    for i in range(7):
        x = 74 + i * 10
        p.append(f'<path d="M{x} 136 l6 20" stroke="#211d14" stroke-width="5" opacity="0.75"/>')
    # навершие
    p.append('<rect x="52" y="136" width="14" height="26" rx="4" fill="url(#brass)"/>')
    p.append('<circle cx="59" cy="149" r="4.4" fill="#2b2313"/>')
    # темляк
    p.append('<path d="M56 162 q-16 22 -2 34 q12 8 20 -2" fill="none" stroke="#8e2f24" stroke-width="4" stroke-linecap="round"/>')
    p.append('</g>')
    p.append('<path d="M470 118 C 380 126, 268 132, 168 138 L 160 150 C 262 146, 380 142, 472 136 Z" fill="url(#scratches)" opacity="0.35"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 5. Пистолет-пулемёт
# --------------------------------------------------------------------------
def smg():
    p = []
    p.append('<g filter="url(#grunge)">')
    # ствол
    p.append('<rect x="96" y="132" width="86" height="16" rx="4" fill="url(#steelDark)"/>')
    p.append('<rect x="96" y="132" width="86" height="5" rx="2" fill="#8f9087" opacity="0.5"/>')
    p.append('<rect x="82" y="128" width="18" height="24" rx="4" fill="url(#steel)"/>')
    # ресивер
    p.append('<rect x="176" y="112" width="168" height="56" rx="7" fill="url(#steel)"/>')
    p.append('<rect x="176" y="112" width="168" height="10" rx="5" fill="#b7b8ad" opacity="0.32"/>')
    # вентиляция
    for i in range(5):
        p.append(f'<rect x="{190 + i * 16}" y="126" width="9" height="9" rx="2" fill="#15160f" opacity="0.75"/>')
    # барабанный магазин
    p.append('<circle cx="252" cy="192" r="42" fill="url(#steelDark)"/>')
    p.append('<circle cx="252" cy="192" r="30" fill="#232420"/>')
    p.append('<circle cx="252" cy="192" r="9" fill="url(#brass)"/>')
    p.append('<circle cx="252" cy="192" r="42" fill="none" stroke="#15160f" stroke-width="4"/>')
    # пистолетная рукоять
    p.append('<path d="M300 168 l32 2 -10 62 -34 -4 z" fill="url(#woodDark)"/>')
    p.append('<path d="M304 182 l24 2 M302 196 l24 2 M300 210 l24 2" stroke="#1b1008" stroke-width="2.4" opacity="0.6"/>')
    # спусковая скоба
    p.append('<path d="M286 168 q-2 22 18 24" fill="none" stroke="#2a2b26" stroke-width="5" stroke-linecap="round"/>')
    # приклад-проволока
    p.append('<path d="M344 122 l58 -6 v12 l-58 8 z" fill="none" stroke="#5c5d55" stroke-width="6" stroke-linejoin="round"/>')
    p.append('<path d="M344 158 l58 10 v-34 l-58 8" fill="none" stroke="#5c5d55" stroke-width="6" stroke-linejoin="round"/>')
    p.append('<rect x="398" y="116" width="14" height="56" rx="5" fill="url(#steelDark)"/>')
    # рукоять-цевьё
    p.append('<rect x="152" y="156" width="24" height="40" rx="6" fill="url(#woodDark)"/>')
    # мушка
    p.append('<rect x="104" y="118" width="8" height="16" rx="2" fill="#2c2d27"/>')
    p.append('<rect x="330" y="102" width="10" height="14" rx="2" fill="#2c2d27"/>')
    p.append(rivets([(190, 120), (214, 120), (238, 120), (262, 120), (286, 120), (310, 120)]))
    p.append('</g>')
    p.append('<rect x="176" y="112" width="168" height="56" fill="url(#scratches)" opacity="0.5"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 6. Копьё
# --------------------------------------------------------------------------
def spear():
    p = []
    p.append('<g filter="url(#grunge)" transform="rotate(-14 300 150)">')
    # древко
    p.append('<rect x="52" y="142" width="418" height="14" rx="6" fill="url(#wood)"/>')
    p.append('<rect x="52" y="142" width="418" height="4" rx="2" fill="#ad7c4c" opacity="0.35"/>')
    # обмотка
    for x in (120, 158, 196):
        p.append(f'<rect x="{x}" y="139" width="26" height="20" rx="4" fill="url(#tape)"/>')
    p.append('<rect x="330" y="140" width="34" height="18" rx="4" fill="url(#cloth)"/>')
    # наконечник
    p.append('<path d="M470 148 L556 132 L590 149 L556 166 L470 152 Z" fill="url(#steelLight)"/>')
    p.append('<path d="M470 148 L556 132 L590 149 L556 140 L470 145 Z" fill="#ffffff" opacity="0.3"/>')
    p.append('<path d="M470 148 L556 132" stroke="#e7e8dd" stroke-width="2" opacity="0.5"/>')
    # втулка наконечника
    p.append('<rect x="452" y="136" width="24" height="26" rx="5" fill="url(#steelDark)"/>')
    p.append('<rect x="452" y="136" width="24" height="5" rx="2" fill="#9a9b91" opacity="0.45"/>')
    # зазубрины у основания
    p.append('<path d="M486 148 l-18 -16 6 18 z" fill="url(#rust)"/>')
    p.append('<path d="M486 152 l-18 16 6 -18 z" fill="url(#rust)"/>')
    p.append('</g>')
    p.append('<rect x="52" y="142" width="418" height="14" fill="url(#scratches)" opacity="0.45"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 7. Ракетница
# --------------------------------------------------------------------------
def rocket():
    p = []
    p.append('<g filter="url(#grunge)" transform="rotate(-8 300 150)">')
    # труба
    p.append('<rect x="96" y="120" width="392" height="60" rx="18" fill="url(#steelDark)"/>')
    p.append('<rect x="96" y="120" width="392" height="14" rx="7" fill="#9a9b91" opacity="0.28"/>')
    p.append('<rect x="96" y="164" width="392" height="16" rx="8" fill="#14150f" opacity="0.55"/>')
    # усиливающие кольца
    for x in (150, 236, 322, 408):
        p.append(f'<rect x="{x}" y="116" width="18" height="68" rx="7" fill="url(#steel)"/>')
        p.append(f'<rect x="{x}" y="116" width="18" height="8" rx="4" fill="#c2c3b8" opacity="0.4"/>')
    # головная часть (боеголовка)
    p.append('<path d="M488 120 h36 q46 4 54 30 q-8 26 -54 30 h-36 z" fill="url(#steelLight)"/>')
    p.append('<path d="M488 120 h36 q46 4 54 30 l-16 0 q-8 -20 -40 -22 h-34 z" fill="#ffffff" opacity="0.28"/>')
    p.append('<path d="M520 128 q28 6 34 22 q-6 16 -34 22" fill="none" stroke="#6f7067" stroke-width="3" opacity="0.6"/>')
    # сопло
    p.append('<path d="M96 122 q-30 18 0 56 l-14 6 q-40 -34 0 -68 z" fill="url(#steel)"/>')
    p.append('<ellipse cx="86" cy="150" rx="9" ry="26" fill="#0c0d09"/>')
    # рукоять и спуск
    p.append('<path d="M236 178 l34 0 -6 58 -32 -2 z" fill="url(#woodDark)"/>')
    p.append('<path d="M240 190 l26 0 M239 204 l26 0 M238 218 l26 0" stroke="#1a1007" stroke-width="2.6" opacity="0.6"/>')
    p.append('<path d="M286 180 q-2 22 18 24" fill="none" stroke="#2a2b26" stroke-width="5" stroke-linecap="round"/>')
    p.append('<path d="M360 182 l30 0 -4 44 -28 -2 z" fill="url(#woodDark)"/>')
    # прицел
    p.append('<rect x="330" y="98" width="84" height="26" rx="7" fill="url(#steel)"/>')
    p.append('<rect x="342" y="104" width="60" height="14" rx="4" fill="#0d1409"/>')
    p.append('<path d="M336 98 v-10 h10 v10" fill="none" stroke="#2c2d27" stroke-width="4"/>')
    p.append('<path d="M406 98 v-10 h10 v10" fill="none" stroke="#2c2d27" stroke-width="4"/>')
    # ремень
    p.append('<path d="M120 182 q26 52 -4 60" fill="none" stroke="url(#cloth)" stroke-width="11" stroke-linecap="round" opacity="0.85"/>')
    p.append(rivets([(159, 128), (159, 176), (245, 128), (245, 176), (331, 128), (331, 176), (417, 128), (417, 176)], 2.2))
    p.append('</g>')
    p.append('<rect x="96" y="120" width="392" height="60" fill="url(#scratches)" opacity="0.5"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 8. Тесак
# --------------------------------------------------------------------------
def tesak():
    p = []
    p.append('<g filter="url(#grunge)" transform="rotate(-12 300 150)">')
    # клинок
    p.append('<path d="M196 118 L470 128 L494 158 L470 182 L196 176 Z" fill="url(#steelLight)"/>')
    p.append('<path d="M196 118 L470 128 L474 136 L196 126 Z" fill="#ffffff" opacity="0.32"/>')
    p.append('<path d="M200 172 L466 178 L470 182 L196 176 Z" fill="#20211c" opacity="0.55"/>')
    # дол (кровосток)
    p.append('<path d="M214 140 L446 148" stroke="#5c5d55" stroke-width="7" stroke-linecap="round" opacity="0.55"/>')
    p.append('<path d="M214 141 L446 149" stroke="#cfd0c6" stroke-width="2" stroke-linecap="round" opacity="0.25"/>')
    # сколы на кромке
    p.append('<path d="M300 174 l8 -6 6 8 10 -7 7 9" fill="none" stroke="#8e8f86" stroke-width="3"/>')
    # пятка клинка
    p.append('<path d="M196 118 L176 122 L172 146 L190 148 Z" fill="url(#steel)"/>')
    # рукоять
    p.append('<rect x="86" y="132" width="94" height="30" rx="10" fill="url(#woodDark)"/>')
    for i in range(4):
        p.append(f'<rect x="{96 + i * 22}" y="130" width="13" height="34" rx="4" fill="url(#tape)" opacity="0.9"/>')
    p.append('<path d="M96 138 l76 4 M96 152 l76 4" stroke="#120b05" stroke-width="2.4" opacity="0.55"/>')
    # навершие
    p.append('<rect x="72" y="134" width="14" height="26" rx="5" fill="url(#brass)"/>')
    # темляк
    p.append('<path d="M76 158 q-14 26 4 36 q14 6 20 -6" fill="none" stroke="#7d2118" stroke-width="4.4" stroke-linecap="round"/>')
    p.append('</g>')
    p.append('<path d="M196 118 L470 128 L494 158 L470 182 L196 176 Z" fill="url(#scratches)" opacity="0.5"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 9. Дробовик помповый
# --------------------------------------------------------------------------
def drobovik():
    p = []
    p.append('<g filter="url(#grunge)">')
    # ствол
    p.append('<rect x="80" y="122" width="230" height="16" rx="5" fill="url(#steelDark)"/>')
    p.append('<rect x="80" y="122" width="230" height="5" rx="2" fill="#9a9b91" opacity="0.45"/>')
    # подствольный магазин
    p.append('<rect x="110" y="146" width="188" height="15" rx="6" fill="url(#steel)"/>')
    p.append('<rect x="110" y="146" width="188" height="5" rx="2" fill="#b7b8ad" opacity="0.3"/>')
    # цевьё-помпа
    p.append('<rect x="150" y="140" width="98" height="32" rx="9" fill="url(#wood)"/>')
    for i in range(5):
        p.append(f'<rect x="{158 + i * 18}" y="140" width="7" height="32" fill="#2b1a0d" opacity="0.45"/>')
    p.append('<rect x="150" y="140" width="98" height="7" rx="3" fill="#ad7c4c" opacity="0.3"/>')
    # ресивер
    p.append('<rect x="300" y="112" width="108" height="62" rx="8" fill="url(#steel)"/>')
    p.append('<rect x="300" y="112" width="108" height="11" rx="5" fill="#b7b8ad" opacity="0.32"/>')
    p.append('<ellipse cx="350" cy="146" rx="18" ry="14" fill="#1b1c16"/>')
    p.append('<ellipse cx="350" cy="146" rx="18" ry="14" fill="none" stroke="#6a6b64" stroke-width="3"/>')
    # окно выброса
    p.append('<rect x="378" y="130" width="22" height="14" rx="3" fill="#15160f"/>')
    # ложа
    p.append('<path d="M406 140 h52 l30 22 8 34 -34 10 -22 -28 -34 -6 z" fill="url(#wood)"/>')
    p.append('<path d="M406 140 h52 l30 22 -6 6 -26 -18 h-50 z" fill="#ad7c4c" opacity="0.3"/>')
    p.append('<rect x="486" y="150" width="10" height="48" rx="4" fill="#2b2c26"/>')
    # рукоять
    p.append('<path d="M406 172 l28 4 -6 46 -28 -4 z" fill="url(#woodDark)"/>')
    # спуск
    p.append('<path d="M392 174 q0 20 18 22" fill="none" stroke="#2a2b26" stroke-width="5" stroke-linecap="round"/>')
    # мушка
    p.append('<rect x="92" y="110" width="9" height="14" rx="2" fill="#2c2d27"/>')
    p.append('<rect x="86" y="116" width="26" height="6" rx="3" fill="#3a3b36"/>')
    p.append('<rect x="80" y="120" width="16" height="22" rx="4" fill="url(#steelLight)"/>')
    p.append(rivets([(314, 120), (334, 120), (354, 120), (374, 120), (394, 120)]))
    p.append('</g>')
    p.append('<rect x="300" y="112" width="108" height="62" fill="url(#scratches)" opacity="0.5"/>')
    return "".join(p)


# --------------------------------------------------------------------------
# 10. Импульсный карабин
# --------------------------------------------------------------------------
def impulse():
    p = []
    p.append('<g filter="url(#grunge)">')
    # ствол
    p.append('<rect x="106" y="132" width="120" height="18" rx="6" fill="url(#steelDark)"/>')
    p.append('<rect x="106" y="132" width="120" height="6" rx="3" fill="#9a9b91" opacity="0.4"/>')
    # светящиеся кольца-катушки
    for i, x in enumerate((126, 158, 190)):
        p.append(f'<rect x="{x}" y="124" width="14" height="34" rx="6" fill="url(#steel)"/>')
        p.append(f'<rect x="{x}" y="128" width="14" height="6" rx="3" fill="#8dfff0" opacity="0.75"/>')
        p.append(f'<circle cx="{x + 7}" cy="141" r="26" fill="url(#glowCyan)" opacity="0.35"/>')
    # дуло
    p.append('<rect x="88" y="126" width="24" height="30" rx="8" fill="url(#steelLight)"/>')
    p.append('<ellipse cx="92" cy="141" rx="7" ry="12" fill="#eafffb"/>')
    p.append('<ellipse cx="92" cy="141" rx="7" ry="12" fill="url(#glowCyan)"/>')
    p.append('<circle cx="92" cy="141" r="26" fill="url(#glowCyan)" opacity="0.5"/>')
    # корпус
    p.append('<rect x="226" y="116" width="150" height="54" rx="10" fill="url(#steel)"/>')
    p.append('<rect x="226" y="116" width="150" height="11" rx="5" fill="#b7b8ad" opacity="0.3"/>')
    # энергоячейка
    p.append('<rect x="244" y="130" width="60" height="28" rx="6" fill="#1d3d36"/>')
    p.append('<rect x="244" y="130" width="60" height="28" rx="6" fill="url(#glowCyan)" opacity="0.55"/>')
    for i in range(4):
        p.append(f'<rect x="{250 + i * 14}" y="132" width="6" height="24" rx="2" fill="#c9fff4" opacity="0.7"/>')
    # индикатор
    p.append('<circle cx="330" cy="128" r="6" fill="#8dfff0"/>')
    p.append('<circle cx="330" cy="128" r="12" fill="url(#glowCyan)" opacity="0.5"/>')
    # вентиляция
    for i in range(3):
        p.append(f'<rect x="{344 + i * 10}" y="140" width="6" height="20" rx="3" fill="#15160f" opacity="0.8"/>')
    # пистолетная рукоять
    p.append('<path d="M290 168 l34 0 -8 60 -34 -2 z" fill="url(#steelDark)"/>')
    p.append('<path d="M294 180 l26 0 M292 194 l26 0 M291 208 l26 0" stroke="#0e0f0b" stroke-width="2.6" opacity="0.6"/>')
    # спусковая скоба
    p.append('<path d="M334 168 q0 22 20 24" fill="none" stroke="#2a2b26" stroke-width="5" stroke-linecap="round"/>')
    # приклад
    p.append('<path d="M376 122 h50 l22 16 6 30 -26 10 -20 -20 -32 -4 z" fill="url(#steelDark)"/>')
    p.append('<rect x="436" y="140" width="12" height="34" rx="5" fill="#23241f"/>')
    # кабель
    p.append('<path d="M300 116 q22 -22 52 -14" fill="none" stroke="#2b2b28" stroke-width="5" stroke-linecap="round"/>')
    p.append('<path d="M300 116 q22 -22 52 -14" fill="none" stroke="#8dfff0" stroke-width="1.6" opacity="0.6"/>')
    # прицел
    p.append('<rect x="352" y="100" width="46" height="18" rx="6" fill="url(#steelLight)"/>')
    p.append('<rect x="360" y="104" width="30" height="10" rx="3" fill="#0b1a17"/>')
    p.append(rivets([(238, 124), (238, 162), (364, 124), (364, 162)]))
    p.append('</g>')
    p.append('<rect x="226" y="116" width="150" height="54" fill="url(#scratches)" opacity="0.45"/>')
    return "".join(p)


WEAPONS = {
    "sniper": sniper,
    "grenade": grenade,
    "taser": taser,
    "katana": katana,
    "smg": smg,
    "spear": spear,
    "rocket": rocket,
    "tesak": tesak,
    "drobovik": drobovik,
    "impulse": impulse,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for key, fn in WEAPONS.items():
        path = os.path.join(OUT, f"{key}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg(fn(), key))
        print("wrote", path)


if __name__ == "__main__":
    main()
