"""
Silly Star Wars themed math game for my kids
"""

import pygame, random, sys, os
from pygame.locals import *

# Color definitions
whiteColor = pygame.Color(255, 255, 255)
blueColor = pygame.Color(0, 0, 255)
greenColor = pygame.Color(0, 255, 0)
redColor = pygame.Color(255, 0, 0)

class Character():

    def __init__(self, img, xy):
        self.initx, self.inity = xy
        self.x = self.initx
        self.y = self.inity
        self.img = img

    def draw(self, surface):
        imgRect = self.img.get_rect().topleft = (self.x, self.y)
        surface.blit(self.img, imgRect)

    def moveX(self, dx):
        self.x += dx

    def flipX(self):
        self.img = pygame.transform.flip(self.img, True, False)

    def reset(self):
        self.x = self.initx
        self.y = self.inity

class Score():
    def __init__(self, xy):
        self.score = 0
        self.hiscore = 0
        self.score_font = pygame.font.Font('/usr/share/fonts/TTF/DejaVuSansMono.ttf', 64)
        self.x, self.y = xy

    def addScore(self, adder):
        self.score += adder
        if self.score > self.hiscore:
            self.hiscore = self.score

    def reset(self):
        self.score = 0

    def draw(self, surface):
        score_render = self.score_font.render('   Score:', True, greenColor)
        scoreRect = score_render.get_rect().topleft = (self.x,self.y)
        surface.blit(score_render, scoreRect)

        score_render = self.score_font.render("%9d" % self.score, True, greenColor)
        scoreRect = score_render.get_rect().topleft = (self.x,
                self.y + self.score_font.get_linesize())
        surface.blit(score_render, scoreRect)

        score_render = self.score_font.render("Hi-Score:", True, greenColor)
        scoreRect = score_render.get_rect().topleft = (self.x,
                self.y + 2*self.score_font.get_linesize())
        surface.blit(score_render, scoreRect)

        score_render = self.score_font.render("%9d" % self.hiscore, True, greenColor)
        scoreRect = score_render.get_rect().topleft = (self.x,
                self.y + 3*self.score_font.get_linesize())
        surface.blit(score_render, scoreRect)
 

class GameOver():
    def __init__(self, xy):
        self.font = pygame.font.Font('/usr/share/fonts/TTF/DejaVuSansMono.ttf', 128)
        self.x, self.y = xy

    def draw(self, surface):
        gameover_render = self.font.render('Game Over!', True, redColor)
        gameoverRect = gameover_render.get_rect().topleft = (self.x, self.y)
        surface.blit(gameover_render, gameoverRect)


class Equation():

    def _generate(self):
        # Generate some random integers

        op = random.choice(('+', '-'))

        range_low = 1000
        range_high = 9999

        a = random.randint(range_low, range_high)
        b = random.randint(range_low, range_high)

        if a < b:
            [a, b] = [b, a]

        return (a,b,op)

    def __init__(self, xy):
        self.x, self.y = xy
        self.a, self.b, self.op = self._generate()
        self.ans = 0
        self.font = pygame.font.Font('/usr/share/fonts/TTF/DejaVuSansMono.ttf', 128)

    def reset(self):
        self.a, self.b, self.op  = self._generate()
        self.ans = 0

    def draw(self, surface):
        a_render = self.font.render("%5d" % self.a, True, blueColor)
        b_render = self.font.render(self.op + "%4d" % self.b, True, blueColor)
        ans_render = self.font.render("%5d" % self.ans, True, greenColor)

        aRect = a_render.get_rect().topleft = (self.x, self.y)
        bRect = b_render.get_rect().topleft = (self.x, self.y + 130)
        ansRect = ans_render.get_rect().topleft = (self.x, self.y + 280)

        surface.blit(a_render, aRect)
        surface.blit(b_render, bRect)

        if self.ans > 0:
            surface.blit(ans_render, ansRect)

        # Draw line
        pygame.draw.line(surface, blueColor, (self.x, self.y + 280), (self.x + 420, self.y + 280), 8)

    def setAns(self, ans):
        self.ans = ans

    def getAns(self):
        return self.ans

    def checkAns(self):
        if self.op == '+':
            correct_ans = self.a + self.b
        elif self.op == '-':
            correct_ans = self.a - self.b

        if self.ans == correct_ans:
            return True
        else:
            return False

def playRandomSound(soundlist):
    sound = random.choice(soundlist)
    pygame.mixer.Sound(os.path.join('sound',sound)).play()

def main():
    # Map keyboard events to digits
    kb_lookup = {K_0: 0, K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5, K_6: 6,
            K_7: 7, K_8: 8, K_9: 9 }

    darth_sounds = ['darthvader_anger.ogg', 'darthvader_dontmakeme.ogg', 'darthvader_failedme.ogg',
            'darthvader_pointless.ogg']
    luke_sounds = ['lightsaber_01.ogg']

    # Initialize Pygame
    pygame.init()

    # Create window
    windowSurface = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Star Wars Math')

    # Load the images
    bg_img = pygame.image.load(os.path.join('images','stars.jpg'))
    bg_img = pygame.transform.smoothscale(bg_img, (1024,768))

    vader_img = pygame.image.load(os.path.join('images','vader.png'))
    vader_img = pygame.transform.smoothscale(vader_img, (320,320))

    luke_img = pygame.image.load(os.path.join('images','luke.png'))
    luke_img = pygame.transform.smoothscale(luke_img, (320,320))

    # Create the game objects
    score = Score((650, 10))
    eq = Equation((10, 20))
    vader = Character(vader_img, (694, 450))
    luke = Character(luke_img, (10, 450))
    gameovertext = GameOver((150,320))

    # Load sound / music
    pygame.mixer.init()
    #pygame.mixer.music.load(os.path.join('sound', 'Imperial_March.ogg'))
    #pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    failures = 0
    gameover = False

    while True:

        clock.tick(60)

        # Draw the background
        windowSurface.blit(bg_img, (0,0))

        # Draw the elements
        eq.draw(windowSurface)
        score.draw(windowSurface)
        vader.draw(windowSurface)
        luke.draw(windowSurface)

        if gameover:
            gameovertext.draw(windowSurface)

        # Refresh the screen
        pygame.display.update()

        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:

                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if gameover:
                    gameover = False;
                    failures = 0
                    eq.reset()
                    vader.reset()
                    score.reset()
                    luke.reset()
                else:
                    ans = eq.getAns()

                    if event.key in {K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9}:
                        if ans < 10000:
                            ans = ans * 10
                            ans = ans + kb_lookup[event.key]

                    elif event.key == K_BACKSPACE:
                        ans = ans / 10

                    eq.setAns(ans)

                    if event.key == K_RETURN:
                        if ans == 0:
                            pass
                        elif eq.checkAns() == True:
                            playRandomSound(luke_sounds)
                            score.addScore(100)
                            eq.reset()
                        else:
                            vader.moveX(-167)
                            failures += 1

                            playRandomSound(darth_sounds)
                            if failures == 3:
                                gameover = True;

                        ans = 0

                    eq.setAns(ans)


if __name__ == "__main__":
    main()
