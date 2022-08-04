import constants
import pygame
import os
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
    
    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            # TODO ammo add condition and self.ammo > 0
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        #reset movement
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
            self.vel_y = -11 # jump range TODO put in constant?
            self.jump = False
            self.in_air = True
        
        # apply gravity
        self.vel_y += constants.GRAVITY
        if self.vel_y > 10: # TODO current landing
            self.vel_y
        dy += self.vel_y

        # Check collision with floor
        if self.rect.bottom + dy > constants.BASE_GROUND:
            dy = constants.BASE_GROUND - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self, bullet_group):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = constants.SHOOT_COOLDOWN
            bullet = Bullet(self.rect.centerx + (constants.BULLET_RANGE * self.rect.size[0] * self.direction ), self.rect.centery, self.direction)
            bullet_group.add(bullet)

    def update_animation(self):
        # update animation
        # update image depending on current frame
        self.avatar = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > constants.ANIMATION_COOLDOWN:
            self.update_time =  pygame.time.get_ticks()
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
            self.update_action(3) # death