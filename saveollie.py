import pygame
from Character import Character, HealthBar
from Bullet import Bullet
from Grenade import Grenade
from Explosion import Explosion
from ItemBox import ItemBox
from Button import Button
from World import World
import constants
import csv

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Oh! Shoot')

# set framerate
clock = pygame.time.Clock()

# player action variables
moving_left = moving_right = shoot = grenade = grenade_thrown = False

#define colours
BG = (144, 201, 120) # TODO update later
bg = pygame.image.load('images/background/0.png').convert_alpha()
start_img = pygame.image.load('images/buttons/start.png').convert_alpha()
exit_img = pygame.image.load('images/buttons/exit.png').convert_alpha()
restart_img = pygame.image.load('images/buttons/start.png').convert_alpha() # TODO UPDATE BUTTON

screen_scroll = 0
bg_scroll = 0
start_game = False
level = 1

# not using yet
font = pygame.font.SysFont('Futura', 30)

# draw BG
def draw_bg():
    screen.fill(BG)
    rel_x = bg_scroll % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < constants.SCREEN_WIDTH:
        screen.blit(bg, (rel_x, 0))

# draw text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))
    
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

# create buttons
start_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2, start_img, 1)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 + 100, exit_img, 1)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 90, constants.SCREEN_HEIGHT // 2 - 50, restart_img, 1)

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
# load in level data and create world
with open(f'levels/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
             world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group)

# TODO move to top later
# DS-Digital font
font = pygame.font.Font('freesansbold.ttf', 20)


run = True
while run:
    clock.tick(constants.FPS)
    
    if start_game == False:
        # draw menu
        screen.fill(BG)
        # add button
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        # update background
        draw_bg()
        # draw world map
        world.draw(screen, screen_scroll)
        # show user's stats
        health_bar.draw(screen, player.health)
        text = font.render(str(player.coin), True, constants.WHITE)
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
            enemy.ai(player, bullet_group, world, screen_scroll, bg_scroll, water_group, exit_group)
            enemy.update()
            enemy.draw(screen)

        # update and draw groups
        bullet_group.draw(screen)
        bullet_group.update(player, enemy_group, bullet_group, world, screen_scroll)
        grenade_group.draw(screen)
        grenade_group.update(player, enemy_group, world, screen_scroll)
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

        # update player actions
        if player.alive:
            # shooting
            if shoot:
                player.shoot(bullet_group)
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
            screen_scroll, level_complete = player.move(moving_left, moving_right, world, bg_scroll, water_group, exit_group)
            bg_scroll -= screen_scroll
            # check if player has completed the level
            if level_complete:
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= constants.MAX_LEVELS:
                    # load in level data and create world
                    with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group)

        else: #player not alive
            screen_scroll = 0
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                # load in level data and create world
                with open(f'levels/level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group)
                

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
            if event.key == pygame.K_RETURN: # TODO maybe should always let it shoot?
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if (event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE) and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        
        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_RETURN:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
    pygame.display.update()
    
pygame.quit()