import pygame
from pygame import mixer
import constants

#button class
class Button():
    def __init__(self, text, w, h, pos):
        self.top_rect = pygame.Rect(pos, (w,h))
        self.top_color = constants.BLACK
        font = pygame.font.Font('fonts/Minecraft.ttf', 30) # TODO font not working

        self.text_surf = font.render(text, True, constants.WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
        self.clicked = False
        self.last = pygame.time.get_ticks() # delay before went to game
        self.click_fx = mixer.Sound('audio/button-pressed.wav')
        self.click_fx.set_volume(0.5)


    def draw(self, surface):
        #draw button on screen
        pygame.draw.rect(surface, self.top_color, self.top_rect)
        surface.blit(self.text_surf, self.text_rect)

        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.top_rect.collidepoint(pos):
            self.top_color = constants.BLUE
            # TODO update effect button and click sound
            #pygame.draw.rect(surface, constants.RED, self.rect, 1, 1)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.click_fx.play()
                now = pygame.time.get_ticks()
                if now - self.last >= 500:
                    self.clicked = True
                    action = True
        else:
            self.top_color = constants.BLACK

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action