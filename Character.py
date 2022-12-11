import constants
import pygame
import os
import random
from Bullet import Bullet

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, character_type, character, speed, health, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.character = character
        self.character_type = character_type
        self.speed = speed
        # ammo, might not need now
        # TODO if you want uncomment and change constants.TEMPORARY_AMMO to argument
        # self.ammo = constants.TEMPORARY_AMMO
        # self.start_ammo = constants.TEMPORARY_AMMO
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.coin = 0
        self.health = health
        self.max_health = self.health # TODO upgrade this by level?
        self.direction = 1
        self.vel_y = 0
        self.flip = self.jump = False
        self.in_air = True

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks() # next animation
        
        # ai specific variables
        self.move_counter = self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20) # 150 = how far they can look TODO constant
        self.idling = False

        #load all images for players
        animation_types = ['idle', 'run', 'jump', 'death']
        for animation in animation_types:
            temp_list = []
            #count number of files in folder
            number_of_frames = len(os.listdir(f'images/{self.character_type}/{self.character}/{animation}'))
            for i in range(number_of_frames):
                img = pygame.image.load(f'images/{self.character_type}/{self.character}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.avatar = self.animation_list[self.action][self.frame_index]
        self.rect = self.avatar.get_rect()
        self.rect.center = (x, y)
        self.width = self.avatar.get_width()
        self.height = self.avatar.get_height()
        
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.avatar, self.flip, False), self.rect)
        # TODO test rect
        # pygame.draw.rect(screen, BLACK, self.rect, 1)

    
    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            # TODO ammo add condition and self.ammo > 0
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right, world, bg_scroll, water_group, exit_group):
        #reset movement
        screen_scroll = 0
        dx = dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11 # jump RANGE TODO put in constant?
            self.jump = False
            self.in_air = True
        
        # apply gravity
        self.vel_y += constants.GRAVITY
        if self.vel_y > 10: # TODO current landing
            self.vel_y
        dy += self.vel_y

        # Check for collision
        for tile in world.obstacle_list:
            # If there is a collision, move out of the way and stop the player from moving.
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): # check x direction
                dx = 0
                # if the ai has hit the wall then make it turn around
                if self.character_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): # check y direction
                # check if below the ground, (i.e: if the player is jumping)
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, (i.e: if the player is falling)
                if self.vel_y > 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                    
        # check for collision with water / lava
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
        
        # check if fallen off  the map
        if self.rect.bottom > constants.SCREEN_HEIGHT:
            self.health = 0
        
        # check if going of the edges of the screen
        if self.character_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > constants.SCREEN_WIDTH:
                dx = 0
            
        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
        # update scroll based on player position
        if self.character_type ==  'player':
            if (self.rect.right > constants.SCREEN_WIDTH - constants.SCROLL_THRESH and bg_scroll < (world.level_length * constants.TILE_SIZE) - constants.SCREEN_WIDTH)\
                or (self.rect.left < constants.SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        
        return screen_scroll, level_complete

    def shoot(self, bullet_group, shot_fx):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = constants.SHOOT_COOLDOWN
            bullet = Bullet(self.rect.centerx + (constants.BULLET_RANGE * self.rect.size[0] * self.direction ), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            shot_fx.play()
    
    def ai(self, player, bullet_group, world, screen_scroll, bg_scroll, water_group, exit_group, shot_fx): # TODO SHOULD BE DIFFERENT DEPENDS ON ENEMY, LIKE SOME WILL ALWAYS BE IDLING
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1: # sometimes stopped
                self.update_action(constants.ACTION_IDLE)
                self.idling = True
                self.idling_counter = 50
            # check if the  ai in near the player
            if self.vision.colliderect(player.rect):
                # TODO different depend on type of enemy, might not shoot but explode
                # stop running and face the player
                self.update_action(constants.ACTION_IDLE)
                # shoot
                self.shoot(bullet_group, shot_fx)
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, world, bg_scroll, water_group, exit_group)
                    self.update_action(constants.ACTION_RUN)
                    # TODO maybe upgrade to find and run to player
                    self.move_counter += 1
                    # update ai vision as the enemy moves
                    # TODO should still have when idle depend on the type of enemy
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery) # TODO constant
                    # draw vision: pygame.draw.rect(screen, constants.RED, self.vision)
                    
                    if self.move_counter > constants.TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else: # and then move again after stopped at sometime
                    self.idling_counter -=1
                    if self.idling_counter <= 0:
                        self.idling = False
        # scroll                
        self.rect.x += screen_scroll
            

    def update_animation(self):
        # update animation
        # update image depending on current frame
        self.avatar = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > constants.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation run out then reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3: #death action
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(constants.ACTION_DEATH) # death TODO do we need to kill object for enemy type as well?
            
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    def draw(self, screen, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, constants.BLACK, (self.x-2, self.y-2, constants.HEALTH_BAR_WIDTH, constants.HEALTH_BAR_HEIGHT), 1)
        pygame.draw.rect(screen, constants.RED, (self.x, self.y, constants.HEALTH_BAR_WIDTH, constants.HEALTH_BAR_HEIGHT))
        pygame.draw.rect(screen, constants.GREEN, (self.x, self.y, constants.HEALTH_BAR_WIDTH * ratio, constants.HEALTH_BAR_HEIGHT))