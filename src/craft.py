#crafting system
import pygame, sys, os
from pygame.locals import *
<<<<<<< HEAD
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
=======
type_list = {K_1: 1, K_2 : 2, K_3 : 3, K_4 :1, K_5 : 2, K_6 : 3, K_q : 1, K_w :2, K_e : 3, K_r : 1, K_t : 2, K_y: 3}
inv_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond']
my_dict = {}
for material in inv_list:
    if material not in my_dict:
        my_dict[material] = 1
    else:
        my_dict[material] += 1
print my_dict

random_val = [0,0,0,0]
keys = {K_1: 'Copper', K_2: "Aluminum", K_3: "Uranium", K_4: "Copper", K_5:"Amuminum", K_6:"Uranium", K_q: "Ruby", K_w: "Emerald", K_e : "Diamond", K_r : "Ruby", K_t : "Emerald", K_y : "Diamond"}
>>>>>>> origin/olivierWIP
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.update()
item_type = [0,0,0,0]
item_qtty = [0,0,0,0]
keys_metal = [K_1,K_2,K_3,K_4,K_5,K_6]
keys_gems = [K_q,K_w,K_e,K_r,K_t,K_y]
<<<<<<< HEAD
keys_end = [K_SPACE, K_RETURN, K_ESCAPE, K_p]
=======
keys_end = [K_RETURN]
>>>>>>> origin/olivierWIP
m_tuple = (0,0)
g_tuple = (0,0)
foo = True
def potater (index):
    if event.key in keys:
                random_val[index] = item_type[index]
<<<<<<< HEAD
                if event.key in {K_1,K_2,K_3, K_q,K_w,K_e}:
                    item_type[index] = type_list[event.key]
                    item_qtty[index] += 1
=======
                if event.key in [K_1,K_2,K_3, K_q,K_w,K_e]:
                    if my_dict[keys[event.key]] == 0:
                        print 'U suk no moar'
                    else:
                        item_type[index] = type_list[event.key]
                        item_qtty[index] += 1
                        my_dict[keys[event.key]] -= 1
>>>>>>> origin/olivierWIP
                    if item_type[index] == random_val[index]:
                        pass
                    else:
                        item_qtty[index] = 1
                    print keys[event.key], "added, total amount:", item_qtty[index]
<<<<<<< HEAD
                elif event.key in {K_4,K_5,K_6,K_r,K_t,K_y}:
                    item_type[index] = type_list [event.key]
                    item_qtty[index] -= 1
=======
                    print 'amount left:', my_dict[keys[event.key]]
                elif event.key in [K_4,K_5,K_6,K_r,K_t,K_y]:
                    if item_qtty[index] == 0:
                        print 'stahp exploit'
                    else:
                        item_type[index] = type_list [event.key]
                        item_qtty[index] -= 1
                        my_dict[keys[event.key]] +=1
>>>>>>> origin/olivierWIP
                    if item_qtty[index] < 0:
                        item_qtty[index] = 0
                    if item_type[index] == random_val[index]:
                        pass
                    else:
                        item_qtty[index] = 0
                    print keys[event.key], "removed, total amount", item_qtty[index]
<<<<<<< HEAD
=======
                    print 'amount left:', my_dict[keys[event.key]]
>>>>>>> origin/olivierWIP
while foo:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in keys_metal:
                metal_tuple = potater(0)
            elif event.key in keys_gems:
                gem_tuple = potater(1)
            elif event.key in keys_end:
<<<<<<< HEAD
                foo = False
            else:
                pass
print "crafting finished"
#En bas: tree prototype
dict = {(1,1,1,1) : 'pistol', (1,2,1,1): 'shotgun', (1,3,1,1): 'potato launcher'}
crafting_list = [item_type[0], item_qtty[0], item_type[1], item_qtty[1]]
print dict[tuple(crafting_list)]
=======
                print 'crafting finished, result:'
                foo = False
            else:
                pass
#En bas: tree prototype
dict = {(1,1,1,1) : 'pistol', (1,2,1,1): 'shotgun', (1,3,1,1): 'potato launcher'}
crafting_list = [item_type[0], item_qtty[0], item_type[1], item_type[1]]
crafting_list = tuple(crafting_list)
print dict [crafting_list]
>>>>>>> origin/olivierWIP
#we can add more possibilities (more metals, more gems, more stuff (rocks? idk) just need to edit the recipes
