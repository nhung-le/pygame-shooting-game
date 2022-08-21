import pygame
from Character import Character, HealthBar
from Bullet import Bullet
from Grenade import Grenade
from Explosion import Explosion
from ItemBox import ItemBox
import constants

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Oh! Shoot')

# set framerate
clock = pygame.time.Clock()

# player action variables
moving_left = moving_right = shoot = grenade = grenade_thrown = False

#define colours
BG = (144, 201, 120) # TODO update later

# not using yet
font = pygame.font.SysFont('Futura', 30)

# draw BG
def draw_bg():
    screen.fill(BG)
    # draw base line for now
    pygame.draw.line(screen, constants.RED, (0, constants.BASE_GROUND), (constants.SCREEN_WIDTH, constants.BASE_GROUND))

# draw text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

# create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()


#temp - create item boxes TODO remove later
item_box_hp = ItemBox(constants.ITEM_BOX_NAME_HEALTH, 600, constants.BASE_GROUND - 100) # TODO aim manually lol
item_box_group.add(item_box_hp)
item_box_grenade = ItemBox(constants.ITEM_BOX_NAME_GRENADE, 500, constants.BASE_GROUND - 100)
item_box_group.add(item_box_grenade)

player = Character(200, 200, 1, 'player', 'moona', constants.PLAYER_SPEED, constants.PLAYER_HP, 5) # TODO constant grenades?
health_bar = HealthBar(10, 10, player.health, player.max_health)

enemy = Character(500, 200, 1, 'enemy', 'tnt', constants.ENEMY_TNT_SPEED, constants.ENEMY_TNT_HP, 0) # no grenade for enemy
enemy2 = Character(300, 200, 1, 'enemy', 'tnt', constants.ENEMY_TNT_SPEED, constants.ENEMY_TNT_HP, 0) # no grenade for enemy
enemy_group.add(enemy)
enemy_group.add(enemy2)


run = True
while run:
    clock.tick(constants.FPS)

    draw_bg()
    # show user's stats
    health_bar.draw(screen, player.health)
    for x in range(player.grenades):
        screen.blit(pygame.image.load('images/icons/grenade_tiny.png').convert_alpha(), (10 + (x * 15), 50))

    player.update()
    player.draw(screen)

    for enemy in enemy_group:
        enemy.update()
        enemy.draw(screen)

    # update and draw groups
    bullet_group.draw(screen)
    bullet_group.update(player, enemy_group, bullet_group)
    grenade_group.draw(screen)
    grenade_group.update(player, enemy_group)
    explosion_group.draw(screen)
    explosion_group.update()
    item_box_group.draw(screen)
    item_box_group.update(player)


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
        player.move(moving_left, moving_right)

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
            if event.key == pygame.K_SPACE: # TODO maybe should always let it shoot?
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        
        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE: # TODO remove later
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
    pygame.display.update()
pygame.quit()