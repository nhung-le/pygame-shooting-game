import pygame
import constants

class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        # TODO not colour maybe whole picture
        self.colour = colour 
        self.speed = speed
        self.fade_counter = 0
        
    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == constants.FADE_ALL: # whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
        if self.direction == constants.FADE_GO_DOWN: # vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True
        
        return fade_complete