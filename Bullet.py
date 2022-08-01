import constants
import pygame

# load images
#bullet
bullet_img = pygame.image.load('images/icons/bullet.png')

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self, player, enemies, group):
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
        if pygame.sprite.spritecollide(enemies, group, False):
            if enemies.alive:
                enemies.health -= constants.ENEMY_TAKE_DAMAGE
                self.kill()