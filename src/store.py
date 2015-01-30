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
for i in pos_order:
    for j in range(len(yaml_is_sexy['store']['smallsquares']['positions'][i])):
        pos.append(tuple(yaml_is_sexy['store']['smallsquares']['positions'][i][j]) + tuple(map(add, yaml_is_sexy['store']['smallsquares']['positions'][i][j], yaml_is_sexy['store']['smallsquares']['size'])))
for i in range(len(yaml_is_sexy['store']['buttons']['positions'])):
    pos.append(tuple(yaml_is_sexy['store']['buttons']['positions'][i]) + tuple(map(add, yaml_is_sexy['store']['buttons']['positions'][i], yaml_is_sexy['store']['buttons']['size'])))

inv_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond']
store_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond', 'Particle Physics']
inv_dict = {}
store_dict = {}

def fill_dict(list,dict):
    for x in list:
        if x not in dict:
            dict[x] = 1
        else:
            dict[x] += 1
def finish_dict(dict1,dict2):
    for x in dict1:
        if x not in dict2:
            dict2[x] = 0
fill_dict(inv_list, inv_dict)
fill_dict(store_list, store_dict)
finish_dict(inv_dict,store_dict)
finish_dict(store_dict,inv_dict)


items = []
for i in pos_order:
    items.extend(yaml_is_sexy['item_types'][i])
yaml_is_sexy['items'] = items

type_dict =[
    {j%6+1:yaml_is_sexy['item_types'][i][j%6] for j in range(pos_order.index(i)*6,pos_order.index(i)*6+len(yaml_is_sexy['item_types'][i]))} for i in pos_order]

prices_dict =[
    {j%6+1:yaml_is_sexy['store']['prices'][pos_order.index(i)*6+j] for j in range(len(yaml_is_sexy['store']['prices'])/len(pos_order))} for i in pos_order]

buy_list = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
sell_list = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

money = 25000
buy_value = 0
sell_value = 0
shopping = True

item_sprites = [[] for i in range(len(pos_order))]
item_sprites_store = [[] for i in range(len(pos_order))]

pygame.init()
screen = pygame.display.set_mode(display_res)
screen_render = pygame.Surface((3840,2160))
store_square = pygame.image.load(os.path.join(*yaml_is_sexy['store']['smallsquares']['img']))
inv_square = pygame.image.load(os.path.join(*yaml_is_sexy['craftstore']['smallsquares']['img']))
store_button = pygame.image.load(os.path.join(*yaml_is_sexy['store']['buttons']['img']))
small_yes = pygame.image.load(os.path.join(*yaml_is_sexy['craftstore']['yeah']['img']))
small_no = pygame.image.load(os.path.join(*yaml_is_sexy['craftstore']['nope']['img']))
item_spritesheet = pygame.image.load(os.path.join(*yaml_is_sexy['item_icons']['img']))

for i in pos_order:
    for j in range(len(yaml_is_sexy['item_types'][i])):
        item_subsurface = item_spritesheet.subsurface((j*yaml_is_sexy['item_icons']['size'][0],pos_order.index(i)*yaml_is_sexy['item_icons']['size'][1],yaml_is_sexy['item_icons']['size'][0],yaml_is_sexy['item_icons']['size'][1]))
        item_subsurface = pygame.transform.smoothscale(item_subsurface, (tuple(yaml_is_sexy['store']['smallsquares']['size'])))
        item_sprites_store[pos_order.index(i)].append(item_subsurface)
        item_subsurface = pygame.transform.smoothscale(item_subsurface, (tuple(yaml_is_sexy['craftstore']['smallsquares']['size'])))
        item_sprites[pos_order.index(i)].append(item_subsurface)
print item_sprites
storefont = pygame.font.Font(None,60)

status_inv = [0 for i in range(len(yaml_is_sexy['items']))]
status_store = [0 for i in range(len(yaml_is_sexy['items']))]
counts_inv = [0 for i in range(len(yaml_is_sexy['items']))]
counts_store = [0 for i in range(len(yaml_is_sexy['items']))]
counts_inv_s = [0 for i in range(len(yaml_is_sexy['items']))]
counts_store_s = [0 for i in range(len(yaml_is_sexy['items']))]

