import constants
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = constants.BULLET_SPEED
        self.image = pygame.image.load('images/icons/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self, player, enemy_group, group):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check  if bullet has gone off screen (refresh memory)
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH - 100: # TODO constant ?
            self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, group, False):
            if player.alive:
                player.health -= constants.PLAYER_TAKE_DAMAGE
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, group, False):
                if enemy.alive:
                    enemy.health -= constants.ENEMY_TAKE_DAMAGE
                    self.kill()