import random
import pygame
import sys
import pygame.mixer
import math
import time
from pygame.locals import *
#  start pygame
pygame.init()
pygame.display.set_caption('Reaction Game')

FPS = 60            # frames per second, the general speed of the program
WINDOWWIDTH = 640   # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels
SCORE = 0
ARCADEHIGHSCORE = 0
SURVIVALHIGHSCORE = 0
PAUSE = False

#  colours used
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (240, 196, 50)
GREEN = (0, 255, 0)
BLUE = (32, 78, 230)
PURPLE = (160, 32, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKRED = (200, 0, 0)
HIGHLIGHTCOLOUR = DARKRED
CIRCLECOLOUR = BLUE
BACKGROUNDCOLOUR = BLACK
TEXTCOLOUR = WHITE

#  fonts used
LARGETEXT = pygame.font.Font('freesansbold.ttf', 32)
SMALLTEXT = pygame.font.Font("freesansbold.ttf", 20)
beep = pygame.mixer.Sound('Beep.wav')

#  surface object to draw on
global DISPLAYSURF
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
DISPLAYSURF.fill(BACKGROUNDCOLOUR)

#  used to track FPS
global FPSCLOCK
FPSCLOCK = pygame.time.Clock()


def main():
    importSave()
    drawMenu()

#  saves highscores
def exportSave():
    global ARCADEHIGHSCORE, SURVIVALHIGHSCORE
    with open('save.txt', 'w') as textFile:
        textFile.write(str(ARCADEHIGHSCORE) + '\n')
        textFile.write(str(SURVIVALHIGHSCORE) + '\n')

#   imports highscores
def importSave():
    global ARCADEHIGHSCORE, SURVIVALHIGHSCORE

    with open('save.txt', 'r') as textFile:
        ARCADEHIGHSCORE = int(textFile.readline())
        SURVIVALHIGHSCORE = int(textFile.readline())


def drawMenu():
    global SCORE, PAUSE, ARCADEHIGHSCORE
    PAUSE = False
    SCORE = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        drawText(530, 20, SMALLTEXT, "Arcade Highscore: " + str(ARCADEHIGHSCORE), CIRCLECOLOUR)
        drawText(523, 50, SMALLTEXT, "Survival Highscore: " + str(SURVIVALHIGHSCORE), CIRCLECOLOUR)

        #  draw buttons
        button("Arcade", 230, 150, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "arcade")
        button("Survival", 230, 200, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "survival")
        button("Options", 230, 250, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "options")
        button("Quit", 230, 300, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "quit")
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def arcadeMode():
    global PAUSE, SCORE, ARCADEHIGHSCORE

    #  Store coordinates of circle
    circleX = 0
    circleY = 0

    drawText(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, "Score: " + str(SCORE), TEXTCOLOUR)
    circleX, circleY, hit = drawCircle(circleX, circleY, True)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    timer = 30
    #  Used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

    while True:
        drawTimer(100, WINDOWHEIGHT - 50, LARGETEXT, timer, TEXTCOLOUR)

        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # if ESC is pressed
                    PAUSE = True
                    pause()
            elif event.type == USEREVENT + 1:
                timer -= 1

        circleX, circleY, hit = drawCircle(circleX, circleY)

        if hit:
            #  If clicked on a circle
            SCORE += 1
            drawText(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT , "Score: " + str(SCORE), TEXTCOLOUR)
            playSound()

        checkIfGameOver(timer, "arcade")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def survivalMode():
    global PAUSE, SCORE, SURVIVALHIGHSCORE

    #  store coordinates of circle
    circleX = 0
    circleY = 0

    drawText(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT , "Score: " + str(SCORE), TEXTCOLOUR)
    circleX, circleY, hit = drawCircle(circleX, circleY, True)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    timer = 5
    #  used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

    while True:
        drawTimer(100, WINDOWHEIGHT - 50, LARGETEXT, timer, TEXTCOLOUR)

        mouseClicked = False

        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #  If ESC is pressed
                    PAUSE = True
                    pause()
            elif event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
            elif event.type == USEREVENT + 1:
                timer -= 1

        if mouseClicked and not checkifCircleClicked(circleX, circleY):
            #  if clicked and missed
            timer -= 1

        #  draw circle and determine if clicked
        circleX, circleY, hit = drawCircle(circleX, circleY)

        if hit:
            #  if clicked a circle
            SCORE += 1
            drawText(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, "Score: " + str(SCORE), TEXTCOLOUR)
            playSound()
            if timer < 5:
                timer += 1

        checkIfGameOver(timer, "survival")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def checkIfGameOver(timer, mode):
    global SCORE, SURVIVALHIGHSCORE, ARCADEHIGHSCORE

    if timer <= 0:
        if mode == "survival":
            if SCORE > SURVIVALHIGHSCORE:
                SURVIVALHIGHSCORE = SCORE
            drawGameOver(SURVIVALHIGHSCORE)
        if mode == "arcade":
            if SCORE > ARCADEHIGHSCORE:
                ARCADEHIGHSCORE = SCORE
            drawGameOver(ARCADEHIGHSCORE)


def drawCircle(x, y, intialise=False):
    hit = False

    if (checkifCircleClicked(x, y)) or intialise:
        #  if circle is clicked

        #  redraw circle
        pygame.draw.circle(DISPLAYSURF, BACKGROUNDCOLOUR, (x, y), 10, 0)
        x = random.randint(15, WINDOWWIDTH - 10)

        #  prevents from spawning circles in bad locations
        if x < 200:
            y = random.randint(75, WINDOWHEIGHT - 10)
        elif x > WINDOWWIDTH - 200:
            y = random.randint(0, WINDOWHEIGHT - 75)
        else:
            y = random.randint(0, WINDOWHEIGHT - 10)

        hit = True

    pygame.draw.circle(DISPLAYSURF, CIRCLECOLOUR, (x, y), 10, 0)

    return x, y, hit



def drawText(x, y, textSize, text, colour):
    textSurfaceObj = textSize.render(str(text), True, colour, BACKGROUNDCOLOUR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def drawTimer(x, y, textSize, timer, colour):
    textSurfaceObj = textSize.render(str("Timer: " + str(timer)), True, colour, BACKGROUNDCOLOUR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)

    # hard coded value to refresh a specific part of the screen
    pygame.draw.rect(DISPLAYSURF, BACKGROUNDCOLOUR, (20, 400, 200, 70))

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def drawGameOver(highScore):
    global SCORE
    DISPLAYSURF.fill(BACKGROUNDCOLOUR)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        #  draw game over text
        gameover_display = LARGETEXT.render('Game over!', True, CIRCLECOLOUR, BACKGROUNDCOLOUR)
        DISPLAYSURF.blit(gameover_display, (WINDOWWIDTH/2 - 80, WINDOWHEIGHT/2 - 25))

        drawText(330, 280, SMALLTEXT, "High Score: " + str(highScore), CIRCLECOLOUR)
        drawText(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, "Score: " + str(SCORE), TEXTCOLOUR)

        button("Main Menu", 230, 350, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def unpause():
    global PAUSE
    PAUSE = False


def pause():
    while PAUSE:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BACKGROUNDCOLOUR)

        gameover_display = LARGETEXT.render('Game paused!', True, RED, BACKGROUNDCOLOUR)
        DISPLAYSURF.blit(gameover_display, (220, 150))

        button("Continue", 230, 300, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "unpause")
        button("Main Menu", 230, 350, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "menu")
        button("Quit", 230, 400, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "quit")

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    DISPLAYSURF.fill(BACKGROUNDCOLOUR)
    drawText(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, "Score: " + str(SCORE), CIRCLECOLOUR)


def drawOptions():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        drawText(330, 70, SMALLTEXT, "Circle colour", TEXTCOLOUR)
        colourSelectionButton(230, 100, 50, 50, RED)
        colourSelectionButton(300, 100, 50, 50, ORANGE)
        colourSelectionButton(370, 100, 50, 50, YELLOW)
        colourSelectionButton(230, 170, 50, 50, GREEN)
        colourSelectionButton(300, 170, 50, 50, BLUE)
        colourSelectionButton(370, 170, 50, 50, PURPLE)

        drawText(310, 265, SMALLTEXT, "Theme:", TEXTCOLOUR)
        darkModeCheckbox(370, 250, 30, 30)
        button("Main Menu", 230, 350, 190, 50, BACKGROUNDCOLOUR, CIRCLECOLOUR, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def darkModeCheckbox(x, y, w, h):
    global BACKGROUNDCOLOUR, TEXTCOLOUR
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1:
        # if mouse clicked in the box

        # prevents the left click from being held down
        time.sleep(0.1)
    
        if BACKGROUNDCOLOUR == WHITE:
            BACKGROUNDCOLOUR = BLACK
            TEXTCOLOUR = WHITE
        elif BACKGROUNDCOLOUR == BLACK:
            BACKGROUNDCOLOUR = WHITE
            TEXTCOLOUR = BLACK
        DISPLAYSURF.fill(BACKGROUNDCOLOUR)

    pygame.draw.rect(DISPLAYSURF, TEXTCOLOUR, (x, y, w, h))


def colourSelectionButton(x, y, w, h, colour):
    global CIRCLECOLOUR

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    drawButtonBorder(x, y, w, h)

    if x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1:
        #  If on the button and clicked
        CIRCLECOLOUR = colour

    pygame.draw.rect(DISPLAYSURF, colour, (x, y, w, h))


def button(msg, x, y, w, h, inactiveColour, activeColour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        #  if mouse is inside the box

        pygame.draw.rect(DISPLAYSURF, activeColour, (x, y, w, h))

        if click[0] == 1 and action is not None:
            #  if mouse clicked

            # prevents the left click from being held down
            time.sleep(0.1)

            if action == "unpause":
                unpause()

            DISPLAYSURF.fill(BACKGROUNDCOLOUR)

            if action == "survival":
                survivalMode()
            elif action == "arcade":
                arcadeMode()
            elif action == "menu":
                drawMenu()
            elif action == "options":
                drawOptions()
            elif action == "unpause":
                unpause()
            elif action == "quit":
                exportSave()
                pygame.quit()
                sys.exit()
    else:
        #  if mouse is outside the box
        pygame.draw.rect(DISPLAYSURF, inactiveColour, (x, y, w, h))

    textSurf, textRect = textObjects(msg, SMALLTEXT)
    textRect.center = ((x + (w / 2), (y + (h / 2))))
    DISPLAYSURF.blit(textSurf, textRect)


def drawButtonBorder(x, y, w, h):
    mouse = pygame.mouse.get_pos()
    # print(mouse)
    # if mouse is inside the box
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOUR, (x - 5, y - 5, w + 10, h + 10), 4)
    else:
        pygame.draw.rect(DISPLAYSURF, BACKGROUNDCOLOUR, (x - 5, y - 5, w + 10, h + 10), 4)


# Helper function for rendering fonts
def textObjects(text, font):
    textSurface = font.render(text, True, TEXTCOLOUR)
    return textSurface, textSurface.get_rect()


def playSound():
    beep.play()


def getColour(x, y):
    return DISPLAYSURF.get_at((x, y))


def checkifCircleClicked(x, y):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Used to find area of circle
    xSquared = (mouse[0] - x)**2
    ySquared = (mouse[1] - y)**2
    return math.sqrt(xSquared + ySquared) < 10 and click[0] == 1


if __name__ == '__main__':
    main()