def update_screen():
    for i in yaml_is_sexy['craftstore']['smallsquares']['positions']:
        for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            screen_render.blit(inv_square, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
    for i in yaml_is_sexy['store']['smallsquares']['positions']:
        for j in range(len(yaml_is_sexy['store']['smallsquares']['positions'][i])):
            screen_render.blit(inv_square, tuple(yaml_is_sexy['store']['smallsquares']['positions'][i][j]))
    for i in range(len(yaml_is_sexy['store']['buttons']['positions'])):
        screen_render.blit(store_button, tuple(yaml_is_sexy['store']['buttons']['positions'][i]))
    draw_items()
    outlines()
    counter()
    draw_money()
    screen_final = pygame.transform.smoothscale(screen_render, display_res)
    screen_render.fill((0,0,0))
    screen.blit(screen_final,(0,0))
    pygame.display.flip()


def buy():
    global money, buy_value, buy_list
    if buy_value != 0:
        buy_value = 0
    for i in range(len(buy_list)):
        for j in range(len(buy_list[i])):
            buy_value += buy_list[i][j]*prices_dict[i][j+1]

    if buy_value <= money:
        money -= buy_value
        print money, buy_value
        for i in range(len(buy_list)):
            for j in range(len(buy_list[i])):
                if buy_list[i][j] != 0:
                    store_dict[type_dict[i][j+1]] -= buy_list[i][j]
                    inv_dict[type_dict[i][j+1]] += buy_list[i][j]
        buy_list = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        buy_value = 0
    else:
        print 'u poorfag'

def sell():
    global money, sell_value, sell_list
    for i in range(len(sell_list)):
        for j in range(len(sell_list[i])):
            sell_value += sell_list[i][j]*prices_dict[i][j+1]
    money += sell_value
    print money, sell_value
    for i in range(len(buy_list)):
            for j in range(len(buy_list[i])):
                if sell_list[i][j] != 0:
                    inv_dict[type_dict[i][j+1]] -= sell_list[i][j]
                    store_dict[type_dict[i][j+1]] += sell_list[i][j]
    sell_list = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    sell_value = 0


def shop_adder(action,index,typeof_item):
    if action == 0:
        try:
            inv_dict[type_dict[index][typeof_item]]
        except:
            print 'nigger'
        else:
            if sell_list[index][typeof_item-1] < inv_dict[type_dict[index][typeof_item]]:
                sell_list[index][typeof_item-1] += 1
                print type_dict[index][typeof_item], action, 'adding'
            else:
                print 'foo'
            print 'sell list', sell_list
    elif action == 1:
        try:
            store_dict[type_dict[index][typeof_item]]
        except:
            print 'nigger'
        else:
            if buy_list[index][typeof_item-1] < store_dict[type_dict[index][typeof_item]]:
                buy_list[index][typeof_item-1] += 1
                print type_dict[index][typeof_item], action, 'adding'
            else:
                print 'foo'
            print 'buy list', buy_list

def shop_remover(action,index,typeof_item):
    if action == 0:
        try:
            inv_dict[type_dict[index][typeof_item]]
        except:
            print 'nigger'
        else:
            if sell_list[index][typeof_item-1] > 0:
                sell_list[index][typeof_item-1] -= 1
                print type_dict[index][typeof_item], action, 'removing'
            else:
                print 'bar'
            print 'sell list', sell_list
    elif action == 1:
        try:
            store_dict[type_dict[index][typeof_item]]
        except:
            print 'nigger'
        else:
            print type_dict[index][typeof_item]
            if buy_list[index][typeof_item-1] > 0:
                buy_list[index][typeof_item-1] -= 1
                print type_dict[index][typeof_item], action, 'removing'
            else:
                print 'bar'
            print 'buy list', buy_list

def outlines():
    for i in pos_order:
        for item in yaml_is_sexy['item_types'][i]:
            try:
                inv_dict[item]
            except:
                status_inv[yaml_is_sexy['items'].index(item)] = 0
            else:
                if inv_dict[item] == 0:
                    status_inv[yaml_is_sexy['items'].index(item)] = 0
                elif inv_dict[item] != 0:
                    try:
                        sell_list[pos_order.index(i)][yaml_is_sexy['items'].index(item)%6]
                    except:
                        pass
                    else:
                        if sell_list[pos_order.index(i)][yaml_is_sexy['items'].index(item)%6] != 0:
                            status_inv[yaml_is_sexy['items'].index(item)] = 2
                        else:
                            status_inv[yaml_is_sexy['items'].index(item)] = 0
        buy_value_temp = buy_value
        for item in yaml_is_sexy['item_types'][i]:
            try:
                store_dict[item]
            except:
                status_store[yaml_is_sexy['items'].index(item)] = 0
            else:
                if store_dict[item] == 0:
                    status_store[yaml_is_sexy['items'].index(item)] = 0
                elif store_dict[item] != 0:
                    try:
                        buy_list[pos_order.index(i)][yaml_is_sexy['items'].index(item)%6]
                    except:
                        pass
                    else:
                        buy_value_temp = 0
                        for k in range(len(buy_list)):
                            for l in range(len(buy_list[k])):
                                buy_value_temp += buy_list[k][l]*prices_dict[k][l+1]
                        if buy_list[pos_order.index(i)][yaml_is_sexy['items'].index(item)%6] != 0 and buy_value_temp <= money:
                            status_store[yaml_is_sexy['items'].index(item)] = 2
                        elif buy_list[pos_order.index(i)][yaml_is_sexy['items'].index(item)%6] != 0 and buy_value_temp > money:
                            status_store[yaml_is_sexy['items'].index(item)] = 1
                        else:
                            status_store[yaml_is_sexy['items'].index(item)] = 0
    for i in pos_order:
        for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            if status_inv[pos_order.index(i)*6+j] == 2:
                screen_render.blit(small_yes, tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
        for k in range(len(yaml_is_sexy['store']['smallsquares']['positions'][i])):
            if status_store[pos_order.index(i)*6+k] == 2:
                screen_render.blit(small_yes, tuple(yaml_is_sexy['store']['smallsquares']['positions'][i][k]))
            elif status_store[pos_order.index(i)*6+k] == 1:
                screen_render.blit(small_no, tuple(yaml_is_sexy['store']['smallsquares']['positions'][i][k]))

def draw_items():
    for i in pos_order:
        for j in range(len(type_dict[pos_order.index(i)])):
            try:
                inv_dict[type_dict[pos_order.index(i)][j+1]]
            except:
                pass
            else:
                if inv_dict[type_dict[pos_order.index(i)][j+1]] != 0:
                    screen_render.blit(item_sprites[pos_order.index(i)][j], tuple(yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j]))
    for i in pos_order:
        for j in range(len(type_dict[pos_order.index(i)])):
            try:
                store_dict[type_dict[pos_order.index(i)][j+1]]
            except:
                pass
            else:
                if store_dict[type_dict[pos_order.index(i)][j+1]] != 0:
                    screen_render.blit(item_sprites_store[pos_order.index(i)][j], tuple(yaml_is_sexy['store']['smallsquares']['positions'][i][j]))


def counter(): #this function will have to change a bit once the icons are in, i.e. don't draw item count if it's 1 (sprite info will suffice)
    for item in inv_dict:
        counts_inv[yaml_is_sexy['items'].index(item)] = storefont.render(str(inv_dict[item]), 1, (255,255,255))
    for i in pos_order:
        for j in  range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            if yaml_is_sexy['items'][pos_order.index(i)*6+j] in inv_dict:
                if inv_dict[yaml_is_sexy['items'][pos_order.index(i)*6+j]] >= 1:
                    try:
                        text_offset = (-counts_inv[pos_order.index(i)*6+j].get_width(),-counts_inv[pos_order.index(i)*6+j].get_height())
                        padding = tuple(map(add, text_offset, (-10,-10)))
                        icon_pos = tuple(map(add, yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j], yaml_is_sexy['craftstore']['smallsquares']['size']))
                        screen_render.blit(counts_inv[pos_order.index(i)*6+j], tuple(map(add, icon_pos, padding)))
                    except:
                        pass
    for item in store_dict:
        counts_store[yaml_is_sexy['items'].index(item)] = storefont.render(str(store_dict[item]), 1, (255,255,255))
    for i in pos_order:
        for j in  range(len(yaml_is_sexy['store']['smallsquares']['positions'][i])):
            if yaml_is_sexy['items'][pos_order.index(i)*6+j] in store_dict:
                if store_dict[yaml_is_sexy['items'][pos_order.index(i)*6+j]] >= 1:
                    try:
                        text_offset = (-counts_store[pos_order.index(i)*6+j].get_width(),-counts_store[pos_order.index(i)*6+j].get_height())
                        padding = tuple(map(add, text_offset, (-10,-10)))
                        icon_pos = tuple(map(add, yaml_is_sexy['store']['smallsquares']['positions'][i][j], yaml_is_sexy['store']['smallsquares']['size']))
                        screen_render.blit(counts_store[pos_order.index(i)*6+j], tuple(map(add, icon_pos, padding)))
                    except:
                        pass
    for i in pos_order:
        for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
            if sell_list[pos_order.index(i)][j] != 0:
                counts_inv_s[yaml_is_sexy['items'].index(yaml_is_sexy['item_types'][i][j])] = storefont.render(str(sell_list[pos_order.index(i)][j]), 1, (0,255,0))
        for i in pos_order:
            for j in range(len(yaml_is_sexy['craftstore']['smallsquares']['positions'][i])):
                if yaml_is_sexy['items'][pos_order.index(i)*6+j] in inv_dict and sell_list[pos_order.index(i)][j] != 0:
                    try:
                        text_offset = (-counts_inv_s[pos_order.index(i)*6+j].get_width(),-counts_inv_s[pos_order.index(i)*6+j].get_height())
                        padding = tuple(map(add, text_offset, (-10,-120)))
                        icon_pos = tuple(map(add, yaml_is_sexy['craftstore']['smallsquares']['positions'][i][j], yaml_is_sexy['craftstore']['smallsquares']['size']))
                        screen_render.blit(counts_inv_s[pos_order.index(i)*6+j], tuple(map(add, icon_pos, padding)))
                    except:
                        pass
    for i in pos_order:
        for j in range(len(yaml_is_sexy['store']['smallsquares']['positions'][i])):
            if buy_list[pos_order.index(i)][j] != 0 and status_store[pos_order.index(i)*6+j] == 2:
                counts_store_s[yaml_is_sexy['items'].index(yaml_is_sexy['item_types'][i][j])] = storefont.render(str(buy_list[pos_order.index(i)][j]), 1, (0,255,0))
            elif buy_list[pos_order.index(i)][j] != 0 and status_store[pos_order.index(i)*6+j] == 1:
                counts_store_s[yaml_is_sexy['items'].index(yaml_is_sexy['item_types'][i][j])] = storefont.render(str(buy_list[pos_order.index(i)][j]), 1, (255,0,0))
        for i in pos_order:
            for j in range(len(yaml_is_sexy['store']['smallsquares']['positions'][i])):
                if yaml_is_sexy['items'][pos_order.index(i)*6+j] in store_dict and status_store[pos_order.index(i)*6+j] != 0:
                        try:
                            text_offset = (-counts_store_s[pos_order.index(i)*6+j].get_width(),-counts_store_s[pos_order.index(i)*6+j].get_height())
                            padding = tuple(map(add, text_offset, (-10,-120)))
                            icon_pos = tuple(map(add, yaml_is_sexy['store']['smallsquares']['positions'][i][j], yaml_is_sexy['store']['smallsquares']['size']))
                            screen_render.blit(counts_store_s[pos_order.index(i)*6+j], tuple(map(add, icon_pos, padding)))
                        except:
                            pass

