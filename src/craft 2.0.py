#crafting system
import pygame, sys, os
from pygame.locals import *
inv_m1_qtty = 10
inv_m2_qtty = 10
inv_m3_qtty = 10
inv_g1_qtty = 10
inv_g2_qtty = 10
inv_g3_qtty = 10
metal_type = 0
metal_qtty = 0
metal_1_qtty = 0
metal_2_qtty = 0
metal_3_qtty = 0
gem_type = 0
gem_qtty = 0
gem_1_qtty = 0
gem_2_qtty = 0
gem_3_qtty = 0
pygame.init()
keys=pygame.key.get_pressed()
while True:
    keys=pygame.key.get_pressed()
    print keys
    if K_1 in keys:
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
#we can add more possibilities (more metals, more gems, more stuff (rocks? idk) just need to edit the recipes
