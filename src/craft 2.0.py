#crafting system
import pygame, sys, os
from pygame.locals import *
inv_m_qtty = [10,10,10]
inv_g_qtty = [10,10,10]
metal_type = 0
type_list = {K_1: 1, K_2 : 2, K_3 : 3, K_4 :1, K_5 : 2, K_6 : 3, K_q : 1, K_w :2, K_e : 3, K_r : 1, K_t : 2, K_y: 3}
metal_qtty = 0
metal_1_qtty = 0
metal_2_qtty = 0
metal_3_qtty = 0
m_qtty = 0
gem_type = 0
gem_qtty = 0
random_val = [0,0,0,0]
keys = {K_1: 'Metal 1', K_2: "Metal 2", K_3: "Metal 3", K_4: "Metal 1", K_5:"Metal 2", K_6:"Metal 3", K_q: "Gem 1", K_w: "Gem 2", K_e : "Gem 3", K_r : "Gem 1", K_t : "Gem 2", K_y : "Gem 3"}
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.update()
item_type = [0,0,0,0]
item_qtty = [0,0,0,0]
keys_metal = {K_1,K_2,K_3,K_4,K_5,K_6}
keys_gems = {K_q,K_w,K_e,K_r,K_t,K_y}
m_tuple = (0,0)
g_tuple = (0,0)
def potater (index):
    if event.key in keys:
                random_val[index] = item_type[index]
                if event.key in {K_1,K_2,K_3, K_q,K_w,K_e}:
                    item_type[index] = type_list[event.key]
                    item_qtty[index] += 1
                    if item_type[index] == random_val[index]:
                        pass
                    else:
                        item_qtty[index] = 1
                    print keys[event.key], "added, total amount:", item_qtty[index]
                elif event.key in {K_4,K_5,K_6,K_q,K_w,K_e}:
                    metal_type[index] = type_list [event.key]
                    item_qtty[index] -= 1
                    if item_qtty[index] < 0:
                        item_qtty[index] = 0
                    if item[index] == random_val[index]:
                        pass
                    else:
                        item_qtty[index] = 0
                    print keys[event.key], "removed, total amount", item_qtty[index]
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in keys_metal:
                metal_tuple = potater(0)
            elif event.key in keys_gems:
                gem_tuple = potater(1)
            else:
                pass
"""if K_1 in keys:
    metal_type = 1
    metal_1_qtty = metal_1_qtty + 1
    print "metal 1 added, current amount:", metal_1_qtty
elif keys[K_2]:
    metal_type = 2
    metal_2_qtty = metal_2_qtty + 1
    print "metal 2 added, current amount:", metal_2_qtty
elif keys[K_3]:
    metal_type = 3
    metal_3_qtty = metal_3_qtty + 1
pygame.display.flip()
if metal_type == 1:
    inv_m1_qtty = inv_m1_qtty - metal_qtty
elif metal_type == 2:
        inv_m2_qtty = inv_m2_qtty - metal_qtty
elif metal_type == 3:
        inv_m3_qtty = inv_m3_qtty - metal_qtty
#^set le type et le nombre de metal
#mtn gems
print 'Wat gem type??'
while True:
    try:
        gem_type = input()
    except:
        print '1 2 or 3'
    else:
        if gem_type == 1 or gem_type == 2 or gem_type == 3:
            break
        else:
            print 'Tas un ptit zizi  1 2 ou 3'
            pass
print 'How many gems?'
while True:
    try :
        gem_qtty = input()
    except:
        print '1 2 or 3'
    else:
        if gem_qtty == 1 or gem_qtty == 2 or gem_qtty == 3:
            break
        else:
            print '1 2 or 3 n00blord'
            pass
if gem_type == 1:
    gem_1_qtty = gem_qtty
    inv_g1_qtty = inv_g1_qtty - gem_qtty
elif metal_type == 2:
    gem_2_qtty = gem_qtty
    inv_g2_qtty = inv_g2_qtty - gem_qtty
elif metal_type == 3:
    gem_3_qtty = gem_qtty
    inv_g3_qtty = inv_g3_qtty - gem_qtty
#En bas: tree prototype
dict = {(1,1,1,1) : 'pistol', (1,2,1,1): 'shotgun', (1,3,1,1): 'potato launcher'}
crafting_list = [metal_type, metal_qtty, gem_type, gem_qtty]
crafting_list = tuple(crafting_list)
print dict [crafting_list]
#we can add more possibilities (more metals, more gems, more stuff (rocks? idk) just need to edit the recipes"""
