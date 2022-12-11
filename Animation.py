import pygame
import os

class Animation(pygame.sprite.Sprite):
    def __init__(self, scale, dir):
        self.update_time = pygame.time.get_ticks() # next animation
        self.animation_list = []
        self.frame_index = 0
        number_of_frames = len(os.listdir(f'{dir}'))
        for i in range(number_of_frames):
            img = pygame.image.load(f'{dir}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
    def update_animation(self):
        # update animation
        # update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > 50:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation run out then reset back to start
        if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
