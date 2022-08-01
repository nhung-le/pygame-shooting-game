import pygame
from Character import Character
from Bullet import Bullet
import constants

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# set framerate
clock = pygame.time.Clock()

# player action variables
moving_left = moving_right = shoot = False

#define colours
BG = (251, 110, 216) # TODO update later
RED = (255, 0, 0) # TODO constant?

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (constants.SCREEN_WIDTH, 300)) # TODO 300 to constant

def draw_character(character):
    screen.blit(pygame.transform.flip(character.avatar, character.flip, False), character.rect)


player = Character(200, 200, 1/12, 'player', 'moona', constants.PLAYER_SPEED, constants.PLAYER_HP)
enemy = Character(500, 200, 1/2, 'enemy', 'tnt', constants.ENEMY_TNT_SPEED, constants.ENEMY_TNT_HP)

# create sprite groups
bullet_group = pygame.sprite.Group()

run = True
while run:

    clock.tick(constants.FPS)

    draw_bg()

    player.update()
    draw_character(player)

    enemy.update()
    draw_character(enemy)

    # update and draw groups
    bullet_group.update(player, enemy, bullet_group)
    bullet_group.draw(screen)

    # update player actions
    if player.alive:
        # shooting
        if shoot:
            player.shoot(bullet_group)
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


    pygame.display.update()


pygame.quit()