def mouse_check(mouse_pos):
    #print mouse_pos[0], mouse_pos[1]
    for x in pos:
        #print x[0]*factor[0], x[2]*factor[0], x[1]*factor[1], x[3]*factor[1]
        if (mouse_pos[0] >= x[0]*factor[0] and mouse_pos[0] <= x[2]*factor[0] and mouse_pos[1] >= x[1]*factor[1] and mouse_pos[1] <= x[3]*factor[1]):
            if pos.index(x) < 30:
                return (0,pos.index(x)/6,pos.index(x)%6)
            elif pos.index(x) >= 30 and pos.index(x) < 60:
                return (1,(pos.index(x)/6)%5,pos.index(x)%6)
            elif pos.index(x) == 60:
                return (2,)
            elif pos.index(x) == 61:
                return (3,)
            elif pos.index(x) == 62:
                return (4,)
            else:
                pass
        else:
            pass

def draw_money():
    money_amount = storefont.render("Your money: "+str(money), 1, (255,255,255))
    screen_render.blit(money_amount, (10,300))


while shopping:
    update_screen()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed()
            which_rect = mouse_check(mouse_pos)
            """print which_rect""" #debug
            try:
                 len(which_rect)
            except:
                 pass
            else:
                if len(which_rect) == 3 and mouse_button == (1,0,0):
                     shop_adder(which_rect[0], which_rect[1], (which_rect[2]+1))
                elif len(which_rect) == 3 and mouse_button == (0,0,1):
                    shop_remover(which_rect[0], which_rect[1], (which_rect[2]+1))
                elif which_rect == (2,):
                    buy()
                elif which_rect == (3,):
                    sell()

            """if event.key in item_keys:
                if pygame.key.get_mods() & KMOD_SHIFT == 1:
                    sell(item_keys[event.key])
                elif pygame.key.get_mods() & KMOD_SHIFT == 0:
                    buy(item_keys[event.key])
            elif event.key == K_RETURN:
                shopping = False
            else:
                pass"""
print "Finished shopping!"
print "Money remaining: ", money
print "Your items: ", inv_dict
print "Store items: ", store_dict
