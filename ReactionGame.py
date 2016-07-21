import random
import pygame
import sys
import pygame.mixer
import math
from pygame.locals import *

#  start pygame
pygame.init()

FPS = 60   # frames per second, the general speed of the program
WINDOWWIDTH = 640   # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels

#  colours used
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (240, 196, 50)
GREEN = (0, 255, 0)
BLUE = (32, 78, 230)
PURPLE = (160, 32, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_RED = (200, 0, 0)
HIGHLIGHTCOLOUR = DARK_RED
CIRCLECOLOUR = RED

#  fonts used
LARGETEXT = pygame.font.Font('freesansbold.ttf', 32)
SMALLTEXT = pygame.font.Font("freesansbold.ttf", 20)
beep = pygame.mixer.Sound('Beep.wav')

#  surface object to draw on
global DISPLAYSURF
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#  used to track FPS
global FPSCLOCK
FPSCLOCK = pygame.time.Clock()

pygame.display.set_caption('Reaction Game')
DISPLAYSURF.fill(WHITE)

SCORE = 0
ARCADEHIGHSCORE = 0
SURVIVALHIGHSCORE = 0

PAUSE = False


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

        drawScore(530, 20, SMALLTEXT, 'Arcade Highscore: ', ARCADEHIGHSCORE, CIRCLECOLOUR)
        drawScore(523, 50, SMALLTEXT, 'Survival Highscore: ', SURVIVALHIGHSCORE, CIRCLECOLOUR)

        #  draw buttons
        button("Arcade", 230, 150, 190, 50, WHITE, CIRCLECOLOUR, "arcade")
        button("Survival", 230, 200, 190, 50, WHITE, CIRCLECOLOUR, "survival")
        button("Options", 230, 250, 190, 50, WHITE, CIRCLECOLOUR, "options")
        button("Quit", 230, 300, 190, 50, WHITE, CIRCLECOLOUR, "quit")
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def arcadeMode():
    global PAUSE, SCORE, ARCADEHIGHSCORE

    #  Store coordinates of circle
    circleX = 0
    circleY = 0

    drawScore(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, 'Score: ', SCORE, CIRCLECOLOUR)
    circleX, circleY, hit = drawCircle(circleX, circleY, True)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    timer = 30
    #  Used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

    while True:
        drawTimer(timer)

        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PAUSE = True
                    pause()
            elif event.type == USEREVENT + 1:
                timer -= 1

        circleX, circleY, hit = drawCircle(circleX, circleY)

        if hit:
            #  If clicked on a circle
            SCORE += 1
            drawScore(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT , 'Score: ', SCORE, CIRCLECOLOUR)
            playSound()

        checkIfGameOver(timer, "arcade")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def survivalMode():
    global PAUSE, SCORE, SURVIVALHIGHSCORE

    #  store coordinates of circle
    circleX = 0
    circleY = 0

    drawScore(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT , 'Score: ', SCORE, CIRCLECOLOUR)
    circleX, circleY, hit = drawCircle(circleX, circleY, True)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    timer = 5
    #  used to correctly implement seconds
    pygame.time.set_timer(USEREVENT + 1, 1000)

    while True:
        drawTimer(timer)

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
            drawScore(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, 'Score: ', SCORE, CIRCLECOLOUR)
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
        if mode == "arcade":
            if SCORE > ARCADEHIGHSCORE:
                ARCADEHIGHSCORE = SCORE

        drawGameOver(SCORE)


def drawCircle(x, y, intialise=False):
    hit = False

    if (checkifCircleClicked(x, y)) or intialise:
        #  if circle is clicked

        #  redraw circle
        pygame.draw.circle(DISPLAYSURF, WHITE, (x, y), 10, 0)
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


def drawTimer(timer):
    font = pygame.font.SysFont('Consolas', 30)
    timer_display = font.render("Timer: " + str(timer), 1, (0, 0, 0))
    pygame.draw.rect(DISPLAYSURF, WHITE, (8, 20, 190, 50))
    DISPLAYSURF.blit(timer_display, (10, 30))


def drawScore(x, y, textSize, text, score, colour):
    scoreStr = str(score)
    textSurfaceObj = textSize.render(str(text + scoreStr), True, colour, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def drawGameOver(highScore):
    global SCORE
    DISPLAYSURF.fill(WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        #  draw game over text
        gameover_display = LARGETEXT.render('Game over!', True, RED, WHITE)
        DISPLAYSURF.blit(gameover_display, (WINDOWWIDTH/2 - 80, WINDOWHEIGHT/2 - 25))

        drawScore(330, 300, SMALLTEXT, 'High Score ', highScore, BLACK)

        drawScore(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, 'Score: ', SCORE, CIRCLECOLOUR)
        button("Main Menu", 230, 350, 190, 50, WHITE, CIRCLECOLOUR, "menu")

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

        DISPLAYSURF.fill(WHITE)

        gameover_display = LARGETEXT.render('Game paused!', True, RED, WHITE)
        DISPLAYSURF.blit(gameover_display, (220, 150))

        button("Continue", 230, 300, 190, 50, WHITE, CIRCLECOLOUR, "unpause")
        button("Main Menu", 230, 350, 190, 50, WHITE, CIRCLECOLOUR, "menu")
        button("Quit", 230, 400, 190, 50, WHITE, CIRCLECOLOUR, "quit")

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    DISPLAYSURF.fill(WHITE)
    drawScore(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, 'Score: ', SCORE, CIRCLECOLOUR)


def drawOptions():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        colourSelectionButton(230, 150, 50, 50, RED)
        colourSelectionButton(300, 150, 50, 50, ORANGE)
        colourSelectionButton(370, 150, 50, 50, YELLOW)
        colourSelectionButton(230, 220, 50, 50, GREEN)
        colourSelectionButton(300, 220, 50, 50, BLUE)
        colourSelectionButton(370, 220, 50, 50, PURPLE)

        button("Main Menu", 230, 350, 190, 50, WHITE, CIRCLECOLOUR, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


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
            if action == "unpause":
                unpause()

            DISPLAYSURF.fill(WHITE)

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
        pygame.draw.rect(DISPLAYSURF, WHITE, (x - 5, y - 5, w + 10, h + 10), 4)


# Helper function for rendering fonts
def textObjects(text, font):
    textSurface = font.render(text, True, BLACK)
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
