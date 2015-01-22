#crafting system
import pygame, sys, os
from pygame.locals import *
import yaml
import pdb
from operator import add
yaml_is_sexy = yaml.load(open('../data/craftstore.yaml','r'))
display_res = (1920,1080)
factor = (float(display_res[0])/3840.0,float(display_res[1])/2160.0)

pos = []
pos_order = ['metal','gem','potato','tomato','science']
for i in pos_order:
    for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
        pos.append(tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]) + tuple(map(add, yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j], yaml_is_sexy['craftstore']['smallsquares']['size'])))
pos_metal = pos[0:6]
pos_gems = pos[6:12]

inv_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond']
qty_dict = {}
for material in inv_list:
    if material not in qty_dict:
        qty_dict[material] = 1
    else:
        qty_dict[material] += 1
print qty_dict

"""cell_dict ={
    pos_metal[0]: 'Copper',
    pos_metal[1]: 'Aluminum',
    pos_metal[2]: 'Uranium',
    pos_gems[0]: 'Ruby',
    pos_gems[1]: 'Emerald',
    pos_gems[2]: 'Diamond'
    }"""
type_dict = [
    {1: 'Copper', 2: 'Aluminum', 3: 'Uranium'},
    {1: 'Ruby', 2: 'Emerald', 3: 'Diamond'}]

"""type_dict = [
    {'Copper': 1, 'Aluminum': 2, 'Uranium': 3},
    {'Ruby': 1, 'Emerald': 2, 'Diamond': 3}]"""
item_type = [0,0,0,0,0]
item_qty = [0,0,0,0,0]

keys_gems = [K_q,K_w,K_e,K_r,K_t,K_y]
keys_end = [K_RETURN]
crafting = True

pygame.init()
screen = pygame.display.set_mode(display_res)
screen_render = pygame.Surface((3840,2160))
craft_square = pygame.image.load(os.path.join(*yaml_is_sexy['craft']['largesquares']['img']))
inv_square = pygame.image.load(os.path.join(*yaml_is_sexy['craftstore']['smallsquares']['img']))
craft_button = pygame.image.load(os.path.join(*yaml_is_sexy['craft']['buttons']['img']))
for i in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
    screen_render.blit(craft_square, tuple(yaml_is_sexy['craft']['largesquares']['positions'][i]))
for i in yaml_is_sexy['craftstore']['smallsquares']['positions']:
    for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
        screen_render.blit(inv_square, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
print tuple(yaml_is_sexy['craft']['largesquares']['positions'])
screen_render.blit(craft_button, tuple(yaml_is_sexy['craft']['buttons']['positions']))
screen_final = pygame.transform.smoothscale(screen_render, display_res)
screen.blit(screen_final,(0,0))
pygame.display.flip()


def potater (index, typeof_item):
    if qty_dict[type_dict[index][typeof_item]] == 0:
        print 'U suk no moar' #change to gui function
    elif item_type[index] != 0 and item_qty[index] !=0:
        if item_type[index] == typeof_item:
            item_type[index] = typeof_item
            item_qty[index] += 1
            qty_dict[type_dict[index][typeof_item]] -= 1
            print type_dict[index][typeof_item], "added, total amount:", item_qty[index] #change to gui function
            print 'amount left:', qty_dict[type_dict[index][typeof_item]] #change to gui function
        else:
            print 'Cannot add different material', 'Your crafting inventory:' #change to gui function
            print item_type , item_qty #change to gui function
    else:
        item_type[index] = typeof_item
        item_qty[index] += 1
        qty_dict[type_dict[index][typeof_item]] -= 1
        print type_dict[index][typeof_item], "added, total amount:", item_qty[index] #change to gui function
        print 'amount left:', qty_dict[type_dict[index][typeof_item]] #change to gui function
    print typeof_item, item_type[index]
    return (item_type[index],item_qty[index])
        
            
            
        
"""def potater (index):
                if event.key in keys:
                    if event.key in [K_1,K_2,K_3, K_q,K_w,K_e]:
                        if my_dict[keys[event.key]] == 0:
                                        print 'U suk no moar'
                        else:
                            if item_type[index] != 0 and item_qtty[index] != 0:
                                if item_type[index] == type_list[event.key]:
                                    item_type[index] = type_list[event.key]
                                    item_qtty[index] += 1
                                    my_dict[keys[event.key]] -= 1
                                    print keys[event.key], "added, total amount:", item_qtty[index]
                                    print 'amount left:', my_dict[keys[event.key]]
                                else:
                                    print 'Cannot add different material', 'Your crafting inventory:'
                                    print item_type , item_qtty
                            else:
                                item_type[index] = type_list[event.key]
                                item_qtty[index] += 1
                                my_dict[keys[event.key]] -= 1
                                print keys[event.key], "added, total amount:", item_qtty[index]
                                print 'amount left:', my_dict[keys[event.key]]

                    elif event.key in [K_4,K_5,K_6,K_r,K_t,K_y]:
                        if item_qtty[index] == 0:
                            print 'stahp exploit'
                        else:
                            if item_type[index] != 0 and item_qtty[index] != 0:
                                if item_type[index] == type_list[event.key]:
                                    item_type[index] = type_list [event.key]
                                    item_qtty[index] -= 1 
                                    my_dict[keys[event.key]] +=1
                                    if item_qtty[index] < 0:
                                        item_qtty[index] = 0
                                    print keys[event.key], "removed, total amount", item_qtty[index]
                                    print 'amount left:', my_dict[keys[event.key]]
                                else:
                                    print 'Cannot remove different material', 'Your crafting inventory:'
                                    print item_type , item_qtty
                            else:
                                item_type[index] = type_list [event.key]
                                item_qtty[index] -= 1 
                                my_dict[keys[event.key]] +=1
                                if item_qtty[index] < 0:
                                    item_qtty[index] = 0
                                print keys[event.key], "removed, total amount", item_qtty[index]
                                print 'amount left:', my_dict[keys[event.key]]
                return (item_type[index],item_qtty[index])"""

def mouse_check(mouse_pos):
    print mouse_pos[0], mouse_pos[1]
    for x in pos:
        #print x[0]*factor[0], x[2]*factor[0], x[1]*factor[1], x[3]*factor[1]
        if (mouse_pos[0] >= x[0]*factor[0] and mouse_pos[0] <= x[2]*factor[0] and mouse_pos[1] >= x[1]*factor[1] and mouse_pos[1] <= x[3]*factor[1]):
            return (pos.index(x)/6,pos.index(x)%6)
        else:
            pass
        
    
    
    
    
                    
while crafting:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            which_rect = mouse_check(mouse_pos)
            #print which_rect
            potater(which_rect[0],(which_rect[1]+1))
        if event.type == KEYDOWN:
            if event.key in keys_end:
                print 'crafting finished, result:'
                crafting = False

#En bas: tree prototype
dict = {(1,1,1,1) : 'pistol', (1,2,1,1): 'shotgun', (1,3,1,1): 'potato launcher'}
crafting_list = metal_tuple+gem_tuple
print dict [crafting_list]
#we can add more possibilities (more metals, more gems, more stuff (rocks? idk) just need to edit the recipes
