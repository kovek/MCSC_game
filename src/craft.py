#crafting system
import pygame, sys, os
from pygame.locals import *
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
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.update()
item_type = [0,0,0,0]
item_qtty = [0,0,0,0]
keys_metal = [K_1,K_2,K_3,K_4,K_5,K_6]
keys_gems = [K_q,K_w,K_e,K_r,K_t,K_y]
keys_end = [K_RETURN]
m_tuple = (0,0)
g_tuple = (0,0)
foo = True
def potater (index):
    if event.key in keys:
                random_val[index] = item_type[index]
                if event.key in [K_1,K_2,K_3, K_q,K_w,K_e]:
                    if my_dict[keys[event.key]] == 0:
                        print 'U suk no moar'
                    else:
                        item_type[index] = type_list[event.key]
                        item_qtty[index] += 1
                        my_dict[keys[event.key]] -= 1
                    if item_type[index] == random_val[index]:
                        pass
                    else:
                        item_qtty[index] = 1
                    print keys[event.key], "added, total amount:", item_qtty[index]
                    print 'amount left:', my_dict[keys[event.key]]
                elif event.key in [K_4,K_5,K_6,K_r,K_t,K_y]:
                    if item_qtty[index] == 0:
                        print 'stahp exploit'
                    else:
                        item_type[index] = type_list [event.key]
                        item_qtty[index] -= 1
                        my_dict[keys[event.key]] +=1
                    if item_qtty[index] < 0:
                        item_qtty[index] = 0
                    if item_type[index] == random_val[index]:
                        pass
                    else:
                        item_qtty[index] = 0
                    print keys[event.key], "removed, total amount", item_qtty[index]
                    print 'amount left:', my_dict[keys[event.key]]
while foo:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in keys_metal:
                metal_tuple = potater(0)
            elif event.key in keys_gems:
                gem_tuple = potater(1)
            elif event.key in keys_end:
                print 'crafting finished, result:'
                foo = False
            else:
                pass
#En bas: tree prototype
dict = {(1,1,1,1) : 'pistol', (1,2,1,1): 'shotgun', (1,3,1,1): 'potato launcher'}
crafting_list = [item_type[0], item_qtty[0], item_type[1], item_type[1]]
crafting_list = tuple(crafting_list)
print dict [crafting_list]
#we can add more possibilities (more metals, more gems, more stuff (rocks? idk) just need to edit the recipes