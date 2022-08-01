# pygame-shooting-game
## Development on pygame: https://www.pygame.org/wiki/GettingStarted

### 90% reference from this guy: http://codingwithruss.com/pygame/shooter/intro.html. But we will some more features like: checkpoint / save-load / dialoges and choices lead to multi endings / boss

# Installation and Run:
Assumed you already have python3, to install pygame, run:
> python3 -m pip install -U pygame --user

To run game:
> `py -m saveollie`

# Assets structure:
1. `images/{character_type}/{character}/{animation}` : 
+ `character_type` eg enemy / player / boss.
+ `character` is character name if you have mutlti players characters to choose: eg: `protagonist`
+ `animation` are the folder contains sprites like: run / jump / shoot ...
2. `images/icons/` : contain all other objects like `hp.png`, `bullet.png`