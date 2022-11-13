import constants
import pygame

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        item_boxes = {
            constants.ITEM_BOX_NAME_HEALTH  : pygame.image.load('images/icons/health_box.png').convert_alpha(),
            constants.ITEM_BOX_NAME_GRENADE : pygame.image.load('images/icons/grenade_box.png').convert_alpha(),
            constants.ITEM_BOX_NAME_COIN    : pygame.image.load('images/icons/coin.png').convert_alpha() # TODO animation coin
        }
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        # TODO update position of item depend on map later
        self.rect.midtop = (x + constants.TILE_SIZE // 2, y + (constants.TILE_SIZE - self.image.get_height()))
        
    def update(self, player, screen_scroll):
        self.rect.x += screen_scroll
        # check if the player have picked up the box
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.item_type == constants.ITEM_BOX_NAME_HEALTH:
                player.health += constants.ITEM_BOX_VALUE_HEALTH
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == constants.ITEM_BOX_NAME_GRENADE:
                player.grenades += constants.ITEM_BOX_VALUE_GRENADE
            elif self.item_type == constants.ITEM_BOX_NAME_COIN:
                player.coin += constants.ITEM_BOX_VALUE_COIN
            self.kill()