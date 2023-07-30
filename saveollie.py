import pygame
from pygame import mixer
from Character import Character, HealthBar
from Bullet import Bullet
from Grenade import Grenade
from Explosion import Explosion
from ItemBox import ItemBox
from Button import Button
from World import World
from ScreenFade import ScreenFade
from Animation import Animation
import constants
import csv

mixer.init()
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Id:Dream')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# set framerate
clock = pygame.time.Clock()

# player action variables
moving_left = moving_right = shoot = grenade = grenade_thrown = False

#define colours
menu_center = Animation(0.8, constants.DEFAULT_ANIMATION_SPEED, 'images/menu')
menu_effect = Animation(0.2, 50, 'images/flask')
menu_title = pygame.image.load('images/title.png').convert_alpha()
manual = Animation(1, 1000, 'images/manual')

#load music and sounds
menu_channel = pygame.mixer.Channel(0)
bgm_channel = pygame.mixer.Channel(1)

menu_fx = mixer.Sound('audio/menu.wav')
menu_fx.set_volume(0.05)
bgm_fx = mixer.Sound('audio/bgm.wav')
bgm_fx.set_volume(0.8)

menu_channel.play(menu_fx, loops=-1, fade_ms=5000)
bgm_channel.play(bgm_fx, loops=-1, fade_ms=5000)

jump_fx = mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.5)
# TODO can update another shooting sounds for enemies as well, just pass new one into ai()
shot_fx = mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.5)
grenade_fx = mixer.Sound('audio/explosion.ogg')
grenade_fx.set_volume(0.5)
hit_fx = mixer.Sound('audio/take-damaged.wav')
hit_fx.set_volume(0.5)
dead_fx = mixer.Sound('audio/dead.wav')
dead_fx.set_volume(0.5)

screen_scroll = 0
bg_scroll = 0
start_game = start_intro = in_menu = False
level = 1
saved_coin = 0
final_coin = 0

# not using yet
font = pygame.font.SysFont('Futura', 30)

bg1 = pygame.image.load('images/background/0.png').convert_alpha()
bg2 = pygame.image.load('images/background/1.png').convert_alpha()
snowing = Animation(1, constants.DEFAULT_ANIMATION_SPEED, 'images/background/snow')
# draw BG
def draw_bg():
    screen.fill(constants.GREEN)
    if level == 1:
        bg = bg1
    elif level == 2:
        bg = bg2
    else:
        bg = bg1 # default 1 
        
    rel_x = bg_scroll % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if level == 2:
        snowing.update_animation()
        screen.blit(snowing.image, (rel_x - bg.get_rect().width, 0))
        
    if rel_x < constants.SCREEN_WIDTH:
        screen.blit(bg, (rel_x, 0))
        if level == 2:
            screen.blit(snowing.image, (rel_x, 0))

