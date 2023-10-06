import constants
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, type):
        pygame.sprite.Sprite.__init__(self)
        self.speed = constants.BULLET_SPEED
        self.image = pygame.image.load(f'images/icons/bullet_{type}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self, player, enemy_group, group, world, screen_scroll, hit_fx):
        # move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check if bullet has gone off screen (refresh memory)
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH - 30: # TODO constant ?
            self.kill()
        # check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, group, False):
            if player.alive:
                player.health -= constants.PLAYER_TAKE_DAMAGE
                self.kill()
                player.last_shot_time = pygame.time.get_ticks()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, group, False):
                if enemy.alive:
                    enemy.health -= constants.ENEMY_TAKE_DAMAGE
                    hit_fx.play()
                    self.kill()
                    enemy.damage_by_bullet = True