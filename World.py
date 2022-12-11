import constants
import pygame
from Character import Character, HealthBar
from ItemBox import ItemBox

class World():
    def __init__(self):
        # TODO the same for enemy types ?
        self.obstacle_list = []

        # TODO move to outside so no need to load m ulti time same images
        self.img_list = []
        for x in range(constants.TILE_TYPES):
            img = pygame.image.load(f'images/tiles/{x}.png') # TODO level different folder because different map?
            img = pygame.transform.scale(img, (constants.TILE_SIZE, constants.TILE_SIZE))
            self.img_list.append(img)
        
    def process_data(self, data, enemy_group, item_box_group, water_group, decoration_group, exit_group, saved_coin):
        self.level_length = len(data[0])
        # iterate through each value in level file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                # no process -1
                if tile >= 0:
                    img = self.img_list[tile] # TODO move img_list
                    img_rect = img.get_rect()
                    img_rect.x = x * constants.TILE_SIZE
                    img_rect.y = y * constants.TILE_SIZE
                    tile_data = (img, img_rect)
                    # TODO CONSTANT TILE TYPES
                    if tile >= 0 and  tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and  tile <= 10:
                        water = Water(img, x * constants.TILE_SIZE, y * constants.TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 11:
                        decoration = Decoration(img, x * constants.TILE_SIZE, y * constants.TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15: #create player
                        player = Character(x * constants.TILE_SIZE, y * constants.TILE_SIZE, 0.65, 'player', 'moona', constants.PLAYER_SPEED, constants.PLAYER_HP, constants.GRENADE_NUMBER)
                        health_bar = HealthBar(10, 10, player.health, player.max_health)
                        player.coin = saved_coin
                    elif tile == 16: #create enemy (TODO types)
                        enemy = Character(x * constants.TILE_SIZE, y * constants.TILE_SIZE, 0.65, 'enemy', 'tnt', constants.ENEMY_TNT_SPEED, constants.ENEMY_TNT_HP, 0) # no grenade for enemy
                        # enemy2 = Character(300, 200, 0.65, 'enemy', 'tnt', constants.ENEMY_TNT_SPEED, constants.ENEMY_TNT_HP, 0) # no grenade for enemy
                        # enemy_group.add(enemy2)
                        enemy_group.add(enemy)
                    elif tile == 17: # create item box
                        item_box_hp = ItemBox(constants.ITEM_BOX_NAME_HEALTH, x * constants.TILE_SIZE, y * constants.TILE_SIZE) # TODO aim manually lol
                        item_box_group.add(item_box_hp)
                    elif tile == 18: # create grenade box
                        item_box_grenade = ItemBox(constants.ITEM_BOX_NAME_GRENADE, x * constants.TILE_SIZE, y * constants.TILE_SIZE)
                        item_box_group.add(item_box_grenade)
                    elif tile == 19:
                        item_box_coin = ItemBox(constants.ITEM_BOX_NAME_COIN, x * constants.TILE_SIZE, y * constants.TILE_SIZE)
                        item_box_group.add(item_box_coin)
                    elif tile == 20: #create exit
                        exit = Exit(img, x * constants.TILE_SIZE, y * constants.TILE_SIZE)
                        exit_group.add(exit)
        return player, health_bar
    
    def draw(self, screen, screen_scroll):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


# TODO should combine all these classes?
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + constants.TILE_SIZE // 2, y + (constants.TILE_SIZE - self.image.get_height()))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
                              
class Water(pygame.sprite.Sprite): # Or any effective tile
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + constants.TILE_SIZE // 2, y + (constants.TILE_SIZE - self.image.get_height()))
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        
# TODO handle dialouge before or after
class Exit(pygame.sprite.Sprite): # Go to next level
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + constants.TILE_SIZE // 2, y + (constants.TILE_SIZE - self.image.get_height()))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll