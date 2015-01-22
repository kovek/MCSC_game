#crafting system
import pygame, sys, os
from pygame.locals import *
import yaml
import pdb
from operator import add
yaml_is_sexy = yaml.load(open('../data/craftstore.yaml','r'))
display_res = (960,540)
factor = (float(display_res[0])/3840.0,float(display_res[1])/2160.0)

pos = []
pos_order = ['metal','gem','potato','tomato','science']
for i in pos_order:
    for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
        pos.append(tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]) + tuple(map(add, yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j], yaml_is_sexy['craftstore']['smallsquares']['size'])))
for i in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
    pos.append(tuple(yaml_is_sexy['craft']['largesquares']['positions'][i]) + tuple(map(add, yaml_is_sexy['craft']['largesquares']['positions'][i], yaml_is_sexy['craft']['largesquares']['size'] )))
pos.append(tuple(yaml_is_sexy['craft']['buttons']['positions']) + tuple(map(add, yaml_is_sexy['craft']['buttons']['positions'], yaml_is_sexy['craft']['buttons']['size'])))
print pos

inv_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond']
qty_dict = {}
for material in inv_list:
    if material not in qty_dict:
        qty_dict[material] = 1
    else:
        qty_dict[material] += 1
print qty_dict

type_dict = [
    {1: 'Copper', 2: 'Aluminum', 3: 'Uranium'},
    {1: 'Ruby', 2: 'Emerald', 3: 'Diamond'}]

item_type = [0,0,0,0,0]
item_qty = [0,0,0,0,0]
item_dict = {(1,1,1,1) : 'pistol', (1,2,1,1): 'shotgun', (1,3,1,1): 'potato launcher'}
crafting_tuples = [(),(),(),(),()]
crafting_tuple_final = ()

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
        print "amount left:", qty_dict[type_dict[index][typeof_item]] #change to gui function
    return (item_type[index],item_qty[index])

def unpotater (index, typeof_item):
    if item_qty[index] == 0:
        print 'stahp exploit' #change to gui function
    elif item_type[index] != 0 and item_qty[index] != 0:
        if item_type[index] == typeof_item:
            item_type[index] == typeof_item
            item_qty[index] -= 1
            qty_dict[type_dict[index][typeof_item]] += 1
            if item_qty[index] < 0:
                item_qty[index] == 0
            print type_dict[index][typeof_item], "removed, total amount: ", item_qty[index] #change to gui function
            print "amount left:", qty_dict[type_dict[index][typeof_item]] #change to gui function
    else:
        item_type[index] == typeof_item
        item_qty[index] -= 1
        qty_dict[type_dict[index][typeof_item]] += 1
        if item_qty[index] == 0:
            item_qty[index] = 0
        print type_dict[index][typeof_item], "removed, total amount: ", item_qty[index] #change to gui function
        print "amount left:", qty_dict[type_dict[index][typeof_item]] #change to gui function
    return (item_type[index],item_qty[index])

def mouse_check(mouse_pos):
    #print mouse_pos[0], mouse_pos[1]
    for x in pos:
        #print x[0]*factor[0], x[2]*factor[0], x[1]*factor[1], x[3]*factor[1]
        if (mouse_pos[0] >= x[0]*factor[0] and mouse_pos[0] <= x[2]*factor[0] and mouse_pos[1] >= x[1]*factor[1] and mouse_pos[1] <= x[3]*factor[1]):
            if pos.index(x) < 30:
                return (pos.index(x)/6,pos.index(x)%6)
            elif pos.index(x) >= 30 and pos.index(x) < 35:
                return (pos.index(x)%6,)
            elif pos.index(x) >= 35:
                return ()
            else:
                pass
        else:
            pass
        
while crafting:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            which_rect = mouse_check(mouse_pos)
            print which_rect
            try:
                len(which_rect)
            except:
                pass
            else:
                if len(which_rect) == 2:
                    crafting_tuples[which_rect[0]] = potater(which_rect[0],(which_rect[1]+1))
                elif len(which_rect) == 1:
                    if item_type[which_rect[0]] != 0:
                        crafting_tuples[which_rect[0]] = unpotater(which_rect[0], item_type[which_rect[0]])
                    else:
                        pass
                elif len(which_rect) == 0:
                    print "crafting finished, result:"
                    for i in range(5):
                        crafting_tuple_final += crafting_tuples[i]
                    try:
                        print item_dict[crafting_tuple_final]
                    except:
                        print "none"