def draw_menu():
    # black screen first
    screen.fill(constants.BLACK)
    menu_center.update_animation()
    menu_effect.update_animation()
    screen.blit(menu_center.image, (constants.SCREEN_WIDTH // 6, 0))
    screen.blit(menu_effect.image, (menu_effect.image.get_rect().width, menu_effect.image.get_rect().height * 4))
    screen.blit(menu_effect.image, (menu_effect.image.get_rect().width * 6, menu_effect.image.get_rect().height * 5))
    screen.blit(menu_title, (50, constants.SCREEN_HEIGHT // 2 - 100))

def draw_manual(): # todo
    screen.fill(constants.BLACK)
    manual.update_animation()
    screen.blit(manual.image, (0, 0))

# draw text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))
    
def count_enemies(enemy_group):
    count = 0
    for enemy in enemy_group:
        if enemy.alive == True:
            count += 1
    return count


# reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    
    # create empty tile list
    data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLS
        data.append(r)
    return data

def load_world(level):
    # load in level data and create world
    with open(f'levels/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    return World(level)
    
# create screen fades
# TODO update PINK to screen transition you want
death_fade = ScreenFade(constants.FADE_GO_DOWN, constants.PINK, 4)
intro_fade = ScreenFade(constants.FADE_ALL, constants.BLACK, 4)

# create buttons
start_button = Button('Start', 200, 40, (constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 + 100))
exit_button = Button('Exit', 200, 40, (constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 + 150))
manual_button = Button('Manual', 200, 40, (constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 + 200)) 
restart_button = Button('Reset', 200, 40, (constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 50))
back_button = Button('Return', 200, 40, (constants.SCREEN_WIDTH // 2 - 50, constants.SCREEN_HEIGHT // 2 - 50))
return_to_menu_button = Button('return', 100, 40, (constants.SCREEN_WIDTH - 100, constants.SCREEN_HEIGHT - 50))

# create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

world = load_world(level)
player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group, saved_coin)

enemy_len = count_enemies(enemy_group)

run = True
while run:
    clock.tick(constants.FPS)
    
    if start_game == False:
        bgm_channel.pause()
        menu_channel.unpause()
        if in_menu == False:
            draw_menu()
            # add button
            if start_button.draw(screen):
                final_coin = player.coin
                print(final_coin)
                saved_coin = 0
                player.coin = 0
                start_game = True
                start_intro = True
            if manual_button.draw(screen):
                in_menu = True
            if exit_button.draw(screen):
                run = False
        else:
            draw_manual()
            if return_to_menu_button.draw(screen):
                in_menu = False

    else:            
        # stop menu music
        menu_channel.pause()
        bgm_channel.unpause()
        # update background
        draw_bg()
        # draw world map
        world.draw(screen, screen_scroll)
        # show user's stats
        health_bar.draw(screen, player.health)
        text = font.render(str(player.coin), True, constants.WHITE, constants.BLUE)
        textRect = text.get_rect()
        textRect.center = (60, 110)

        screen.blit(pygame.image.load('images/icons/coin.png').convert_alpha(), (10, 90))
        screen.blit(text, textRect)

        # pygame.draw.rect(screen, constants.BLACK, (self.x-2, self.y-2, constants.HEALTH_BAR_WIDTH, constants.HEALTH_BAR_HEIGHT), 1)
        for x in range(player.grenades):
            screen.blit(pygame.image.load('images/icons/grenade_tiny.png').convert_alpha(), (10 + (x * 15), 50))

        player.update()
        player.draw(screen)

        for enemy in enemy_group:
            enemy.ai(player, bullet_group, world, screen_scroll, bg_scroll, water_group, exit_group, shot_fx, dead_fx)
            enemy.update()
            enemy.draw(screen)

        # update and draw groups
        bullet_group.draw(screen)
        bullet_group.update(player, enemy_group, bullet_group, world, screen_scroll, hit_fx)
        grenade_group.draw(screen)
        grenade_group.update(player, enemy_group, world, screen_scroll, grenade_fx)
        explosion_group.draw(screen)
        explosion_group.update(screen_scroll)
        item_box_group.draw(screen)
        item_box_group.update(player, screen_scroll)
        water_group.draw(screen)
        water_group.update(screen_scroll)
        decoration_group.draw(screen)
        decoration_group.update(screen_scroll)
        exit_group.draw(screen)
        exit_group.update(screen_scroll)

        # show intro
        if start_intro == True:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0 # reset fade counter back to zero
        
        # update player actions
        if player.alive:
            if enemy_len > 0 and enemy_len > count_enemies(enemy_group):
                player.coin += 20
                enemy_len = count_enemies(enemy_group)
            # shooting
            if shoot:
                player.shoot(bullet_group, shot_fx)
            # throw grenades
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction, explosion_group)
                grenade_group.add(grenade)
                # reduce grenades
                player.grenades -= 1
                grenade_thrown = True
            if player.in_air:
                player.update_action(constants.ACTION_JUMP)
            elif moving_left or moving_right:
                player.update_action(constants.ACTION_RUN)
            else:
                player.update_action(constants.ACTION_IDLE)
            screen_scroll, level_complete = player.move(moving_left, moving_right, world, bg_scroll, water_group, exit_group, dead_fx)
            bg_scroll -= screen_scroll
            # check if player has completed the level
            if level_complete:
                if level < constants.MAX_LEVELS:
                    start_intro = True
                    level += 1
                    saved_coin += player.coin
                    bg_scroll = 0
                    world_data = reset_level()
                    # load in level data and create world
                    world = load_world(level)
                    player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group, saved_coin)
                else: # PLAYER FINISH THE GAME (TODO using death_fade temporary )
                    screen_scroll = 0
                    bg_scroll = 0
                    if death_fade.fade(screen):
                        if back_button.draw(screen):
                            death_fade.fade_counter = 0 # reset back to zero
                            start_intro = False
                            start_game = False
                            world_data = reset_level()
                            level = 1 # restart to first level
                            world = load_world(level)
                            player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group, saved_coin)

                
        else: #player not alive
            screen_scroll = 0
            if death_fade.fade(screen):
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0 # reset back to zero
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    # load in level data and create world
                    world = load_world(level)
                    player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group, saved_coin)
                

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False
        
        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
    pygame.display.update()
    
pygame.quit()