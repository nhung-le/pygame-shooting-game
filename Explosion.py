import constants
import pygame
import os

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        number_of_frames = len(os.listdir(f'images/explosion'))
        for num in range (number_of_frames):
            img = pygame.image.load(f'images/explosion/{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale))) # scale
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-50)
        self.counter = 0
    
    def update(self, screen_scroll):
        # scroll
        self.rect.x += screen_scroll
        # update explosion animation
        self.counter += 1
        if self.counter >= constants.EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if the animation is completed then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else: self.image = self.images[self.frame_index]
            # TO DEBUG
            # if self.frame_index < len(self.images):
            #     self.image = self.images[self.frame_index]