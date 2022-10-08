from Explosion import Explosion
import constants
import pygame

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, explosion_group):
        pygame.sprite.Sprite.__init__(self)
        self.timer = constants.GRENADE_TIMER
        self.vel_y = -11 # TODO constants
        self.speed = constants.GRENADE_SPEED
        self.image = pygame.image.load('images/icons/grenade.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        self.explosion_group = explosion_group
        
    def update(self, player, enemy_group, world):
        self.vel_y += constants.GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        
        # Check for collisions with the level
        for tile in world.obstacle_list:
            # check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # check if below the ground, (i.e: if throw up)
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, (i.e: falling)
                if self.vel_y > 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        # coundown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1) # TODO constant scale?
            self.explosion_group.add(explosion)
            # do damage to anyone that is nearby even player (?)
            # NO abs for y so it won't cause damage below
            if abs(self.rect.centerx - player.rect.centerx) < constants.TILE_SIZE * 2 and \
                self.rect.centery - player.rect.centery < constants.TILE_SIZE * 2:
                player.health -= 30 # TODO need this? constant this?
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < constants.TILE_SIZE * 2 and \
                    self.rect.centery - enemy.rect.centery < constants.TILE_SIZE * 2:
                    enemy.health -= 50 # TODO constant this?
        