import simpleGE, pygame, random

# need to get rid of these; currently only here for the label
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640

# in theory, should give consistent movement across any given screen
# definitely a better way to do this
PLAYER_MOVE_SPEED = 0.02 * SCREEN_WIDTH
COIN_MOVE_SPEED = 0.005 * SCREEN_WIDTH

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        # create player object
        self.player = Player(self)
        self.setImage("bg.png")

        self.score_label = ScoreLabel()
        self.score = 0

        # create 10 coins with random vertical offset
        # this should keep them all from appearing at once
        self.coins = []
        for i in range(10):
            self.coins.append(Coin(self))
            self.coins[-1].y = random.randint(-300, 0)

        self.sprites = [self.player, self.coins, self.score_label]

    def process(self):
        # check if each coin collides with player, reset and increment score
        for coin in self.coins:
            if self.player.collidesWith(coin):
                coin.reset()
                self.score += 1
                self.score_label.text = f"{self.score}"


class ScoreLabel(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.fgColor = "light green"
        self.clearBack = True
        self.text = "0"
        self.center = (SCREEN_WIDTH - 20, 20)
        self.size = (150, 30)


class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        # this was a placeholder, but now it's not
        self.setImage("bob_rest.png")


    def update(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= PLAYER_MOVE_SPEED
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += PLAYER_MOVE_SPEED
        if self.isKeyPressed(pygame.K_UP):
            self.y -= PLAYER_MOVE_SPEED
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += PLAYER_MOVE_SPEED

        # THESE HAVE TO BE CHECKED SEPARATE
        # otherwise, we'll go off the screen in corners
        if self.right >= self.screenWidth:
            self.right = self.screenWidth
        elif self.left <= 0:
            self.left = 0
        if self.bottom >= self.screenHeight:
            self.bottom = self.screenHeight
        elif self.top <= 0:
            self.top = 0



class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        # this is supposed to give them a random x position
        # it doesn't work at the beginning of the game
        self.x = random.randint(0, self.screenWidth)
        self.setImage("coin.png")
        # get a random float from 0.5 to 1.5; causes coins to move at different speeds
        # need to find a cleaner way to do this if possible
        self.move_speed = random.uniform(0.5, 1.5) * COIN_MOVE_SPEED

    # reset to top
    def reset(self):
        self.x = random.randint(0, self.screenHeight)
        self.bottom = 0

    # move, reset if it *fully* reaches the bottom
    def update(self):
        self.y += self.move_speed

        if self.top >= SCREEN_HEIGHT:
            self.reset()



game = Game()
game.start()


