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
for i in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
    pos.append(tuple(yaml_is_sexy['craft']['largesquares']['positions'][i]) + tuple(map(add, yaml_is_sexy['craft']['largesquares']['positions'][i], yaml_is_sexy['craft']['largesquares']['size'] )))
pos.append(tuple(yaml_is_sexy['craft']['buttons']['positions']) + tuple(map(add, yaml_is_sexy['craft']['buttons']['positions'], yaml_is_sexy['craft']['buttons']['size'])))
"""print pos""" #debug

inv_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond']
qty_dict = {}
for material in inv_list:
    if material not in qty_dict:
        qty_dict[material] = 1
    else:
        qty_dict[material] += 1
"""print qty_dict""" #debug

items = []
for i in pos_order:
    items.extend(yaml_is_sexy['item_types'][i])
yaml_is_sexy['items'] = items

type_dict =[
    {j%6+1:yaml_is_sexy['item_types'][i][j%6] for j in range(pos_order.index(i)*6,pos_order.index(i)*6+len(yaml_is_sexy['item_types'][i]))} for i in pos_order]
print type_dict

item_type = [0,0,0,0,0]
item_qty = [0,0,0,0,0]
item_dict = {(4,1,3,1) : 'pistol', (4,2,3,1): 'shotgun', (4,3,3,1): 'potato launcher'}
crafting_tuples = [(),(),(),(),()]
crafting_tuple_final = ()
crafting_results = []
crafting = True

texts = []
text_list = [i for i in yaml_is_sexy['craft']['text']]

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(display_res)
screen_render = pygame.Surface((3840,2160))
craft_square = pygame.image.load(os.path.join(*yaml_is_sexy['craft']['largesquares']['img']))
inv_square = pygame.image.load(os.path.join(*yaml_is_sexy['craftstore']['smallsquares']['img']))
craft_button = pygame.image.load(os.path.join(*yaml_is_sexy['craft']['buttons']['img']))
small_yes = pygame.image.load(os.path.join(*yaml_is_sexy['craftstore']['yeah']['img']))
small_no = pygame.image.load(os.path.join(*yaml_is_sexy['craftstore']['nope']['img']))
for i in yaml_is_sexy['craft']['text']:
    text = pygame.image.load(os.path.join(*yaml_is_sexy['craft']['text'][i]['img']))
    texts.append(text)
craftfont = pygame.font.Font(None, 60)

status = [0 for i in range(len(yaml_is_sexy['items']))]
counts = [0 for i in range(len(yaml_is_sexy['items']))]
counts_craft = [0 for i in range(len(yaml_is_sexy['craft']['largesquares']['positions']))]

def update_screen():
    for i in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
        screen_render.blit(craft_square, tuple(yaml_is_sexy['craft']['largesquares']['positions'][i]))
    for i in yaml_is_sexy['craftstore']['smallsquares']['positions']:
        for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            screen_render.blit(inv_square, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
    """print tuple(yaml_is_sexy['craft']['largesquares']['positions'])""" #debug
    screen_render.blit(craft_button, tuple(yaml_is_sexy['craft']['buttons']['positions']))
    for i in pos_order:
        for j in  range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            if status[pos_order.index(i)*6+j] == 2:
                screen_render.blit(small_yes, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
            elif status[pos_order.index(i)*6+j] == 1:
                screen_render.blit(small_no, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
    for i in range(len(yaml_is_sexy['craft']['text'])):
        screen_render.blit(texts[i], yaml_is_sexy['craft']['text'][text_list[i]]['positions'])
    counter()
    outlines()
    screen_final = pygame.transform.smoothscale(screen_render, display_res)
    screen.blit(screen_final,(0,0))
    pygame.display.flip()
    
def potater (index, typeof_item):
    try:
        qty_dict[type_dict [index][typeof_item]] 
    except:
        print 'nigger'
    else:
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
        if item_qty[index] <= 0:
            item_qty[index] = 0
        print type_dict[index][typeof_item], "removed, total amount: ", item_qty[index] #change to gui function
        print "amount left:", qty_dict[type_dict[index][typeof_item]] #change to gui function
    return (item_type[index],item_qty[index])

def counter(): #this function will have to change a bit once the icons are in, i.e. don't draw item count if it's 1 (sprite info will suffice)
    for item in qty_dict:
        counts[yaml_is_sexy['items'].index(item)] = craftfont.render(str(qty_dict[item]), 1, (255,255,255))
    for i in pos_order:
        for j in  range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            if yaml_is_sexy['items'][pos_order.index(i)*6+j] in qty_dict:
                if qty_dict[yaml_is_sexy['items'][pos_order.index(i)*6+j]] >= 1:
                    try:
                        text_offset = (-counts[pos_order.index(i)*6+j].get_width(),-counts[pos_order.index(i)*6+j].get_height())
                        padding = tuple(map(add, text_offset, (-10,-10)))
                        icon_pos = tuple(map(add, yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j], yaml_is_sexy['craftstore']['smallsquares']['size']))
                        screen_render.blit(counts[pos_order.index(i)*6+j], tuple(map(add, icon_pos, padding)))
                    except:
                        pass
        for item in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
            """print item_qty[item]""" #debug
            if item_qty[item] >= 1:
                counts_craft[item] = craftfont.render(str(item_qty[item]), 1, (255,255,255))
        for i in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
            if item_qty[i] >= 1:
                text_offset = (-counts_craft[i].get_width(),-counts_craft[i].get_height())
                padding = tuple(map(add, text_offset, (-10,-10)))
                icon_pos = tuple(map(add, yaml_is_sexy['craft']['largesquares']['positions'][i], yaml_is_sexy['craft']['largesquares']['size']))
                try:
                    
                    screen_render.blit(counts_craft[i], tuple(map(add, icon_pos, padding)))  
                except:
                    pass
      
# here will be implemented a function that blits the item sprites

def outlines():
    
    for i in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
        if item_qty[i] != 0:
            for item in type_dict[i]:
                if item != item_type[i]:
                    if type_dict[i][item] in qty_dict:
                        status[i*6+item-1] = 1
        else:
            for item in type_dict[i]:
                if type_dict[i][item] in qty_dict:
                    status[i*6+item-1] = 2

    for item in yaml_is_sexy['items']:
        try:
            qty_dict[item]
        except:
            status[yaml_is_sexy['items'].index(item)] = 0
        else:
            if qty_dict[item] == 0:
                status[yaml_is_sexy['items'].index(item)] = 0
            elif qty_dict[item] != 0:
                pass
    for i in pos_order:
        for j in  range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            if status[pos_order.index(i)*6+j] == 2:
                screen_render.blit(small_yes, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
            elif status[pos_order.index(i)*6+j] == 1:
                screen_render.blit(small_no, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))

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
    update_screen()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            which_rect = mouse_check(mouse_pos)
            """print which_rect""" #debug
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
                    if crafting_tuple_final in item_dict:
                        for i in range(len(yaml_is_sexy['craft']['largesquares']['positions'])):
                            item_type[i] = 0
                            item_qty[i] = 0
                        print item_dict[crafting_tuple_final]
                        crafting_results.append(item_dict[crafting_tuple_final])
                    else:
                        print "none"
                    crafting_tuple_final = ()
                    print crafting_results
                    
