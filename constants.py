import string

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HEALTH_BAR_WIDTH:int = 150
HEALTH_BAR_HEIGHT:int = 20

ACTION_IDLE:int = 0
ACTION_RUN:int = 1
ACTION_JUMP:int = 2
ANIMATION_COOLDOWN:int = 100
#TEMPORARY_AMMO:int = 20

PLAYER_HP:int = 100
ENEMY_TNT_HP:int = 80
BOSS_HP:int = 9999
PLAYER_SPEED:int = 5
ENEMY_TNT_SPEED:int = 5
PLAYER_TAKE_DAMAGE = 5 # TODO input argument instead because depend on level and boss?
ENEMY_TAKE_DAMAGE = 20 # TODO input argument?

BULLET_RANGE:float = 0.6
BULLET_SPEED:int = 10
SHOOT_COOLDOWN:int = 20
GRENADE_TIMER:int = 100
GRENADE_SPEED:int = 7
EXPLOSION_SPEED:int = 4
TILE_SIZE:int = 100

FPS:int = 60
GRAVITY:float = 0.75
SCREEN_WIDTH:int = 800
SCREEN_HEIGHT:int = int(SCREEN_WIDTH * 0.8)
BASE_GROUND:int = 300

ITEM_BOX_NAME_HEALTH:string = 'Health'
ITEM_BOX_NAME_GRENADE:string = 'Grenade'
ITEM_BOX_VALUE_HEALTH:int = 25
ITEM_BOX_VALUE_GRENADE:int = 2