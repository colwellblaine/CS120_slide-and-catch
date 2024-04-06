import simpleGE, pygame, random

# I was working on moving these into their individual classes, but I don't think I'll have time
PLAYER_MOVE_SPEED = 0.02 * 640
COIN_MOVE_SPEED = 0.005 * 640



class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        # create player object
        self.player = Player(self)
        self.setImage("assets/bg.png")
        
        #score, timer, and sound
        self.score_label = ScoreLabel()
        self.time_label = TimeLabel()
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 30
        self.score = 0
        self.collect_sound = simpleGE.Sound("assets/pickup0.wav")

        # create 10 coins with random vertical offset
        # this should keep them all from appearing at once
        self.coins = []
        for i in range(10):
            self.coins.append(Coin(self))
            self.coins[-1].y = random.randint(-300, 0)

        self.sprites = [self.player, self.coins, self.score_label, self.time_label]


    def process(self):
        # check if each coin collides with player, reset and increment score
        for coin in self.coins:
            if self.player.collidesWith(coin):
                coin.reset()
                # originally was going to have this play incrementally instead of randomly
                # but that's a low priority right now. It is kinda annoying though
                self.collect_sound = simpleGE.Sound("assets/pickup" + str(random.randint(0, 5)) + ".wav")
                self.collect_sound.play()
                self.score += 1
                self.score_label.text = f"{self.score}"

        self.time_label.text = str(self.timer.getTimeLeft())[0:5]
        
        # actually stop the game at some point
        if self.timer.getTimeLeft() < 0:
            self.stop()


class ScoreLabel(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.fgColor = "light green"
        self.clearBack = True
        self.text = "0"
        # I couldn't figure out a good way to get screen width here, so it's just hard set to 640
        self.center = (640 - 20, 20)
        
        self.size = (150, 30)


class TimeLabel(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.fgColor = "light green"
        self.clearBack = True
        self.text = "0"
        self.center = (40, 20)
        self.size = (150, 30)


class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        # the guy
        self.setImage("assets/character.png")
        self.y = self.screenHeight - (self.screenHeight * 0.08)
        self.move_speed = 0.02 * self.screenHeight


    def update(self):
        # A/D and left/right both work. Up/down and W/S don't.
        if self.isKeyPressed(pygame.K_a) or self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.move_speed
        if self.isKeyPressed(pygame.K_d) or self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.move_speed
        #if self.isKeyPressed(pygame.K_UP):
        #    print("up")
        #if self.isKeyPressed(pygame.K_DOWN):
        #    print("up")


        # No escaping
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
        self.setImage("assets/coin2.png")
        # turns out setting the x value before the image causes the x to be set back to 0
        self.x = random.randint(0, self.screenWidth)
        # get a random float from 0.5 to 1.5; causes coins to move at different speeds
        self.move_speed = random.uniform(0.5, 1.5) * COIN_MOVE_SPEED

    # reset to top
    def reset(self):
        self.x = random.randint(0, self.screenHeight)
        self.bottom = 0

    # move, reset if it *fully* reaches the bottom
    def update(self):
        self.y += self.move_speed

        if self.top >= self.screenHeight:
            self.reset()






#     menu
class Menu(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.status = ""

        # SECOND LINE
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = (
                "Collect as many coins as possible within the time limit",
                ""
                )
        self.instructions.center = (self.background.get_width() / 2, 100)
        self.instructions.size = (self.background.get_width(), 200)
        self.instructions.fgColor = "light green"
        self.instructions.bgColor = "black"

        # buttons
        self.play_button = simpleGE.Button()
        self.play_button.text = "Play"
        self.play_button.fgColor = "light green"
        self.play_button.center = ((self.background.get_width() / 2), (self.background.get_height() / 2))
        self.play_button.size = (150, 30)
        self.play_button.clearBack = True
        
        self.quit_button = simpleGE.Button()
        self.quit_button.text = "Quit"
        self.quit_button.fgColor = "light green"
        self.quit_button.clearBack = True
        self.quit_button.center = ((self.background.get_width() / 2), (self.background.get_height() / 1.8))

        # last score
        self.last_score = simpleGE.Label()
        self.last_score.text = "Previous score: 0"
        self.last_score.size = (250, 25)
        self.last_score.fgColor = "light green"
        self.last_score.clearBack = True                            # change this
        self.last_score.center = (self.background.get_width()/2, self.background.get_height()/2 - 100)
        


        self.sprites = [self.play_button, self.quit_button, self.instructions, self.last_score]

    def set_last_score(self, value):
        self.last_score.text = "Previous score: " + value

    def update(self):
        if self.play_button.clicked == True:
            self.status = "play"
            self.stop()
        elif self.quit_button.clicked:
            self.status = "quit"
            self.stop()








if __name__ == "__main__":
    # run the menu once at the start
    menu = Menu()
    menu.start()

    playing = True
    while playing:
        if menu.status == "play":
            game = Game()
            game.start()

            menu = Menu()
            # set last score value
            menu.set_last_score(str(game.score))
            menu.start()

        else:
            playing = False

