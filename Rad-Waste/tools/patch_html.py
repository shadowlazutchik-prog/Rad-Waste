# -*- coding: utf-8 -*-
"""Замена блока inline-спрайтов в waste2.html на загрузку PNG из папки Weapons."""
p = r"E:\Rad-Waste\waste2.html"
src = open(p, encoding='utf-8').read()

start = src.index('// --- PIXEL ART WEAPON SPRITES')
end = src.index('// Generate Cards')
indent = ' ' * 8

new_block = indent + '''// --- SPRITES ОРУЖИЯ: внешние PNG из папки Weapons ---
        const weaponSpriteKeys = ['pipe','obrez','bat','laserp','chainsaw','crossbow','rifle','flamethrower','machete','kuvarda','sniper','grenade','taser','katana','smg','spear','rocket','tesak','drobovik','impulse'];

        function spriteSVG(key) {
            return `<img class="wpn-sprite" src="Weapons/${key}.png" alt="">`;
        }

'''

src = src[:start] + new_block + src[end:]
open(p, 'w', encoding='utf-8').write(src)
print('OK, block replaced')
