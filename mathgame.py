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

class Character(pygame.sprite.DirtySprite):

    def __init__(self, img, xy):
        pygame.sprite.DirtySprite.__init__(self) # Initialize base class
        self.initx, self.inity = xy
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = self.initx
        self.rect.y = self.inity
        self.soundlist = None

    def update(self):
        pass

    def move(self, dxdy):
        self.rect.x += dxdy[0]
        self.rect.y += dxdy[1]
        self.dirty = 1

    def getpos(self):
        return (self.rect.x,self.rect.y)

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.dirty = 1

    def reset(self):
        self.rect.x = self.initx
        self.rect.y = self.inity
        self.dirty = 1

    def saySomething(self):
        if( self.soundlist ):
            sound = random.choice(self.soundlist)
            pygame.mixer.Sound(os.path.join('sound',sound)).play()

class Vader(Character):

    def __init__(self, xy):
        image = pygame.image.load(os.path.join('images','vader.png'))
        image = pygame.transform.smoothscale(image, (320,320))
        Character.__init__(self, image, xy)

        self.soundlist = ['darthvader_anger.ogg', 'darthvader_dontmakeme.ogg', 
                'darthvader_failedme.ogg', 'darthvader_pointless.ogg']

class Luke(Character):

    def __init__(self, xy):
        image = pygame.image.load(os.path.join('images','luke.png'))
        image = pygame.transform.smoothscale(image, (320,320))
        Character.__init__(self, image, xy)

        self.soundlist = ['lightsaber_01.ogg']
        self.attacking = False
        self.attackcntr = 0

    def attack(self,xy):
        self.rect.x, self.rect.y = xy
        self.flip()
        if self.attacking:
            self.attacking = False
        else:
            self.attacking = True;
            self.attackcntr = 60

    def update(self):
        Character.update(self)
        if self.attacking:
            self.attackcntr -= 1
            if self.attackcntr == 0:
                self.attacking = False
                self.flip()
                self.rect.x, self.rect.y = self.initx, self.inity

class Obi(Character):

    def __init__(self, xy):
        image = pygame.image.load(os.path.join('images','obi.png'))
        image = image.convert_alpha()
        image = pygame.transform.smoothscale(image, (300,220))
        image.set_alpha(50)
        Character.__init__(self, image, xy)

        self.soundlist = ['force.wav', 'useforce.wav']
        self.isPlaying = False

    def update(self):
        Character.update(self)
        if self.isPlaying and not pygame.mixer.get_busy():
            self.isPlaying = False
            self.kill();

    def saySomething(self):
        Character.saySomething(self)
        self.isPlaying = True


class Score(pygame.sprite.DirtySprite):

    def __newSurface(self):
        image = pygame.Surface((400,300), pygame.SRCALPHA, 32)
        image = image.convert_alpha()

        return image

    def __init__(self, xy):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = self.__newSurface()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xy
        self.score = 0
        self.hiscore = 0
        self.font = pygame.font.Font('/usr/share/fonts/TTF/DejaVuSansMono.ttf', 64)
        self.__renderScore()

    def addScore(self, adder):
        self.score += adder
        if self.score > self.hiscore:
            self.hiscore = self.score
        self.__renderScore()

    def reset(self):
        self.score = 0
        self.__renderScore()

    def update(self):
        pass

    def __renderScore(self):
        self.image = self.__newSurface()
        score_render = self.font.render('   Score:', True, greenColor)
        self.image.blit(score_render, (0, 0))

        score_render = self.font.render("%9d" % self.score, True, greenColor)
        self.image.blit(score_render, (0, self.font.get_linesize()))

        score_render = self.font.render("Hi-Score:", True, greenColor)
        self.image.blit(score_render, (0, 2*self.font.get_linesize()))

        score_render = self.font.render("%9d" % self.hiscore, True, greenColor)
        self.image.blit(score_render, (0, 3*self.font.get_linesize()))
        self.dirty = 1
 

