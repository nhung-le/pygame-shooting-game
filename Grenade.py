import constants
import pygame

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = constants.GRENADE_TIMER
        self.vel_y = -11 # TODO constants
        self.speed = constants.GRENADE_SPEED
        self.image = pygame.image.load('images/icons/grenade.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self):
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
        