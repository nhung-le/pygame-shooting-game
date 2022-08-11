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
        self.direction = direction
        self.explosion_group = explosion_group
    def update(self, player, enemy_group):
        self.vel_y += constants.GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # Check collision with floor
        if self.rect.bottom + dy > constants.BASE_GROUND:
            dy = constants.BASE_GROUND - self.rect.bottom
            self.speed = 0

        # check collision with the walls
        if self.rect.left + dx < 0 or self.rect.right + dx > constants.SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

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
            if abs(self.rect.centerx - player.rect.centerx) < constants.TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < constants.TILE_SIZE * 2:
                player.health -= 50 # TODO need this? constant this?
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < constants.TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < constants.TILE_SIZE * 2:
                    enemy.health -= 50 # TODO need this? constant this? bigger than player?
        