class GameOver(pygame.sprite.DirtySprite):
    def __init__(self, xy):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((1000,300), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xy
        self.font = pygame.font.Font('/usr/share/fonts/TTF/DejaVuSansMono.ttf', 128)

        gameover_render = self.font.render('Game Over!', True, redColor)
        self.image.blit(gameover_render, (0, 0))

    def update(self):
        self.dirty = 1

class Equation(pygame.sprite.DirtySprite):

    def __generate(self):
        # Generate some random integers

        op = random.choice(('+', '-'))

        range_low = 1000
        range_high = 9999

        a = random.randint(range_low, range_high)
        b = random.randint(range_low, range_high)

        if a < b:
            [a, b] = [b, a]

        return (a,b,op)

    def __newSurface(self):
        image = pygame.Surface((1000,500), pygame.SRCALPHA, 32)
        image = image.convert_alpha()

        return image

    def __init__(self, xy):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = self.__newSurface()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xy
        self.a, self.b, self.op = self.__generate()
        self.ans = 0
        self.font = pygame.font.Font('/usr/share/fonts/TTF/DejaVuSansMono.ttf', 128)
        self.__draw()

    def update(self):
        pass

    def reset(self):
        self.a, self.b, self.op  = self.__generate()
        self.ans = 0
        self.__draw()

    def __draw(self):
        self.image = self.__newSurface()
        a_render = self.font.render("%5d" % self.a, True, blueColor)
        b_render = self.font.render(self.op + "%4d" % self.b, True, blueColor)
        ans_render = self.font.render("%5d" % self.ans, True, greenColor)

        self.image.blit(a_render, (0, 0))
        self.image.blit(b_render, (0, 130))

        if self.ans > 0:
            self.image.blit(ans_render, (0, 280))

        # Draw line
        pygame.draw.line(self.image, blueColor, (0, 280), (420, 280), 8)
        self.dirty = 1

    def setAns(self, ans):
        self.ans = ans
        self.__draw()

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

def main():

    # Constants
    vader_dx = -167

    # Map keyboard events to digits
    kb_lookup = {K_0: 0, K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5, K_6: 6,
            K_7: 7, K_8: 8, K_9: 9 }

    # Initialize Pygame
    pygame.init()

    # Create window
    windowSurface = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Star Wars Math')

    # Load the background images
    bg_img = pygame.image.load(os.path.join('images','Tatooine_1024_768.jpg'))
    bg_img = pygame.transform.smoothscale(bg_img, (1024,768))

    # Create the game objects
    score = Score((650, 10))
    eq = Equation((10, 20))
    vader = Vader((694, 450))
    luke = Luke((10, 450))
    obi = Obi((400, 250))
    gameovertext = GameOver((150,320))

    # Load sound / music
    pygame.mixer.init()

    # Draw the background
    windowSurface.blit(bg_img, (0,0))
    pygame.display.update()

    # Create a group with the initial set of sprites
    allsprites = pygame.sprite.LayeredDirty((vader,luke,score, eq))
    allsprites.clear(windowSurface, bg_img)

    # Clock object is needed for frame timer
    clock = pygame.time.Clock()

    failures = 0
    gameover = False

    while True:

        # Set max framerate
        clock.tick(60)

        # Update and draw the sprites
        allsprites.update()
        rects = allsprites.draw(windowSurface)
        pygame.display.update(rects)

        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:

                # Cleanup and exit
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if gameover:
                    # If the game has ended, restart
                    gameover = False;
                    failures = 0
                    eq.reset()
                    vader.reset()
                    score.reset()
                    luke.reset()
                    allsprites.remove(gameovertext)
                else:
                    # Process keystroke. First get current candidate answer
                    ans = eq.getAns()

                    # If the key pressed was 0-9 then process it
                    if event.key in {K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9}:
                        if ans < 10000:
                            ans = ans * 10
                            ans = ans + kb_lookup[event.key]

                    elif event.key == K_BACKSPACE:
                        ans = ans / 10

                    # Set the new answer
                    eq.setAns(ans)

                    if event.key == K_RETURN:
                        if ans == 0:
                            pass
                        elif eq.checkAns() == True:
                            # Make Luke attack vader and say something
                            vader_xy = vader.getpos()
                            luke.attack((vader_xy[0]-200, vader_xy[1]))
                            luke.saySomething()

                            # Move vader back a bit and add more "lives"
                            if failures > 0:
                                failures -= 1
                                vader.move((-vader_dx, 0))

                            # Add to the score and make a new equation
                            score.addScore(100)
                            eq.reset()
                        else:
                            # Oops, incorrect answer
                            # Move Vader closer to Luke and subtract a "life"
                            vader.move((vader_dx, 0))
                            failures += 1

                            if failures == 3:
                                # Bummer, game over
                                gameover = True;
                                allsprites.add(gameovertext)
                                vader.saySomething()
                            else:
                                # Randomly make Obi-won appear and say something
                                if random.choice([True, False]):
                                    vader.saySomething()
                                else:
                                    obi.saySomething()
                                    allsprites.add(obi)

                        ans = 0

                    eq.setAns(ans)


if __name__ == "__main__":
    main()
